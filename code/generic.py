#! /usr/bin/env python
from collections import defaultdict
from collections import OrderedDict

"""Returns the non-personalized rank for some query-doc combination for a particular user"""
def get_non_personalized_rank(userid, sessions_list):
    query_doc=OrderedDict() #a dictionary keyed by query-doc combination
    for line in sessions_list:                  ##sessions of that user
        items = line.split()
        if items[2] == 'Q':
            rank=1
            for doc in items[6:]:
                key=(items[4],doc)          ##items[4]: queryID
                if key not in query_doc.keys():
                    query_doc[key]=OrderedDict()
                query_doc[key]['rank']=rank         ##nonPersonalizedRank
                rank+=1
    return query_doc
