!/bin/bash
docker_image_name="api:yahoo"
sudo docker stop $(docker ps -a -q --filter ancestor=$docker_image_name)
sudo docker rm $(docker ps -a -q --filter ancestor=$docker_image_name)
sudo docker rmi -f $docker_image_name
sudo docker build -t $docker_image_name --no-cache .
