import sys
import numpy as np
import pandas as pd


specfile = '../Data/uvm_spec.h5'


starname = str(sys.argv[1])
print(starname)
f = pd.read_hdf('../Data/'+specfile,'table')
starnames = np.array(f['#'])
indices = np.arange(len(starnames))
nstar = indices.compress(starnames == starname)
print(nstar)

