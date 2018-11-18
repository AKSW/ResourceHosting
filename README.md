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
http://your.host/
```

Insert data via PUT/POST

```
http://your.host/a_graph_or_resource_uri_which_is_free
```

e.g.

```
curl --request PUT \
  --url http://localhost:5000/5bc2a4997778f54dbca356730a627b4a \
  --header 'content-type: application/n-quads' \
  --data '<http://localhost:5000/5bc2a4997778f54dbca356730a627b4a> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/SomeThing> .
<http://localhost:5000/5bc2a4997778f54dbca356730a627b4a> <http://example.org/prop> "Value" .
<http://example.org/SomeThing> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Class> <http://localhost:5000/5bc2a4997778f54dbca356730a627b4a> .'
```

Linked Data Endpoint via GET

```
http://your.host/existing_resource_or_graph
```
e.g.
```
curl --request GET \
  --url http://localhost:5000/5bc2a4997778f54dbca356730a627b4a \
  --header 'accept: text/turtle'
```

# Install python environment

Install [pip](https://pypi.python.org/pypi/pip/) to be able to do the following:
```
pip install virtualenv
cd /path/to/this/repo
mkvirtualenv -p /usr/bin/python3 ldow
pip install -r requirements.txt
./ldowapi.py start.nq --input nquads
```
