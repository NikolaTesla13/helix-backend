from src.app import app
from dotenv import load_dotenv
import os

load_dotenv()

is_debug = bool(os.getenv("DEV"))

port = 4000
if not is_debug:
    port = 80

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=is_debug)
