# flask_ngrok_example.py
from flask import Flask, request
import requests
from scorer import *
from dotenv import load_dotenv
import os
from helper import extract_text_from_stream

load_dotenv()
API_KEY = os.getenv("API_KEY")
app = Flask(__name__)
THRESHOLD = 13

@app.route("/", methods=["POST"])
def analyze_resume():

    
    webhook_data = request.json
    opportunity_id = webhook_data["data"]["opportunityId"]
    json_data = {
        'links': ["recommended"],
    }

    pdf_metadata = requests.get(f"https://api.lever.co/v1/opportunities/{opportunity_id}/resumes", auth=(API_KEY,""))
    downloaded_pdf = requests.get(pdf_metadata.json()["data"][0]["file"]["downloadUrl"], auth=(API_KEY, ""),  stream=True)

    text = extract_text_from_stream(downloaded_pdf.content)

    is_resume_pass = score_resume(text, THRESHOLD)

    if not (is_resume_pass):
        json_data["links"][0]="not recommended"

    response = requests.post(f"https://api.lever.co/v1/opportunities/{opportunity_id}/addLinks", json=json_data, auth=(API_KEY, ''))

    return "action completed"



    
  



    

if __name__ == '__main__':
    app.run(debug=True)  # If address is in use, may need to terminate other sessions:
               # Runtime > Manage Sessions > Terminate Other Sessions