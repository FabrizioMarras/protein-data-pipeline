from flask import Flask, render_template
import os
from dotenv import load_dotenv
from src.routes.search import search_blueprint

load_dotenv()

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.register_blueprint(search_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

server_port = os.getenv('SERVER_PORT')
# server_port = 6000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
