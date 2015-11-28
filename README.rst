====================
Widukind Environment
====================

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
    
    $ git clone https://github.com/Widukind/dlstats.git
    $ git clone https://github.com/Widukind/widukind-web.git
    
    # Replace 1.1.1.1 with your ip address
    $ sudo sed -i 's/HOST_BIND_WEB/1.1.1.1/' docker-compose.yml
    
    $ docker-compose up -d
    
    # Go to http://1.1.1.1
    
Resume for load datas
---------------------

::

    # run this commands in ./widukind directory
    
    alias dlstats='docker-compose run --rm cli dlstats'
    
    # help with:
    dlstats --help
    
    # Create ES index    
    dlstats es create-index -S

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

