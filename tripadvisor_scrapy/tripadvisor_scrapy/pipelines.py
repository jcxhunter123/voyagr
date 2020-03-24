# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# Mongodb Pipeline
class TripadvisorScrapyPipeline(object):

    def __init__(self):
        # Create a connection to local mongodb compass
        self.connection = pymongo.MongoClient(
            'localhost',
            27017
        )
        # Create database 'City'
        db = self.connection['Tripadvisor']

        # Create table inside database
        self.collection = db['City_Details']
    
    def process_item(self, item, spider):
        # Inserts items in dictionary form
        self.collection.insert(dict(item))
        return item
