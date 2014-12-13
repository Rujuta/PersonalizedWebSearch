#! /usr/bin/env python
from collections import OrderedDict
import fileread
import query
import generic
import writefile
import user

"""This is the file that will be run always"""

#Get history logs
history_logs=fileread.read_file('../data/history/traa')

#Get train logs
train_logs=fileread.read_file('../data/train/traj')

#Get session wise user objects
user_objects_history=fileread.get_user_objects(train_logs)

query.get_dict_query_counts(history_logs)

query.get_terms_in_query(train_logs)
#query_docs=query.fill_query_doc_features(query_doc)

#Get non personalized rank per user AND create a per user dictionary
for userid, sessions in user_objects_history.items():
    #query_doc=OrderedDict()
    user_details = {'num_query':0,'num_avg_terms':0,'num_clicks12':0, 'num_clicks35':0,'num_clicks6':0}
    query_doc = generic.get_non_personalized_rank(user_objects_history[userid])
    query_doc=query.fill_query_doc_features(query_doc)
    query_doc = generic.get_relevance_score(user_objects_history[userid], query_doc)
    user_details = user.add_user_features(user_details, user_objects_history[userid])
    writefile.create_input_file(userid,query_doc) #,user_details
    exit(1)
