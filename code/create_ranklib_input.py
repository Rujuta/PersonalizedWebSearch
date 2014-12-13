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

def create_file(user_features,feature_set, filename2):
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
                if(k=='aggr' and len(feature_set['aggr'])>0):
                    indices=feature_set['aggr']
                    interim=feature_file[k].replace("], ","--")
                    interim1=interim.replace("[","")
                    interim1=interim1.replace("]","")
                    vectors=interim1.split("--")
                    for on in indices:
                        for p in vectors[on].split(","):
                           p=p.replace(" ","")
                           f.write(str(no)+":"+str(p)+" ")
                           no+=1
                else:
                  feature_file[k].replace(" ","")
                  f.write(str(no)+":"+str(feature_file[k])+" ")
                no+=1
            if(cnt!=len(user_features)):
                f.write("\n")
            cnt+=1
            
   
def get_features_needed(file_name):
    features_on=defaultdict(int)
    with open(file_name) as f:
        lines=f.readlines()
        for line in lines:
            line=line.split()
            key=line[0].replace(":","")
            val=line[1]
            set_on=line[1]
            if(key!='aggr'):
                if(set_on=='1'):
                    features_on[key]=set_on
            elif(key == 'aggr'):
                    indices_old=val.split(",")
                    indices = [int(i) for i, x in enumerate(indices_old) if x == "1"]
                    features_on[key]=indices
        return features_on

USER_FILES="../data/user_features/"
RANKLIB_INPUT='../data/ranklib/'

feature_set=get_features_needed('../data/feature_list/list')
dir_entries_users=os.listdir(USER_FILES)
dir_entries=sorted(dir_entries)
for dir_entry in dir_entries:
    dir_entry_path=os.path.join(USER_FILES,dir_entry)
    dir_entry_path_input=os.path.join(RANKLIB_INPUT,dir_entry)
    if os.path.isfile(dir_entry_path):
        user_vector=get_features(dir_entry_path)
        create_file(user_vector,feature_set,dir_entry_path_input)
    

