
import tomopy as tp
import numpy as np
import matplotlib.pyplot as plt
# from mayavi import mlab
from dxchange import exchange
from dxchange import writer
# import dxchange.reader as dr

# obj = tp.lena()
# plt.imshow(obj[0,:,:])
# plt.show()
#
# mlab.imshow(obj[64,:,:])
#
#
# mlab.contour3d(obj[:,:,:])
# mlab.show()

# h5fname = '/media/hijizhou/Data2/NeronXRecon/Data/brain2_MOSAIC-TOMO_180722_2039/rep01_00091_brain2_-085.00_Degree_x01_y00_00000.00_eV_001of001.xrm'

h5fname3 = '/Users/hijizhou/Downloads/rep01_00038_brain2_-088.00_Degree_x02_y00_00000.00_eV_001of001.xrm'

# proj, metadata = dxchange.reader.read_xrm(h5fname, [])
#
# h5fname2 = '/media/hijizhou/Data2/NeronXRecon/Data/brain2_MOSAIC-TOMO_180722_2039/rep01_02996_brain2_0076.00_Degree_x08_y00_00000.00_eV_001of001.xrm'
#
# proj, metadata2 = dxchange.reader.read_xrm(h5fname2, [])


h5fname3 = '/media/hijizhou/Data2/NeronXRecon/Data/brain2_MOSAIC-TOMO_180722_2039/'
h5fname3 = '/media/hijizhou/Data2/NeronXRecon/Data/TestDataX01/'

# h5fname3 = '/Users/hijizhou/Downloads/TestDataX01/'


tomo, flat, metadata = exchange.read_slac_ssrl(h5fname3, 0)
#
# arr, metadata = exchange.dxreader.read_xrm_stack(h5fname3 + 'rep01_00038_brain2_-088.00_Degree_x02_y00_00000.00_eV_001of001.xrm.xrm', list(range(0, 1)))

# reconstruction (1,1) object
ind = metadata["motorX"]==1
tomo_x1 = tomo[ind,:,:]
flat_x1 = flat[ind,:,:]
degree = metadata["degree"][ind]

# proj = tp.normalize(tomo_x1, flat, dark)
proj = tomo_x1
proj = tp.minus_log(proj)

writer.write_hdf5(proj, '/media/hijizhou/Data2/NeronXRecon/Data/TestDataX01.h5')

rot_center = tp.find_center(proj, degree, init=290, ind=0, tol=0.5)

degree +=90
extra_options ={'MinConstraint':0}
options = {'proj_type':'cuda', 'method':'SIRT_CUDA', 'num_iter':5, 'extra_options':extra_options}
recon = tp.recon(proj, degree, center=rot_center, algorithm=tp.astra, options=options,ncore=1)
recon = tp.circ_mask(recon, axis=0, ratio=0.95)
print(len(recon))
plt.imshow(recon[0], cmap='Greys_r')
plt.show()


writer.write_tiff(recon, '/media/hijizhou/Data2/NeronXRecon/Data/Test.tiff')

# options = {'proj_type':'cuda', 'method':'FBP_CUDA'}
# recon = tp.recon(proj, degree, center=rot_center, algorithm=tp.astra, options=options)
# recon = tp.circ_mask(recon, axis=0, ratio=0.95)

# recon = tp.recon(proj, degree+90, center=rot_center, algorithm='gridrec')
# recon = tp.circ_mask(recon, axis=0, ratio=0.95)
#
# plt.imshow(recon[800,:,:], cmap='Greys_r')
# plt.show()

