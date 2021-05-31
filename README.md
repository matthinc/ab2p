# ab2p "Audiobook to Podcast"

[![Build Status](https://travis-ci.com/matthinc/ab2p.svg?branch=main)](https://travis-ci.com/matthinc/ab2p)
[![Docker hub](https://img.shields.io/docker/pulls/matthinc/ab2p.svg)](https://hub.docker.com/r/matthinc/ab2p)
[![Docker hub](https://img.shields.io/docker/image-size/matthinc/ab2p)](https://hub.docker.com/r/matthinc/ab2p)

Generates an RSS feed for use in a podcast app from your personal audiobook library.
All audio- and xml files are served statically, so the software uses minimal system resources.

# Sample docker-compose

```yaml
version: '3.0'

services:
    ab2p:
        image: matthinc/ab2p
        ports:
            - 3000:3000
        environment: 
            HOSTNAME: http://192.168.1.70:3000
            BASEDIR: /audiobooks
        volumes:
            - "/media/hdd-master/audiobooks/Audiobook 1:/audiobooks/Audiobook 1"
            - "/media/hdd-master/audiobooks/Audiobook 2:/audiobooks/Audiobook 2"
```

The above docker-compose.yml would serve two podcast feeds: `http://192.168.1.70:3000/Audiobook 1.xml` and `http://192.168.1.70:3000/Audiobook 2.xml`.