#!/usr/bin/env python3
#/home/mat/anaconda3/envs/qiime2-2019.10/bin python3
#/home/mat/anaconda3/envs/qiime2-2019.10/bin Python3


"""
Foundation of a visualization pipeline using Qiime2 artifact API and
Holoviz tools for interactive data comparison
"""

# Built-in/Generic Imports
import os
import sys
import argparse
# Libs
import csv
import re
import unittest
import zipfile
from pathlib import Path
import glob
import argparse
import fnmatch
# Import Holoviz libraries
import pandas as pd
import numpy as np
import hvplot.pandas
import datashader as ds
import dask
import bokeh
import holoviews as hv
from distutils.version import LooseVersion
from qiime2 import Artifact
from qiime2 import Visualization
from qiime2.plugins import feature_table
import biom

# min_versions = dict(pd='0.24.0', ds='0.7.0', dask='1.2.0', bokeh='1.2.0',
#                     hv='1.12.3')

__author__ = 'Mathew Richards'
__copyright__ = 'Copyright 2020, AAFC-AAC'
__credits__ = ['Mathew Richards', 'Rodrigo Ortega Polo']
__license__ = 'GPL'
__version__ = '3'
__maintainer__ = 'Mathew Richards'
__email__ = 'mathew.richards@canada.ca'
__status__ = 'Draft'

print("\n", "****Visualization Tools****", "\n")

def setup():
    """Get the directory path from command line arg"""
    # argparse section for command line arguments
    parser = argparse.ArgumentParser(description='Visualization stuff')
    parser.add_argument('directory',
                        help='The directory path where '
                        'your qiime2 files are located')
    args = parser.parse_args()
    try:
        dir_name = args.directory
        print("The entered directory is:", dir_name, "\n")
    except OSError:
        print('ERROR: Enter path to data in command line argument')
    return dir_name


def main():
    dir_name = setup()
    print('\n', 'Start of main', '\n')
    p = Path('extract_dir')
    p.mkdir(exist_ok=True)
    demux = dir_name + '/demux.qzv'
    print(demux)
    data_zip = zipfile.ZipFile(demux, 'r')
    data_zip.extractall(path='extract_dir')
    # potential to add a RegEx condition to create extract_dir based
    # on input files or directory
    plot = ' '
    for file in glob.iglob('extract_dir/*/data/per-*.csv'):
        print(file)
        data = pd.read_csv(file)
    print(type(data))
    data = data.set_index('Sample name')
    data.tail()
    # with gzip.open(demux, 'rb'):
        # get into random directory beneath the qzv then to data
    # for root, dirs, files in os.walk(dir_name):
    #    isDirectory = os.path.isdir(fpath)
        # file = open('*/data/per-sample-fastq-counts.csv'
    # file = Visualization.load(demux)
    # doesn't seem like many options for this method
    # file.hvplot()
    # hvplot
    tutorial(dir_name)
    # data_zip.close()

def tutorial(dir_name):
    print('\n', 'Running the Artifact API tutorial section', '\n')
    table = dir_name + '/table.qza'
    unrarefied_table = Artifact.load(table)
    rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100)
    rarefied_table = rarefy_result.rarefied_table
    biom_table = rarefied_table.view(biom.Table)
    print(biom_table.head())

if __name__ == '__main__':
    main()

"""
ROADMAP
import holoviz and re-create existing graphs from qiime2 analysis
    multiple plots at once!!
    filters and categories!!
    how to automate the import of their data??

output those in the proper bokeh server?
    create a conda env with the req. packages for this
        python-snappy, fastparquet, pyarrow, bokeh, etc.

add interactivity and other plots in future
    transcriptomics, proteomics, metabolomics, etc.
"""
