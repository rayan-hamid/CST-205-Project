from flask import Flask, render_template, redirect, request
import random
#API STUFF
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired
import requests

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
app.config['SECRET_KEY'] = 'csumb-otter'
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

@app.route('/effects')
def effects():
    return render_template('effects.html')

@app.route('/carbon')
def carbon():
    return render_template('carbon.html')


@app.route('/solutions')
def solutions():
    main_icon = 'main_icon'
    bike_icon = 'bike_icon'
    ev_icon = 'ev_icon'
    food_icon = 'food_icon'
    fruits_icon = 'fruits_icon'
    house_icon = 'house_icon'
    rrr_icon = 'rrr_icon'
    solar_icon = 'solar_icon'
    travel_icon = 'travel_icon'
    return render_template('solutions.html', 
                           main_icon=main_icon, 
                           bike_icon=bike_icon, 
                           ev_icon=ev_icon, 
                           food_icon=food_icon, 
                           fruits_icon=fruits_icon, 
                           house_icon=house_icon, 
                           rrr_icon=rrr_icon, 
                           solar_icon=solar_icon, 
                           travel_icon=travel_icon)


@app.route('/resources')
def resources():
    return render_template('resources.html')

# QuizForm Definition
class QuizForm(FlaskForm):
    question_1 = RadioField('What is the main cause of climate change?', choices=[
        ('Deforestation', 'Deforestation'),
        ('Carbon emissions', 'Carbon emissions'),
        ('Recycling', 'Recycling'),
        ('Solar power', 'Solar power')
    ], validators=[InputRequired()])

    question_2 = RadioField('What is the greenhouse effect?', choices=[
        ('A way to grow plants', 'A way to grow plants'),
        ('Warming of Earth due to trapped gases', 'Warming of Earth due to trapped gases'),
        ('A type of pollution', 'A type of pollution'),
        ('None of the above', 'None of the above')
    ], validators=[InputRequired()])

    question_3 = RadioField('What can help reduce carbon emissions?', choices=[
        ('Driving a car', 'Driving a car'),
        ('Using public transportation', 'Using public transportation'),
        ('Using more plastic', 'Using more plastic'),
        ('Burning fossil fuels', 'Burning fossil fuels')
    ], validators=[InputRequired()])

    question_4 = RadioField('Recycling alone is enough to solve the climate crisis.', choices=[
        ('True', 'True'),
        ('False', 'False')
    ], validators=[InputRequired()])

    question_5 = RadioField('Which of the following is a sustainable way to reduce waste?', choices=[
        ('Throwing everything in the trash', 'Throwing everything in the trash'),
        ('Composting food scraps', 'Composting food scraps'),
        ('Burning trash to reduce volume', 'Burning trash to reduce volume'),
        ('Buying more plastic products', 'Buying more plastic products')
    ], validators=[InputRequired()])

    submit = SubmitField('Submit')

@app.route('/test-your-knowledge', methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        user_responses = {
            'question_1': form.question_1.data,
            'question_2': form.question_2.data,
            'question_3': form.question_3.data,
            'question_4': form.question_4.data,
            'question_5': form.question_5.data
        }
        responses.append(user_responses)
        return redirect('/submit')
    return render_template('test_your_knowledge.html', form=form)

@app.route('/submit')
def results():
    answers = [
        'Carbon emissions', 
        'Warming of Earth due to trapped gases', 
        'Using public transportation', 
        'False', 
        'Composting food scraps'
    ]
    
    #GET THE MOST RECENT SUBMISSION 
    user_responses = responses[-1]
    score = 0

    if user_responses.get('question_1') == answers[0]:
        score += 1

    if user_responses.get('question_2') == answers[1]:
        score += 1

    if user_responses.get('question_3') == answers[2]:
        score += 1

    if user_responses.get('question_4') == answers[3]:
        score += 1

    if user_responses.get('question_5') == answers[4]:
        score += 1
        
    return render_template('submit.html', score=score)
    

# cd Desktop/cst205
# source cst205env/bin/activate
# cd project_solutions_page
# flask --app solutions --debug run

#must enter /solutions to see webpage 
