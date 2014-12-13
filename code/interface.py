#! /usr/bin/env python
from collections import OrderedDict
import fileread
import query
import generic
import writefile
import user
import urls

"""This is the file that will be run always"""

#Get history logs
history_logs=fileread.read_file('../data/history/try')

#Get train logs
train_logs=fileread.read_file('../data/train/tr1')

#Get session wise user objects
user_objects_train=fileread.get_user_objects(train_logs)
user_objects_history=fileread.get_user_objects(history_logs)

query_counts = query.get_dict_query_counts(history_logs)

query_terms = query.get_terms_in_query(train_logs)

#get all urls returned in train data
url_set = urls.get_urls(train_logs)
query_url_set = query.get_urls_in_query(train_logs)
query_doc_history=OrderedDict()
query_doc = OrderedDict()
#query_docs=query.fill_query_doc_features(query_doc)
for user_id, sessions in user_objects_history.items():
    query_doc_history = generic.get_non_personalized_rank(user_objects_history[user_id], user_id, query_doc_history)
    query_doc_history = generic.get_relevance_score(user_objects_history[user_id], user_id, query_doc_history)
##gets any user aggregate feature data from history
dict_agg_000 = generic.any_user_aggregate_000(query_doc_history, url_set)
dict_agg_001 = generic.any_user_aggregate_001(query_doc_history, url_set)
dict_agg_010 = generic.any_user_aggregate_010(query_doc_history, query_url_set)
dict_agg_011 = generic.any_user_aggregate_011(query_doc_history, query_url_set)

#Get non personalized rank per user AND create a per user dictionary
for user_id in user_objects_train.keys():
    #query_doc=OrderedDict()
    user_details = {'num_query':0,'num_avg_terms':0,'num_clicks12':0, 'num_clicks35':0,'num_clicks6':0}
    query_doc = generic.get_non_personalized_rank(user_objects_train[user_id], user_id, query_doc)
    query_doc= query.fill_query_doc_features(query_doc)
    query_doc = generic.get_relevance_score(user_objects_train[user_id], user_id, query_doc)
    dict_agg_100 = generic.aggregate_100(user_id, query_doc_history, query_doc)
    dict_agg_101 = generic.aggregate_101(user_id, query_doc_history, query_doc)
    dict_agg_110 = generic.aggregate_110(user_id, query_doc_history, query_doc, query_url_set)
    dict_agg_111 = generic.aggregate_111(user_id, query_doc_history, query_doc, query_url_set)
    print dict_agg_111
    exit(0)
    if user_id in user_objects_history.keys():
        user_details = user.add_user_features(user_details, user_objects_history[user_id])

    writefile.create_input_file(user_id,query_doc) #,user_details
    exit(1)
