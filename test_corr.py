import sys
import scipy
from scipy import stats
import nibabel as nb
import numpy as np

cpac_func_img = nb.load(str(sys.argv[1]))

fmriprep_func_img = nb.load(str(sys.argv[2]))

cpac_func_data = cpac_func_img.get_fdata()
fmriprep_func_data = fmriprep_func_img.get_fdata()

if len(cpac_func_img.shape) < 4 or len(fmriprep_func_img.shape) < 4:
    raise Exception("\n\n[!] At least one of the input files is not a " \
                    "4D/time series dataset.\n")

ts_corrs = []

for i in range(0, cpac_func_img.shape[0]):
    print(f"calculating {i} of {cpac_func_img.shape[0]} row of voxels")
    for j in range(0, cpac_func_img.shape[1]):
        for k in range(0, cpac_func_img.shape[2]):
            ts_corrs.append(scipy.stats.pearsonr(cpac_func_data[i][j][k], fmriprep_func_data[i][j][k])[0])
    print(f"corr: {ts_corrs[-1]}")

ts_corrs = np.asarray(ts_corrs)
ts_corrs = ts_corrs[~np.isnan(ts_corrs)]

print(f"The mean correlation is : {ts_corrs.mean()}")