#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the xrm tomography data from
the original stack of xrm. To use rename the xrm data as 
radios/image_00000.xrm and flats/ref_00000.xrm
"""

from __future__ import print_function
import tomopy
from dxchange import exchange
import dxchange.writer as writer
import numpy as np
# from spimagine import volshow
import matplotlib.pyplot as plot

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    fname = '/media/hijizhou/Data2/SLAC/TestDataX05'

    proj_start = 0
    proj_end = 360
    flat_start = 0
    flat_end = 5

    ind_tomo = range(proj_start, proj_end)
    ind_flat = range(flat_start, flat_end)

    # Select the sinogram range to reconstruct.
    start = 0
    end = 1000

    file_pattern = 'rep01_00001_brain2_-090.00_Degree_x01_y00_00000.00_eV_001of001.xrm'
    ref_pattern = 'rep01_ref_00000_brain2_-090.00_Degree_00000.00_eV_001of003.xrm'
    # APS 26-ID has an x-radia system collecting raw data as xrm.
    proj, flat, metadata = exchange.read_ssrl_xrm2(fname, ind_tomo, ind_flat, sino=(start, end))

    print("Finished data importing")

    # make the darks
    dark = np.zeros((1, proj.shape[1], proj.shape[2]))    

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    # Find rotation center.
    #rot_center = tomopy.find_center(proj, theta, init=1024,
     #                               ind=0, tol=0.5)
    #print("Center of rotation: ", rot_center)

    proj = tomopy.minus_log(proj)

    rot_center = 1020
    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    #rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    writer.write_tiff_stack(rec, fname='recon_dir/recon')
    plot.imshow(rec[0])
    plot.show()

    # # render the data and returns the widget
    # w = volshow(rec)
    #
    # # manipulate the render states, e.g. rotation and colormap
    # w.transform.setRotation(.1, 1, 0, 1)
    # w.set_colormap("hot")
    #
    # # save the current view to a file
    # w.saveFrame("scene.png")
