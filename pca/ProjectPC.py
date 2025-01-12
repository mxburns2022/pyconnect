#!/usr/bin/env python

'''
Simple script which reads three files;
1. format_file: a .pdb file which contatins .pdb specific information required
   effective plotting in VMD.
2. pc_file: a .xyz file which contains the normed PC we are interested in 
   studying.
3. projection_file: a .xyz file which contains the structure we shall project 
   the PC onto.
'''
import numpy as np
import os
import sys
#from PCAprep import MyPCAprep as PCA
from pca.PCAprint import PCAprint

__metaclass__ = type

class Keyword():
    '''
    Object which reads keywords from file self.kw_file and stores them as 
    attributes.
    '''
    def __init__(self):
        
        self.input_file = "project_inpt"
        
        self.format_file = None
        self.pc_file = None
        self.base_file = None
        
        self.pc = None
        self.ensemble_average_file = None
        self.mu_sigma_file = None
#        self.base_pc = None # This is the value of the

        self.n_atoms = None
        
        self.pdb_output = None
        
        self.n_steps = None
        self.parm_min = None
        self.parm_max = None
        
        self.FileCheck(self.input_file)
        self.InputRead()
        
        self.InfoCheck()
        self.TypeCheck()
        
    def FileCheck(self, file_name):
        '''
        Checks for the existence of the file "file_name"
        '''
        if not os.path.exists(file_name):
            sys.exit('ERROR: Could not find file "%s"'%file_name)
            
    def InputRead(self):
        '''
        
        '''
        for line in open(self.input_file,'r'):
            self.LineRead(line)
            
    def LineRead(self, line):
        '''
        Processes the line passed to it from InputRead in self.input_file
        '''
        line = line.split()
        if (len(line) == 0
            or str(line[0]) == '#' 
            or str(line[0]).lower() == 'comment'): 
                return
        elif self.__dict__.has_key(str(line[0])):
            self.__dict__[str(line[0])] = line[1]
            
    def InfoCheck(self):
        '''
        Checks if all required information is present
        '''
        required_dict = self.__dict__.copy()
        missing_list = [] # List of missing keywords

        for attr, var in required_dict.iteritems():

            if not var: missing_list.append(attr)
        
        if missing_list:
            print('WARNING: Following Keywords not found:\n', missing_list)
            sys.exit()
            
    def TypeCheck(self):
        '''
        Ensure Attributes are correct type
        '''
        self.n_atoms = int(self.n_atoms)
        self.format_file = str(self.format_file)
        self.pc_file = str(self.pc_file)
        self.pc = int(self.pc)
        self.ensemble_average_file = str(self.ensemble_average_file)
        self.mu_sigma_file = str(self.mu_sigma_file)
        self.base_file = str(self.base_file)
        self.pdb_output = str(self.pdb_output)
        self.n_steps = int(self.n_steps)
        self.parm_min = float(self.parm_min)
        self.parm_max = float(self.parm_max)

class PC_project(PCAprint):
    '''
        
    '''
    def __init__(self,kw):
        self.kw = kw
        
        self.pdb_template = [] # Initialise empty list
        self.pdb = []
        
        # Check if three input files can be found
        self.kw.FileCheck(self.kw.format_file)
        self.kw.FileCheck(self.kw.pc_file)
        self.kw.FileCheck(self.kw.base_file)
        
        # Read PCs from numpy binary
        self.PCs = np.load(self.kw.pc_file)
        self.ensemble_average = np.load(self.kw.ensemble_average_file)
        self.config_mu = np.load(self.kw.mu_sigma_file)['arr_0']
        self.config_sigma = np.load(self.kw.mu_sigma_file)['arr_1']
        
        # Initialise xyz vectors
        self.pc_xyz = self.Initxyz()
        self.base_xyz = self.Initxyz()
        self.projection_xyz = self.Initxyz()
        
        # Initialise pdb output file name base
        self.pdb_output_file = ""
        
        # Read input files into relevant attributes
        self.PCFileRead()
        self.BaseFileRead()
        self.pdbFileRead()

        
        
    def Initxyz(self):
        '''
        
        '''
        xyz = np.zeros([self.kw.n_atoms, 3])
        
        return xyz
        
    def pdbFileRead(self):
        '''
        Reads .pdb file and saves it as a nested list.
        '''
        for line in open(self.kw.format_file):

            line = self.modsplit(line)#list(str(line).split())
            
            self.pdbLineRead(line)
#            print(line, len(line))

    def pdbLineRead(self, line):
        '''
        Analysyses line to check content, and saves in appropriate format to
        self.pdb_template
        '''
#        if line[0] == "ATOM": 
        if line[0].find("ATOM") >= 0:
            line[10:15] = [],[],[]
#            for i in range(5,8): line[i] = []
            self.pdb_template.append(line)

    def modsplit(self,line):
        '''
        A modified version of split() which tokenises line into array but which
        contains the trailing whitespace of each word
        '''
        split_list = []
        split_list.append(line[0])
        for i in line[1:]:
            if i == '\n': break

            if i == ' ':
                if split_list[-1][-1] != ' ': split_list.append(i)
                else: split_list[-1] = split_list[-1] + i
            else: 
                if split_list[-1][-1] == ' ': split_list.append(i)
                else: split_list[-1] = split_list[-1] + i
