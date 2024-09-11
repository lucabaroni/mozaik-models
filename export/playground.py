#%%
import os
import numpy as np
import matplotlib.pyplot as plt
folder = 'test'

resp = np.load('/CSNG/baroni/test/single_trial/0000000001/V1_Exc_L23.npy')
stim = np.load('/CSNG/baroni/test/single_trial/0000000001/stimulus.npy')
plt.imshow(stim)
plt.show()
plt.plot(resp)
plt.show()

# %%

folder = 'Dic23data'
resp2 = np.load('/CSNG/baroni/LSV1M_Dec23/temp/CSNG/baroni/Dic23data/single_trial/0000000001/V1_Exc_L23.npy')
stim2 = np.load('/CSNG/baroni/LSV1M_Dec23/temp/CSNG/baroni/Dic23data/single_trial/0000000001/stimulus.npy')


plt.imshow(stim2)
plt.show()
plt.plot(resp2)
plt.show()
# %%
resp2

# %%
resp2
# %%
resp
# %%