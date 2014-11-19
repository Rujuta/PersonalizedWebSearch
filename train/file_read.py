#! /usr/bin/env python
from collections import defaultdict
from collections import OrderedDict

search_logs=[]
query_counts=defaultdict(int)
user_objects=defaultdict(list)
query_terms=defaultdict(int)


""" This function reads the train file and 
    puts everything into a list. 
    This list is what is going to be referred to by the rest of the 
    training program
"""
def read_file(file_name):
    global search_logs
    with open(file_name) as f:
       search_logs = f.readlines()


#def get_dict_indexed_user(search_logs):

"""Returns a dictionary of type {<Query_ID>, count} that indicates how many times 
a particular query has been queried"""
def get_dict_query_counts():
    global search_logs
    global query_counts
    for log in search_logs:
            items=log.split()
            if items[2] == 'Q':
                count=query_counts[items[4]]
                count+=1
                query_counts[items[4]]=count


"""create a dictionary per user. The key is User_ID and the value is the list of user sessions"""
def get_user_objects():
    global search_logs
    global user_objects
    for log in search_logs:
        items=log.split()
        if items[1] == 'M':
            user_id=items[3]
            continue;
        user_objects[user_id].append(log)
    return user_objects

"""Create a dictionary keyed by queryID and the number of terms in the query"""
def get_terms_in_query():
    global search_logs
    global query_terms
    for log in search_logs:
            items=log.split()
            if items[2] == 'Q':
                count_query_terms=len(items[5].split(","))
                query_terms[items[4]]=count_query_terms


""" Creates a file per user to be fed into rank net
The file's format is Score, QueryID, Features"""
def create_input_file(userid, sessions_list):
    f=open("user_train_files/"+userid,'w')
    query_doc=OrderedDict() #a dictionary keyed by query-doc combination
    for line in sessions_list:
        items = line.split()
        if items[2] == 'Q':
            rank=1
            for doc in items[6:]:
                key=(items[4],doc)
                if key not in query_doc.keys():
                    query_doc[key]=OrderedDict()
                query_doc[key]['rank']=rank
                rank+=1
     
    # Fill in the number of times an item has been queried for
    for k,v in query_doc.items():
        count_terms= query_terms[k[0]]
        query_doc[k]['terms']=count_terms
        count_queried_for=query_counts[k[0]]
        query_doc[k]['frequency']=count_queried_for

    for k,v in query_doc.items():
        f.write(str(k[0])+"\t"+str(k[1])+ "\trank:" + str(v['rank'])+ "\tterms:"+ str(v['terms'])+"\tfrequency:"+str(v['frequency'])+"\n")
          
       # for item,rank in query_doc[k].items():
        #    f.write(item+":"+str(rank))
    f.close()
    
#Globals

read_file("../data/xaa")
get_dict_query_counts()
get_user_objects()
get_terms_in_query()
for user,sessions in user_objects.items():
    create_input_file(user,sessions)
