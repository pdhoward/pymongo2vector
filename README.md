## MONGO TO WEAVIATE

### set up server

Note: This uses pymongo. If an error is encountered related to SSL, your certificate on your machine may be expired. To resolve

1. Download https://letsencrypt.org/certs/lets-encrypt-r3.pem
2. rename the file .pem to .cer
3. double click. In the dialogue box, click on install

And then rerun your app

### Loading Data from GitHub Repo using Python

import requests
url = 'https://raw.githubusercontent.com/weaviate/weaviate-examples/main/jeopardy_small_dataset/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

### RESEARCH
https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

https://kb.objectrocket.com/mongo-db/how-to-access-and-parse-mongodb-documents-in-python-364


