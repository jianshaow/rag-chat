#!/bin/bash

docker pull jianshao/li-app-base:latest

llamaindex_ver=$(docker run --rm jianshao/li-app-base:latest pip list | grep llama-index-core| awk '{print $2}')
echo "Using llama-index version ${llamaindex_ver}"

image_tag=$(date +%Y%m%d)

docker build -t jianshao/rag-chat-demo:${image_tag} . --build-arg LLAMAINDEX_VER=${llamaindex_ver}
docker push jianshao/rag-chat-demo:${image_tag}

echo "Done"