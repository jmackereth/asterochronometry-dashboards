import os
import numpy as np
import matplotlib.pyplot as plt

from AsteroMergers.processing import load_data as ld
from AsteroMergers.processing import plotting as pl
from AsteroMergers.utils import functions as uf


hist_nums = os.listdir('../OUTREACH_GRID/WALTER')
# hist_nums = ['0003', '0004', '0005', '0007', '0008', '0009', '0017', '0018',
#              '0019', '0031', '0032', '0033', '0041', '0042', '0043', '0044',
#              '0045', '0046', '0047', '0048', '0051', '0052', '0055', '0056',
#              '0057', '0058', '0066', '0071', '0080', '0081', '0082', '0085',
#              '0086', '0090', '0091', '0092', '0094', '0095', '0096', '0097',
#              '0100', '0101', '0104', '0105', '0110', '0113', '0114', '0115',
#              '0116', '0119', '0123', '0124', '0125', '0127', '0128', '0129',
#              '0138', '0139', '0150', '0151', '0152', '0153', '0154', '0161',
#              '0162', '0163', '0164', '0166', '0167', '0168', '0172']

grid = '/rds/projects/2017/miglio-stellar-grids/walter/base_grid'
all_hist = [ld.MesaData(f'{grid}/{hist_num}/LOGS/history.data') for hist_num in hist_nums]


for hist in all_hist:
    hist_num = hist.path.split(os.sep)[-3]
    figname = f'evo_kipp_{hist_num}.png'
    f, ax = plt.subplots()
    ax, args, out = pl.make_kipp(hist, ax=ax, xaxis='star_age')

    mask = uf.get_rc_mask(hist)
    rc_ages = hist.get('star_age')[mask] /1e6
    ax.set_xlim(min(rc_ages), max(rc_ages))

    f.savefig(f'kippenhahn_diagrams/{figname}')
    plt.close(f)
