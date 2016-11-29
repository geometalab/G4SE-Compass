Overview
--------

Architecture
~~~~~~~~~~~~

.. figure:: images/architecture/deployment.png
    :width: 50%
    :alt: map to buried treasure


Deployment
~~~~~~~~~~

The Service runs on the switch cloud infrastructure (SwitchEngines). It is a
virtual server with:

* 2 cores
* 4 GB RAM
* 20 GB diskspace

It is powered by `Debian Jessie (Linux)`.

All services run on the same hardware, as shown below.

.. figure:: images/architecture/deployment.png
    :width: 50%
    :alt: map to buried treasure

    Deployment Diagram as currently in use (Switch Cloud Infrastructure)

Scaling Options
~~~~~~~~~~~~~~~

.. sidebar::
    Note: Whenever increasing the CPU-Count, also increase RAM
    otherwise the more processes are using more RAM and have to start swapping,
    which is a major cause for degraded performance.

There are multiple scaling options, some of which require more work than others.

More CPUs, RAM
``````````````

Assuming running with uwsgi, we need to harness the power, and because we have
elasticsearch and postgres running on the same machine, we have to take not
to degrade their performance.

A good rule of thumb, which has proven quite useful, is with N-Cores, where N is larger than 2:

N+1 processes, N/2 (if N is odd, add 0.5) threads.

Examples:

* N=2: uwsgi /uwsgi.ini --processes 3 --threads 1 (see code-snippet below)
* N=3: uwsgi /uwsgi.ini --processes 4 --threads 2
* N=4: uwsgi /uwsgi.ini --processes 5 --threads 2

.. code-block:: yaml
    version: '2'
    services:
      api:
        # your own configuration
        command: uwsgi /uwsgi.ini --processes 3 --threads 1


Adding additional Servers
`````````````````````````

Putting every service on it's own server has the big advantage that
scaling is possible much more easily.

This can be achieved using docker-cloud or a similar service, the
configuration for this scenario is so divers,
that it cannot be included in this documentation.

If much more power is required, the elasticsearch service can be run on a separate,
dedicated machine or even be distributed on multiple machines.
FOr Postgres the same can be done, using a master-slave configuration where for example
writes go only to master, and reads only to slave.

The application/api should of course also be run separately for maximum benefit.

Switching to a more powerful server
```````````````````````````````````

This is the same as more CPU, RAM, just that I use have a real world example.

Using a Hetzner Server, specifically the https://www.hetzner.de/de/hosting/produkte_rootserver/ex51ssd
with 2X500GB Harddisk, 64GB RAM and 4 Cores/8 Threads without much tweaking a load up to
600 to 700 Request per second was possible. This is more than 20 fold of what is possible
with the server above - this method might be the most cost effective way.

