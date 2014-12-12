#! /usr/bin/env/python
from collections import defaultdict
from collections import OrderedDict

""" Creates a file per user to be fed into rank net
The file's format is Score, QueryID, Features"""
def create_input_file(userid, query_doc):
    f=open("../data/user_features/"+userid,'w')
    for k,v in query_doc.items():
        f.write(str(k[0])+"\t"+str(k[1])+ "\trank:" + str(v['rank'])+ "\tterms:"+ str(v['terms'])+"\tfrequency:"+str(v['frequency'])+"\n") 
    f.close()
  
