#! /usr/bin/env/python
from collections import defaultdict
from collections import OrderedDict
import json

""" Creates a file per user to be fed into rank net
The file's format is Score, QueryID, Features"""
def create_input_file(user_id, query_doc, user_details):
    f=open("../data/user_features/"+user_id,'w')
    for k,v in user_details.items():
        f.write(str(k) + ":" + str(v)+ "\t")
    f.write("\n")
    for k,v in query_doc.items():
    #json.dump(query_doc,open('../data/user_features/'+userid,"w"))
    #exit(0)
        if k[0]==user_id:
            f.write(str(k))
            f.write("\t")
            for inner_key in v.keys():
                f.write(str(inner_key) + ":" + str(v[inner_key])+ "\t")
            f.write("\n")
    f.close()


def create_input_file_history( query_doc):
    f=open("../data/user_features/history",'w')
    for k,v in query_doc.items():
    #json.dump(query_doc,open('../data/user_features/'+userid,"w"))
    #exit(0)
        f.write(str(k))
        f.write("\t")
        for inner_key in v.keys():
            f.write(str(inner_key) + ":" + str(v[inner_key])+ "\t")
        f.write("\n")
    f.close()
