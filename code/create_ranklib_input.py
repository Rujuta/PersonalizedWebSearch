#! /usr/bin/env python

from collections import defaultdict
from collections import OrderedDict
import json

"""The file name will be a user specific file name from which we get the features
that need to specified for a particular user"""
def get_features(filename):
    with open(filename) as f:
        user_features=f.readlines()
    return user_features

def create_file(user_features,filename2):
    with open(filename2,"w") as f:
        cnt=1
        feature_file=OrderedDict()
        prev_key=None

        for line in user_features:
            keyset=[]
            no=1
            fields=line.split("\t")
        #Separate query ID first
        #Take fields[0]
            key=fields[0].split(",")[1].replace("'","").replace(" ","")
            feature_file["qid"]=key
            for field in fields[1:len(fields)-1]:
                k=field.replace("'","")
                k1,v1=k.split(":")
                feature_file[k1]=v1
                if(k1!='score'):
                    keyset.append(k1) 
            f.write(feature_file['score']+" qid:"+key+" ")
            for k in keyset:
                f.write(str(no)+":"+str(feature_file[k])+" ")
                no+=1
            if(cnt!=len(user_features)):
                f.write("\n")
            cnt+=1
            
   

user_features=get_features('../data/user_features/347448')
create_file(user_features,'tmp')
