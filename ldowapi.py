from flask import request, Flask, Response
from flask_negotiate import consumes, produces
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

exportformats = {
        'text/plain':'nt',
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
fi =os.path.abspath(args.file)

if args.input == 'guess':
    fo = rdflib.util.guess_format(fi)
else:
    fo = args.input

# new graph
g = fg.FileGraph(fi, fo)

#app = FlaskAPI(__name__)
app = Flask(__name__)


def savegraph(path):
    print('Saving graph')
    g.savefile(path)

def __dumpgraph(graphuri):
    return g.dumpgraph(graphuri)

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
    print(query)
    result = g.query(query)
    print(result)

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
    triples = g.getresource(request.url)
    print('Triples')
    for triple in triples:
        print(triple)

    if request.method == 'POST' or request.method == 'PUT':
        # we have to write data
        if request.environ['CONTENT_TYPE'] not in importformats:
            print('Content-Type ' + request.environ + ' not supported')
            resp = Response(status=404)
            return resp

        # but not if the resource already exists
        if __resourceexists(request.url) == True:
            print('Could not insert data. Resource \"' + request.url + '\" allready exists.')
            resp = Response(status=404)
            return resp

        # and if the resource already exists as a graph
        if __resourceisgraphuri(request.url) == True:
            print('Could not insert data. A graph with URI \"' + request.url + '\" allready exists.')
            resp = Response(status=404)
            return resp

        # write
        __addstatement(request.data, importformats[request.environ['CONTENT_TYPE']])
        resp = Response(status=200)

        # and save
        # TODO: if exithandler will work, there is no need to save after every input
        savegraph(fi)
        return resp

    elif request.method == 'GET':
        if __resourceisgraphuri(request.url) == True:
            print('Resource ist Graph, dumpe ganzen Graph')
            data = __dumpgraph(request.url)
            resp = Response(data, status=200, mimetype='text/plain')
        elif __resourceexists(request.url) == True:
            print('Resource gefunden, hier kommt sie')
            data = __getresource(request.url)
            resp = Response(data, status=200, mimetype='text/plain')
        else:
            print('Resource nicht gefunden')
            resp = Response(status=404)

        return resp

def main():
    app.run(debug=True)

if __name__ == '__main__':
    with handleexit.handle_exit(savegraph(fi)):
        main()
