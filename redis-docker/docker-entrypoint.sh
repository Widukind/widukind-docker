#!/bin/bash
set -e

sysctl -w net.core.somaxconn=65535
sysctl -w vm.overcommit_memory=1

[ -f /sys/kernel/mm/transparent_hugepage/enabled ] && echo never > /sys/kernel/mm/transparent_hugepage/enabled

if [ "$1" = 'redis-server' ]; then
        chown -R redis .
        exec gosu redis "$@"
fi

exec "$@"
