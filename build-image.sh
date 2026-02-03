#!/bin/bash

if [ -z "$version" ]; then
    version=0.3.0
else
    git checkout v$version
fi

echo "Building version: ${version}"

docker run -v $PWD/frontend:/home/node/frontend \
       --rm jianshao/node-dev:lts \
       npm --prefix /home/node/frontend install

docker run -v $PWD/frontend:/home/node/frontend \
       --rm jianshao/node-dev:lts \
       npm --prefix /home/node/frontend run build

base_image=jianshao/li-app-base
docker pull ${base_image}:latest

li_ver=$(docker run --rm jianshao/li-app-base:latest pip list | grep llama-index-core | awk '{print $2}')
echo "Using llama-index version ${li_ver}"

image=jianshao/rag-chat-demo
docker build -t ${image}:latest . --build-arg TAG=${li_ver} --build-arg VERSION=${version} $*

docker tag ${image}:latest ${image}:${version}
docker push ${image}:latest
docker push ${image}:${version}

echo "Done"
