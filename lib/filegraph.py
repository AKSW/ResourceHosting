import rdflib
from rdflib.plugins.parsers.nquads import NQuadsParser
import os
import sys
import random

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

    def serializetriples(self, triples):
        data = []
        for triple in triples:
            data.append(triple[0].n3() + ' ' + triple[1].n3() + ' ' + triple[2].n3() + ' .\n')
        return data

    def addstatement(self, statement, rdfserialization):
        data = statement.decode('UTF-8')
        self.tempgraph = rdflib.graph.ConjunctiveGraph()
        self.tempgraph.parse(data=data, format=rdfserialization)
        quads = self.tempgraph.quads((None, None, None, None))
        bnodes = {}
        newdata = ''

        # rdflib will reidentify blanknodes during a sessions
        # a parsed BNode '_:a' will always get the same hash from rdflib
        # this is a quick workaround
        for quad in quads:
            subject = quad[0].n3().strip('[]')
            if subject.startswith('_:', 0, 2):
                if subject not in bnodes:
                    bnodes[subject] = '_:' + str(random.getrandbits(128))
                subject = bnodes[subject]
            else:
                subject = quad[0].n3()
            object = quad[2].n3().strip('[]')
            if object.startswith('_:', 0, 2):
                if object not in bnodes:
                    bnodes[object] = '_:' + str(random.getrandbits(128))
                object = bnodes[object]
            else:
                object = quad[2].n3()
            graph = quad[3].n3().strip('[]')
            if graph.startswith('_:', 0, 2):
                newdata += subject + ' ' + quad[1].n3() + ' ' + object + ' .\n'
            else:
                newdata += subject + ' ' + quad[1].n3() + ' ' + object + ' ' + graph + ' .\n'

        self.graph.parse(data=newdata, format='nquads')
        g = None
        return

    def triplestest(self, resource):
        return self.graph.context_id(resource)

    def savefile(self, path):
        f = open(path, 'w')

        self.content = self.graph.serialize(format='nquads')

        f.write( self.content.decode('UTF-8'))
        f.close

    def getcontexts(self):
        return self.graph.context()

    def getresource(self, subjecturi, serialization):
        # check if subject is BNode
        if subjecturi.startswith('_:', 0, 2):
            subject = rdflib.BNode(subjecturi[2:])
        else:
            subject = rdflib.term.URIRef(subjecturi)

        # get the quads
        triples = self.graph.quads((subject, None, None, None))

        data = []

        if serialization == 'nquads':
            data+= self.serializequads(triples)
        else:
            data+= self.serializetriples(triples)

        # get them again
        triples = self.graph.quads((subject, None, None, None))
        for triple in triples:
            test = triple[2].n3().strip('[]')
            if test.startswith('_:', 0, 2):
                data+=self.getresource(test, serialization)

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
