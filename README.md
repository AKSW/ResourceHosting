# Run in docker

For tests build a local docker image and run the container
```
docker build  -t "resourcehosting" .
docker run --name=resourcehosting -p port:80 resourcehosting:latest
```
with "port" being an unused port of your host.

# API

Get a free URL/Hash under
```
http://your.host/getresource
```

Insert data via PUT/POST

```
http://your.host/a/graphuri/you/want
```

Linked Data Endpoint via GET

```
http://your.host/existing/resource
```
or
```
http://your.host/existing/graphuri
```

# Install python environment

Install [pip](https://pypi.python.org/pypi/pip/) to be able to do the following:
```
pip install virtualenv
cd /path/to/this/repo
mkvirtualenv -p /usr/bin/python3.4 ldow
pip install -r requirements.txt
./ldowapi.py start.nq --input nquads
```
