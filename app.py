from flask import Flask, render_template, request, jsonify

import os
import json
import requests
import time
from sklearn.externals import joblib

from secrets import creds_hmac,wml_credentials
from utils import *

app = Flask(__name__, static_url_path='')


# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


CURRENT_NEW = 'current_new.json'
CURRENT_TOP = 'current_top.json'

#refresh_COS_data(CURRENT_NEW,'data/current_new.json',creds_hmac)
refresh_COS_data(CURRENT_TOP,'data/current_top.json',creds_hmac)
lda_model = load_wml_model(wml_credentials)
df = score_stories('data/current_top.json','data/scored_top.json',lda_model)

story_list = prep_card_data( source_json = 'data/scored_top.json',threshold=0.05, mode= 'cluster')


@app.route('/')
def root():
    return render_template('index_template.html', stories=story_list)

@app.route('/top') # still need to add
def top():
    return render_template('index_template.html', stories=new_stories)


@app.route('/model/<model_id>')
def modeled_cards(model_id="nmf"):
    return render_template('model_template.html', stories=prep_card_data('data/scored_{}.json'.format(model_id),threshold= 0.05))

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
# refresh_COS_data('scored_nmf_kl.json','data/scored_nmf_kl.json',creds_hmac)
# refresh_COS_data('scored_lda.json','data/scored_lda.json',creds_hmac)
# refresh_COS_data('clustered_stories.json','data/clustered_stories.json',creds_hmac)

# hn = hn_collector()
# top_stories = hn.get_top_stories()
# new_stories = hn.get_new_stories()
# story_list = update_stories()


# @app.route('/')
# def root():
#     return render_template('index_template.html', stories=story_list)



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
