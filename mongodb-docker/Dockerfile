FROM debian:jessie

RUN apt-get update -y -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  && rm -rf /var/lib/apt/lists/*
  
ENV MONGO_RELEASE 3.2.0

RUN curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-$MONGO_RELEASE.tgz \
	&& tar -zxvf mongodb-linux-x86_64-$MONGO_RELEASE.tgz \
	&& mv -v mongodb-linux-x86_64-$MONGO_RELEASE/bin/* /usr/local/bin \
	&& rm -rf mongodb-linux-x86_64-$MONGO_RELEASE \
	&& mkdir -vp /data/db

VOLUME /data/db

EXPOSE 27017
EXPOSE 28017

CMD ["mongod", "--noauth", "--storageEngine", "wiredTiger", "--wiredTigerCacheSizeGB", "1", "--wiredTigerDirectoryForIndexes", "--httpinterface", "--cpu", "--directoryperdb", "--rest"]
