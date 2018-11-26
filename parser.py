import json
import sys


# Function to parse games from Google Play
def parser(url, patt1, patt2):
    import requests
    import re

    out = {}

    try:
        response = requests.get(url, timeout=20)     # try to send HTTP GET message
        if response.status_code == 200:     # proceed in case of success

            collections = re.findall(patt1,
                                     response.text)  # collections of games in format [collection_url, collection_name]
            if collections:
                for c in collections:
                    collection_url = 'https://play.google.com' + c[0]
                    collection_name = c[1]

                    try:    # try to send HTTP GET message
                        response = requests.get(collection_url, timeout=20)
                        if response.status_code == 200:     # proceed in case of success
                            items = re.findall(patt2, response.text)    # list of games inside collection

                            if items is None:
                                items = ["No games was found inside"]
                            else:
                                out[collection_name] = items    # add game collection name (key) and list of games
                                # inside collection (value) to the "out" dictionary

                        else:
                            print(response.status_code)

                    except requests.exceptions.RequestException as error:
                        print error
                        sys.exit(1)
            else:
                print('No collections of games found')

        else:
            print(response.status_code)

    except requests.exceptions.RequestException as error:
        print error
        sys.exit(1)

    return out


# Function to Post out data to the HTTP server
def post_to_server(server, data_to_post):
    import requests
    r = requests.post(server, json=data_to_post)     # httpbin.org is a public HTTP server
    print "Data posted on the server", server, " Status code: ", r.status_code


# Define website to parse and regex patterns
website = 'https://play.google.com/store/apps/category/GAME?hl=en'
pattern1 = r'(/store/apps/collection/recommended_for_you_.*?)">(.*?)</a>'   # pattern to search for collections of games
pattern2 = r'"\/store\/apps\/details\?id=com\..*?" title="(.*?)"'   # pattern to search for games inside collection

# Get out_data in a format {collection_name: [list of games]}
data = parser(website, pattern1, pattern2)
print data

# Write out data to the file
with open('out_data.json', 'w') as outfile:
    json.dump(data, outfile)
    print('Data written to the  file. Check out_data.json')

# Post out data to the HTTP server
server = 'http://httpbin.org/post'
data_to_post = data
post_to_server(server, data_to_post)
