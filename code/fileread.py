#! /usr/bin/env python
from collections import defaultdict

"""
This module will have two inputs <History files path> <Train/Dev/Test files path>.
On getting these files, a user specific dictionary is made. 
All feature functions will have to call the functions in this file 
"""

""" This function reads the train file and 
    puts everything into a list. 
    This list is what is going to be referred to by the rest of the 
    training program
"""
#user_objects=defaultdict(list)
def read_file(file_name):
    #global search_logs
    with open(file_name) as f:
       search_logs = f.readlines()
    return search_logs


"""create a dictionary per user. The key is User_ID and the value is the list of user sessions - This would be done for obtaining 
user history in an easy format"""
def get_user_objects(search_logs):
#    global search_logs
 #   global user_objects
    user_objects=defaultdict(list)
    for log in search_logs:
        items=log.split()
        if items[1] == 'M':
            user_id=items[3]
            continue;
        user_objects[user_id].append(log)
    return user_objects


