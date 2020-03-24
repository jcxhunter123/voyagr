# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class TripadvisorScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    title = scrapy.Field()
    no_reviews = scrapy.Field()
    rating = scrapy.Field()
    ranking = scrapy.Field()
    category = scrapy.Field()
    categorytags = scrapy.Field()