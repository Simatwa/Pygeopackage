#!/usr/bin/env python
# coding: utf-8

# In[9]:


# !pip install pathlib
# !pip install rasterio

from rasterio.plot import show
from rasterio.merge import merge
import rasterio as rio
from pathlib import Path
path = Path(r'F:\Users\Lawrence\DEM')
Path('output').mkdir(parents=True, exist_ok=True)
output_path = r'F:\Users\Lawrence\DEMM3MOSAIC\mosaic_output.tif'

raster_files = list(path.iterdir())
raster_to_mosiac = []

for p in raster_files:
    raster = rio.open(p)
    raster_to_mosiac.append(raster)

mosaic, output = merge(raster_to_mosiac)

output_meta = raster.meta.copy()
output_meta.update(
    {"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": output,
    }
)

with rio.open(output_path, 'w', **output_meta) as m:
    m.write(mosaic)

