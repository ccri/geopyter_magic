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

    @line_magic
    def json_to_histogram(self, line):
        js_template = (
            'requirejs(["../../nbextensions/geopyter/geopyter.js"], function(geopyter) {'
            '   var xhr = new XMLHttpRequest();'
            '   xhr.onreadystatechange = function() {'
            '       if (this.readyState == 4 && this.status == 200) {'
            '           var data = JSON.parse(this.response);'
            '           console.log(data);'
            '           geopyter.histogram("hg_0", data, element);'
            '       }'
            '   };'
            '   xhr.open("GET", "%s", true);'
            '   xhr.send();'
            '});'
        )

        return Javascript(js_template % line)

    @line_magic
    def json_to_time_series(self, line):
        js_template = (
            'requirejs(["../../nbextensions/geopyter/geopyter.js"], function(geopyter) {'
            '   var xhr = new XMLHttpRequest();'
            '   xhr.onreadystatechange = function() {'
            '       if (this.readyState == 4 && this.status == 200) {'
            '           var data = JSON.parse(this.response);'
            '           console.log(data);'
            '           geopyter.timeSeries("ts_0", data, element);'
            '       }'
            '   };'
            '   xhr.open("GET", "%s", true);'
            '   xhr.send();'
            '});'
        )

        return Javascript(js_template % line)

def load_ipython_extension(ipython):
    ipython.register_magics(GeopyterMagic)