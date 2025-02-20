import numpy as np
from SCEUA import sceua
import sys

maxn=1000
kstop=30
pcento=0.01
peps=0.001
iseed= 42
ngs=5
bU = np.array([0.4,1.0,50.0,1.0,30,30,30,0.5,1.5,1.5,0.99])
bL = np.array([0.00001, 0.001,0.1, 0.001,3.0,3.0,3.0,0.01,0.1,0.1,0.0])
number = int(sys.argv[1])
# soil_all[['infilt', 'Ds', 'Dsmax', 'Ws',
#        'expt1', 'expt2', 'expt3','Depth1', 'Depth2', 'Depth3' Kq(routing)]]
initial_parm  =  np.array([0.3,0.1,10.0,0.7,12.0,12.0,12.0,0.1,0.3,1.5,0.23])
states        =  np.array([15.0, 50.0,150.0, 0.5,0.5,0.5])
bestx,bestf = sceua(initial_parm,bL,bU,maxn,kstop,pcento,peps,ngs,iseed,states,number)
print(bestf)
print(bestx)
np.save(f"Parm_{number}.npy", bestx)
