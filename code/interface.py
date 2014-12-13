#! /usr/bin/env python
from collections import OrderedDict
from collections import defaultdict
import fileread
import query
import generic
import writefile
import user
import urls
import os


"""This is the file that will be run always"""

#Get history logs
#This will loop  through all files in the history directory and fill in the history_logs[]
#section
history_logs=[]

HISTORY='../data/history_tmp/'
TRAIN='../data/train_tmp/'
DEV='../data/dev/'
TEST='../data/test/'

query_counts=defaultdict(int)
query_terms=defaultdict(int)
dir_entries=os.listdir(HISTORY)
dir_entries=sorted(dir_entries)
for dir_entry in dir_entries:
    dir_entry_path=os.path.join(HISTORY,dir_entry)
    if os.path.isfile(dir_entry_path):
        history_logs=fileread.read_file(dir_entry_path, history_logs)

print "Loaded history logs"

#Get train logs - fill in train logs after looping through all files in train
train_logs=[]
dir_entries=os.listdir(TRAIN)
dir_entries=sorted(dir_entries)
for dir_entry in dir_entries:
    dir_entry_path=os.path.join(TRAIN,dir_entry)
    if os.path.isfile(dir_entry_path):
        train_logs=fileread.read_file(dir_entry_path, train_logs)


print "Loaded train logs"

#Get session wise user objects for both history and train logs
user_objects_train=fileread.get_user_objects(train_logs)

print "Got user objects train"

user_objects_history=fileread.get_user_objects(history_logs)


print "Got user objects history"

#Get the number of times something was queried for from all history logs - or frequency of query
query_counts = query.get_dict_query_counts(query_counts,history_logs)

print "Got query counts"
# Get number of terms in a query in each train log result
query_terms = query.get_terms_in_query(query_terms,train_logs)

print "Got query terms"
#get all urls returned in train data 
url_set = urls.get_urls(train_logs)

print "Got url set"
#get the set of all queries in train logs
query_url_set = query.get_urls_in_query(train_logs)

print "Got query set"
#This is a key-value store where key  = tuple of <UserID, SessionID, QueryID, URL-Domain combo> The values will be the set of features 
#computed for those. For history only -ranks and scores will be computed
query_doc_history=OrderedDict()


#Same data structure as above, but obtained from train logs. We will also compute aggregate features, query counts, query terms, user specific
#features etc. This will be dumped to a file which would act as input for a script converting it to LETOR format
query_doc = OrderedDict()

#Read userid, list of user's sessions from history data
#Get non personalized rank for each query-doc-pair for that user and the relevance score
value_error=0
for user_id, sessions in user_objects_history.items():
    query_doc_history = generic.get_non_personalized_rank(user_objects_history[user_id], user_id, query_doc_history)
    query_doc_history = generic.get_relevance_score(user_objects_history[user_id], user_id, query_doc_history)


print "Processed query doc history for all users" 

print "history :::",value_error
##gets any user aggregate feature data from history
#Any user Any query same domain

dict_agg_000 = generic.any_user_aggregate_000(query_doc_history, url_set)
print "got agg 000"
#Any user, Any query, same URL
dict_agg_001 = generic.any_user_aggregate_001(query_doc_history, url_set)
print "got agg 001"

#Any user, Same query, same domain
dict_agg_010 = generic.any_user_aggregate_010(query_doc_history, query_url_set)
print "got agg 010"

#Any user, same query, same URL
dict_agg_011 = generic.any_user_aggregate_011(query_doc_history, query_url_set)
print "got agg 011"

#Get non personalized rank per user AND create a per user dictionary
for user_id in user_objects_train.keys():
    #query_doc=OrderedDict()
    user_details = {'num_query':0,'num_avg_terms':0,'num_clicks12':0, 'num_clicks35':0,'num_clicks6':0}
    query_doc = generic.get_non_personalized_rank(user_objects_train[user_id], user_id, query_doc)
    query_doc= query.fill_query_doc_features(query_terms,query_counts,query_doc)
    query_doc = generic.get_relevance_score(user_objects_train[user_id], user_id, query_doc)
    dict_agg_100 = generic.aggregate_100(user_id, query_doc_history, query_doc)
    dict_agg_101 = generic.aggregate_101(user_id, query_doc_history, query_doc)
    dict_agg_110 = generic.aggregate_110(user_id, query_doc_history, query_doc, query_url_set)
    dict_agg_111 = generic.aggregate_111(user_id, query_doc_history, query_doc, query_url_set)
    #if user_id in user_objects_history.keys():
     #   user_details = user.add_user_features(user_details, user_objects_history[user_id])
    query_doc=generic.add_aggr_features(user_id,query_doc, dict_agg_000, dict_agg_001, dict_agg_010,dict_agg_011, dict_agg_100, dict_agg_101, dict_agg_110,dict_agg_111)
    writefile.create_input_file(user_id,query_doc) #,user_details
    print "wrote file"
print "Finished"
