FROM mongo:3.0.8

RUN apt-get update -q \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
	
ENTRYPOINT ["/entrypoint.sh"]

CMD ["mongod"]     