from flask import Flask, render_template, request
import requests

app = Flask(__name__)


causes_data = [
    {
        "id": "fossil-fuels",
        "name": "Fossil Fuels",
        "description": "Burning coal, oil, and gas releases CO2.",
        "image": "fossil_fuel.jpeg",
        "detail_image": "fossil_fuel2.jpg",
        "history": "Fossil fuels have powered industries since the industrial revolution.",
        "effects": "Contributes significantly to greenhouse gas emissions and global warming."
    },
    {
        "id": "agriculture",
        "name": "Agriculture",
        "description": "Methane emissions from livestock and nitrous oxide from fertilizers.",
        "image": "agriculture.jpeg",
        "detail_image": "agriculture2.jpg",
        "history": "Modern agriculture practices have increased methane emissions.",
        "effects": "Impacts biodiversity, water resources, and contributes to climate change."
    },
    {
        "id": "deforestation",
        "name": "Deforestation",
        "description": "Deforestation reduces CO2 absorption and increases carbon release.",
        "image": "deforestation.jpg",
        "detail_image": "desforestation2.jpg",
        "history": "Deforestation is driven by agriculture, logging, and urbanization.",
        "effects": "Leads to biodiversity loss, habitat destruction, and increased CO2 emissions."
    },
    {
        "id": "urbanization",
        "name": "Urbanization",
        "description": "Expanding cities lead to deforestation and increased emissions.",
        "image": "urbanization.jpg",
        "detail_image": "urbanization2.jpg",
        "history": "Urbanization transforms rural areas into cities, affecting the environment.",
        "effects": "Increases energy demand, air pollution, and disrupts ecosystems."
    }
]

# OpenWeatherMap API Configuration
API_KEY = "eec9f0249feea8cff9f2e5477562e1e6"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

@app.route('/')
def home():
    # Redirect to causes page
    return render_template('index.html')

@app.route('/causes', methods=['GET', 'POST'])
def causes():
    selected_cause = None
    weather_data = {}
    pollution_data = {}
    location = " "  # Default location

    # Check if a cause is selected
    cause_id = request.args.get('cause_id')
    if cause_id:
        for c in causes_data:
            if c["id"] == cause_id:
                selected_cause = c
                break

    # Handle location input for weather and pollution data
    if request.method == 'POST':
        location = request.form.get('location', '  ')

    # Fetch current weather data
    weather_params = {"q": location, "appid": API_KEY, "units": "imperial"}
    weather_response = requests.get(WEATHER_URL, params=weather_params)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()

    # Fetch air pollution data
    # Requires geographic coordinates, so fetch latitude and longitude from weather data
    if "coord" in weather_data:
        lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]
        pollution_params = {"lat": lat, "lon": lon, "appid": API_KEY}
        pollution_response = requests.get(POLLUTION_URL, params=pollution_params)
        if pollution_response.status_code == 200:
            pollution_data = pollution_response.json()

    return render_template(
        'causes.html',
        causes=causes_data,
        selected_cause=selected_cause,
        weather=weather_data,
        pollution=pollution_data,
        location=location
    )
