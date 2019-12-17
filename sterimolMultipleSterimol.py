#!/usr/bin/python2.7
###############################################################
####  Assembled by: Ian M. Pendleton     ######################
#### www.pendletonian.com                ######################
###############################################################

# Updated December 17, 2019

### This program is designed to take all of the bonded atoms 
### to the metal center and find the sterimol parameters of those
### bonded atoms.  This program assumes that the vector of interest
### is from the metal center toward the phosphine (or whatever).  
############################
### Be sure to adjust the metal center label and the distance cutoff in the variables
### section below.  Default is to ignore hydrides (no sterimol information)
##module list###
import sys
import os
import argparse
import numpy as np

from openbabel import pybel
from sterimoltools import *
from tqdm import tqdm
#### variables ####
directory=os.path.dirname(os.path.abspath(__file__))

### User variables ### 
METAL = 27  #atomic number of metal center in question for calculating tau
HYDRO_BOOL = 0 #consider hydrogens bound to the metal center or not?
DISTANCE_THRESHHOLD = 2.8 #Sets the cutoff for considering an atom "bound" that open babel doens't see bound

########File Handling - Program operates on all available XYZ files in directory#########
obatom = None
bondedlist={}
##output bonded atoms ###
def bite_angles(mol1, d_cutoff):
 ''' calculates bite angles for 1-M-2 and 3-M-4 ligands where 1-4 are determined based on distcutoff

 rigid and ungeneralized, careful on use!

 :params mol1: pybel molecule object (typically generated from readfile function)
 :params d_cutoff: value of distance cutoff in angstroms

 :returns: tuple (1-M-2 angle, 3-M-4 angle)

 '''
 y=[]
 for atom in mol1:
  if atom.atomicnum == METAL:
   global obatom
   obatom = atom.OBAtom
 for atom2 in mol1:
   N = atom2.OBAtom
   if N.GetDistance(obatom) < d_cutoff:
    if atom2.atomicnum != METAL:
     if atom2.atomicnum != 1:
      y.append(N)
  #TODO: generalize to find relevant(tm) angles -- hard generalization...
 return (y[0].GetAngle(obatom, y[1]), y[2].GetAngle(obatom, y[3]))

def atomsbonded(mol1, d_cutoff):
 ''' finds atoms proximal to the metal center returns as a list
 :params mol1: pybel molecule object (typically generated from readfile function)
 :params d_cutoff: value of distance cutoff in angstroms
  
 :returns: list of atom numbers (from specified input file) [M, atom1, atom2,... n]
 '''
 y=[]
 for atom in mol1:
  if atom.atomicnum == METAL:
   global obatom
   obatom = atom.OBAtom
   y.append(atom.idx)
 for atom2 in mol1:
   N = atom2.OBAtom
   if N.GetDistance(obatom) < d_cutoff:
    if atom2.atomicnum != METAL:
     if atom2.atomicnum != 1:
      y.append(atom2.idx)
 return y

def run_sterimol(file, atom1, atom2):
      radii = 'bondi'
      file_Params = calcSterimol(file, radii, atom1, atom2, True)
      lval = file_Params.lval; B1 = file_Params.B1; B5 = file_Params.newB5
      with open('sterimol_values.csv', 'a') as f:
       print >>f, file,', L:,',"%.2f" % lval, ", B1:,", "%.2f" % B1,", B5:,","%.2f" % B5, "\n"
#       print >>f, file.ljust(22),"%.2f".rjust(9) % lval,", L","%.2f".rjust(9) % B1,"B1","%.2f".rjust(9) % B5,"B5"

def main_pipeline(mol_obj, d_cutoff, file):
  # Generate the bite angles (angle of ligands on specified metal)
  #TODO: generalize for all metal bonded angles
  angle_1, angle_2 = bite_angles(mol_obj, d_cutoff) # hard coded for specific 2 angle return (add more above!)
  with open('biteangle_values.csv', 'a') as myfile:
    print >>myfile, file, ", 1-M-2:,", angle_1, ", 3-M-4:,", angle_2, "\n"

  bonded_atom_list = atomsbonded(mol_obj, d_cutoff)
  count = 1
  while count < len(bonded_atom_list):
   run_sterimol(file, bonded_atom_list[0], bonded_atom_list[count])
   count+=1
  # generate list of pairs from original metal center
  #for atom in bonded_atom_list

if __name__ == "__main__":
 lst=os.listdir(directory)
 lst.sort()
 xyz_list = []
 for file in lst:
  if file.endswith(".xyz"):
    xyz_list.append(file)
 for file in xyz_list:
   if os.stat(file).st_size == 0:
    print file, "0 0"
   else:
    molecule_obj = next(pybel.readfile("xyz", file))
    main_pipeline(molecule_obj, DISTANCE_THRESHHOLD, file)
print("Operation completed successfully, please check output files")