import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = os.environ.get("WEAVIATE_PRODUCT_URL")
OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")
print(OPEN_API_KEY)
print(type(OPEN_API_KEY))

client  = weaviate.Client(
  url = WEAVIATE_URL,
  additional_headers={
      "X-OpenAI-Api-Key": OPEN_API_KEY
  }
)

# instruction for the generative module
generateTask = '"Write a Facebook ad for each product"'

result = (
  client.query
  .get("Product", ["name", "price", "description"])
  .with_additional(
    "generate(groupedResult:{ task: " + generateTask + " }) { groupedResult }"
  )
  .with_near_text({
    "concepts": ["hammers"]
  })
  .with_limit(10)
).do()

print(result)