from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

from flask import render_template
from utils import hn_collector, refresh_COS_data, prep_card_data
import requests


refresh_COS_data('scored_nmf.json','data/scored_nmf.json')
refresh_COS_data('scored_nmf_kl.json','data/scored_nmf_kl.json')
refresh_COS_data('scored_lda.json','data/scored_lda.json')

story_list = prep_card_data()


@app.route('/')
def root():
    return render_template('index_template.html', stories=story_list)

@app.route('/model/<model_id>')
def modeled_cards(model_id="nmf"):
    return render_template('index_template.html', stories=prep_card_data('data/scored_{}.json'.format(model_id)))

@app.route('/story/<story_id>')
def story(story_id=None):

    hn = hn_collector()
    story = hn.get_story(story_id)

    if story.get('url') is None:
        return render_template('post.html', story_id=hn.get_story(story_id))
    else:
        return render_template('story.html', story_id=hn.get_story(story_id))

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */


# hn = hn_collector()
# stories = hn.get_new_stories()
# story_list = []
# id_to_url = {}
# for story in stories[:50]:
#     try:
#         s = hn.get_story(story)
#         s['kids'] = str(s.get('kids',None))
#         story_list.append(s)
#         #id_to_url[str(s['id'])] = s['url']
#     except:
#         pass
#



    #if 'VCAP_SERVICES' in os.environ:
    #     vcap = json.loads(os.getenv('VCAP_SERVICES'))
    #     print('Found VCAP_SERVICES')
    #     if 'cloudantNoSQLDB' in vcap:
    #         creds = vcap['cloudantNoSQLDB'][0]['credentials']
    #         user = creds['username']
    #         password = creds['password']
    #         url = 'https://' + creds['host']
    #         client = Cloudant(user, password, url=url, connect=True)
    #         db = client.create_database(db_name, throw_on_exists=False)
    # elif os.path.isfile('vcap-local.json'):
    #     with open('vcap-local.json') as f:
    #         vcap = json.load(f)
    #         print('Found local VCAP_SERVICES')
    #         creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
    #         user = creds['username']
    #         password = creds['password']
    #         url = 'https://' + creds['host']
    #         client = Cloudant(user, password, url=url, connect=True)
    #         db = client.create_database(db_name, throw_on_exists=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
