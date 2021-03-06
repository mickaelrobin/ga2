"""A simple example of how to access the Google Analytics API."""
import pprint
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='7daysAgo',
            end_date='today',
            metrics='ga:sessions',
		dimensions='ga:country,ga:source').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
#        print 'View (Profile):', results.get('profileInfo').get('profileName')
#        print 'Total Sessions:', results.get('rows')[0]
#	encoded_results = results.encode("utf-8")
	pprint.pprint(results)
#	pprint.pprint(encoded_results['rows'])
#	print(results['rows'])
#	pprint.pprint(results.get('rows'))
	rows = results['rows']

# geting the headers dynamically from GA response
	metrics = results['query']['metrics']
	print(metrics)

	dimensions1 = results['query']['dimensions']
	print(dimensions1)

	colheader =results['columnHeaders'][0]['name']
	print(colheader)

	GAcolheaders = results['columnHeaders']
	cols = []
	for header in GAcolheaders:
		cols.append(header['name'].replace("ga:", ""))
#	print('dynamic cols are')
#	cols.replace("ga:", "")
	print(cols)


	############################ writing into a csv file ###########################
	# inspired from https://www.geeksforgeeks.org/working-csv-files-python/
	# importing the csv module 
	import csv 

	# field names 
#	fields = ['country', 'source', 'sessions']
	fields = cols
	# name of csv file 
	filename = "GAexport2.csv"

 
# writing to csv file 
	with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
		 csvwriter = csv.writer(csvfile) 
      
    # writing the fields 
		 csvwriter.writerow(fields) 
      
    # writing the data rows 
		 csvwriter.writerows(rows)


    else:
        print 'No results found'






def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = '/home/mickael_robin/mickael/GA-API/client_secrets.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    profile_id = get_first_profile_id(service)
    print_results(get_results(service, profile_id))


if __name__ == '__main__':
    main()
