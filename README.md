Sterimol.py
=====

Python program for the calculation of [Sterimol](http://www.ccl.net/cca/software/SOURCES/FORTRAN/STERIMOL/) parameters: L, B1 and B5 for half-sandwich complexes and organic molecules. If used on half-sandwich complexes, it also generates [Tolman cone angles](https://en.wikipedia.org/wiki/Ligand_cone_angle) and metal to ring-centroid (unweighted) distances. The results have been validated against the original Fortran77 code compiled with gfortran on OSX v10.11.3 27/03/2016.

Developed by Dr Kelvin Jackson (Oxford) and [Prof Robert Paton](http://paton.chem.ox.ac.uk) (Oxford).



####Installation
1. Download the scripts from https://github.com/bobbypaton/Sterimol
2. Add the directory of the scripts to the PATH environmental variable (optional).  
3.	Run the script with Gaussian input or output files.

####Correct Usage

#####For half-sandwich complexes

```python
sterimol.py file(s)
```
* This program will read Gaussian input or output files or half-sandwich complexes.


#####For organic molecules

```python
sterimol.py (-a1 atom A) (-a2 atom B) (-radii radius-model) file(s)
```
* `-a1` and `-a2` specify atoms A and B atoms for the calculation - these fields are mandatory as they specify the axis along which Sterimol parameters are calculated.
* The `-radii` option specifies the radial model used; it may be set to `-radii bondi` or `-radii cpk` for either van der Waals radii from [Bondi](http://pubs.acs.org/doi/abs/10.1021/j100785a001) or [CPK](https://en.wikipedia.org/wiki/Space-filling_model). If left blank, the default setting uses the original CPK radii.


####Example 1:
Calculating Tolman cone angles, metal to ring-centroid distances, and Sterimol parameters for a half-sandwich complex from a Gaussian output file.

```python
python sterimol.py examples/RhCpMe5Cl2PMe3.log

Sandwich Analysis
STERIMOL: using original CPK Van der Waals parameters

Structure                 Tolman_CA   MC_dist         L        B1        B5
RhCpMe5Cl2PMe3.log           173.97     1.833     4.016     3.902     4.304


```

The output shows the tolman cone angle (in degrees) and metal to centroid distance, L, B1 and B5 (all in Angstrom). Cone angles and Sterimol parameters are calculated using the original CPK atomic radii. 

####Example 2:
Calculating Sterimol parameters for an organic functional group (e.g. *tert*-butyl) from a Gaussian-formatted input file.

```python
python sterimol.py -a1 2 -a2 1 examples/tBu.com

   STERIMOL: using original CPK Van der Waals parameters
   Atoms 1 and 2 define the L-axis and direction [ 1.1  0.   0. ]

   Atom       Xco/A     Yco/A     Zco/A    VdW/pm
   ##############################################
   H          0.000     0.000     0.000     100.0
   C         -1.100     0.000     0.000     150.0
   C         -1.610     1.030     1.030     150.0
   H         -2.710     1.030     1.030     100.0
   H         -1.250     0.760     2.030     100.0
   H         -1.250     2.030     0.760     100.0
   C         -1.610     0.380    -1.400     150.0
   H         -2.710     0.380    -1.400     100.0
   H         -1.250     1.380    -1.670     100.0
   H         -1.250    -0.360    -2.140     100.0
   C         -1.610    -1.400     0.380     150.0
   H         -2.710    -1.400     0.380     100.0
   H         -1.250    -2.140    -0.360     100.0
   H         -1.250    -1.670     1.380     100.0

   Structure                      L        B1        B5
   examples/tBu.gjf            4.11      2.76      3.17

```

The output in this case returns the element types, Cartesian coordinates and atomic radii according to the CPK radial definitions. The Sterimol parameters for the structure are underneath; L, B1 and B5 are all given in Angstroms.

####Example 3:
Calculating parameters for a dimeric half-sandwich complex from a Gaussian output file.

```python
python sterimol.py examples/Rh_AsymmetricDimer.log

Sandwich Analysis
STERIMOL: using original CPK Van der Waals parameters

   Structure                 Tolman_CA   MC_dist         L        B1        B5
   Rh_AsymmetricDimer.log      191.283     1.763     6.184     3.381     5.607
   Rh_AsymmetricDimer.log      190.174     1.766     6.239     3.386     5.608

```

In this example two sets of parameters are produced - this occurs when the dimeric complex does not have a symmetry plane and thus measurements from each of the two metal centres yields different results. In the case of symmetric dimers, only a single set of parameters is generated (as they would be the same when measured from either metal centre).


####Tips and Troubleshooting
* Errors will occur if this program is used on systems containing atoms for which there are no CPK defined radii.
* When running on organic molecules, the directionality of `-a1` and `-a2` is important - make sure the `-a1` to `-a2` vector is pointing towards the functional group being measured.
* It is possible to run on any number of files at once, for example using wildcards to specify all of the Gaussian files in a directory (*.out)
* The python file doesn’t need to be in the same folder as the Gaussian files. Just set the location of sterimol.py in the `$PATH` variable.

=====
####Citing Sterimol.py
*Correlating Reactivity and Selectivity to Cyclopentadienyl Ligand Properties in Rh(III)-Catalyzed C-H Activation Reactions: an Experimental and Computational Study* Piou, T.; Romanov-Michailidis, F.; Romanova-Michaelides, T.; **Jackson, K. E.**; Semakul, N.; Taggart, T. D.; Newell, B S.; Rithner, C. D.; **Paton, R. S.**; Rovis, T. *J. Am. Chem. Soc.* **2017** *139*, 1296–1310[DOI: 10.1021/jacs.6b11670](http://dx.doi.org/10.1021/jacs.6b11670)


### IPendleton notes on edits
Starting from geometry optimization: There are a number of scripts floating around to convert gamess/gaussian/qchem outputs to energies/xyz structures.  If those don't suffice I point you to open babel for other types of file / type conversion that might be amenable to your purposes. 
Regarding sterimol: I am not entirely sure that the version on the github was the most up to date version of the code (I have updated that version to the one attached to this email).  Clearly that script didn't work as-is, so I ended up doing some minor edits on the code and have posted the updates to github.  I have also updated some of the comments in the script and made it so the code generates two output files ('sterimol_values.csv' and 'biteangle_values.csv').  Just a few notes about running it:
1) Make sure you are using python 2.7 (check out conda https://docs.anaconda.com/anaconda/user-guide/tasks/install-packages/) --> conda create -n sterimolenv python=2.7
2) If on a mac, install openbabel using homebrew (if not see the website for instructions), if on other install open babel via website instructions (make sure to include python bindings)
3) The script will target all XYZ files in a given directory (that means you will have to get the geometry optimized structure from you QM code into XYZ format -- this is required by sterimoltools.py -- though you could likely fiddle with it to make it work with gaussian too)4) Make sure to select the metal, whether or not to include hydrides (likely not, so leave as 0), and the distance cutoff (you don't want to include atoms more than a single bond away from the metal center by accident!).  This will go in the sterimolMultipleSterimol.py header. Open the file and change the "user variables section" how you see fit.

The first output file will consist of the sterimol parameters for every metal-ligand(atom) vector.  This means that if you have a bisphosphine you will get sterimol parameters for both phosphoruses bound to the metal center.  I don't expect this is a problem, but you might want to make the print statements more informative for your purposes.  I attempted to capture the salient information in ouput files, but you will have to configure it for what you want.  I updated the code to write to CSV files.  That way at least it can be parsed without much editing. 

I also pushed through the bite angle portion of the code.  For my grad school work all of the files were prepared in the same way so I always knew that the phosphines in the XYZ file were ordered sequentially (i.e. first and second phosphorus were part of the same ligand, etc).  This code will also generate a second output file which permutes and calculates the angle between every ligand of the metal center.  


License: [CC-BY](https://creativecommons.org/licenses/by/3.0/)


#� �S�t�e�r�i�m�i�o�l�
�
�
