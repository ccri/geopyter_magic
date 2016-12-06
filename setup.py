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
          ('share/jupyter/nbextensions', [
              'geopyter_magic/geopyter.js']),
          ('share/jupyter/nbextensions/geopyter', [
              'geopyter_magic/geopyter.js',
              'geopyter_magic/geopyter.css']),
          ('share/jupyter/nbextensions/d3js', [
              'external/d3js/d3.v4.4.min.js']),
          ('share/jupyter/nbextensions/leaflet', [
              'external/leaflet/leaflet.v1.0.2.min.js',
              'external/leaflet/leaflet.css']),
          ('share/jupyter/nbextensions/leaflet/images', [
              'external/leaflet/images/layers.png',
              'external/leaflet/images/layers-2x.png',
              'external/leaflet/images/marker-icon.png',
              'external/leaflet/images/marker-icon-2x.png',
              'external/leaflet/images/marker-shadow.png'])
          ]
      )