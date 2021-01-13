from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenz123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# ??? Don't get why this is needed, nothing in lesson about this
RESPONSES_KEY = "responses"



@app.route('/')
def homepage():
    return render_template('survey_start.html', survey = satisfaction_survey)


@app.route('/start', methods=["POST"])
def start():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:id>')
def find_question(id):
    question = satisfaction_survey.questions
    responses = session.get(RESPONSES_KEY)
    if (len(question) <= id):
        return redirect("/thankyou")
    elif (len(responses) != id):
        flash('In life the correct order is important', 'error')
        return redirect (f"/questions/{len(responses)}")
    else:
        return render_template('questions.html', question=question[id])

@app.route('/next', methods =["POST"])
def next_question():
    answer = request.form['answer']
    
   #??? find the RESPONSE_KEY confusing
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    id_num = len(responses)
    return redirect(f"/questions/{id_num}")

@app.route('/thankyou')
def thank_you_page():
    responses = session.get(RESPONSES_KEY)
    return render_template('thankyou.html', response = responses)