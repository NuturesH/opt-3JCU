
###############
#Nutures
#2017/12/18
###############

#First read pdbname to list
#Second write the type of input file
#Third write sh file  

import os
import re

class amber():
	""" build amber input file, from pdb name file"""
	def __init__(self):
		self.pdbname = []
		self.tleapname = []
		self.M_file = 'test_tleap.tleap'
		self.I_file = './pdb_name_list.txt'
		self.O_dir = './tleap_amber/'
		return		


	""" read pdb name for pdb_name_list.txt """
	def Numpdb(self):
		Pdb_name = []
		ifile = self.I_file
		for line in open(ifile, "r"):
			line=''.join(line.strip().split('.pdb'))
			Pdb_name.append(line)
		self.pdbname = Pdb_name
		return

	""" write the tleap file """
	def Tleap_file(self):
		Pdb_name = self.pdbname
		tleap_name = []
		odir = self.O_dir
		mfile = self.M_file
		num = 0
		for i in Pdb_name:
			res_dir = "_".join(re.findall(r"[A-Z]+",i))
			OFN = odir+"tleap_"+i+".tleap"
			tleap_name.append(OFN)
			loadpdb = 'aa = '+'../add_H_3JCU/'+res_dir+'/'+i+".pdb"+'\n'
			prmtop = '../amber_opt_3JCU/'+res_dir+'/'+i+'.prmtop  '
			inpcrd = '../amber_opt_3JCU/'+res_dir+'/'+i+'.inpcrd'+'\n'
			savepdb = 'savepdb aa '+prmtop+inpcrd
			print loadpdb.strip()
			fp = open(OFN,'w')
			num=num+1
			#acording pdbname to write the tleap file
			for k in open(mfile,'r'):
				k = k.strip()
				if k == "aa = loadpdb 10.pdb":
					fp.write(loadpdb)
				elif k == "savepdb aa 10.pdb":
					fp.write(savepdb)
				else:
					fp.write(k+'\n')

		self.tleapname = tleap_name
		print num
		return
		
	""" write sh file"""
	def sh_file(self):
		tleapname = self.tleapname
		fp = open("./top_inp.sh","w")
		for i in tleapname:
			input = "tleap -f "+i
			fp.write(input)
		return


	""" run sh script """
	def run_sh(self):
		for line in open("./top_inp.sh","r"):
			line = line.strip()
			run = "sh "+line
			os.system(run)
		return
run_amber = amber()
run_amber.Numpdb()
run_amber.Tleap_file()
run_amber.sh_file()
run_amber.run_sh()

















