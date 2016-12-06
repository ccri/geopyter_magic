from .geopyter_magic import *

def load_ipython_extension(ipython):
    ipython.register_magics(GeopyterMagic)

def load_jupyter_server_extension(nb_server_app):
    nb_server_app.log.info('geopyter_magic enabled')

def _jupyter_server_extension_paths():
    return [{
        'module': 'geopyter_magic'
    }]