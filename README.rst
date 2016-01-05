===============
Widukind Docker
===============

**Features:**

* `Dlstats`_
* `pySDMX`_
* `Widukind Web`_

Resume Installation
-------------------

**Requires:**

* Docker 1.9+
* docker-compose 1.5+
* sudo right or root access

::

    $ sudo git clone https://github.com/Widukind/widukind-docker.git widukind
    $ cd widukind
    
    $ git clone https://github.com/Widukind/widukind-web.git
    
    # Replace 1.1.1.1 with your ip address
    $ sudo sed -i 's/HOST_BIND_WEB/1.1.1.1/' docker-compose.yml
    
    # Edit ./docker_environ for adap configuration
    $ vi ./docker_environ
    
    $ docker-compose up -d
    
    # Go to http://1.1.1.1
    
Configuration
-------------

Edit ./docker_environ before launch docker-compose up

::

    WIDUKIND_SECRET_KEY=examplesecretkey
    WIDUKIND_WEB_MAIL_DEFAULT_SENDER=root@localhost.com
    WIDUKIND_WEB_MAIL_ADMIN=root@localhost.com
    WIDUKIND_WEB_SERVER_NAME=localhost
    WIDUKIND_WEB_USERNAME=admin
    WIDUKIND_WEB_PASSWORD=admin
    WIDUKIND_WEB_MAIL_SERVER=localhost        
    
Resume for load datas
---------------------

::

    # run this commands in ./widukind directory
    
    alias dlstats='docker-compose run --rm --no-deps web dlstats'
    
    # help with:
    dlstats --help
    
    # Provider list:    
    dlstats fetchers list

    # Load Fetcher BIS - CNFS dataset
    dlstats fetchers run -l ERROR -f BIS -d CNFS

    # Load Fetcher BIS - All datasets
    dlstats fetchers run -l ERROR -f BIS

    # Display report:
    dlstats fetchers report
    
.. _`Dlstats`: https://github.com/Widukind/dlstats
.. _`pySDMX`: https://github.com/Widukind/pysdmx
.. _`Widukind Web`: https://github.com/Widukind/widukind-web

