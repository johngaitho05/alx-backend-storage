#!/usr/bin/env python3
"""Write a Python script that provides some stats
about Nginx logs stored in MongoDB:"""
from pymongo import MongoClient

if __name__ == "__main__":
    local_client = MongoClient()
    collection = local_client['logs']['nginx']

    count = collection.count_documents({})
    print('{} logs'.format(count))
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print('Methods:')
    for mtd in methods:
        print('\tmethod {}: {}'.format(
            mtd, collection.count_documents({'method': mtd})))
    print('{} status check'.format(
        collection.count_documents({'method': 'GET', 'path': '/status'})))
