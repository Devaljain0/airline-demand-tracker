# ✈️ Airline Demand Tracker

A web application that scrapes flight data using SerpAPI and generates AI-powered travel market insights using Ollama. Users can search for flights between two cities on a specific date, view filtered flight data, and download a CSV report with pricing and airline details.

---

## 📌 Features

- 🔎 Search flights using **city/airport code**, date, and destination.
- 📊 Display flight details: **Airline, Price, Travel Class, Date**.
- 🧠 Generate **market insights** using a local AI model (Ollama).
- 📁 Save scraped flight data to `data/routes.csv`.
- 🔍 Apply filters: **Travel Class**, **Max Price**, **Airline**.
- ✅ Lightweight Flask backend with Bootstrap frontend.

---

## 🛠 Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, Bootstrap 5, Vanilla JS
- **Scraping API:** [SerpAPI](https://serpapi.com/)
- **AI Model:** [Ollama](https://ollama.com/) with LLaMA2
- **CSV Handling:** Python `csv` module

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/airline-demand-tracker.git
cd airline-demand-tracker
