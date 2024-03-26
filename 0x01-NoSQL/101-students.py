#!/usr/bin/env python3
"""
Write a Python function that returns all students sorted by average score:

Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore

"""


def top_students(mongo_collection):
    """Returns students ordered by average score"""
    students = list(mongo_collection.find())

    # Calculate average score for each student
    for student in students:
        total_score = sum(topic['score'] for topic in student['topics'])
        average_score = total_score / len(student['topics'])
        student['averageScore'] = average_score

    # Sort students based on average score
    sorted_students = sorted(students, key=lambda x: x['averageScore'],
                             reverse=True)

    return sorted_students
