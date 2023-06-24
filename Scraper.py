from bs4 import BeautifulSoup
import requests 

# search result item abstraction
class SearchEntry:
    def __init__(self, title, link, price, location, time, data_ids, desc, length):
        self.title = title
        self.link = link
        self.price = price
        self.location = location
        self.time = time
        self.data_ids = data_ids  # hash

        # meta data
        self.desc = desc
        self.length = length
        self.price = price
        self.location = location
        self.time = time

    def update_desc(self, desc):
        self.desc = desc

    def update_length(self, length):
        self.length = length

class Scraper:

    def __init__(self):
        self.search_results = []
        self.raw_html = ""
        self.save_title = "clist.html"

    # send http request to given url (stored in result.content) and save the html page
    def get_html(self, url, save_flag):
        session = requests.session()
        result = session.get(url)
        print(result.content)
        if save_flag == 1:
            self.save_html()

        return 0

    #save raw html
    def save_html(self):
        html = open(self.save_title, "w")
        html.write(str(self.raw_html.content))
        html.close()

    # open local version of html and compile results
    def get_results(self):
        html = open(self.save_title, "r")
        clist_results = BeautifulSoup(html, "html.parser")  # get soup object of clist page and close the file
        html.close()

        # get actual results (result-row class)
        result_list = clist_results.find_all(class_="result-row")

        # create a list of all results and their data

        # iterate each result and retrieve relevant information
        for result in result_list:
            # title
            result_title = result.find(class_='result-title hdrlnk').string

            # link
            result_link = result.find(class_='result-image').get('href')

            # price: -1 means no price available on search page
            result_price_available = result.find(class_='result-meta').find(class_='result-price')
            if result_price_available is None:
                result_price = -1
            else:
                result_price = result_price_available.string

            # location: if statement differentiates between nearby and in the search area
            result_location = result.find(class_='result-meta').find(class_='result-hood')
            if result_location is None:
                result_location = result.find(class_='result-meta').find(class_='nearby').get('title')
            else:
                result_location = result_location.string

            # time
            result_time = result.find(class_='result-info').find(class_='result-date').get('title')

            # postid (craiglist)
            result_id = result.find(class_='result-image').get('data-ids')

            new_entry = SearchEntry(result_title, result_link, result_price, result_location, result_time, result_id,
                                    None, None)

            self.get_info(new_entry)


            self.search_results.append(new_entry)

        self.save_results()

    def get_info(self, entry):
        self.get_html(entry.link, 0)

    # save results
    def save_results(self):
        output = open("results.txt", 'w')
        for entry in self.search_results:
            print(entry.title + "\n    "
                  + str(entry.price) + "\n    "
                  + entry.location + "\n    "
                  + entry.time + "\n    "
                  + entry.link + "\n    ")

        output.close()