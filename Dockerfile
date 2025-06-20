FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git curl wget zip sysbench preload unzip
    #&& apt-get clean \
    #&& rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir -U -r requirements.txt


CMD bash start
