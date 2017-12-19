#!python
import os
import sys
import re
#read pdb file to output gaussian files


#first read pdblist get pdb file name
#second read pdb model file
#third read gjf model file
#forth output

# ===============
# huangxianhui
# date: 2017-12-09
# ===============

class mkgau():
    """build gaussian input file, from pdb file"""
    def __init__(self):
        self.nmol = 0
        self.template={'head':[], 'title':'', 'sc':''}
        self.charge_res = ['HIS', 'LYS', 'ARG']
        self.tfile = 'tmp.gjf'
        self.pfile = './pdb_name_list.txt'
        #pdb name
        self.pnum = []
        return

    def rd_template(self):
        """ read template file """
        tfile= self.tfile
        fp = open(tfile, 'r')
        # header
        head = []
        title = ''
        sc = ''
        line = 'STARTER'
        while line.strip() != "":
            line = fp.readline().strip()
            if line== "":
                break
            if line.lower().find('%mem') == 0:
                head.append(line)
            elif line.lower().find('%nproc') == 0:
                head.append(line)
            elif line.lower().find('#') == 0:
                head.append(line)
        line = fp.readline().strip()
        title = line
        line= fp.readline().strip()
        line = fp.readline().strip()
        sc= line

        self.template['head']= head
        self.template['title'] = title
        self.template['sc'] = sc

        fp.close()
        return
            
    def rd_pdb_list(self):
        rec = []
        filename = self.pfile
	
	for line in open(filename, "r"):
		line ="".join(line.strip().split(".pdb"))
		resname = "".join(re.findall(r"[A-Z]+",line))
	#	print resname
		rec.append(line)
        print len(rec)
        self.pnum= rec
        return

    def rd_pdb_file(self):
        pnum = self.pnum
        body = []
        tail = []
        for i in range(len(pnum)):
            ibody = [] 
	    resname = "_".join(re.findall(r"[A-Z]+",pnum[i]))
	    filename = "./add_H_3JCU/"+resname+"/"+pnum[i]+".pdb"
            print filename
	    for line in open(filename,"r"):
		line = line.strip()
		if line == "END":	break
		rec = line.split()	
                if len(rec) >1:
                    atom = rec[2][0]
		    if rec[2]=="MG":
			atom = "MG"
			coord = line[30:56]
			newline = atom + "  " + coord
			ibody.append(newline)
                    else:
                        coord = line[30:56]
                        newline = atom + "   " +coord
                        ibody.append(newline)
            
            itail = []
            for j in range(len(ibody)):
                if ibody[j][0] != "H":
                    rec = "X" + " "+ str(j+1)+" "+ "F"
                    itail.append(rec)                
            #print ibody
            #print tail
            tail.append(itail) 
            #print tail
            body.append(ibody)
        self.template['tail']=tail
        self.body = body
        return

    def wrt_gau_file(self):
        pnum = self.pnum
        head = self.template['head']
        title = self.template['title']
        charge_res= self.charge_res
#        if resname in charge_res:
#            sc = "1 1"
#        else:
#            sc = self.template['sc']
        tail = self.template['tail']
        body = self.body
	fd = open("opt_3JCU.sh","w")
        for i in range(len(pnum)):
	    
	    resname = re.findall(r"[A-Z]+",pnum[i])
	    path_res = "_".join(resname)
	    z_res = "".join(charge_res)
	    sc = self.template['sc']  
	    if resname[0] in z_res or resname[1] in z_res:
		sc = "1 1"
	    if resname[0] in z_res and resname[1] in z_res:
		sc = "2 1"
            filename = "../opt_3JCU/"+path_res+"/"+pnum[i]+".gjf"
	    chk_name = "%chk=../opt_3JCU/"+path_res+"/"+pnum[i]+".chk"
	    log_name = "../opt_3JCU/"+path_res+"/"+pnum[i]+".log"
	    sh_file = "g16 "+filename+" > "+log_name+"\n"
	    fd.write(sh_file)
            print filename
            fp = open(filename, 'w')
	    
            print >>fp, chk_name
            for h in head:
                print >>fp, h
            print >>fp, ""
            print >>fp, title
            print >>fp, ""
            print >>fp, sc
            for x in body[i]:
                print >>fp, x
            print >>fp, ""
            for x in tail[i]:
                print >>fp, x
            print >>fp, "\n"
        fp.close()           
        return


#resname = sys.argv[1].strip()
gau = mkgau()
gau.rd_template()
gau.rd_pdb_list()
gau.rd_pdb_file()
gau.wrt_gau_file()










