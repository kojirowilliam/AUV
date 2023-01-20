docker ps -ql
image_id="$(docker ps -ql)"
docker stop $image_id
docker rm $image_id
xhost -local:root