# Final-Project

## Restful Interface

### Server

The server is a coap interface that leverages pymongo for the database functionality.
It requires that the python modules: `pymongo` and `aiocoap` are installed.

Also, it requires that a mongoDB instance is running.

### Client

The client is a simple module that you can import and use.
It requires that `aiocoap` is installed.

The constructor takes a single argument: `ip_address`
 - This is the ip address of the server

Member functions:
 - `connect()`: This is necessary for proper operation. It setups the COAP interface. Must be run first.
 - `get_user_info(uid)`: This returns `None` if the user is not found and a dictionary with the user's database entry if found
 - `check_user_exists(uid)`: This is an alias for `get_user_info`
 - `new_user(uid,options,credentials)`: Adds a new user and returns the success state of the operation. You cannot add a duplicate uid. The values can be whatever can be entered into a dict.
 - `update_user(uid,options,credentials)`: Updates the user entry. Returns the success of the operation.
 - `delete_user(uid)`: Deletes the user entry. Returns the success of the operation.

## TODO:
Find a good idea on the final project for now.
