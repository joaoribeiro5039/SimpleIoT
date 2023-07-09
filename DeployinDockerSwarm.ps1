#docker service rm $(docker service ls -q)                       Remove all services
#docker service ls                                               See all services
#docker node ls                                                  See all nodes
#docker stack deploy -c docker-compose-swarm.yml my-stack        Deploy service 


#Inicialize docker swarm visualizer
docker run -it -d -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name swarm-visualizer \
  dockersamples/visualizer


#Clear all services

docker service rm $(docker service ls -q)

#Deploy OPC UA Server on each worker node
#NUM_WORKERS=$(docker node ls --filter "role=worker" --format "{{.Hostname}}" | wc -l)
#docker service create --name opcua-server --replicas $NUM_WORKERS --constraint 'node.role==worker' -p 4840:4840 joaoribeiro5039/opcuaserver:latest
#Deploy OPC UA Server on the swarm
docker service create --name opcua-server --mode global -p 4840:4840 joaoribeiro5039/opcuaserver:latest



#Deploy opctobroker node1
docker service create --name opctobroker --constraint 'node.hostname==node1' \
    --env RABBITMQ_BROKER_HOST=rabbitmq \
    --env RABBITMQ_BROKER_USER=admin \
    --env RABBITMQ_BROKER_PASSWORD=admin \
    --env RABBITMQ_BROKER_QUEUE_PREFIX=server1 \
    --env OPC_UA_HOST=opcuaserver:4840 \
    --env KAFKA_BROKER_HOST=kafka:9092 \
    --env KAFKA_PRODUCER_ID=my_producer \
    --env KAFKA_PRODUCER_PREFIX=server1 \
    --env MQTT_BROKER_HOST=mqtt \
    --env MQTT_BROKER_PORT=1883 \
    --env MQTT_BROKER_PREFIX=server1 \
    --restart always \
    joaoribeiro5039/opctobroker:latest
