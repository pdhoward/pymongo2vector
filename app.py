"""Load html from files, clean up, split, ingest into Weaviate."""
import os
from pymongo import MongoClient
from pathlib import Path
import requests
import weaviate
import pprint
import json
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = os.environ.get("WEAVIATE_URL")
OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")
MONGO_DB=os.environ.get("DB")

client = MongoClient(MONGO_DB)
db = client['openai']
collection = db['product']

"""
ids = []
for docs in collection.find():
    ids += [docs["_id"]]
print("Total number of products are ", len(ids))
"""
# Instantiate Weaviate client
weaveClient = weaviate.Client(
    url="https://product.weaviate.network",  # Replace this with your WCS or Docker endpoint (use HTTP, not HTTPS for local addresses)
    additional_headers={
        "X-OpenAI-Api-Key": OPEN_API_KEY  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key" 
    }
)
# Delete existing schema (if necessary - THIS WILL ALSO DELETE ALL OF YOUR DATA)
weaveClient.schema.delete_all()

# Fetch & inspect schema (should be empty)
schema = weaveClient.schema.get()
print(json.dumps(schema, indent=4))

# define the schema for Product Catalog

className = "Product"

classObj = {  
    "class": "Product",
    "description": "A product catalog",
    "vectorize": "text2vec-openai",
    "properties": [
      { "dataType": ["string"],
        "description": "Id of the product object from Mongo DB",
        "name": "objectId"
      },
      { "dataType": ["string"],
        "description": "url for the product",
        "name": "url"
      },
      { "dataType": ["string"],
        "description": "date the information was retrieved from website",
        "name": "crawledAt"
      },
      { "dataType": ["string"],
        "description": "website where product is hosted",
        "name": "source"
      },
      { "dataType": ["text"],
        "description": "Product long name",
        "name": "name"
      },
      { "dataType": ["string[]"],
        "description": "string of endpoints for product images",
        "name": "images"
      },
      { "dataType": ["text"],
        "description": "description of the product",
        "name": "description"
      },
      { "dataType": ["string"],
        "description": "Brand name of the product",
        "name": "brand"
      },
      { "dataType": ["string"],
        "description": "SKU id for the product",
        "name": "skuId"
      },
      { "dataType": ["text"],
        "description": "Retail price for the product",
        "name": "price"
      },
      { "dataType": ["text"],
        "description": "Indicator of current product availability",
        "name": "in_stock"
      },
      { "dataType": ["text"],
        "description": "Currency of the listed price",
        "name": "currency"
      },
      { "dataType": ["text"],
        "description": "The color of the product if relevant",
        "name": "color"
      },
      { "dataType": ["text"],
        "description": "URL path segment",
        "name": "breadcrumbs"
      },
      { "dataType": ["text"],
        "description": "Average of the total product reviews",
        "name": "averageRating"
      },
      { "dataType": ["text"],
        "description": "A detailed review of the product and associated considerations",
        "name": "overview"
      },
      { "dataType": ["text"],
        "description": "The set of specifications for the product, such as warranties, size, tolerances etc",
        "name": "specifications"
      },
      { "dataType": ["text"],
        "description": "Unique id of the product",
        "name": "productId"
      },
    ]
   
}

weaveClient.schema.create_class(classObj)

"""

for docs["images] and docs["overview"]

const cleanString = (str) => {
  if ((str === null) || (str === "")) return false
  str = str.toString()
  let regex = /<a.*?<\/a>/ig
  return str.replaceAll(regex, "")
}

const convertArray = (str) => {
  if ((str === null) || (str === "")) return []
  return str.split('~')
}

"""

# ===== import data ===== 

# Configure a batch process
with weaveClient.batch as batch:
    batch.batch_size=50
    # Batch import all Questions
    ids=[]
    for docs in collection.find():
        ids += [docs["_id"]]        
        properties = {
          "objectId": docs["_id"],
          "url": docs["url"],
          "crawledAt": docs["crawled_at"],
          "source": docs["source"],
          "name": docs["name"],
          "images": docs["images"],
          "description": docs["description"],
          "brand": docs["brand"],
          "skuId": docs["sku_id"],
          "price": docs["price"],
          "inStock": docs["in_stock"],
          "currency": docs["currency"],
          "color": docs["color"],
          "breadcrumbs": docs["breadcrumbs"],
          "averageRating": docs["avg_rating"],
          "totalReviews": docs["total_reviews"],
          "overview": docs["overview"],
          "specifications": docs["specifications"],
          "productId": docs["id"]
        }

        weaveClient.batch.add_data_object(properties, "Product")

print("Total number of products processed was ", len(ids))
