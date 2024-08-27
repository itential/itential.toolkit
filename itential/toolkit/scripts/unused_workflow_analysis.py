import sys, getopt
import pymongo
import getpass
from datetime import datetime
from dateutil.relativedelta import relativedelta

def connect_to_mongo(uri, database_name, username=None, password=None):
    try:
        client = pymongo.MongoClient(uri, username=username, password=password)
        db = client[database_name]
        return db

    except ConnectionError as ce:
        print(f"Connection error: {ce}")
    except AuthenticationError as ae:
        print(f"Authentication error: {ae}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

def query_workflow_names(db):
    try:
        collection = db['workflows']
        results = collection.distinct('name')
        return results

    except pymongo.Exception as e:
        print(f"An error occurred while querying the 'workflows' collection: {e}")
        return []

def query_last_run(db, worklfow_name):
    try:
        collection = db['jobs']
        result = collection.find({'name': worklfow_name}).sort('last_updated', -1)
        try:
            date = result[0]['last_updated']
        except Exception as e:
            return 0
        return date

    except Exception as e:
        print(f"An error occurred while querying the 'jobs' collection: {e}")
        return 0

def within_x_days_ago(date_time_obj, num_of_days):
    try:
        now = datetime.now()
        x_days_ago = now - relativedelta(days=num_of_days)
        
        # Check if the given datetime is between X days ago and now
        return x_days_ago <= date_time_obj <= now

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # Setting default variables
    mongo_uri = 'mongodb://localhost:27017/'
    db_name = 'itential'
    username = 'itential'
    password = ''
    days = 180
    display_never_run = False
    never_run = []
    workflows = []

    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "hd:u:D:u:"

    # Long options
    long_options = ["HELP", "DAYS=", "URI=", "DB=", "USERNAME="]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--HELP"):
                print ("")
                print ("Usage: python3 unused_workflow_analysis.py [-h] [-d DAYS] [-U URI] [-D DB] [-u USERNAME]")
                print ("Options and Arguments:")
                print ("-h               Display help menu")
                print ("-d DAYS          Number of days to search for the last run of the workflow. Default to 180")
                print ("-U URI           Mongo URI. Defaults to 'mongodb://localhost:27017/'")
                print ("-D DB            Itential DB name. Defaults to 'itential'")
                print ("-u USERNAME      Mongo authentication username.")
                print ("")
                print ("example:")
                print ("python3 unused_workflow_analysis.py -d 6 -U mongodb://localhost:27017/ -D itential")
                print ("")
                print ("")
                quit()

            elif currentArgument in ("-d", "--DAYS"):
                days = currentValue
                
            elif currentArgument in ("-U", "--URI"):
                mongo_uri = currentValue
                
            elif currentArgument in ("-D", "--DB"):
                db_name = currentValue
                
            elif currentArgument in ("-u", "--USERNAME"):
                username = currentValue
                

    except getopt.error as err:
        print (str(err))

    try:
        password = getpass.getpass()
    except Exception as error:
        print('ERROR', error)

    # Connect to MongoDB
    db = connect_to_mongo(mongo_uri, db_name, username, password)

    if db.list_collection_names():
        # Get all workflow names 
        workflow_names = query_workflow_names(db)
        for workflow in workflow_names:
            # Get the last run datetime of the workflow
            last_run = query_last_run(db, workflow)
            if isinstance(last_run, datetime):
                if not within_x_days_ago(last_run, int(days)):
                    # The workflow has not been run within the last X days
                    workflows.append(workflow)
            else:
                never_run.append(workflow)

    
    print(f"Workflows that have not run in the last {days} days:")
    for workflow in workflows:
        print(f"{workflow}")
    for workflow in never_run:
        print(f"{workflow}")
