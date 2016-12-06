from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
    line_cell_magic)
from IPython.display import (HTML, Javascript)

@magics_class
class GeopyterMagic(Magics):
    @line_magic
    def lmagic(self, line):
        print('Full access to the main IPython object:', self.shell)
        print('Variables in the user namespace:', list(self.shell.user_ns.keys()))
        return line

    @cell_magic
    def cmagic(self, line, cell=None):
        return line, cell

    @line_magic
    def geopyter_test(self, line=None):
        js_template = (
            'requirejs(["../../nbextensions/geopyter/geopyter.js"], function(geopyter) {'
            '   geopyter.test();'
            '});'
        )

        return Javascript(js_template)

    @line_magic
    def geojson_to_leaflet(self, line):
        js_template = (
            'requirejs(["../../nbextensions/geopyter/geopyter.js"], function(geopyter) {'
            '   geopyter.geojsonToLeaflet("geojson_example", "%s", element);'
            '});'
        )

        return Javascript(js_template % line)

def load_ipython_extension(ipython):
    ipython.register_magics(GeopyterMagic)