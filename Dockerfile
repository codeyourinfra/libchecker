FROM codeyourinfra/python3:alpine
LABEL maintainer "Gustavo Muniz do Carmo <gustavo@codeyourinfra.today>"

WORKDIR /libchecker

COPY requirements.txt .
COPY *.py ./

RUN apk add --no-cache python3-dev musl-dev gcc && \
    pip3 install -r requirements.txt

# Environment variables to be defined:
# LIBRARIESIO_API_KEY
# LIBRARIES_PLATFORM
# LIBRARY_NAME
# MONGODB_URI
# MONGODB_USERNAME
# MONGODB_PASSWORD
# MONGODB_NAME

CMD ["python3", "./libchecker.py"]