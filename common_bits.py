import sys
import requests

base_url = 'https://firewall.com:0000/api/objects'

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic ENCRYPTED_TOKEN'
}


def removeNestedLists(l, final_list):
    """Flatten nested list."""
    for i in l:
        if type(i) == list:
            removeNestedLists(i, final_list)
        else:
            final_list.append(i)


def get_request(url, headers, payload):
    """Returns API get request response."""
    try:
        response = requests.request('GET', url, headers=headers, data = payload)
    except requests.exceptions.RequestException as cerror:
        print('Error processing request', cerror)
        sys.exit(1)

    return response
