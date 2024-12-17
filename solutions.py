from flask import Flask , render_template, request, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

@app.route('/solutions')
def home():
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

responses = []

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