#!/usr/bin/python2.7
###############################################################
#                         sterimolMultipleSterimol.py         #
#                                                             #
###############################################################
####  Assembled by: Ian Pendleton     #########################
####  Last modified:  Jan 13, 2018 ############################
###############################################################

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
import pybel as pb
import math
##smallchange
#### variables ####
directory=os.path.dirname(os.path.abspath(__file__))


#total bonded thresh
tb = 6
Metal=27  #atomic number of metal center in question for calculating tau
hydrogens=0 #consider hydrogens bound to the metal center or not?
DistCutoff=2.8 #Sets the cutoff for considering an atom "bound" that open babel doens't see bound

### File line arguments ####
#parser=argparse.ArgumentParser(description='This script is intended for converting xyz molfiles into useable molfiles for gamess input. The basis set and header can be specified in the molfile "header"')

#parser.add_argument('molfile_name', help='required input; /your/molfile/location/and/name.xyz; no default')
#parser.add_argument('Length_name')
#parser.add_argument('Angle_name')

##demoline## parser.add_argument('-ECP', type=int, default=0, help='sets whether the pro')

#args = parser.parse_args()
#Sets the inputfiles to the variable molfile for each run#
#molfile = args.molfile_name
#lengthfile = args.Length_name

########File Handling - Program operates on all available XYZ files in directory#########

bondedlist={}
##output bonded atoms ###
def OBread(mol1):
 y=[]
 global count1
 count1=0
 for atom in mol1:
  if atom.atomicnum == Metal:
   global obatom
   print obatom
   obatom = atom.OBAtom
 for atom2 in mol1:
   N = atom2.OBAtom
   if N.GetDistance(obatom) < DistCutoff:
    if atom2.atomicnum != Metal:
     if atom2.atomicnum != 1:
      y.append(N)
      print y
# return y[0].GetAngle(obatom, y[1]), y[2].GetAngle(obatom, y[3])

def printstuff(file, atom1, atom2):
      radii = bondii
      file_Params = calcSterimol(file, radii, atom1, atom2, True)
      lval = file_Params.lval; B1 = file_Params.B1; B5 = file_Params.newB5
#         print "\n   STERIMOL: using", radii, "van der Waals parameters"
#         print "\n","   Structure".ljust(25),"L".rjust(9),"B1".rjust(9),"B5".rjust(9)
      print "   "+file.ljust(22),"%.2f".rjust(9) % lval,"L","%.2f".rjust(9) % B1,"B1","%.2f".rjust(9) % B5,"B5"

lst=os.listdir(directory)
lst.sort()
for file in lst:
#    mol1 = next(pb.readfile("xyz", molfile))
    if file.endswith(".xyz"):
     if os.stat(file).st_size == 0:
       print file, "0 0"
     else:
        print pb.readfile("xyz", file)
#        mol1 = next(pb.readfile("xyz", file))
#        y=OBread(mol1)[1]
#        a=x[0].GetAngle(obatom, y[x])
#        hold=str(test[0])
#        hold1=hold.strip("['']")
#        print file,x,y
