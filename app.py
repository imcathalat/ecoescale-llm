from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())   

import os
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY não carregada!"

from application import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5053)