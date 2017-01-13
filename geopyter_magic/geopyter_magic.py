from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
    line_cell_magic)
from IPython.display import (HTML, Javascript)

import ast
import os
import requests

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

    @line_magic
    def typeof_var(self, line):
        output = ast.literal_eval(line)
        # py_dict = json.loads(line)
        # sum = 0
        # for n in line:
        #     sum += int(n)

        print type(output), output

    @line_cell_magic
    def geopyter(self, line, cell=None):

        if cell is not None:
            line += ' ' + cell.replace('\n', ' ')

        args = line.strip().split(' ')

        cleaned_args = {}
        for arg in args:
            arg = arg.replace(')', '')
            key, value = arg.split('(')
            cleaned_args[key] = value

        r = requests.post('http://localhost:8888/geopyter', json=cleaned_args)
        print r.json()
        print os.environ

def load_ipython_extension(ipython):
    ipython.register_magics(GeopyterMagic)