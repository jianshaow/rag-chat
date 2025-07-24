# rag-chat

Demo a RAG besed Q&A system.

## build react frontend
~~~shell
# install dependencies
docker run -v $PWD/frontend:/home/node/frontend \
       --rm jianshao/node-dev:lts-slim \
       npm --prefix /home/node/frontend install
# build package
docker run -v $PWD/frontend:/home/node/frontend \
       --rm jianshao/node-dev:lts-slim \
       npm --prefix /home/node/frontend run build
~~~

## buld docker
~~~shell
./build-image.sh
~~~

### Test image
~~~ shell
docker run -v $PWD/backend/chroma:/home/devel/chroma \
       -v $PWD/backend/data:/home/devel/data -p 8000:8000 \
       --add-host=host.docker.internal:host-gateway \
       --rm jianshao/rag-chat-demo:latest
~~~