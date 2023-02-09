# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    # Name for the spider
    name = 'tmdb_spider'
    
    # starting at the description page for The Blacklist
    start_urls = ['https://www.themoviedb.org/tv/46952-the-blacklist']
    
    def parse(self, response):
        '''
        This method assumes you start on the description page for a film / TV show.
        It then navigates to the casting page for the show, where it conducts the 
        parse_full_credits method.
        '''

        # the link for the casting page is the description page url + /cast
        cast_link = response.request.url + "/cast"
        # navigates to casting page, where it calls parse_full_credits
        yield scrapy.Request(cast_link, callback =  self.parse_full_credits)
        
    def parse_full_credits(self, response):
        '''
        This method assumes you start on the description page for a film / TV show.
        It then scrapes all the cast for the film / TV show. It does not scrape the crew.
        For each cast member, this method navigates to the bio page for the actor, where
        it conducts the parse_actor_page method.
        '''

        # retrieves selector object for table of cast
        cast_list = response.css("section.panel.pad")[0]
        # retrieves a list of all the url extensions for the cast of the film 
        actor_links = cast_list.css("div.info > span > p:not(.character) > a::attr(href)").getall()
        # navigates to the casting page for each actor, where it calls parse_actor_page
        for link in actor_links:
            yield response.follow(link, callback =  self.parse_actor_page)

    def parse_actor_page(self, response):
        '''
        This method assumes you start on the bio page for a specific actor. It then scrapes
        all projects that the actor worked in. For each project, this method returns a dictionary
        of the form {actor : move_or_TV_name}
        '''

        # retrieves the name of the actor from the title of the webpage
        actor_name = response.css("title::text").get().split(" — ")[0]
        # retrieves the table of all projects the actor appeared in
        acting_table = response.css("table.card.credits")[0]
        # scrapes the list of all projects from the table
        acting_list = acting_table.css("a.tooltip bdi::text").getall()
        # for each project, the method return a dictionary with key being the actor's name
        # and value being the name of the project
        for movie_or_TV_name in acting_list:
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}