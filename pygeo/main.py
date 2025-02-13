#!/usr/bin/env python
# coding: utf-8

from rasterio.plot import show
from rasterio.merge import merge
import rasterio as rio
from os import path, makedirs, listdir
import logging
import argparse
from . import __version__

logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s ",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def error_handler():
    def decorator(func):
        def main(*args, **kwargs):
            try:
                logging.debug("Program started")
                resp = func(*args, **kwargs)
                logging.debug("Program stopped")
            except Exception as e:
                logging.error(e.args[0] if len(e.args) > 1 else str(e))
            else:
                return resp

        return main

    return decorator


class pygeo:
    def __init__(self, args: object):
        self.args = args
        self.create_dirs()

    def __str__(self):
        return "Mosaic rasterfile"

    @error_handler()
    def create_dirs(self):
        dirname = path.dirname(self.args.output_path)
        if not path.isdir(dirname):
            makedirs(dirname)

    @error_handler()
    def main(self):
        """Main method"""
        path = self.args.input_dir
        output = self.args.output_path
        raster_files = listdir(output)  # List of contents - input
        raster_to_mosiac = []
        for p in raster_files:
            raster = rio.open(p)
            raster_to_mosiac.append(raster)
        mosaic, output = merge(raster_to_mosiac)
        output_meta = raster.meta.copy()
        output_meta.update(
            {
                "driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": output,
            }
        )
        with rio.open(output, "w", **output_meta) as m:
            m.write(mosaic)


def main():
    parser = argparse.ArgumentParser(description="Mosaic rasterfile")
    parser.add_argument("-v", "--version", action="version", version=f"v{__version__}")
    parser.add_argument(
        "--input-dir", help="Path to directory containing raster files", required=True
    )
    parser.add_argument(
        "--output", dest="output_path", help="Path to save the output", required=True
    )
    resp = parser.parse_args()
    if not resp.output_path.endswith(".tif"):
        resp.output_path = resp.output_path + ".tif"
    run = pygeo(resp)
    run.main()
