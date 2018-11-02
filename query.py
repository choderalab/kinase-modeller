import sys
from kinaseModel import *
import subprocess
import ast
import urllib.request

'''
When given a PDB code plus a chain index, this script collect information including (1) the kinase ID, (2) the standard name, (3) the KLIFS-defined structure ID, (4) the KLIFS-defined sequence of 85 binding pocket residues (http://klifs.vu-compmedchem.nl/index.php), (5) the indices of the 85 residues in the corresponding structure, and (6) residue indices involved in collective variables for kinase conformational changes and ligand interactions.
'''
#Get the user input (a PDB code and a chain index) 
inputInfo = input('Please input kinase info (PDB code, chain index) e.g. (3pp0, A): ').replace(' ','').split(',')
pdbChain = tuple(inputInfo)

'''
The following function gets information of the query kinase from the KLIFS database and gives values of kinaseID, name and pocketSeq (numbering). 
'''
def getInfo(pdbChain):
    cmd="curl -X GET --header 'Accept: application/json' 'http://klifs.vu-compmedchem.nl/api/structures_pdb_list?pdb-codes="+str(pdbChain[0])+"'" # form the query command
    clean = subprocess.check_output(cmd, shell=True, universal_newlines=True).replace('true','True').replace('false','False') # clean up the info from KLIFS
    for structure in ast.literal_eval(clean): # each pdb code corresponds to multiple structures
        if structure['chain'] == str(pdbChain[1]): # find the specific chain
            kinaseID = int(structure['kinase_ID'])
            name = str(structure['kinase'])
            pocketSeq = str(structure['pocket'])
            structID = int(structure['structure_ID'])

    # Get the numbering of the 85 pocket residues
    cmd = "http://klifs.vu-compmedchem.nl/details.php?structure_id="+str(structID)
    info = urllib.request.urlopen(cmd)
    for line_number, line in enumerate(info):
        line = line.decode()
        if 'pocketResidues=[' in line:
            numbering = ast.literal_eval((line[line.find('=')+1:line.find(';')]))
    # check if there is gaps/missing residues among the pocket residues. If so, enforce their indices as 0 and avoid using them to compute collective variables..
    for i in range(len(numbering)):
        if numbering[i] == -1:
            print ("Warning: There is a gap/missing residue at position: "+str(i+1)+". Its index will be enforced as 0 and it will not be used to compute collective variables.")
            numbering[i] = 0
    return kinaseID, name, pocketSeq, structID, numbering

'''
The following function defines indices of the residues relevant to a list of 12 collective variables relevant to kinase conformational changes. These variables include: angle between aC and aE helices, the key K-E salt bridge, DFG-Phe conformation (two distances), X-DFG-Phi, X-DFG-Psi, DFG-Asp-Phi, DFG-Asp-Psi, DFG-Phe-Phi, DFG-Phe-Psi, DFG-Phe-Chi1, and the FRET L-S distance. All features are under the current numbering of the structure provided.
'''
def defineCV(numbering):
    keyRes = []
    # angle between aC and aE helices
    keyRes.append(numbering[20]) # residue 21 (res1 in aC)
    keyRes.append(numbering[28]) # res29 (res2 in aC)
    keyRes.append(numbering[60]) # res61 (res1 in aE)
    keyRes.append(numbering[62]) # res63 (res2 in aE)

    # key salt bridge
    keyRes.append(numbering[16]) # res17 (K in beta3) 
    keyRes.append(numbering[23]) # res24 (E in aC)

    # DFG conformation and Phe conformation
    keyRes.append(numbering[27]) # res28 (ExxxX)
    keyRes.append(numbering[81]) # res82 (DFG-Phe)

    # X-DFG Phi/Psi
    keyRes.append(numbering[79]) # res80 (X-DFG)

    # DFG-Asp conformation
    keyRes.append(numbering[80]) # res81 (DFG-Asp)

    # FRET distance
    keyRes.append(numbering[84]+6 if numbering[84] else 0) # not in the list of 85 (equivalent to Aura"S284"), only infer if the reference is non-zero
        
    keyRes.append(numbering[58]+2 if numbering[58] else 0) # not in the list of 85 (equivalent to Aura"L225"), only infer if the reference is non-zero

    return keyRes

# Print out kinase information
(kinaseID, name, pocketSeq, structID, numbering) = getInfo(pdbChain)
keyRes = defineCV(numbering)
print ("---------------------Results----------------------")
print ("Kinase ID: "+str(kinaseID))
print ("Kinase name: "+str(name))
print ("Pocket residues: "+str(pocketSeq))
print ("Structure ID: "+str(structID))
print ("Numbering: "+str(numbering))
print ("Residues involved in collective variables: "+str(keyRes))

# Pupolate a kinase object
myKinase = kinase(pdbChain, kinaseID, name, structID, pocketSeq, numbering, keyRes)
print (myKinase.kinaseID)
