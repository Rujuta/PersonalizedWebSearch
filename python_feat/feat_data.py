#! /usr/bin/env python
       
class Session:
    def __init__(self, session_id):
        self._session_id = session_id
    def get_all_queries(self, session_id):
        #Add code here

class Domain:
    def __init(self, domain_id):
        self._domain_id = domain_id
        self.urls_in_domain = []

class Click:
    def __init__(self, url_id, dwell_time,obj_url_query_session):
        self.url_id = url_id        ###make private?
        self.dwell_time = dwell_time        ###make private?

class URL:
    def __init__(self, url_id):
        self._url_id = url_id

class URLQuerySession:
    def __init__(self, url_id, query_id, session_id, rank):
        self.url_id = url_id
        self.query_id = query_id
        self.session_id = session_id
        self._rank = rank        ###make private?
    def get_score(self):

class QuerySession:
    def __init__(self, query_id, session_id, position):
        self.query_id = query_id
        self.session_id = session_id
        self._position = position        ###make private? ###make private?
        ##get position function if it is private
