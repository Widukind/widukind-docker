#!/bin/bash

BASE_DIR="/home/persist/widukind"
FETCHER="$1"
DATASET="$2"

CMD_COMPOSE="docker-compose run --no-deps --rm cli"
CMD_DLSTATS_RUN="dlstats-gevent fetchers run -S -C -l INFO --datatree -f ${FETCHER}"
CMD_DLSTATS_TAGS="dlstats-gevent fetchers tags --quiet -S -u -l INFO -f ${FETCHER}"
CMD_DLSTATS_CONSOLIDATE="dlstats-gevent fetchers consolidate --quiet -S -l INFO -f ${FETCHER}"

if [ -n "$DATASET" ]; then
   CMD_DLSTATS_RUN="${CMD_DLSTATS_RUN} -d ${DATASET}"
fi

cd ${BASE_DIR}

${CMD_COMPOSE} ${CMD_DLSTATS_RUN} 2>>${BASE_DIR}/widukind/update-${FETCHER}.log 1>&2
${CMD_COMPOSE} ${CMD_DLSTATS_TAGS} 2>>${BASE_DIR}/widukind/tags-${FETCHER}.log 1>&2
${CMD_COMPOSE} ${CMD_DLSTATS_CONSOLIDATE} 2>>${BASE_DIR}/widukind/consolidate-${FETCHER}.log 1>&2
