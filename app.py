from flask import Flask, render_template, request
from flows import analyze_influencer
from prefect import logging
from logging import INFO
from dotenv import load_dotenv

# Configure Prefect logging to show in console
logging.get_logger().setLevel(INFO)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        print(f"Submitted name: {name}")
        # Uncomment to run the flow
        analyze_influencer(name)
        return render_template('index.html', message="Analysis started!")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 