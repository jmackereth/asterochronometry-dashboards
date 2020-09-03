#!/bin/sh
#SBATCH --account miglioa-stellar-grids
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time 1:00:00
#SBATCH --qos bbdefault
#SBATCH --out slurm-%j.out
#SBATCH --error slurm-%j.err
#SBATCH --mail-type FAIL,END

set -e
module purge; module load bluebear

cd /rds/projects/2017/miglioa-stellar-grids/walter/asterochronometry-dashboards/kippenhahn_diagrams

python make_kipp.py

