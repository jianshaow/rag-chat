#!/bin/bash

base_image=jianshao/li-app-base
docker pull ${base_image}:latest

li_ver=$(docker run --rm jianshao/li-app-base:latest pip list | grep llama-index-core | awk '{print $2}')
echo "Using llama-index version ${li_ver}"

image=jianshao/rag-chat-demo
version=$(date +%Y%m%d)
docker build -t ${image}:latest . --build-arg TAG=${li_ver} --build-arg VERSION=${version}

docker tag ${image}:latest ${image}:${version}
docker push ${image}:latest
docker push ${image}:${version}

echo "Done"
