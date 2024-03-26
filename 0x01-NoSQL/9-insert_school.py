#!/usr/bin/env python3
"""Inserts a record to a collection"""


def insert_school(mongo_collection, **kwargs):
    """inserts a record to a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
