import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import os

def read_profiles(name):

    dct = {}
    f = open(name)
    for i, line in enumerate(f):
        if i == 5:
            keys = line.split()
            break
    f.close()
    data = np.genfromtxt(name,skip_header=5)
    for j, key in enumerate(keys):
        dct[key] = data[:,j]

    return dct

def writenew(where,hgrid,whereto,Prun=False):

    M = []
    FeH = []
    WHO = []

    for hfil in hgrid:
        hdata = np.genfromtxt(hfil,skip_header=6)
        nr = hdata[:,0]
        wo = len("m0.80.ovh0.20.ovhe0.50.z0.01105.y0.26287")+6
        stem = hfil[:-wo]
        pfil = glob(stem+"*.index")
        pfil = pfil[0]
        newfolder = whereto+hfil[len(where):-wo]

        # Create new directories
        if not os.path.exists(newfolder):
            os.mkdir(newfolder)
            os.mkdir(newfolder+"/LOGS/")
            os.mkdir(newfolder+"/FREQS/")

        # Find the corresponding frequency files
        Gyrewhere = stem+"*profile*l0"
        print(Gyrewhere)
        Gyre = glob(Gyrewhere+"*")
        GP = []
        for g in Gyre:
            gp = int(g[g.find("_n")+2:g.find(".prof")])
            GP.extend([gp])
            os.popen("cp " + g + " " + newfolder+"/FREQS/") #Copy frequencies

        # Find and save profiles
        if Prun:
            Prof = glob(stem+"prof*.data")            
            for p in Prof:
                pp = int(p[len(stem)+len("profile"):p.find(".da")])
                if pp in GP:
                    os.popen("cp "+ p +" " + newfolder+"/")

        os.popen("cp "+ pfil + " " +newfolder+"/LOGS/")

        # Check which model numbers correspond to which profile numbers
        pdata = np.genfromtxt(pfil,skip_header=1)
        nrp = pdata[:,0]
        profile = pdata[:,2]

        # Only include those models, for which frequency files exist
        exfr = [i for i, n in enumerate(nrp) if profile[i] in GP]
        nrp = nrp[exfr]
        row = [i+6 for i, n in enumerate(nr) if n in nrp]

        # Write reduced history file
        Done = []
        with open(newfolder+"/LOGS/history.data","w") as f2:
            ofile = open(hfil)
            lines = ofile.readlines()
            for i, line in enumerate(lines):
                if i < 6:
                    f2.write(line)
                elif i in row:
                    words = line.split()
                    modelnr = int(words[0])
                    if (modelnr not in Done):
                        Done.extend([int(words[0])])
                        f2.write(line)

        ofile.close()
        f2.close()
        print(newfolder+"/LOGS/history.data CREATED")

        # To evaluate FeH, we could look in the profile files
        # The initial conditions are, however, also in the inlist-file

#        m0.60.ovh0.20.ovhe0.50.z0.00002.y0.24853
 
        nametag = stem.find("ovh")
        m = float(stem[nametag-5:nametag-1])
        z = float(stem[nametag+18:nametag+25])
        y = float(stem[nametag+27:nametag+34]) 

        print(z,y)

        x = 1. - z - y
        M.extend([m])
        FeH.extend([np.log10(z/x)-np.log10(0.0181)])
        WHO.extend([newfolder])
        print(M,FeH)

        # Write summary so far
        with open(whereto+"overview.txt","w") as f:
            for i, m in enumerate(M):
                f.write(str(m)+ " " + str(FeH[i]) + " " + WHO[i] + "\n")


where = "/rds/projects/2017/miglioa-stellar-grids/GRIDS_PARAM/GRIDPARAM_Diffusion/"
hgrid = glob(where + "*/*track")
whereto = "./OUTREACH_GRID/"
writenew(where,hgrid,whereto,Prun=False)
