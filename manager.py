import os
from app import create_app


app = create_app(os.getenv('FLASKENV') or 'default')

# run_config = {'develop': {'debug': True, 'host': '0.0.0.0', 'port': 8081}}
if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
