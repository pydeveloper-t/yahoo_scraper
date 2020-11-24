# Yahoo finance scraper

The Scrapy based parser for crawling feefo.com



## Requirements

- Python 3.9
- MySQL 
- pipenv(pip)
- Docker


## How to install?
- Install Docker (https://docs.docker.com/get-docker/)
- Download folder Docker from this repo
- Build image
```
	../Docker/build
```	
```	

## How to run?

### Edit run.sh
Set 
- the actual credentials for MySQL:  DBHOST, DBPORT, DBBASE, DBUSER, DBPASSWORD 
- set actual shared folder for running docker image, like this
 
```
-v /home/user/Shared:/work
```

### Run parser
```
run.sh  <searched company name> <path for downloaded files for docker>

Example:
	./run.sh  RUN  /work

```

  

