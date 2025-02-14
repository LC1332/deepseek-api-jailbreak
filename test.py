import server
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("SILICONFLOW_API_KEY")
a=server.siliconflow(api_key)

a.send_message("hi")
print(a.get_response())

