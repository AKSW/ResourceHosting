from flask.ext.api.decorators import set_parsers, set_renderers
from flask.ext.api.parsers import JSONParser, BaseParser
from flask.ext.api.renderers import JSONRenderer
from flask.ext.api import renderers
'''
PARSER
'''

class NquadsParser(BaseParser):
    """
    This pclass YAMLRenderer(renderers.BaseRenderer):
    """
    media_type = 'application/nquadsfrom flask.ext.api.decorators import set_renderers'

    def parse(self, stream, media_type, **options):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read().decode('utf8')

class TurtleParser(BaseParser):
    """
    This parser accepts some RDF serializations.
    """
    media_type = 'text/turtle'

    def parse(self, stream, media_type, **options):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read().decode('utf8')

class TrigParser(BaseParser):
    """
    This parser accepts some RDF serializations.
    """
    media_type = 'text/TrigParser'

    def parse(self, stream, media_type, **options):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read().decode('utf8')

'''
RENDERER
'''

class TurtleRenderer(renderers.BaseRenderer):
    media_type = 'application/turtle'

    def render(self, data, media_type, **options):
        return yaml.dump(data, encoding=self.charset)

class NquadsRenderer(renderers.BaseRenderer):
    media_type = 'application/turtle'

    def render(self, data, media_type, **options):
        return yaml.dump(data, encoding=self.charset)
