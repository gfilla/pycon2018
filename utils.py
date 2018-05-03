import requests
from bs4 import BeautifulSoup
from ibm_botocore.client import Config
import ibm_boto3
import json
from secrets import creds_hmac

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



def refresh_COS_data(file_key ='hn_stories.csv', out_path='data/new_stories.csv', creds_hmac = creds_hmac):

    import boto
    import boto.s3.connection
    access_key = creds_hmac["cos_hmac_keys"][ "access_key_id"]   # Change to match your setup
    secret_key = creds_hmac["cos_hmac_keys"][ "secret_access_key"] # Change to match your setup
    bucket = 'pyconproject-donotdelete-pr-hvlammk95c1rrk'      # Change to match your setup

    host = "s3-api.us-geo.objectstorage.softlayer.net"

    conn = boto.connect_s3(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            host = host,
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
            )

    b =conn.get_bucket(bucket)
    key = b.get_key(file_key)
    key.get_contents_to_filename(out_path)

def prep_card_data(source_json = 'data/scored_nmf.json',threshold=0.05):
    with open(source_json) as json_data:
        d = json.load(json_data)
    story_list= d[:500]
    for story in story_list:
        filtered_dict = {k:v for k,v in story.items() if "Topic" in k and v > threshold} #filter topics for scores in topics
        story['ml_topics'] = filtered_dict
        story['card_class'] = 'element-item ' + ' '.join(list(filtered_dict.keys()))
        try:
            story['id'] = str(story['id'])[:-2]
        except:
            pass
    return(story_list)
