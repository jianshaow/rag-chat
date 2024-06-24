# rag-chat

## Local Environment

### Prepare
~~~ shell
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
~~~

## Docker Environment

### Build
~~~ shell
export image_ver=0.0.7
docker build -t jianshao/rag-chat-dev:$image_ver .
docker push jianshao/rag-chat-dev:$image_ver
~~~