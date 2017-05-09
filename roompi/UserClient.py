#!/usr/bin/env python3
# This is the Coap Client API to connect to the user server

# imports
from aiocoap import *
import pickle
import logging
import asyncio


# must await...
class UserClient():
    # ctor
    def __init__(self, ip_address):
        self.run = asyncio.get_event_loop().run_until_complete
        self.uri = "coap://%s/user" % (ip_address)

    # this must be run immediatly after init in order to operate
    async def do_connect(self):
        self.proto = await Context.create_client_context()

    # perform a get
    async def do_get(self, uri, data):
        # encode the data
        p = pickle.dumps(data)
        # create message
        req = Message(code=GET, uri=uri, payload=p)
        # perform request
        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            print("Type Error")
        except Exception as e:
            print("Failed GET")
            print(e)
            return None
        finally:
            # get the result
            p = pickle.loads(res.payload)
            return p

    # perfor a put
    async def do_put(self, uri, data):
        # encode the data
        p = pickle.dumps(data)
        # create message
        req = Message(code=PUT, uri=uri, payload=p)
        # perform the request
        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed PUT")
            print(e)
            return None
        finally:
            # return data
            p = pickle.loads(res.payload)
            return p

    # perfor a put
    async def do_post(self, uri, data):
        # encode the data
        p = pickle.dumps(data)
        # create message
        req = Message(code=POST, uri=uri, payload=p)
        # perform the request
        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed POST")
            print(e)
            return None
        finally:
            # return data
            p = pickle.loads(res.payload)
            return p

    # perform a delete
    async def do_delete(self, uri, data):
        # encode the data
        p = pickle.dumps(data)
        # create message
        req = Message(code=DELETE, uri=uri, payload=p)
        # perform the request
        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed DELETE")
            print(e)
            return None
        finally:
            # return data
            p = pickle.loads(res.payload)
            return p

    # public wrappers
    def connect(self):
        self.run(self.do_connect())
        print('Connected')

    def get(self, uri, data):
        return self.run(self.do_get(uri, data))

    def put(self, uri, data):
        return self.run(self.do_put(uri, data))

    def post(self, uri, data):
        return self.run(self.do_post(uri, data))

    def delete(self, uri, data):
        return self.run(self.do_delete(uri, data))

    def check_user_exists(self, uid):
        fake_data = {'uid': uid}
        return self.get(self.uri, fake_data)

    def get_user_info(self, uid):
        return self.check_user_exists(uid)

    def new_user(self, uid, options, credentials):
        data = {'uid': uid, 'options': options, 'credentials': credentials}
        return self.post(self.uri, data)

    def update_user(self, uid, options, credentials):
        data = {'uid': uid, 'options': options, 'credentials': credentials}
        return self.put(self.uri, data)

    def delete_user(self, uid):
        fake_data = {'uid': uid}
        return self.delete(self.uri, fake_data)


# test program if this is run standalone
if __name__ == '__main__':
    c = UserClient('localhost')
    c.connect()
    R = c.check_user_exists('steven')
    print('Getting user: %s' % R)
    R = c.new_user('steven', {'a': 'b'}, ('None',))
    print('Creating  user: %s' % R)
    R = c.check_user_exists('steven')
    print('Getting  user: %s' % R)
    R = c.new_user('steven', {'a': 'b'}, ('None',))
    print('Creating  user: %s' % R)
    R = c.update_user('steven', {'a': 'c'}, ('None',))
    print('Updating  user: %s' % R)
    R = c.get_user_info('steven')
    print('Getting  user: %s' % R)
    R = c.delete_user('steven')
    print('Deleting  user: %s' % R)
    R = c.check_user_exists('steven')
    print('Getting  user: %s' % R)
