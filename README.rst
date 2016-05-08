===============
Widukind Docker
===============

**Includes:**

* `Dlstats`_
* `Widukind Web`_
* `Widukind Rest Api`_
* `MongoDB Server`_
* `Redis Server`_

.. contents:: **Table of Contents**
    :depth: 1
    :backlinks: none

Installation
------------

**Requires:**

* Docker 1.10+
* docker-compose 1.7+
* Two ip address
* sudo right or root access

::

    $ sudo git clone https://github.com/Widukind/widukind-docker.git widukind
    $ cd widukind

    $ git clone https://github.com/Widukind/widukind-web.git
    $ git clone https://github.com/Widukind/widukind-api.git
    $ git clone https://github.com/Widukind/dlstats.git
    
    # Replace 1.1.1.1 with your ip address
    $ sudo sed -i 's/HOST_BIND_WEB/1.1.1.1/' docker-compose.yml
    
    # Replace 1.1.1.2 with your ip address or change port in docker-compose.yml file
    $ sudo sed -i 's/HOST_BIND_API/1.1.1.2/' docker-compose.yml
    
    # Edit ./docker_environ for adap configuration
    $ vi ./docker_environ
    
    $ docker-compose pull
    
    $ docker-compose up -d
    
    # Go to http://1.1.1.1
   
Configuration
-------------

Edit ./docker_environ before launch docker-compose up

::

    WIDUKIND_SECRET_KEY=examplesecretkey
    WIDUKIND_WEB_MAIL_DEFAULT_SENDER=root@localhost.com
    WIDUKIND_WEB_MAIL_ADMIN=root@localhost.com
    WIDUKIND_WEB_USERNAME=admin
    WIDUKIND_WEB_PASSWORD=admin
    WIDUKIND_WEB_MAIL_SERVER=localhost
    
    WIDUKIND_API_SECRET_KEY=examplesecretkeyapi
    WIDUKIND_API_MAIL_DEFAULT_SENDER=root@localhost.com
    WIDUKIND_API_MAIL_ADMIN=root@localhost.com
    WIDUKIND_API_USERNAME=admin
    WIDUKIND_API_PASSWORD=admin
    WIDUKIND_API_MAIL_SERVER=localhost
            
    
Resume for load datas
---------------------

::

    # run this commands in ./widukind directory
    
    alias dlstats='docker-compose run --rm --no-deps cli dlstats'
    or
    alias dlstats_bash='docker-compose run --rm --no-deps cli bash'
    
    # First installation (comming soon...)
    # dlstats install
        
    # help with:
    dlstats --help
    
    # Provider list:    
    dlstats fetchers list

    # Datasets list for BIS:    
    dlstats fetchers datasets -f BIS

    # Create or Update datatree for BIS (--force for replace)
    dlstats fetchers datatree -f BIS

    # Load Fetcher BIS - CNFS dataset
    dlstats fetchers run -C -l INFO -f BIS -d CNFS

    # Load Fetcher BIS with before update datatree
    dlstats fetchers run -C --datatree -l INFO -f BIS -d CNFS

    # Load Fetcher BIS - All datasets
    dlstats fetchers run -C -l INFO -f BIS

    # Display report:
    dlstats fetchers report
    
    # Other tasks after run or launch run command with --run-full option
    dlstats fetchers tags -f BIS
    dlstats fetchers consolidate -f BIS

Installation with nginx proxy and dns cache (dnsmasq)
-----------------------------------------------------

**Requires:**

* Docker 1.10+
* docker-compose 1.7+
* sudo right or root access

::

    $ sudo git clone https://github.com/Widukind/widukind-docker.git widukind
    $ cd widukind
    
    # Use docker-compose -f docker-compose-nginx.yml or rename docker-compose-nginx.yml to docker-compose.yml

    $ git clone https://github.com/Widukind/widukind-web.git
    $ git clone https://github.com/Widukind/widukind-api.git
    $ git clone https://github.com/Widukind/dlstats.git
    
    # if docker0 interface is not 172.17.0.1, replace value in compose file 
    $ sudo sed -i 's/172.17.0.1/YOUR_DOCKER0_IP/' docker-compose-nginx.yml
    
    # Replace www.mydomain.org by your url for web site
    $ sudo sed -i 's/www.mydomain.org/www.example.org/' docker-compose-nginx.yml

    # Replace api.mydomain.org by your url for api site
    $ sudo sed -i 's/api.mydomain.org/api.example.org/' docker-compose-nginx.yml
    
    # Edit ./docker_environ for adap configuration
    $ vi ./docker_environ
    
    $ docker-compose -f docker-compose-nginx.yml pull
    
    $ docker-compose -f docker-compose-nginx.yml up -d
    
    # Load Fetcher BIS - CNFS dataset
    $ docker-compose run --rm --no-deps cli dlstats fetchers run -S -C -l INFO -f BIS -d CNFS

    # Go to http://www.example.org or http://api.example.org

Installation with Mongodb Sharding and Nginx proxy / dns discovery (comming soon...)
------------------------------------------------------------------------------------

**Requires:**

* Docker 1.10+
* docker-compose 1.7+
* sudo right or root access

**This release include:**

* Three mongod server
* One config server
* One router server
* Nginx proxy
* DNS auto-discovery
* Private network 172.16.238.0/24

::

    $ sudo git clone https://github.com/Widukind/widukind-docker.git widukind
    $ cd widukind
    
    # Use docker-compose -f docker-compose-shard.yml or rename docker-compose-shard.yml to docker-compose.yml

    $ git clone https://github.com/Widukind/widukind-web.git
    $ git clone https://github.com/Widukind/widukind-api.git
    $ git clone https://github.com/Widukind/dlstats.git
    
    # Replace www.mydomain.org by your url for web site
    $ sudo sed -i 's/www.mydomain.org/www.example.org/' docker-compose-shard.yml

    # Replace api.mydomain.org by your url for api site
    $ sudo sed -i 's/api.mydomain.org/api.example.org/' docker-compose-shard.yml
    
    # Edit ./docker_environ for adap configuration
    $ vi ./docker_environ
    
    $ docker-compose -f docker-compose-shard.yml pull
    
    $ docker-compose -f docker-compose-shard.yml up -d
    
    $ docker-compose run --rm --no-deps cli dlstats install
    
    $ docker-compose restart web
    
    $ docker-compose restart api

    # Load Fetcher BIS - CNFS dataset
    $ docker-compose run --rm --no-deps cli dlstats fetchers run -S -C -l INFO -f BIS -d CNFS
    
    # Go to http://www.example.org or http://api.example.org
    
.. _`Dlstats`: https://github.com/Widukind/dlstats
.. _`Widukind Web`: https://github.com/Widukind/widukind-web
.. _`Widukind Rest Api`: https://github.com/Widukind/widukind-api
.. _`MongoDB Server`: http://www.mongodb.org
.. _`Redis Server`: http://redis.io

