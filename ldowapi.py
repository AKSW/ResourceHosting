from flask import request, url_for, Flask, Response
from flask_negotiate import consumes, produces
from flask.ext.api import status #, exceptions, FlaskAPI
#from flask.ext.api.decorators import set_parsers, set_renderers
#from flask.ext.api.parsers import JSONParser, BaseParser
#from flask.ext.api.renderers import JSONRenderer
#from flask.ext.api import renderers
#from lib.misc import TrigParser, TurtleParser, NquadsParser, TurtleRenderer, NquadsRenderer
import lib.filegraph as fg
import rdflib
from  lib import handleexit
import argparse
import os

importformats = {'text/html' : 'html',
        'text/n3':'n3',
        'application/n-quads':'nquads',
        'text/plain':'nt',
        'application/turtle':'turtle',
        'application/rdf+xml':'rdf'
    }

exportformats = {'text/html' : 'html',
        'application/n-quads':'nquads',
    }

# command line parameters
parser = argparse.ArgumentParser()
parser.add_argument('file')
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
global fi
fi =os.path.abspath(args.file)

if args.input == 'guess':
    fo = rdflib.util.guess_format(fi)
else:
    fo = args.input

# new graph
global g
g = fg.FileGraph(fi, fo)

#app = FlaskAPI(__name__)
app = Flask(__name__)


def savegraph(path):
    print('Saving graph')
    g.savefile(path)

def __dumpgraph(resourceuri):
    query = ' CONSTRUCT { ?s ?p ?o .}'
    query+= ' WHERE { ?s ?p ?o } '

    result = g.query(query, resourceuri)

    print('Dump-Result')
    content = ''
    for row in result:
        print(row)

    return content

def __getresource(resourceuri):
    query = ' SELECT ?s ?p ?o WHERE { '
    query+= '   ?s ?p ?o . '
    query+= '   <' + resourceuri + ' ?p ?o . '
    query+= ' } '

    result = g.query(query)

    return result

def __resourceexists(resourceuri):
    query = ' ASK { <' + resourceuri + '> ?p ?o . } '
    result = g.query(query)

    return bool(result)

def __resourceisgraphuri(resourceuri):
    query = ' ASK {graph <' + resourceuri + '> { ?s ?p ?o } } '
    result = g.query(query)

    return bool(result)

def __addstatement(statement, serialization=''):
    g.addstatement(statement, serialization)

    return

'''
API
'''

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET', 'PUT'])
#@set_parsers(JSONParser, TurtleParser, TrigParser, NquadsParser)
#@set_renderers(JSONRenderer, TurtleRenderer, NquadsRenderer)
def index(path):
    '''
    List last commits.
    '''
    print('MediaType: ' + str(request.environ['CONTENT_TYPE']))
    print('Accept: ' + str(request.environ['HTTP_ACCEPT']))

    print(__dumpgraph('http://127.0.0.1:5000/hier/kommt/json/geflogen/3'))

    if request.method == 'POST' or request.method == 'PUT':
        if request.environ['CONTENT_TYPE'] not in importformats:
            resp = Response(js, status=404)
            return resp

        # tage url and add all statements that cotain url as resource uri
        if __resourceexists(request.url) == True:
            return 'Could not insert data. Resource ' + request.url + ' allready exists.'
        if __resourceisgraphuri(request.url) == True:
            return 'Could not insert data. A graph with URI ' + request.url + ' allready exists.'

        #result = __getgraph('http://127.0.0.1:5000/hier/kommt/json/geflogen/3')
        print('Das hier habe ich empfangen: ')
        print(str(request.data.decode('UTF-8')))

        __addstatement(request.data, importformats[request.environ['CONTENT_TYPE']])
        savegraph(fi)

        return 'Cool ein POST-Request kam an, du wolltest Path: ' + path, status.HTTP_201_CREATED
    elif request.method == 'GET':
        if __resourceexists(request.url) == False:
            resp = Response(status=404)
            return resp
        # act as a linked data endpoint
        if __resourceisgraphuri(request.url) == True:
            data = __dumpgraph(request.url), status.HTTP_201_CREATED
            resp = Response(data, status=404, mimetype='application/n-triples')
        else:
            data = __getresource(request.url), status.HTTP_201_CREATED
            resp = Response(data, status=404, mimetype='application/n-triples')
        return resp
    #elif request.method == 'PUT':
        # do something
    #    return 'Cool, ein PUT-Request kam an, du wolltest Path: ' + path, status.HTTP_201_CREATED

def main():
    app.run(debug=True)

if __name__ == '__main__':
    with handleexit.handle_exit(savegraph(fi)):
        main()
