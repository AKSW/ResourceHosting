#!/usr/bin/env python
from flask import request, Flask, Response
from flask_negotiate import consumes, produces
from flask.ext.cors import CORS
import lib.filegraph as fg
import rdflib
from  lib import handleexit
import argparse
import os, hashlib, time, json

# TODO: jquery ajax requests always get a 'charset=UTF-8' entry as Content-Type
importformats = {'text/html' : 'html',
        'text/n3':'n3',
        'application/n-triples':'nquads',
        'application/n-triples; charset=UTF-8':'nquads',
        'application/n-quads':'nquads',
        'application/n-quads; charset=UTF-8':'nquads',
        'text/plain; charset=UTF-8':'nt',
        'application/turtle':'turtle',
        'application/rdf+xml':'rdf'
    }

exportformats = {
        'application/n-quads':'nquads',
        #'text/plain':'nt',
    }

# command line parameters
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--host', default='127.0.0.1', type=str)
parser.add_argument('-p', '--port', default=5000, type=int)
parser.add_argument('-i', '--input', default='guess', choices=[
        'html',
        'hturtle',
        'mdata',
        'microdata',
        'n3',
        'nquads',
        'nt',
        'rdfa',
        'rdfa1.0',
        'rdfa1.1',
        'trix',
        'turtle',
        'xml'
    ], help='Optional input format')

args = parser.parse_args()
fi =os.path.abspath(args.file)

if args.input == 'guess':
    fo = rdflib.util.guess_format(fi)
else:
    fo = args.input

# new graph
g = fg.FileGraph(fi, fo)

#app = FlaskAPI(__name__)
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def __savegraph(path):
    g.savefile(path)

def __resourceexists(resourceuri):
    query = ' ASK { <' + resourceuri + '> ?p ?o . } '
    result = g.query(query)

    return bool(result)

def __resourceisgraphuri(resourceuri):
    query = ' ASK {graph <' + resourceuri + '> { ?s ?p ?o } } '
    result = g.query(query)

    return bool(result)

'''
API
'''

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET', 'PUT'])
def index(path):
    '''
    List last commits.
    '''
    url                = request.url
    print('URL', url)
    resourceisgraphuri = __resourceisgraphuri(url)
    resourceexists     = __resourceexists(url)

    if request.method == 'POST' or request.method == 'PUT':
        # we have to write data
        if request.environ['CONTENT_TYPE'] not in importformats:
            print('Content-Type ' + request.environ + ' not supported')
            resp = Response(status=404)
            return resp

        # but not if the resource already exists
        if resourceexists:
            print('Could not insert data. Resource \"' + request.url + '\" allready exists.')
            resp = Response(status=404)
            return resp

        # and if the resource already exists as a graph
        if resourceisgraphuri:
            print('Could not insert data. A graph with URI \"' + request.url + '\" allready exists.')
            resp = Response(status=404)
            return resp

        # write
        g.addstatement(request.data, importformats[request.environ['CONTENT_TYPE']])
        resp = Response(status=201)

        # and save
        # TODO: if exithandler will work, there is no need to save after every input
        __savegraph(fi)
        return resp

    elif request.method == 'GET':
        #
        print('GET empfangen')
        if resourceisgraphuri and resourceexists:
            print('Resource existiert und ein Graph ebenfalls')
            data = g.dumpgraph(url)
            data+= g.getresource(url)
            data+= g.getobject(url)
            resp = Response(data, status=200, mimetype='application/n-quads')
        elif resourceisgraphuri:
            print('Resource ist Graph, dumpe ganzen Graph')
            data = g.dumpgraph(request.url)
            resp = Response(data, status=200, mimetype='application/n-quads')
        elif resourceexists:
            print('Resource ' + request.url + ' gefunden, hier kommt sie')
            data = g.getresource(request.url)
            resp = Response(data, status=200, mimetype='application/n-quads')
        else:
            print('Resource ' + request.url + ' nicht gefunden')
            resp = Response(status=404)

        return resp


#@app.route("/nextresource", methods=['GET'])
@app.route("/", methods=['GET'])
def getnextresourceuri():
    dn = request.url_root
    m = hashlib.sha1()
    while True:
        now = str(time.time())
        m.update(now.encode('UTF-8'))
        urihash = m.hexdigest()[:32]
        print(urihash)
        resource = request.url_root + urihash
        if __resourceexists(resource) == False:
            data = ('url', dn)
            resp = Response(json.dumps({'nexthash':urihash, 'nexturl':resource}), status=200, mimetype='application/json')
            return resp

def main():
    app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    with handleexit.handle_exit(__savegraph(fi)):
        main()