#        print(split_list)
        return split_list
    
    def BaseFileRead(self):
        '''
        
        '''
        i = 0
        for line in open(self.kw.base_file):
            line = line.split()
            if len(line)==0 or i == self.kw.n_atoms: break

            try: self.base_xyz[i,:] = self.xyzLineRead(line)
            except IndexError:
                
                sys.exit("i = %d"%i)
            i += 1
            
    def PCFileRead(self):
        '''
        
        '''
        self.pc_xyz = self.PCs[self.kw.pc - 1]
        self.pc_xyz = self.pc_xyz.reshape([self.kw.n_atoms,
                                           3])
#        self.config_space = np.swapaxes(self.config_space,1,2)
#        self.shape = np.shape(self.config_space)
#        print(self.pc_xyz)
        
    def xyzLineRead(self,line):
        '''
        
        '''

        self.xyzLineCheck(line)
        xyz = np.array([])
        for l in line:

            try: xyz = np.append(xyz, float(l))
            except IndexError:

                sys.exit('!!!%s'%type(l))
        return xyz
    
    def xyzLineCheck(self,line):
        '''
        Checks line is in expected format (currently only checks that line 
        contains only 3 numbers).
        '''
        if len(line) != 3:
            sys.exit('Was expecting 3 numbers per line, got %d'
                     %len(line))
        
        
    def Project(self,t):
        '''
        Projects self.pc_xyz onto self.base_xyz by parameter t and saves in 
        self.projection_xyz
        '''
        mu = self.config_mu.reshape(1,self.kw.n_atoms,3)#.swapaxes(1,2)
        sigma = self.config_sigma.reshape(1,self.kw.n_atoms,3)#.swapaxes(1,2)
        self.projection_xyz = self.base_xyz + t*(self.pc_xyz*sigma[0] + mu[0])
        
    def ZeroProject(self):
        '''
        Updates base such that self.base_xyz has a self.pc_xyz component = 0.
        '''
        mu = self.config_mu.reshape(1,self.kw.n_atoms,3)#.swapaxes(1,2)
        sigma = self.config_sigma.reshape(1,self.kw.n_atoms,3)#.swapaxes(1,2)
        print('single point', self.single_point[self.kw.pc -1])
        self.base_xyz = self.base_xyz - self.single_point[self.kw.pc - 1]*(self.pc_xyz*sigma[0] + mu[0])
        
    def pdbMake(self):
        '''
        Generates a nested list based on self.pdb_template, and then fills in 
        co-ordinate info from self.projection_xyz
        '''
        self.pdb = self.pdb_template[:][:]
        i = 0
        for x, y, z in self.projection_xyz:

            self.pdb[i][10:14] = [x,y,z]
            i += 1
    
    def pdbWrite(self):
        '''
        Writes self.pdb to file "self.pdb_output" 
        '''

        f = open(self.pdb_output_file, 'w')
        for l in self.pdb:
#            print(l[10:14])
            for c in l[0:9]:
                f.write(str(c))
            x, y, z = l[10:13]
            f.write('     {: 1.3f}  {: 1.3f}  {: 1.3f}'.format(x,y,z))
            for c in l[14:]:
                f.write(str(c))
            f.write('\n')
        f.close()
    
    def pdbGenerateName(self, base, index):
        '''
        Generates a string self.pdb_file_name which can be used as a filename
        of the form "base" + "_" + "index"
        '''
        self.pdb_output_file = str(base) + "_" + str(index) + ".pdb"
        
        
    def SetProjectionCoord(self):
        '''
        Performs a parameter sweep of self.kw.n_steps between self.kw.parm_min
        and self.kw.parm_max
        '''
        step_size = (self.kw.parm_max - self.kw.parm_min)/self.kw.n_steps
        
        for i in range(self.kw.n_steps + 1):
            t = self.kw.parm_min
            t += i*step_size
            print(t, i, step_size)
            self.Project(t)
            self.pdbGenerateName(self.kw.pdb_output, i)
            self.pdbMake()
            self.pdbWrite()
        
    def PCSinglePoint(self, structure):
        '''
        Calculates the value of self.pc_xyz at structure
        '''
        # First rotates 'structure' be oriented as closely as possible to the 
        # ensemble mean structure, self.ensemble_average
       
        structure = np.array(structure)
        structure = structure.reshape(1,self.kw.n_atoms,3)
        structure = structure.swapaxes(1,2)

        structure[0] = self.CalcCentreOfMass(structure[0])
        structure[0] = self.CalcRotate(structure[0])
        structure[0] = structure[0] - self.ensemble_average

        structure = structure.swapaxes(1,2)
        structure = structure.flatten()
        structure = (structure - self.config_mu)/self.config_sigma

        self.single_point = np.dot(self.PCs,structure.T) 


if __name__ == '__main__':
    kw = Keyword()
    pc = PC_project(kw)

#    b = np.load('PC_coords/PCs.npy')
#    a = b[0]
#    a = np.swapaxes(a, 0, 1)

    pc.PCSinglePoint(pc.base_xyz)
    pc.ZeroProject()
    
    pc.SetProjectionCoord()

