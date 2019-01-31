
import tomopy as tp
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
import dxchange

# obj = tp.lena()
# plt.imshow(obj[0,:,:])
# plt.show()
#
# mlab.imshow(obj[64,:,:])
#
#
# mlab.contour3d(obj[:,:,:])
# mlab.show()

h5fname = '/media/hijizhou/Data2/NeronXRecon/Data/brain2_MOSAIC-TOMO_180722_2039/rep01_00091_brain2_-085.00_Degree_x01_y00_00000.00_eV_001of001.xrm'

proj, metadata = dxchange.reader.read_xrm(h5fname, [])

h5fname2 = '/media/hijizhou/Data2/NeronXRecon/Data/brain2_MOSAIC-TOMO_180722_2039/rep01_02996_brain2_0076.00_Degree_x08_y00_00000.00_eV_001of001.xrm'

proj, metadata2 = dxchange.reader.read_xrm(h5fname2, [])


import exchange as ec
ec.app_ssrl_xrm_mosaic_metadata('rep01_02996_brain2_0076.00_Degree_x08_y00_00000.00_eV_001of001.xrm')


h5fname = '/media/hijizhou/Data2/NeronXRecon/Data/201807221943_8000_eV_ref.xrm'

f = h5py.File(fname)
dset = f['exchange/data']
nframes = dset.shape[0]
alloc_sets = allocate_mpi_subsets(nframes, size)
for frame in alloc_sets[rank]:
    print('Rank: {:d}; Frame: {:d}.'.format(rank, frame))
    dset[frame, :, :] = gaussian_filter(dset[frame, :, :], sigma)
f.close()
gc.collect()
h5fname = '/media/hijizhou/Data1/NeronXRecon/Data/201807221943_8000_eV_ref.xrm'
proj = dxchange.reader.read_xrm(h5fname, [])

h5fname = '/media/hijizhou/Data1/NeronXRecon/Data/201807221943_8000_eV_ref.xrm'

f = h5py.File(fname)
dset = f['exchange/data']
nframes = dset.shape[0]
alloc_sets = allocate_mpi_subsets(nframes, size)
for frame in alloc_sets[rank]:
    print('Rank: {:d}; Frame: {:d}.'.format(rank, frame))
    dset[frame, :, :] = gaussian_filter(dset[frame, :, :], sigma)
f.close()
gc.collect()

# mlab.imshow(proj[0])
# mlab.show()

plt.imshow(proj[0])
plt.show()

