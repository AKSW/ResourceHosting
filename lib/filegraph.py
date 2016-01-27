import rdflib
from rdflib.plugins.parsers.nquads import NQuadsParser
import os
import sys

class FileGraph:
    def __init__(self, graphfile, rdfserialization='nquads', defaultgraphuri='http://localhost:5000/default'):
        self.serialization = rdfserialization
        self.defaultgraphuri = defaultgraphuri

        try:
            self.graph = rdflib.graph.ConjunctiveGraph()
            self.graph.parse(graphfile,format=rdfserialization)
        except:
            print('Error: Path ' +  graphfile + ' could not been opened')
            raise ValueError

        print('Success: File ' + graphfile + ' is now known as a graph')

        return

    def serializequads(self, quads):
        data = []
        for quad in quads:
            graph = quad[3].n3().strip('[]')
            if graph.startswith('_:', 0, 2):
                data.append(quad[0].n3() + ' ' + quad[1].n3() + ' ' + quad[2].n3() + ' .\n')
            else:
                data.append(quad[0].n3() + ' ' + quad[1].n3() + ' ' + quad[2].n3() + ' ' + graph + ' .\n')
        return data

    def addstatement(self, statement, rdfserialization):
        data = statement.decode('UTF-8')
        self.graph.parse(data=data, format=rdfserialization)
        return

    def triplestest(self, resource):
        return self.graph.context_id(resource)

    def savefile(self, path):
        f = open(path, "w")

        self.content = self.graph.serialize(format="nquads")

        f.write( self.content.decode('UTF-8'))
        f.close

    def getcontexts(self):
        return self.graph.context()

    def getresource(self, subjecturi, serialization):
        subject = rdflib.term.URIRef(subjecturi)
        triples = self.graph.quads((subject, None, None, None))
        data = []
        if serialization == 'nquads':
            data+= self.serializequads(triples)
        else:
            for triple in triples:
                data.append(triple[0].n3() + ' ' + triple[1].n3() + ' ' + triple[2].n3() + ' .\n')
        return data

    def getobject(self, objecturi, serialization):
        object = rdflib.term.URIRef(objecturi)
        triples = self.graph.quads((None, None, object, None))
        data = []
        if serialization == 'nquads':
            data+= self.serializequads(triples)
        else:
            for triple in triples:
                data.append(triple[0].n3() + ' ' + triple[1].n3() + ' ' + triple[2].n3() + ' .\n')
        return data

    def dumpgraph(self, graphuri, serialization):
        graph = rdflib.term.URIRef(graphuri)
        triples = self.graph.quads((None, None, None, graphuri))
        data = []
        for triple in triples:
            if serialization == 'nquads':
                data.append(triple[0].n3() + ' ' + triple[1].n3() + ' ' + triple[2].n3() + ' <' + graphuri + '> .\n')
            else:
                data.append(triple[0].n3() + ' ' + triple[1].n3() + ' ' + triple[2].n3() + ' .\n')
        return data

    def query(self, querystring, context='default'):
        if context == 'default':
            result = self.graph.query(querystring)
        else:
            contextgraph = self.graph.get_context(context)
            result = contextgraph.query(querystring)
        return result

class FileList:
    def __init__(self):
        self.files = {}

    def getgraphobject(self, graphuri):
        for k, v in self.files.items():
            if k == graphuri:
                return v
        return

    def graphexists(self, graphuri):
        graphuris = list(self.files.keys())
        try:
            graphuris.index(graphuri)
            return True
        except ValueError:
            return False

    def addFile(self, name, graphFileObject):
        try:
            self.files[name] = graphFileObject
        except:
            print('Something went wrong with file: ' + name)
            raise ValueError

    def getgraphlist(self):
        return list(self.files.keys())
