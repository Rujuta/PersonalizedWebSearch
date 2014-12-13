#! /usr/bin/env python
from collections import defaultdict
from collections import OrderedDict

"""Returns the non-personalized rank for some query-doc combination for a particular user"""
def get_non_personalized_rank(sessions_list, user_id, query_doc):
    for session_info in sessions_list:                  ##session of that user
        pos=1
        for line in session_info:
            items = line.split()
            if items[2] == 'Q':
                rank=1
                for doc in items[6:]:
                    key=(user_id,items[0],items[4],doc)          ##items[4]: queryID
                    if key not in query_doc.keys():
                        query_doc[key]=OrderedDict()
                    query_doc[key]['rank']=rank         ##nonPersonalizedRank
                    rank+=1
                    query_doc[key]['pos'] = pos
                pos+=1
    return query_doc

"""This function gets the relevance score. Score of 1: Missed 2: Skipped 3: click0 4: Click1 5: click2"""
def get_relevance_score(sessions_list, user_id, query_doc):
    url_list=[]
    query_id=-1
    ke=0;
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
                        temp_key = (user_id, items[0],query_id,url_list[i])
                        query_doc[temp_key]['score'] = 1;  #-2: missed
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
                try:
                    url_rank = url_only_list.index(items[4])
                    key=(user_id,items[0], query_id, url_list[url_rank])
                    i= last_clicked + 1
                    last_clicked = url_rank
                    if(last_clicked>max_last_clicked):
                        max_last_clicked=last_clicked
                    while(i< url_rank ):
                        temp_key = (user_id, items[0],query_id,url_list[i])
                        query_doc[temp_key]['score'] = 2;  #-1: skipped
                        i+=1
                    if counter+1 == len(session_info):
                        query_doc[key]['score'] = 5
                    else:
                        next_time = session_info[counter+1].split()[1] 
                        dwell_time = float(next_time) - float(items[1])
                        if(dwell_time<50):
                            query_doc[key]['score'] = 3;
                        elif(dwell_time>=50 and dwell_time<300):
                            query_doc[key]['score'] = 4
                        else:
                            query_doc[key]['score'] = 5
                except KeyError:
                    ke+=1
                ##---->can optimize more- need to do only once
        #assign rest as Missed
        i=max_last_clicked+1
        while(i<len(url_list)):
            temp_key = (user_id,items[0],query_id,url_list[i])
            query_doc[temp_key]['score'] = 1;  #-2: missed
            i+=1
        print "key error",ke
    return query_doc

###aggregate for 000
def any_user_aggregate_000(query_doc_history, url_set):

    # user_obj_hist: 'userid':[[SessId],[SessID]..]
    # query_doc_history: 'rank' 'score'
        #for k in user_objects_history.keys(): ## goes over all users
        #for session_info in user_objects_history[k]:
        #for line in session_info:
    #sorting domains
    domain_set = set()
    for url_domain in url_set:
        domain_set.add(url_domain.split(',')[1])
    #finding count(l,P) for a P:000
    dict_agg_000 = defaultdict(float)
    for domain in domain_set:
        count_p=0
        count_1=0
        count_2=0
        count_3=0
        count_4=0
        count_5=0
        for k in query_doc_history.keys():
            d=k[3].split(",")[1]
            if domain == d:
                count_p+=1
                if query_doc_history[k]['score']==1:
                    count_1+=1
                elif query_doc_history[k]['score']==2:
                    count_2+=1
                elif query_doc_history[k]['score']==3:
                    count_3+=1
                elif query_doc_history[k]['score']==4:
                    count_4+=1
                elif query_doc_history[k]['score']==5:
                    count_5+=1
        f_count_p= float(count_p)
        if count_p==0:
            dict_agg_000[domain] = [0,0,0,0,0]
        else:
            dict_agg_000[domain] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_000

#aggregate for 001
def any_user_aggregate_001(query_doc_history, url_set):

    #finding count(l,P) for a P:001
    dict_agg_001 = defaultdict(float)
    for url_domain in url_set:
        url = url_domain.split(',')[0]
        count_p=0
        count_1=0
        count_2=0
        count_3=0
        count_4=0
        count_5=0
        for k in query_doc_history.keys():
            u=k[3].split(",")[0]
            if url == u:
                count_p+=1
                if query_doc_history[k]['score']==1:
                    count_1+=1
                elif query_doc_history[k]['score']==2:
                    count_2+=1
                elif query_doc_history[k]['score']==3:
                    count_3+=1
                elif query_doc_history[k]['score']==4:
                    count_4+=1
                elif query_doc_history[k]['score']==5:
                    count_5+=1
        f_count_p= float(count_p)
        if count_p==0:
            dict_agg_001[url] = [0,0,0,0,0]
        else:
            dict_agg_001[url] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_001

