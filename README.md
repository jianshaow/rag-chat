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
export image_tag=0.0.1
docker build -t jianshao/rag-chat-demo:$image_tag .
docker push jianshao/rag-chat-demo:$image_tag
~~~

### Test image
~~~ shell
docker run -v $PWD/backend/chroma:/home/devel/chroma \
       -v $PWD/backend/data:/home/devel/data -p 5000:5000 \
       --add-host=host.docker.internal:host-gateway \
       --rm jianshao/rag-chat-demo:$image_tag
~~~