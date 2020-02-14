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
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import hvplot.pandas
import datashader as ds
import dask
import bokeh
import holoviews as hv
import panel as pn
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
__license__ = 'MIT'
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
    for file in glob.iglob('extract_dir/*/data/per-*.csv'):
        print(file)
        data = pd.read_csv(file)
        data.head()
    fig = px.bar(data, x = 'Sample name', y = 'Sequence count', title = 'test graph')
    # HIDE FOR NOW fig.show()
    fig1 = go.Figure(go.Scatter(x = data['Sample name'], y = data['Sequence count'],
                                name ='test graph object'))
    fig1.update_layout(title='Demux data', plot_bgcolor='rgb(230,200,170)',
                       showlegend=True)
    # HIDE FOR NOW fig1.show()
    print(type(data)) #produces <class 'pandas.core.frame.DataFrame'>

    df_widget = pn.widgets.DataFrame(data, name='DataFrame')

    df_widget.show()


    ###PANEL MODULE
    def select_row(row=0):
        return data.loc[row]
    slide = pn.interact(select_row, row=(0, len(data)-1))
    # THIS STOPS EXECUTION --> slide.show()
    # slide1 = pn.interact(select_row, row=(0, 25))
    # slide1.show()
    #slide.servable() # FOR USE WITH 'panel serve' command on notebook file .ipynb
    # this above call should also work for .py files

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

    EXTRA - keep for now
    # data = data.set_index('Sample name')

    # with gzip.open(demux, 'rb'):
        # get into random directory beneath the qzv then to data
    # for root, dirs, files in os.walk(dir_name):
    #    isDirectory = os.path.isdir(fpath)
        # file = open('*/data/per-sample-fastq-counts.csv'
    # file = Visualization.load(demux)
    # doesn't seem like many options for this method
    # file.hvplot()
    # hvplot
"""
