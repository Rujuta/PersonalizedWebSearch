#! /usr/bin/env python
from collections import defaultdict
import fileread

query_counts=defaultdict(int)
query_terms=defaultdict(int)
query_url_set = defaultdict(set)

"""Returns a dictionary of type {<Query_ID>, count} that indicates how many times 
a particular query has been queried"""
def get_dict_query_counts(search_logs):
    for log in search_logs:
            items=log.split()
            if items[2] == 'Q':
                count=query_counts[items[4]]
                count+=1
                query_counts[items[4]]=count
    return query_counts

"""Create a dictionary keyed by queryID and the number of terms in the query"""
def get_terms_in_query(search_logs):
    for log in search_logs:
            items=log.split()
            if items[2] == 'Q':
                count_query_terms=len(items[5].split(","))
                query_terms[items[4]]=count_query_terms
    return query_terms

def get_urls_in_query(search_logs):
    for log in search_logs:
            items=log.split()
            if items[2] == 'Q':
                for each in items[6:]:
                    query_url_set[items[4]].add(each)
    return query_url_set

def fill_query_doc_features(query_doc):
    # Fill in the number of times an item has been queried for by anyone and the no of terms in that query
    for k,v in query_doc.items():
        count_terms= query_terms[k[0]]
        query_doc[k]['terms']=count_terms
        count_queried_for=query_counts[k[0]]
        query_doc[k]['frequency']=count_queried_for
    return query_doc



