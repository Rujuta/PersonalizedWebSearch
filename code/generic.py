#! /usr/bin/env python
from collections import defaultdict
from collections import OrderedDict

"""Returns the non-personalized rank for some query-doc combination for a particular user"""
def get_non_personalized_rank(sessions_list):
    query_doc=OrderedDict() #a dictionary keyed by query-doc combination
    for session_info in sessions_list:                  ##session of that user
        pos=1
        for line in session_info:
            items = line.split()
            if items[2] == 'Q':
                rank=1
                for doc in items[6:]:
                    key=(items[0], items[4],doc)          ##items[4]: queryID
                    if key not in query_doc.keys():
                        query_doc[key]=OrderedDict()
                    query_doc[key]['rank']=rank         ##nonPersonalizedRank
                    rank+=1
                    query_doc[key]['pos'] = pos
                pos+=1

    return query_doc

def get_relevance_score(sessions_list, query_doc):
    url_list=[]
    query_id=-1
    for session_info in sessions_list:               ##session of that user
        flag = 0
        counter=-1
        for line in session_info:
            items = line.split()
            counter+=1
            if items[2] == 'Q':
                if(flag!=0):
                    i=max_last_clicked+1
                    while(i<len(url_list)):
                        temp_key = (items[0], query_id,  url_list[i])
                        query_doc[temp_key]['score'] = -2;  #-2: missed
                        i+=1
                query_id = items[4]
                #init_time =  float(items[1])
                last_clicked = -1
                max_last_clicked = -1
                url_list=items[6:]
                url_only_list=[]
                for each in items[6:]:
                    url_only_list.append(each.split(",")[0])
            if items[2] == 'C':
                flag=1
                print "URL LIST:" , url_list
                print "items:", items[4]
                url_rank = url_only_list.index(items[4])
                key=(items[0], query_id, url_list[url_rank])
                i= last_clicked + 1
                last_clicked = url_rank
                if(last_clicked>max_last_clicked):
                    max_last_clicked=last_clicked
                while(i< url_rank ):
                    temp_key = (items[0], query_id,  url_list[i])
                    query_doc[temp_key]['score'] = -1;  #-1: skipped
                    i+=1
                if counter+1 == len(session_info):
                    query_doc[key]['score'] = 2
                else:
                    next_time = session_info[counter+1].split()[1] 
                    dwell_time = float(next_time) - float(items[1])
                    if(dwell_time<50):
                        query_doc[key]['score'] = 0;
                    elif(dwell_time>=50 and dwell_time<300):
                        query_doc[key]['score'] = 1;
                    else:
                      query_doc[key]['score'] = 2;
                ##---->can optimize more- need to do only once
        #assign rest as Missed
        i=max_last_clicked+1
        while(i<len(url_list)):
            temp_key = (items[0], query_id,  url_list[i])
            query_doc[temp_key]['score'] = -2;  #-2: missed
            i+=1
    return query_doc
