git pull
sudo docker build -t taskify/taskify:1.0 .
sudo docker stop Taskify
sudo docker rm Taskify
sudo docker run -p 8080:8080 -d --name Taskify taskify/taskify:1.0
sudo docker logs Taskify