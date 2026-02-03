# rag-chat

Demo a RAG besed Q&A system.

## buld docker
~~~shell
# export version=0.2.0
./build-image.sh
~~~

### Test image
~~~ shell
docker run -v $PWD/backend/chroma:/home/devel/chroma \
       -v $PWD/backend/data:/home/devel/data -p 8000:8000 \
       --add-host=host.docker.internal:host-gateway \
       --rm jianshao/rag-chat-demo:latest
~~~