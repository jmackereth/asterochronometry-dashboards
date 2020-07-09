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
        stem = hfil[:-12]
        pfil = stem+"profiles.index"
        newfolder = whereto+hfil[len(where):-12]

        # Create new directories
        if not os.path.exists(newfolder):
            os.mkdir(newfolder[:-6])
            os.mkdir(newfolder)
            os.mkdir(newfolder[:-6]+"/FREQS/")

        # Find the corresponding frequency files
        Gyrewhere = where+"/other_gyre/"+hfil[len(where):-17]+"gyre_out/profile"
        Gyre = glob(Gyrewhere+"*")
        GP = []
        for g in Gyre:
            gp = int(g[len(Gyrewhere):g.find(".da")])
            GP.extend([gp])
            os.popen("cp " + g + " " + newfolder[:-6]+"/FREQS/") #Copy frequencies

        # Find and save profiles
        if Prun:
            Prof = glob(stem+"prof*.data")            
            for p in Prof:
                pp = int(p[len(stem)+len("profile"):p.find(".da")])
                if pp in GP:
                    os.popen("cp "+ p +" " + newfolder+"/")

        os.popen("cp "+ stem +"/profiles.index " + newfolder+"/")

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
        with open(newfolder+"history.data","w") as f2:
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
        print(newfolder+"history.data CREATED")

        # To evaluate FeH, we could look in the profile files
        # The initial conditions are, however, also in the inlist-file
        inlist = glob(hfil[:-17]+"/inlist_controls*")
        with open(inlist[0],"r") as f1:
            lines = f1.readlines()
            for line in lines:
                words = line.split()
                if "initial_mass" in line:
                    m = words[2]
                    m = float(m.replace("d","e"))
                elif "initial_z" in line:
                    z = words[2]
                    z = float(z.replace("d","e"))
                elif "initial_y" in line:
                    y = words[2]
                    y = float(y.replace("d","e"))

        f1.close()
        x = 1. - z - y
        M.extend([m])
        FeH.extend([np.log10(z/x)-np.log10(0.0181)])
        WHO.extend([newfolder[:-5]])
        print(M,FeH)

        # Write summary so far
        with open(whereto+"overview.txt","w") as f:
            for i, m in enumerate(M):
                f.write(str(m)+ " " + str(FeH[i]) + " " + WHO[i] + "\n")




where = "/rds/projects/2017/miglioa-stellar-grids/walter/base_grid/"
hgrid = glob(where + "*/LOGS/history.data")
whereto = "./OUTREACH_GRID/"
writenew(where,hgrid,whereto,Prun=False)
