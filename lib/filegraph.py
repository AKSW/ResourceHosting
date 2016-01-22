import rdflib
from rdflib.plugins.parsers.nquads import NQuadsParser
import os
import sys

class FileGraph:
    def __init__(self, graphfile, rdfserialization):
        self.serialization = rdfserialization
        self.savecount = 0

        try:
            self.graph = rdflib.graph.ConjunctiveGraph(identifier='default')
            self.graph.parse(graphfile,format='nquads')
        except:
            print('Error: Path ' +  graphfile + ' could not been opened')
            raise ValueError

        print('Success: File ' + graphfile + ' is now known as a graph')

        return

    def addstatement(self, statement, rdfserialization):
        self.graph.parse(data=statement.decode('UTF-8'), format=rdfserialization)
        return

    def triplestest(self, resource):
        return self.graph.context_id(resource)

    def savefile(self, path):
        print('Saving graph ', path)

        f = open(path, "w")

        self.content = self.graph.serialize(format="nquads")
        f.write( self.content.decode('UTF-8'))
        f.close

    def getcontexts(self):
        return self.graph.context()

    def getresource(self, subjecturi):
        subject = rdflib.term.URIRef(subjecturi)
        triples = self.graph.triples((subject, None, None))
        data = ''
        for triple in triples:
            data+= triple[0].n3() + ' ' + triple[1].n3() + ' ' + triple[2].n3() + ' .\n'
        return data

    def dumpgraph(self, graphuri):
        contextgraph = self.graph.get_context(graphuri)
        result = contextgraph.serialize(format='nt')
        return result.decode('UTF-8')

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
