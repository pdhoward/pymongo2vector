import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = os.environ.get("WEAVIATE_PRODUCT_URL")
OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")


client  = weaviate.Client(
  url = WEAVIATE_URL,
  additional_headers={
      "X-OpenAI-Api-Key": OPEN_API_KEY
  }
)

# instruction for the generative module
generateTask = '"Summarize each of the products and provide a price for each"'

result = (
  client.query
  .get("Product", ["name", "price", "description"])
  .with_additional(
    "generate(groupedResult:{ task: " + generateTask + " }) { groupedResult }"
  )
  .with_near_text({
    "concepts": ["drills and drill bits"]
  })
  .with_limit(5)
).do()

print(result)