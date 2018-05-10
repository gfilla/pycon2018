# Hacker News ML Viewer
## End to end example of building an ML powered application


## Prerequisites

###### Data processing and machine learning

- Jupyter Notebooks - code/data IDE
  - Using [IBM Watson Studio notebooks](www.datascience.ibm.com)for this application for easy scheduling and model deployment
  - Recommend downloading Anaconda for local development, includes notebooks.
- Object storage - data persistence
  - This is a _very_ simple app just using IBM Cloud object storage for managing data
  - This app can easily be upgraded to a NoSQL document store DB like Cloudant

###### Application Development

- Text editor of your choice (I like Atom)
- Python environment capable of running Flask (think Anaconda install will cover this dependency)

###### Deploy to IBM Cloud
If you want to deploy your app to the IBM Cloud, you'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

## 1. Clone this repository

Now you're ready to start working with the app. Clone the repo and change to the directory where the sample app is located.
  ```
git clone https://github.com/gfilla/pycon2018
cd pycon2018

  ```

  Peruse the files in the *pycon2018* directory to familiarize yourself with the contents.

## 2. Run the app locally

Install the dependencies listed in the [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

You can optionally use a [virtual environment](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.
  ```
pip install -r requirements.txt
  ```

Run the app.
  ```
python app.py
  ```

 View your app at: http://localhost:8000

## 3. Review stages of app development

1. Requirements gathering
2. Data Collection
3. Machine Learning - Model training / experimentation
4. Flask application Development
5. Model deployment and management

##### See [these slides](https://github.com/gfilla/pycon2018/blob/master/Workshop%20Slides.pptx) for more details



## 4. Prepare the app for deployment

To deploy to IBM Cloud, it can be helpful to set up a manifest.yml file. One is provided for you with the sample. Take a moment to look at it.

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. In this manifest.yml **random-route: true** generates a random route for your app to prevent your route from colliding with others.  You can replace **random-route: true** with **host: myChosenHostName**, supplying a host name of your choice. [Learn more...](https://console.bluemix.net/docs/manageapps/depapps.html#appmanifest)
 ```
 applications:
 - name: pycon2018
   random-route: true
   memory: 128M
 ```

## 5. Deploy the app

You can use the Cloud Foundry CLI to deploy apps.

Choose your API endpoint
   ```
cf api <API-endpoint>
   ```

Replace the *API-endpoint* in the command with an API endpoint from the following list.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |

Login to your IBM Cloud account

  ```
cf login
  ```

From within the *pycon2018* directory push your app to IBM Cloud
  ```
cf push
  ```

This can take a minute. If there is an error in the deployment process you can use the command `cf logs <Your-App-Name> --recent` to troubleshoot.

When deployment completes you should see a message indicating that your app is running.  View your app at the URL listed in the output of the push command.  You can also issue the
  ```
cf apps
  ```
  command to view your apps status and see the URL.
