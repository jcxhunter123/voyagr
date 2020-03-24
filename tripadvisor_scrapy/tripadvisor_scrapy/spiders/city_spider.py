import scrapy
import base64
from scrapy.shell import inspect_response
from ..items import TripadvisorScrapyItem
import json
import re

def open_city_links():
    with open('city_links.txt','r') as f:
        links_dict = json.load(f)
        return links_dict

class CitySpider(scrapy.Spider):
    name = "city"
    start_urls = [
        # 'https://en.tripadvisor.com.hk/Attractions-g60763-Activities-New_York_City_New_York.html',
        #  'https://en.tripadvisor.com.hk/Attractions-g294217-Activities-Hong_Kong.html'
    ]
    links_dict = open_city_links()
    for i in links_dict:
        start_urls.append('https://en.tripadvisor.com.hk'+ links_dict[i]['Things to do'])

    def parse(self,response):
        activities = response.css('div.ui_container div.attractions-carousel-shelf-ShelfCarousel__wrapper--6k_83 div.attractions-carousel-shelf-ShelfCarousel__items--2kwB3 div.attractions-carousel-shelf-ShelfCarouselItem__default_width--1ZGAN') 
        # Send a Scrapy request for every category in a city to scrape details
        for acts in activities:
            relativeurl = acts.css('a::attr(href)').get()
            if relativeurl == None:
                base64_message = acts.css('div::attr(data-encoded-url)').get()
                base64_bytes = base64_message.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                relativeurl = message_bytes.decode('ascii')[3:]
            url = response.urljoin(relativeurl)
            yield scrapy.Request(url, callback=self.parse_city)

    def parse_city(self, response):
        # Create an instance of Item class
        items = TripadvisorScrapyItem()
        
        # Scrape details of each listings for a category
        for details in response.css('div.listing_details'):
            city = response.css('a[id="global-nav-tourism"]::text').get()[:-1]
            title = details.css('div.listing_info div.listing_title h2::text').get()
            no_reviews = details.css('div.listing_info div.listing_rating div.wrap div.rs span.more a[target="_blank"]::text').get()
            rating = details.css('div.listing_info div.listing_rating div.wrap div.rs span.ui_bubble_rating::attr(alt)').get()
            if no_reviews != None:
                no_reviews = no_reviews[1:-1]
            else:
                no_reviews = None
            if rating != None:
                rating = float(''.join(re.findall(r'\d+\.*\d*',rating[:4])))
            else:
                rating = None
            ranking = details.css('div.listing_info div.listing_rating div.popRanking::text')[1].get()[2:-1]
            category = response.css('label[for="ap_filter_c_0"] a::text').get()
            categorytags = response.css('div.filter_list_0 div.jfy_checkbox label[for="ap_filter_t_1"] a::text').get()  
            if categorytags == None:
                categorytags = category

            items['city'] = city
            items['title'] = title
            items['no_reviews'] = no_reviews
            items['rating'] = rating
            items['ranking'] = ranking
            items['category'] = category
            items['categorytags'] = categorytags

            yield items
            
            # yield {
            #     'city': city,
            #     'title': title,
            #     'no_reviews': no_reviews,
            #     'rating': rating,
            #     'ranking': ranking,
            #     'category': category,
            #     'categorytags': categorytags
            # }
      
        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract() 
        if len(next_page) != 0:      
            if next_page is not None:
                next_page = response.urljoin(next_page[-1])
                yield scrapy.Request(next_page, callback=self.parse_city)
        else:
            pass 

        
