import requests
from bs4 import BeautifulSoup


class hn_collector():


    def __init__(self):
        self.API_BASE = 'https://hacker-news.firebaseio.com/v0/'
        self.TOP ='topstories.json'
        self.NEW ='newstories.json'
        self.ITEM ='item/'
        self.HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def get_top_stories(self):
        return(eval(requests.get(self.API_BASE + self.TOP).content))

    def get_new_stories(self):
        return(eval(requests.get(self.API_BASE + self.NEW).content))

    def get_story(self, story_id):
        return(eval(requests.get(self.API_BASE + self.ITEM + str(story_id)+".json").content))

    def get_text(self, story_url):

        try:
            page = requests.get(story_url, headers=self.HEADERS)
            soup = BeautifulSoup(page.content,'lxml')
            s= ' '.join([p.text for p in soup.find_all('p')])
            return(s)
        except:
            return('{} FAILED'.format(story_url))
        
