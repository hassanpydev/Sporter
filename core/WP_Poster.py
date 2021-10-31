import requests
from requests.auth import HTTPBasicAuth
import json
import base64

user = "hassan"
password = "CleanPython059"


# credentials = user+":" +password
# token = base64.b64encode(credentials.encode())
# header = {'Authorization': 'Basic ' + token.decode('utf-8')}
def CreatePost(title, content, date):
    url = "http://23.88.48.121/wp-json/wp/v2/posts"
    post = {
        "title": title,
        "status": "publish",
        "content": f"{content}",
        "categories": 2,
        "date": date,
    }
    response = requests.post(url, auth=HTTPBasicAuth(user, password), json=post)
    print(response.status_code)
    if response.status_code == 201:
        print("Post Published Successfully")
    else:
        print(response.text)
