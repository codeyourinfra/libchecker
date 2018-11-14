FROM codeyourinfra/python3:alpine
LABEL maintainer "Gustavo Muniz do Carmo <gustavo@codeyourinfra.today>"

WORKDIR /libchecker

COPY requirements.txt .
COPY *.py ./

RUN apk add --no-cache python3-dev musl-dev gcc && \
    pip3 install -r requirements.txt

CMD ["python3", "./main.py"]