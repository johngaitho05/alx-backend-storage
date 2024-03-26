#!/usr/bin/env python3
"""Fetches all documents of mongodb relation"""


def list_all(mongo_collection):
    """Returns all documents of a collection"""
    return list(mongo_collection.find())
