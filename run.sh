NAME_DOCKER=face_recognition_api

exist_docker=$(docker images | grep $NAME_DOCKER | wc -l)
if [ $(( $exist_docker )) == 0 ];
then
  echo "Docker image not found. Building from file.."
  docker build -t $NAME_DOCKER:v1 .
fi

echo "Image ready, starting container.."

docker run --name=$NAME_DOCKER --rm -e ENVIRONMENT="dev" -p 5000:5000 -it $NAME_DOCKER:v1
#-v $PWD/src:/app