def any_user_aggregate_010(query_doc_history, query_url_set):
    #finding count(l,P) for a P:010
    #domain matches and query matches

    dict_agg_010 = defaultdict(float)
    for q in query_url_set.keys():
        domain_set = set()
        for url_domain in query_url_set[q]:
            domain_set.add(url_domain.split(',')[1])
        for domain in domain_set:
            count_p=0
            count_1=0
            count_2=0
            count_3=0
            count_4=0
            count_5=0
            for k in query_doc_history.keys():
                if q == k[2]:
                    d=k[3].split(",")[1]
                    if domain == d:
                        count_p+=1
                        if query_doc_history[k]['score']==1:
                            count_1+=1
                        elif query_doc_history[k]['score']==2:
                            count_2+=1
                        elif query_doc_history[k]['score']==3:
                            count_3+=1
                        elif query_doc_history[k]['score']==4:
                            count_4+=1
                        elif query_doc_history[k]['score']==5:
                            count_5+=1
            f_count_p= float(count_p)
            if count_p==0:
                dict_agg_010[(q, domain)] = [0,0,0,0,0]
            else:
                dict_agg_010[(q, domain)] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_010


def any_user_aggregate_011(query_doc_history, query_url_set):
    #finding count(l,P) for a P:010
    #domain matches and query matches

    dict_agg_011 = defaultdict(float)
    for q in query_url_set.keys():
        for url_domain in query_url_set[q]:
            url = url_domain.split(',')[0]
            count_p=0
            count_1=0
            count_2=0
            count_3=0
            count_4=0
            count_5=0
            for k in query_doc_history.keys():
                if q == k[2]:
                    u=k[3].split(",")[0]
                    if url == u:
                        count_p+=1
                        if query_doc_history[k]['score']==1:
                            count_1+=1
                        elif query_doc_history[k]['score']==2:
                            count_2+=1
                        elif query_doc_history[k]['score']==3:
                            count_3+=1
                        elif query_doc_history[k]['score']==4:
                            count_4+=1
                        elif query_doc_history[k]['score']==5:
                            count_5+=1
            f_count_p= float(count_p)
            if count_p==0:
                dict_agg_011[(q, url)] = [0,0,0,0,0]
            else:
                dict_agg_011[(q, url)] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_011

"""Same user, any query, same domain"""
def aggregate_100(user_id, query_doc_history, query_doc):
    dict_agg_100 = defaultdict(float)
    domain_set = set()
    for k in query_doc.keys():
        domain_set.add(k[3].split(',')[1])
    for domain in domain_set:
        count_p=0
        count_1=0
        count_2=0
        count_3=0
        count_4=0
        count_5=0
        for k in query_doc_history.keys():
            if user_id == k[0]:
                d=k[3].split(",")[1]
                if domain == d:
                    count_p+=1
                    if query_doc_history[k]['score']==1:
                        count_1+=1
                    elif query_doc_history[k]['score']==2:
                        count_2+=1
                    elif query_doc_history[k]['score']==3:
                        count_3+=1
                    elif query_doc_history[k]['score']==4:
                        count_4+=1
                    elif query_doc_history[k]['score']==5:
                        count_5+=1
        f_count_p= float(count_p)
        if count_p==0:
            dict_agg_100[(user_id, domain)] = [0,0,0,0,0]
        else:
            dict_agg_100[(user_id, domain)] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_100

"""Same user, any query, same URL"""
def aggregate_101(user_id, query_doc_history, query_doc):
    dict_agg_101 = defaultdict(float)
    for k in query_doc.keys():
        url = k[3].split(',')[0]
        count_p=0
        count_1=0
        count_2=0
        count_3=0
        count_4=0
        count_5=0
        for k in query_doc_history.keys():
            if user_id == k[0]:
                u=k[3].split(",")[0]
                if url == u:
                    count_p+=1
                    if query_doc_history[k]['score']==1:
                        count_1+=1
                    elif query_doc_history[k]['score']==2:
                        count_2+=1
                    elif query_doc_history[k]['score']==3:
                        count_3+=1
                    elif query_doc_history[k]['score']==4:
                        count_4+=1
                    elif query_doc_history[k]['score']==5:
                        count_5+=1
        f_count_p= float(count_p)
        if count_p==0:
            dict_agg_101[(user_id, url)] = [0,0,0,0,0]
        else:
            dict_agg_101[(user_id, url)] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_101

