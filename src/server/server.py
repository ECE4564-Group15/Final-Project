#!/usr/bin/env python3

from aiocoap import *
from aiocoap import resource as resource
from pymongo import MongoClient
import pymongo

import logging
import asyncio
import pickle

class TestResource(resource.Resource):
    #ctor
    def __init__(self):
        super(TestResource, self).__init__()
        self.content = 'Congratz, you made it!'
        self.serialized_content = pickle.dumps(self.content)

    async def render_get(self,r):
        return Message(payload=self.serialized_content)

class UserResource(resource.Resource):
    #ctor
    def __init__(self):
        super(UserResource, self).__init__()
        self.client = MongoClient()
        self.users = self.client.user_db.users
        self.users.create_index([('uid',pymongo.ASCENDING)],unique=True)

    # Function that replies to a GET request for user information
    # It checks first of the user exists in the DB and returns the info
    # if yes and None if no.
    async def render_get(self,r):
        #get the user id
        #expect a dict with "uid"
        req = pickle.loads(r.payload)
        uid = req['uid']
        #query
        print('Getting user %s' % uid)
        user = self.users.find_one({'uid':uid})
        #will return None if not found
        user = pickle.dumps(user)
        return Message(payload=user) 

    #update
    async def render_put(self,r):
        #get the information
        req = pickle.loads(r.payload)
        uid = req['uid']
        res = self.users.find_one_and_replace({'uid':uid},req)
        if res == None:
            print('Updating %s; not found' % uid)
            res = False
        else: 
            print('Updating %s; found' % uid)
            res = True
        res = pickle.dumps(res)
        return Message(payload=res)
    #new
    async def render_post(self,r):
        #get the information
        req = pickle.loads(r.payload)
        uid = req['uid']
        try:
            self.users.insert_one(req)
            res = True
            print('Creating %s; success' % uid)
        except pymongo.errors.DuplicateKeyError:
            res = False
            print('Creating %s; fail: duplicate key' % uid)
        res = pickle.dumps(res)
        return Message(payload=res)

    async def render_delete(self,r):
        #get the information
        req = pickle.loads(r.payload)
        uid = req['uid']
        res = self.users.find_one_and_delete({'uid':req['uid']})
        if res == None:
            print('Deleting %s; not found' % uid)
            res = False
        else: 
            print('Deleting %s; found' % uid)
            res = True
        res = pickle.dumps(res)
        return Message(payload=res)

def main():
    root = resource.Site()

    root.add_resource(('.well-known','core'), resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('test',),TestResource())

    root.add_resource(('user',),UserResource())

    asyncio.Task(Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
