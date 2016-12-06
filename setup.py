from setuptools import setup, find_packages

setup(name='geopyter_magic',
      version='0.0.2',
      author='Gerard C. Briones',
      author_email='gbriones@ccri.com',
      packages=find_packages(),
      install_requires=[
          'ipython',
          'jupyter'
      ],
      data_files=[
          ('share/jupyter/nbextensions/geopyter', [
              'geopyter_magic/assets/js/geopyter.js',
              'geopyter_magic/assets/css/geopyter.css']),
          ('share/jupyter/nbextensions/d3js_v4.4', [
              'geopyter_magic/assets/js/d3.v4.4.min.js']),
          ('share/jupyter/nbextensions/leaflet_v1.0.2', [
              'geopyter_magic/assets/js/leaflet.v1.0.2.min.js',
              'geopyter_magic/assets/css/leaflet.css']),
          ('share/jupyter/nbextensions/leaflet_v1.0.2/images', [
              'geopyter_magic/assets/imgs/images/layers.png',
              'geopyter_magic/assets/imgs/images/layers-2x.png',
              'geopyter_magic/assets/imgs/images/marker-icon.png',
              'geopyter_magic/assets/imgs/images/marker-icon-2x.png',
              'geopyter_magic/assets/imgs/images/marker-shadow.png'])
          ]
      )