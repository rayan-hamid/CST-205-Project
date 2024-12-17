from flask import Flask, render_template
import random
#API STUFF
import openmeteo_requests
from openmeteo_sdk.Variable import Variable

om = openmeteo_requests.Client()
params = {
    "latitude": 36.614906,
    "longitude": -121.842628,
    "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
    "current": ["temperature_2m", "relative_humidity_2m"]
}

responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")

app = Flask(__name__)
quotes = ('"The world will not be destroyed by those who do evil, but by those who watch them without doing anything" - Albert Einstein',
          '"We are the first generation to feel the impact of climate change and the last generation that can do something about it" - Barack Obama',
          '"As consumers we have so much power to change the world by just being careful in what we buy" - Emma Watson',
          '"Climate change is the greatest threat to our existence in our short history on this planet. Nobody is going to buy their way out of its effects" - Mark Ruffalo',
          '“It’s important for me to have hope because that’s my job as a parent, to have hope, for my kids, that we’re not going to leave them in a world that’s in shambles, that’s a chaotic place, that’s a dangerous place.” - James Cameron',
          '“I’ve starred in a lot of science fiction movies and, let me tell you something, climate change is not science fiction. This is a battle in the real world, it is impacting us right now.” - Arnold Schwarzenegger',
          '“Let us double down on solar energy, let us be more energy-efficient, let us weatherize our homes. We can build a better, healthier economy based on good-paying, clean energy jobs.” - Ian Somerhalder',
          '"We don’t have time to sit on our hands as our planet burns. For young people, climate change is bigger than election or re-election. It’s life or death.” - Alexandria Ocasio-Cortez')
@app.route('/')
def home():
    # Current values
    current = response.Current()
    current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
    current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))
    CurrentFarenheit = round(9/5*current_temperature_2m.Value()+32,2)
    return render_template("index.html",quote = quotes[random.randint(0,len(quotes)-1)],temperature = CurrentFarenheit)

@app.route('/causes')
def causes():
    return render_template('causes.html')

@app.route('/effects')
def effects():
    return render_template('effects.html')

@app.route('/solutions')
def solutions():
    return render_template('solutions.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')