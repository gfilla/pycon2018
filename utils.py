import requests
from bs4 import BeautifulSoup
from ibm_botocore.client import Config
import ibm_boto3
import json

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



def refresh_COS_data(file_key ='hn_stories.csv', out_path='data/new_stories.csv'):

    creds_hmac={
      "apikey": "__NBobRme7hbxc51XYbIXDxqp0RIfaTjLy0ttAcxF_GY",
      "cos_hmac_keys": {
        "access_key_id": "e13393fbc8dd4d9fb92b2a9684c1d4a7",
        "secret_access_key": "ba6a5ba31fe616205f834ef9a8d832afc79c84e3246868c4"
      },
      "endpoints": "https://cos-service.bluemix.net/endpoints",
      "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:cloud-object-storage:global:a/f9248c5ce5b260551682838d09c2415e:66a35c59-e0e4-4474-beb1-a026696207e0::",
      "iam_apikey_name": "auto-generated-apikey-e13393fb-c8dd-4d9f-b92b-2a9684c1d4a7",
      "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
      "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/f9248c5ce5b260551682838d09c2415e::serviceid:ServiceId-063bb032-c60f-4bfe-baa4-5a9f884e04b2",
      "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/f9248c5ce5b260551682838d09c2415e:66a35c59-e0e4-4474-beb1-a026696207e0::"
    }

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

def prep_card_data(source_json = 'data/scored_stories.json'):
    with open('data/scored_stories.json') as json_data:
        d = json.load(json_data)
    story_list= d[:500]
    for story in story_list:
        filtered_dict = {k:v for k,v in story.items() if "Topic" in k and v > 0.05} #filter topics for scores in topics
        story['ml_topics'] = filtered_dict
        story['card_class'] = 'element-item ' + ' '.join(list(filtered_dict.keys()))
        try:
            story['id'] = str(story['id'])[:-2]
        except:
            pass
    return(story_list)
