# -*- coding: utf-8 -*-
"""
.. module:: convert_ALS_legacy.py
   :platform: Unix
   :synopsis: Convert ALS TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read ALS raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples
--------

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re


def main():
    
    file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALS_.tif'
    dark_file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALSdrk_.tif'
    white_file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALSbak_.tif'
    log_file = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALS.sct'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/blakely_ALS_2011.h5'

    verbose = True

    # Read ALS log file data
    file = open(log_file, 'r')
    for line in file:
        if '-scanner' in line:
            Source = re.sub(r'-scanner ', "", line)
            if verbose: print 'Facility', Source
        
        if '-object' in line:
            Sample = re.sub(r'-object ', "", line)
            if verbose: print 'Sample', Sample
            
        if '-senergy' in line:
            Energy = re.findall(r'\d+.\d+', line)
            if verbose: print 'Energy', Energy[0]
            
        if '-scurrent' in line:
            Current = re.findall(r'\d+.\d+', line)
            if verbose: print 'Current', Current[0]

        if '-nangles' in line:
            Angles = re.findall(r'\d+', line)
            if verbose: print 'Angles', Angles[0]

        if '-i0cycle' in line:
            WhiteStep = re.findall(r'\s+\d+', line)
            if verbose: print 'White Step', WhiteStep[0]

    file.close()

    dark_start = 0
    dark_end = 20
    dark_step = 1
    white_start = 0
    white_end = int(Angles[0]) 
    white_step = int(WhiteStep[0])
    projections_start = 0
    projections_end = int(Angles[0])

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 800    
#    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name = file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       projections_zeros = False,
                                                       white_zeros = False,
                                                       dark_zeros = False,
                                                       projections_digits = 4,
                                                       log='INFO'
                                                       )

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = 'test',
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