"""Same user, same query, any domain"""
def aggregate_110(user_id, query_doc_history, query_doc, query_url_set):
    dict_agg_110 = defaultdict(float)
    query_set = set()
    for k_train in query_doc.keys():
        query_set.add(k_train[2])
    for q in query_set:
        domain_set = set()
        for url_domain in query_url_set[q]:
            domain_set.add(url_domain.split(',')[1])
        for domain in domain_set:
            count_p=0
            count_1=0
            count_2=0
            count_3=0
            count_4=0
            count_5=0
            for k in query_doc_history.keys():
                if user_id == k[0] and q==k[2]:
                    d=k[3].split(",")[1]
                    if domain == d:
                        count_p+=1
                        if query_doc_history[k]['score']==1:
                            count_1+=1
                        elif query_doc_history[k]['score']==2:
                            count_2+=1
                        elif query_doc_history[k]['score']==3:
                            count_3+=1
                        elif query_doc_history[k]['score']==4:
                            count_4+=1
                        elif query_doc_history[k]['score']==5:
                            count_5+=1
            f_count_p= float(count_p)
            if count_p==0:
                dict_agg_110[(user_id, q,domain)] = [0,0,0,0,0]
            else:
                dict_agg_110[(user_id, q, domain)] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_110

"""Same user same query same url"""
def aggregate_111(user_id, query_doc_history, query_doc, query_url_set):
    dict_agg_111 = defaultdict(float)
    query_set = set()
    for k_train in query_doc.keys():
        query_set.add(k_train[2])
    for q in query_set:
         for url_domain in query_url_set[q]:
            url = url_domain.split(',')[0]
            count_p=0
            count_1=0
            count_2=0
            count_3=0
            count_4=0
            count_5=0
            for k in query_doc_history.keys():
                if user_id == k[0] and q==k[2]:
                    u=k[3].split(",")[0]
                    if url == u:
                        count_p+=1
                        if query_doc_history[k]['score']==1:
                            count_1+=1
                        elif query_doc_history[k]['score']==2:
                            count_2+=1
                        elif query_doc_history[k]['score']==3:
                            count_3+=1
                        elif query_doc_history[k]['score']==4:
                            count_4+=1
                        elif query_doc_history[k]['score']==5:
                            count_5+=1
            f_count_p= float(count_p)
            if count_p==0:
                dict_agg_111[(user_id, q,url)] = [0,0,0,0,0]
            else:
                dict_agg_111[(user_id, q, url)] = [count_1/f_count_p, count_2/f_count_p, count_3/f_count_p, count_4/f_count_p,count_5/f_count_p]
    return dict_agg_111

"""Add the aggregate features to feature vector"""
def add_aggr_features(user_id,query_doc, dict_agg_000, dict_agg_001, dict_agg_010,dict_agg_011, dict_agg_100, dict_agg_101, dict_agg_110,dict_agg_111):
    #iterate through each query-doc combo 
        for key,value in query_doc.items():
            user=key[0]
            session=key[1]
            query=key[2]
            url=key[3].split(",")[0]
            domain=key[3].split(",")[1]
            #We separated all components of a particular query-doc key. 
            #Now we will check values for each attribute we need to compute
            #Feature 000 for this query-doc
            f_000= dict_agg_000[domain]
            f_001= dict_agg_001[url]
            f_010= dict_agg_010[(query,domain)]
            f_011= dict_agg_011[(query,url)]
            f_100= dict_agg_100[(user,domain)]
            f_101= dict_agg_101[(user,url)]
            f_110= dict_agg_110[(user,query,domain)]
            f_111= dict_agg_111[(user,query,url)]
            aggr=[]
            aggr.append(f_000)
            aggr.append(f_001)
            aggr.append(f_010)
            aggr.append(f_011)
            aggr.append(f_100)
            aggr.append(f_101)
            aggr.append(f_110)
            aggr.append(f_111)
            query_doc[key]['aggr']=aggr
        return query_doc
