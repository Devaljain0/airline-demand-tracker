from flask import Flask, render_template, request
import csv
import os
from dotenv import load_dotenv
import requests
import subprocess
import json

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

app = Flask(__name__)

def scrape_google_flights(origin, destination, date):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": date,
        "type": "2",
        "api_key": API_KEY
    }
    res = requests.get(url, params=params)
    data = res.json()

    results = []
    try:
        flights_data = data.get("best_flights", []) + data.get("other_flights", [])
        for item in flights_data:
            first_flight = item.get("flights", [])[0]  # Take first leg
            airline = first_flight.get("airline")
            price = item.get("price")
            travel_class = first_flight.get("travel_class")
            results.append({
                "origin": origin,
                "destination": destination,
                "price": price,
                "date": date,
                "airline": airline,
                "travel_class":travel_class
            })
        print("PARSED RESULTS:",results)
    except Exception as e:
        print("Error while parsing SerpAPI response:", e)
    return results

def save_to_csv(rows, filename="data/routes.csv"):
    os.makedirs("data", exist_ok=True)
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["origin", "destination", "price", "date", "airline","travel_class"])
        writer.writeheader()
        for row in rows:
            print("Writing row to CSV:", row)
            writer.writerow(row)


def analyze_with_ollama(data):
    prompt = f"""
    You are a travel market analyst. Given the flight data below, extract:
    - The most popular routes
    - Notable price trends
    - High demand dates or routes
    Based on this insights suggest the dates and routes that would be great for users.

    Data: {json.dumps(data)}
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "llama2"],
            input=prompt.encode('utf-8'),
            capture_output=True
        )
       
        return result.stdout.decode('utf-8')
    except Exception as e:
        return f"Error running Ollama: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    flights = []
    insights = ""
    if request.method == 'POST':
        origin = request.form['origin'].strip().upper()
        destination = request.form['destination'].strip().upper()
        date = request.form['date'].strip()
        flights = scrape_google_flights(origin, destination, date)
        save_to_csv(flights)
        if flights:
            insights = analyze_with_ollama(flights)
    else:
        try:
            with open('data/routes.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                flights = list(reader)
        except FileNotFoundError:
            flights = []
    return render_template('index.html', flights=flights, insights=insights)

if __name__ == '__main__':
    app.run(debug=True)
