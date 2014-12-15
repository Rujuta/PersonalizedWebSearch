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
    ke=0
    kv=0
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
                flag=1
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
                except ValueError:
                    kv+=1
                ##---->can optimize more- need to do only once
        #assign rest as Missed
        i=max_last_clicked+1
        while(i<len(url_list)):
            temp_key = (user_id,items[0],query_id,url_list[i])
            query_doc[temp_key]['score'] = 1;  #-2: missed
            i+=1
    #print "key error",ke, "value error", kv
    return query_doc

def any_user_aggregate_000(query_doc_history, url_set):

    # user_obj_hist: 'userid':[[SessId],[SessID]..]
    # query_doc_history: 'rank' 'score'
    '''for k in user_objects_history.keys(): ## goes over all users
        for session_info in user_objects_history[k]:
                for line in session_info:'''
    #sorting domains
    dict_agg_000 = {}
    dict_counts = defaultdict(float)
    for url_domain in url_set:
        dict_agg_000[url_domain.split(',')[1]] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
        #[count_miss,count_skip,click0,click1,click2,total_occ,MRR_miss,MRR_skip,MRR_click]
    domain_set = dict_agg_000.keys()
    #finding count(l,P) for a P:000
    for k in query_doc_history.keys():
        d=k[3].split(",")[1]
        if d in domain_set:
            dict_counts[d] +=1
            if query_doc_history[k]['score']==1:
                dict_agg_000[d][0]+=1
                dict_agg_000[d][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_000[d][1]+=1
                dict_agg_000[d][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_000[d][2]+=1
                dict_agg_000[d][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_000[d][3]+=1
                dict_agg_000[d][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_000[d][4]+=1
                dict_agg_000[d][7]+=1.0/query_doc_history[k]['rank']
    for domain in domain_set:
        if dict_agg_000[domain][5]>0.0:
            dict_agg_000[domain][0] = dict_agg_000[domain][0]/(dict_counts[domain]+1)
            dict_agg_000[domain][1] = dict_agg_000[domain][1]/(dict_counts[domain]+1)
            dict_agg_000[domain][2] = dict_agg_000[domain][2]/(dict_counts[domain]+1)
            dict_agg_000[domain][3] = dict_agg_000[domain][3]/(dict_counts[domain]+1)
            dict_agg_000[domain][4] = dict_agg_000[domain][4]/(dict_counts[domain]+1)
            dict_agg_000[domain][5] = dict_agg_000[domain][5]/(dict_counts[domain]+1)
            dict_agg_000[domain][6] = dict_agg_000[domain][6]/(dict_counts[domain]+1)
            dict_agg_000[domain][7] = dict_agg_000[domain][7]/(dict_counts[domain]+1)
    return dict_agg_000

#aggregate for 001
def any_user_aggregate_001(query_doc_history, url_set):

    #finding count(l,P) for a P:001
    dict_agg_001 = {}
    dict_counts= defaultdict(float)
    for url_domain in url_set:
        dict_agg_001[url_domain.split(',')[0]] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    urls = dict_agg_001.keys()
    for k in query_doc_history.keys():
        u=k[3].split(",")[0]
        if u in urls:
            dict_counts[u]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_001[u][0]+=1
                dict_agg_001[u][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_001[u][1]+=1
                dict_agg_001[u][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_001[u][2]+=1
                dict_agg_001[u][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_001[u][3]+=1
                dict_agg_001[u][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_001[u][4]+=1
                dict_agg_001[u][7]+=1.0/query_doc_history[k]['rank']
    for url in urls:
        if dict_agg_001[url][5]>0.0:
            dict_agg_001[url][0] = dict_agg_001[url][0]/(dict_counts[url]+1)
            dict_agg_001[url][1] = dict_agg_001[url][1]/(dict_counts[url]+1)
            dict_agg_001[url][2] = dict_agg_001[url][2]/(dict_counts[url]+1)
            dict_agg_001[url][3] = dict_agg_001[url][3]/(dict_counts[url]+1)
            dict_agg_001[url][4] = dict_agg_001[url][4]/(dict_counts[url]+1)
            dict_agg_001[url][5] = dict_agg_001[url][5]/(dict_counts[url]+1)
            dict_agg_001[url][6] = dict_agg_001[url][6]/(dict_counts[url]+1)
            dict_agg_001[url][7] = dict_agg_001[url][7]/(dict_counts[url]+1)
    return dict_agg_001

def any_user_aggregate_010(query_doc_history, query_url_set):
    #finding count(l,P) for a P:010
    #domain matches and query matches

    dict_agg_010 = {}
    dict_counts= defaultdict(float)
    for q in query_url_set.keys():
        for url_domain in query_url_set[q]:
            dict_agg_010[(q,url_domain.split(',')[1])] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    qds = dict_agg_010.keys()
    for k in query_doc_history.keys():
        d=k[3].split(",")[1]
        q=k[2]
        if (q,d) in qds:
            dict_counts[(q,d)]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_010[(q,d)][0]+=1
                dict_agg_010[(q,d)][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_010[(q,d)][1]+=1
                dict_agg_010[(q,d)][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_010[(q,d)][2]+=1
                dict_agg_010[(q,d)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_010[(q,d)][3]+=1
                dict_agg_010[(q,d)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_010[(q,d)][4]+=1
                dict_agg_010[(q,d)][7]+=1.0/query_doc_history[k]['rank']
    for k in qds:
        if dict_agg_010[k][5]>0.0:
            dict_agg_010[k][0] = dict_agg_010[k][0]/(dict_counts[k]+1)
            dict_agg_010[k][1] = dict_agg_010[k][1]/(dict_counts[k]+1)
            dict_agg_010[k][2] = dict_agg_010[k][2]/(dict_counts[k]+1)
            dict_agg_010[k][3] = dict_agg_010[k][3]/(dict_counts[k]+1)
            dict_agg_010[k][4] = dict_agg_010[k][4]/(dict_counts[k]+1)
            dict_agg_010[k][5] = dict_agg_010[k][5]/(dict_counts[k]+1)
            dict_agg_010[k][6] = dict_agg_010[k][6]/(dict_counts[k]+1)
            dict_agg_010[k][7] = dict_agg_010[k][7]/(dict_counts[k]+1)
    return dict_agg_010


def any_user_aggregate_011(query_doc_history, query_url_set):
    #finding count(l,P) for a P:010
    #domain matches and query matches

    dict_agg_011 = {}
    dict_counts= defaultdict(float)
    for q in query_url_set.keys():
        for url_domain in query_url_set[q]:
            dict_agg_011[(q,url_domain.split(',')[0])] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    qus = dict_agg_011.keys()
    for k in query_doc_history.keys():
        u=k[3].split(",")[0]
        q=k[2]
        if (q,u) in qus:
            dict_counts[(q,u)]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_011[(q,u)][0]+=1
                dict_agg_011[(q,u)][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_011[(q,u)][1]+=1
                dict_agg_011[(q,u)][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_011[(q,u)][2]+=1
                dict_agg_011[(q,u)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_011[(q,u)][3]+=1
                dict_agg_011[(q,u)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_011[(q,u)][4]+=1
                dict_agg_011[(q,u)][7]+=1.0/query_doc_history[k]['rank']
    for k in qus:
        if dict_agg_011[k][5]>0.0:
            dict_agg_011[k][0] = dict_agg_011[k][0]/(dict_counts[k]+1)
            dict_agg_011[k][1] = dict_agg_011[k][1]/(dict_counts[k]+1)
            dict_agg_011[k][2] = dict_agg_011[k][2]/(dict_counts[k]+1)
            dict_agg_011[k][3] = dict_agg_011[k][3]/(dict_counts[k]+1)
            dict_agg_011[k][4] = dict_agg_011[k][4]/(dict_counts[k]+1)
            dict_agg_011[k][5] = dict_agg_011[k][5]/(dict_counts[k]+1)
            dict_agg_011[k][6] = dict_agg_011[k][6]/(dict_counts[k]+1)
            dict_agg_011[k][7] = dict_agg_011[k][7]/(dict_counts[k]+1)
    return dict_agg_011

"""Same user, any query, same domain"""
def aggregate_100(user_id, query_doc_history, query_doc):
    dict_agg_100 = {}
    dict_counts= defaultdict(float)
    for k_train in query_doc.keys():
        dict_agg_100[(user_id,k_train[3].split(',')[1])] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    uds = dict_agg_100.keys()
    for k in query_doc_history.keys():
        d=k[3].split(",")[1]
        if (user_id,d) in uds:
            dict_counts[(user_id,d)]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_100[(user_id,d)][0]+=1
                dict_agg_100[(user_id,d)][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_100[(user_id,d)][1]+=1
                dict_agg_100[(user_id,d)][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_100[(user_id,d)][2]+=1
                dict_agg_100[(user_id,d)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_100[(user_id,d)][3]+=1
                dict_agg_100[(user_id,d)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_100[(user_id,d)][4]+=1
                dict_agg_100[(user_id,d)][7]+=1.0/query_doc_history[k]['rank']
    for k in uds:
        if dict_agg_100[k][5]>0.0:
            dict_agg_100[k][0] = dict_agg_100[k][0]/(dict_counts[k]+1)
            dict_agg_100[k][1] = dict_agg_100[k][1]/(dict_counts[k]+1)
            dict_agg_100[k][2] = dict_agg_100[k][2]/(dict_counts[k]+1)
            dict_agg_100[k][3] = dict_agg_100[k][3]/(dict_counts[k]+1)
            dict_agg_100[k][4] = dict_agg_100[k][4]/(dict_counts[k]+1)
            dict_agg_100[k][5] = dict_agg_100[k][5]/(dict_counts[k]+1)
            dict_agg_100[k][6] = dict_agg_100[k][6]/(dict_counts[k]+1)
            dict_agg_100[k][7] = dict_agg_100[k][7]/(dict_counts[k]+1)
    return dict_agg_100

"""Same user, any query, same URL"""
def aggregate_101(user_id, query_doc_history, query_doc):
    dict_agg_101 = {}
    dict_counts= defaultdict(float)
    for k_train in query_doc.keys():
        dict_agg_101[(user_id,k_train[3].split(',')[0])] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    uus = dict_agg_101.keys()
    for k in query_doc_history.keys():
        u=k[3].split(",")[0]
        if (user_id,u) in uus:
            dict_counts[(user_id,u)]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_101[(user_id,u)][0]+=1
                dict_agg_101[(user_id,u)][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_101[(user_id,u)][1]+=1
                dict_agg_101[(user_id,u)][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_101[(user_id,u)][2]+=1
                dict_agg_101[(user_id,u)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_101[(user_id,u)][3]+=1
                dict_agg_101[(user_id,u)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_101[(user_id,u)][4]+=1
                dict_agg_101[(user_id,u)][7]+=1.0/query_doc_history[k]['rank']
    for k in uus:
        if dict_agg_101[k][5]>0.0:
            dict_agg_101[k][0] = dict_agg_101[k][0]/(dict_counts[k]+1)
            dict_agg_101[k][1] = dict_agg_101[k][1]/(dict_counts[k]+1)
            dict_agg_101[k][2] = dict_agg_101[k][2]/(dict_counts[k]+1)
            dict_agg_101[k][3] = dict_agg_101[k][3]/(dict_counts[k]+1)
            dict_agg_101[k][4] = dict_agg_101[k][4]/(dict_counts[k]+1)
            dict_agg_101[k][5] = dict_agg_101[k][5]/(dict_counts[k]+1)
            dict_agg_101[k][6] = dict_agg_101[k][6]/(dict_counts[k]+1)
            dict_agg_101[k][7] = dict_agg_101[k][7]/(dict_counts[k]+1)
    return dict_agg_101

"""Same user, same query, any domain"""
def aggregate_110(user_id, query_doc_history, query_doc, query_url_set):
    dict_agg_110 = {}
    dict_counts= defaultdict(float)
    query_set = set()
    for k_train in query_doc.keys():
        query_set.add(k_train[2])
    for q in query_set:
         for url_domain in query_url_set[q]:
            dict_agg_110[(user_id,q,url_domain.split(',')[1])] =[1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    uqds= dict_agg_110.keys()
    for k in query_doc_history.keys():
        d=k[3].split(",")[1]
        q=k[2]
        if (user_id,q,d) in uqds:
            dict_counts[(user_id,q,d)]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_110[(user_id,q,d)][0]+=1
                dict_agg_110[(user_id,q,d)][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_110[(user_id,q,d)][1]+=1
                dict_agg_110[(user_id,q,d)][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_110[(user_id,q,d)][2]+=1
                dict_agg_110[(user_id,q,d)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_110[(user_id,q,d)][3]+=1
                dict_agg_110[(user_id,q,d)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_110[(user_id,q,d)][4]+=1
                dict_agg_110[(user_id,q,d)][7]+=1.0/query_doc_history[k]['rank']
    for k in uqds:
        if dict_agg_110[k][5]>0.0:
            dict_agg_110[k][0] = dict_agg_110[k][0]/(dict_counts[k]+1)
            dict_agg_110[k][1] = dict_agg_110[k][1]/(dict_counts[k]+1)
            dict_agg_110[k][2] = dict_agg_110[k][2]/(dict_counts[k]+1)
            dict_agg_110[k][3] = dict_agg_110[k][3]/(dict_counts[k]+1)
            dict_agg_110[k][4] = dict_agg_110[k][4]/(dict_counts[k]+1)
            dict_agg_110[k][5] = dict_agg_110[k][5]/(dict_counts[k]+1)
            dict_agg_110[k][6] = dict_agg_110[k][6]/(dict_counts[k]+1)
            dict_agg_110[k][7] = dict_agg_110[k][7]/(dict_counts[k]+1)
    return dict_agg_110

"""Same user same query same url"""
def aggregate_111(user_id, query_doc_history, query_doc, query_url_set):
    dict_agg_111 = {}
    dict_counts= defaultdict(float)
    query_set = set()
    for k_train in query_doc.keys():
        query_set.add(k_train[2])
    for q in query_set:
         for url_domain in query_url_set[q]:
            dict_agg_111[(user_id,q,url_domain.split(',')[0])] = [1.0,0.0,0.0,0.0,0.0,0.283,0.283,0.283]
    uqus= dict_agg_111.keys()
    for k in query_doc_history.keys():
        u=k[3].split(",")[0]
        q=k[2]
        if (user_id,q,u) in uqus:
            dict_counts[(user_id,q,u)]+=1
            if query_doc_history[k]['score']==1:
                dict_agg_111[(user_id,q,u)][0]+=1
                dict_agg_111[(user_id,q,u)][5]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==2:
                dict_agg_111[(user_id,q,u)][1]+=1
                dict_agg_111[(user_id,q,u)][6]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==3:
                dict_agg_111[(user_id,q,u)][2]+=1
                dict_agg_111[(user_id,q,u)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==4:
                dict_agg_111[(user_id,q,u)][3]+=1
                dict_agg_111[(user_id,q,u)][7]+=1.0/query_doc_history[k]['rank']
            elif query_doc_history[k]['score']==5:
                dict_agg_111[(user_id,q,u)][4]+=1
                dict_agg_111[(user_id,q,u)][7]+=1.0/query_doc_history[k]['rank']
    for k in uqus:
        if dict_agg_111[k][5]>0.0:
            dict_agg_111[k][0] = dict_agg_111[k][0]/(dict_counts[k]+1)
            dict_agg_111[k][1] = dict_agg_111[k][1]/(dict_counts[k]+1)
            dict_agg_111[k][2] = dict_agg_111[k][2]/(dict_counts[k]+1)
            dict_agg_111[k][3] = dict_agg_111[k][3]/(dict_counts[k]+1)
            dict_agg_111[k][4] = dict_agg_111[k][4]/(dict_counts[k]+1)
            dict_agg_111[k][5] = dict_agg_111[k][5]/(dict_counts[k]+1)
            dict_agg_111[k][6] = dict_agg_111[k][6]/(dict_counts[k]+1)
            dict_agg_111[k][7] = dict_agg_111[k][7]/(dict_counts[k]+1)
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
            try:
                f_000= dict_agg_000[domain]
                f_001= dict_agg_001[url]
                f_010= dict_agg_010[(query,domain)]
                f_011= dict_agg_011[(query,url)]
                f_100= dict_agg_100[(user,domain)]
                f_101= dict_agg_101[(user,url)]
                f_110= dict_agg_110[(user,query,domain)]
                f_111= dict_agg_111[(user,query,url)]
            except KeyError:
                f_000= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_001= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_010= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_011= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_100= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_101= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_110= [0.0,0.0,0.0,0.0,0.0,0.0]
                f_111= [0.0,0.0,0.0,0.0,0.0,0.0]
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
