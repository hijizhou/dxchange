#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the xrm tomography data from
the original stack of xrm. To use rename the xrm data as 
radios/image_00000.xrm and flats/ref_00000.xrm
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    fname = '/media/hijizhou/Data2/SLAC/brain2_single_mosaic_MOSAIC_180722_2023'

    proj_start = 0
    proj_end = 1800
    flat_start = 0
    flat_end = 100

    ind_tomo = range(proj_start, proj_end)
    ind_flat = range(flat_start, flat_end)

    # Select the sinogram range to reconstruct.
    start = 0
    end = 16

    file_pattern = 'rep01_00000_brain2_single_mosaic_x00_y00_00000.00_eV_001of001.xrm'
    ref_pattern = 'rep01_ref_00000_brain2_single_mosaic_00000.00_eV_001of003.xrm'
    # APS 26-ID has an x-radia system collecting raw data as xrm.
    proj, flat, metadata = dxchange.read_ssrl_xrm(fname, ind_tomo, ind_flat, image_file_pattern=file_pattern,
                  flat_file_pattern=ref_pattern,
                                                 sino=(start, end))

    # make the darks
    dark = np.zeros((1, proj.shape[1], proj.shape[2]))    

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    # Find rotation center.
    rot_center = tomopy.find_center(proj, theta, init=1024,
                                    ind=0, tol=0.5)
    print("Center of rotation: ", rot_center)

    proj = tomopy.minus_log(proj)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/recon')
