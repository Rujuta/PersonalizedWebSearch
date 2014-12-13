#! /usr/bin/env python
from collections import defaultdict
from collections import OrderedDict

def add_user_features(user_details, sessions_list):
    num_terms = 0
    num_query = 0
    url_list = []
    for session_info in sessions_list:      ##session of that user
        for line in session_info:
            items = line.split()
            if items[2] == 'Q':
                num_query +=1
                num_terms += len(items[5].split(','))
                url_list = []
                for each in items[6:]:
                    url_list.append(each.split(',')[0])
            if items[2] == 'C':
                url_rank = url_list.index(items[4])
                if url_rank==0 or url_rank==1:
                    user_details['num_clicks12'] +=1
                elif url_rank>=2 and url_rank<=4:
                    user_details['num_clicks35'] +=1
                else:
                    user_details['num_clicks6'] +=1
    user_details['num_query'] = num_query
    user_details['num_avg_terms'] = float(num_terms)/float(num_query)
    return user_details