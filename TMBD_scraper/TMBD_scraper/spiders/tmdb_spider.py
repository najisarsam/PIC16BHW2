# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/46952-the-blacklist']
    
    def parse(self, response):
        #cast_link = response.urljoin('cast')
        cast_link = response.request.url + "/cast"
        yield scrapy.Request(cast_link, callback =  self.parse_full_credits)
        
    def parse_full_credits(self, response):
        cast_list = response.css("section.panel.pad")[0]
        actor_links = cast_list.css("div.info > span > p:not(.character) > a::attr(href)").getall()
        for link in actor_links:
            # yield scrapy.Request(link, callback =  self.parse_actor_page)
            yield response.follow(link, callback =  self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css("title::text").get().split(" — ")[0]
        acting_table = response.css("table.card.credits")[0]
        acting_list = acting_table.css("a.tooltip bdi::text").getall()
        for movie_or_TV_name in acting_list:
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}