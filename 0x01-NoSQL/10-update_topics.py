#!/usr/bin/env python3
"""Find and update documents"""


def update_topics(mongo_collection, name, topics):
    """Updates the topics of all documents with the given name"""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
