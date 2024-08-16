#!/bin/bash

docker pull jianshao/li-app-base:latest

llamaindex_ver=$(docker run --rm jianshao/li-app-base:latest pip list | grep llama-index-core| awk '{print $2}')
echo "Using llama-index version ${llamaindex_ver}"

docker build -t jianshao/rag-chat-demo:latest . --build-arg LLAMAINDEX_VER=${llamaindex_ver}

image_tag=$(date +%Y%m%d)
docker tag jianshao/rag-chat-demo:latest jianshao/li-app-dev:${image_tag}
docker push jianshao/rag-chat-demo:latest
docker push jianshao/rag-chat-demo:${image_tag}

echo "Done"