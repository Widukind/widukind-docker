===============
Widukind Docker
===============

**Includes:**

* `Dlstats`_
* `Widukind Web`_
* `Widukind Rest Api`_
* `MongoDB Server`_
* `Redis Server`_
* Nginx Proxy
* DNS Cache Server

.. contents:: **Table of Contents**
    :depth: 1
    :backlinks: none

Installation
------------

**Requires:**

* Docker 1.10+
* docker-compose 1.7+
* sudo right or root access

::

    $ sudo git clone https://github.com/Widukind/widukind-docker.git widukind
    $ cd widukind

    # Replace widukind.cepremap.org by your hostname for Widukind Web
    $ sudo sed -i 's/widukind.cepremap.org/widukind.mydomain.org/' docker-compose.yml
    
    # Replace widukind-api.cepremap.org by your hostname for Widukind API
    $ sudo sed -i 's/widukind-api.cepremap.org/api.mydomain.org/' docker-compose.yml
    
    # Edit ./docker_environ for customize configuration
    $ vi ./docker_environ
    
    $ docker-compose up -d
    
    # Go to http://widukind.mydomain.org or http://widukind-api.mydomain.org
   
Configuration
-------------

Edit ./docker_environ before launch docker-compose up

::

    WIDUKIND_BASE_URL_API=http://widukind-api.cepremap.org/api/v1
    WIDUKIND_SECRET_KEY=examplesecretkey
    WIDUKIND_WEB_MAIL_DEFAULT_SENDER=root@localhost.com
    WIDUKIND_WEB_MAIL_ADMIN=root@localhost.com
    WIDUKIND_WEB_USERNAME=admin
    WIDUKIND_WEB_PASSWORD=admin
    WIDUKIND_WEB_MAIL_SERVER=localhost
    
    WIDUKIND_API_WEB_URL=http://widukind.cepremap.org
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

    # help with:
    dlstats --help
    
    # Create all indexes
    dlstats mongo reindex
    
    # Provider list:    
    dlstats fetchers list

    # Datasets list for BIS:    
    dlstats fetchers datasets -f BIS

    # Load BIS Fetcher
    dlstats fetchers run --quiet -S -C -l INFO --datatree -f BIS --run-full -d CNFS

    # Load Fetcher BIS - All datasets
    dlstats fetchers run --quiet -S -C -l INFO --datatree -f BIS --run-full

    # Display report:
    dlstats fetchers report
    
    # Other tasks after run or launch run command with --run-full option
    dlstats fetchers tags -f BIS
    dlstats fetchers consolidate -f BIS
    
.. _`Dlstats`: https://github.com/Widukind/dlstats
.. _`Widukind Web`: https://github.com/Widukind/widukind-web
.. _`Widukind Rest Api`: https://github.com/Widukind/widukind-api
.. _`MongoDB Server`: http://www.mongodb.org
.. _`Redis Server`: http://redis.io

