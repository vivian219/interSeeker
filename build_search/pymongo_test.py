# -*- coding: utf-8 -*-
from pymongo import MongoClient
client=MongoClient()
db=client.test

posts=db.posts
def post_one_doc():
    post_data={
        'title':'Python and MongoDB',
        'content':'PyMongo is fun,you guys',
        'author':'Scott'
    }
    #insert one document
    result=posts.insert_one(post_data)
    print('One post : {0}'.format(result.inserted_id))
    """ 5a22648c3f54840ac82ab5c8"""
#insert many document
def post_many_doc():
    post1={
        'title':'Python and MongoDB',
        'content':'PyMongo is fun,you guys',
        'author':'Scott'
    }
    post2={
        'title':'Virtual Environments',
        'content':'Use virtual environment,you guys',
        'author':'Scott'
    }
    post3={
        'title':'Learning Python',
        'content':'Learn Python, it is esay',
        'author':'Bill'
    }
    new_result=posts.insert_many([post1,post2,post3])
    print('Multiple posts: {0}'.format(new_result.inserted_ids))
    '''Multiple posts: [ObjectId('5a2266943f548435d4de0115'), ObjectId('5a2266943f548435d4de0116'), ObjectId('5a2266943f548435d4de0117')]'''
def retrieve_one_docu():
    bill_post=posts.find_one({'author':'Bill'})
    print(bill_post)
def retrieve_many_docu():
    scott_posts=posts.find({'author':'Scott'})
    for post in scott_posts:
        print(post)
retrieve_many_docu()