## MONGO TO WEAVIATE

### set up server

Note: This uses pymongo. If an error is encountered related to SSL, your certificate on your machine may be expired. To resolve

1. Download https://letsencrypt.org/certs/lets-encrypt-r3.pem
2. rename the file .pem to .cer
3. double click. In the dialogue box, click on install

In order to run the app 

1. set up keys for weaviate and openai in the .env
2. create the schema which describes the shape of your data based on instructions (see below)
3. run the app

### Loading Data from GitHub Repo using Python

import requests
url = 'https://raw.githubusercontent.com/weaviate/weaviate-examples/main/jeopardy_small_dataset/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

### TEMPORARY SANDBOX FILES CREATED ON WEAVIATE


https://product.weaviate.network/v1/objects

https://product.weaviate.network/v1/schema





