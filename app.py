##  Importing all the dependencies

from flask import Flask, render_template, request, jsonify
import os
import json
import requests
import time
from sklearn.externals import joblib
from secrets import creds_hmac,wml_credentials  # my secret credentials for object storage and watson machine learning
from utils import *


## instantiate Flask app object
app = Flask(__name__, static_url_path='')


# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

# names of json sources for story data that will be updated when app is started, and model path
DATA_DIR = 'data/'
CURRENT_NEW = 'current_new.json'
CURRENT_TOP = 'current_top.json'
SCORED_NEW = 'scored_new.json'
SCORED_TOP = 'scored_top.json'
MODEL_PATH = 'models/svm.pkl'

# currently only pulling Top stories for classification but this can easily be expanded using same method as Top stories
#refresh_COS_data(CURRENT_NEW,'data/current_new.json',creds_hmac)
refresh_COS_data(CURRENT_TOP,'data/current_top.json',creds_hmac)

# score_stories() takes in new "top stories" from HN, scores the stories with the model and saves a new version of json. returns a scored data df but is not used currently
top_df = score_stories(in_path= DATA_DIR+ CURRENT_TOP, out_path = DATA_DIR+ SCORED_TOP,model_path = MODEL_PATH)
new_df = score_stories(in_path= DATA_DIR+ CURRENT_NEW, out_path = DATA_DIR+ SCORED_NEW,model_path =  MODEL_PATH)

# prep_card_data() takes the newly scored data and prepares it to pass to our template in the code below.  returns list of json story objects
top_list = prep_card_data( source_json = DATA_DIR+ SCORED_TOP, threshold=0.05, mode = 'cluster')
new_list = prep_card_data( source_json = DATA_DIR+ SCORED_NEW ,threshold=0.05, mode = 'cluster')

#lda_model = load_wml_model(wml_credentials)  # if using model from Watson Machine Learning

# main landing page of flask app - we pass story_list to the template found in templates/index_template.html
@app.route('/')
def root():
    return render_template('index_template.html', stories=top_list)

@app.route('/new') # still need to add
def top():
    return render_template('index_template.html', stories=story_list)


@app.route('/model/<model_id>')
def modeled_cards(model_id="nmf"):
    return render_template('model_template.html', stories=prep_card_data('data/scored_{}.json'.format(model_id),threshold= 0.05))

@app.route('/story/<story_id>')
def story(story_id=None):

    hn = hn_collector()
    story = hn.get_story(story_id)

    if story.get('url') is None:
        return render_template('post.html', story_id=story)
    else:
        return render_template('story.html', story_id=story)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
