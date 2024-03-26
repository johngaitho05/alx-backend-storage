#!/usr/bin/env python3
"""Find school by topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns school documents that contains a given topic"""
    return list(mongo_collection.find({'topics': {'$in': [topic]}}))
