#! /usr/bin/env python
from collections import OrderedDict
import fileread
import query
import generic
import writefile

"""This is the file that will be run always"""

#Get history logs
history_logs=fileread.read_file('../data/history/xaa')

#Get train logs
train_logs=fileread.read_file('../data/train/xba')

#Get session wise user objects
user_objects_history=fileread.get_user_objects(train_logs)

query.get_dict_query_counts(history_logs)

query.get_terms_in_query(train_logs)

#query_docs=query.fill_query_doc_features(query_doc)

#Get non personalized rank per user AND create a per user dictionary
for userid, sessions in user_objects_history.items():
    #query_doc=OrderedDict()
    query_doc=generic.get_non_personalized_rank(userid,sessions)
    query_doc=query.fill_query_doc_features(query_doc)
    writefile.create_input_file(userid,query_doc) 
    exit(1)
