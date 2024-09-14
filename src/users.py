#!/usr/bin/python3

import uuid

users = set() 

def create_user():
    new_user = str(uuid.uuid4())
    users.add(new_user)
    return new_user

def verify_user(user_id):
    return user_id in users
