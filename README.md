ResourceHosting is a simple Linked Data read & write interface using only HTTP commands.
In the concept it is similar to the [Linked Data Platform](https://www.w3.org/TR/ldp/) but less sophisticated.
It has no complex storage structure underneath, just an RDF file.
The ResourceHosting was implemented as part of the [Structured Feedback Protocol](http://feedback.aksw.org/) prototype. (The paper [*Structured Feedback: A Distributed Protocol for Feedback and Patches on the Web of Data*](http://events.linkeddata.org/ldow2016/papers/LDOW2016_paper_02.pdf) was presented at the LDOW2016 Workshop of the WWW conference.)

## Installation

Requires Python3

Install [pip](https://pypi.python.org/pypi/pip/) to be able to do the following:
```
pip install virtualenvwrapper # If you don't have virtualenvwrapper already
cd /path/to/this/repo
mkvirtualenv -p /usr/bin/python3 ldow
pip install -r requirements.txt
./ldowapi.py start.nq --input nquads
```

## API

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

Read data from the Linked Data Endpoint via GET

```
http://your.host/existing_resource_or_graph
```
e.g.
```
curl --request GET \
  --url http://localhost:5000/5bc2a4997778f54dbca356730a627b4a \
  --header 'accept: text/turtle'
```

## Run in docker

For tests build a local docker image and run the container
```
docker build -t "resourcehosting" .
docker run --name=resourcehosting -p port:80 resourcehosting:latest
```
with `port` being an unused port of your host.
