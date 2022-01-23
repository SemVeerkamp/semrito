from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.models import *
from website import db

import requests
import json
from datetime import datetime

from website.get_startlist import get_startlist
from website.get_result import get_result
from website.tournament import year, tag

views = Blueprint('views', __name__)

startlist, starttimes = get_startlist(year, tag)
results, podium_pictures = get_result(year, tag)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    time_now = datetime.now()
    if request.method == 'POST':
        prediction = request.form.getlist("prediction")
        user = current_user
        event = str(prediction[0])
        if len(prediction) < 4:
            flash(
                'Je hebt niet het goede aantal vakjes geselecteerd. Selecteer de afstand (bovenste veld) en je drie schaatsers en probeer het opnieuw',
                category='error')
        elif len(prediction[0]) < 9:
            flash("Selecteer eerst de startlist_afstand (en je drie rijders) voordat je je voorspelling opslaat",
                  category='error')
        elif prediction[0][9] != "_":
            flash("Selecteer eerst de startlist_afstand (en je drie rijders) voordat je je voorspelling opslaat",
                  category='error')
        else:
            a = []
            for voorspelling in user.predictions:
                a.append(voorspelling.event)
            if event in a:
                flash(
                    "Voor deze afstand heb je al een voorspelling ingevuld. Als je je voorspelling wilt veranderen verwijder dan eerste de oude voorspelling",
                    category="error")
            else:
                event = str(prediction[0])
                rider_one = str(prediction[1])
                rider_two = str(prediction[2])
                rider_three = str(prediction[3])

                new_prediction = Prediction(
                    event=event,
                    rider_one=rider_one,
                    rider_two=rider_two,
                    rider_three=rider_three,
                    user_name=current_user.name
                )
                db.session.add(new_prediction)
                db.session.commit()
                flash('Voorspelling toegevoegd', category='succes')

    return render_template("home.html",
                           startlist=startlist,
                           starttimes=starttimes,
                           user=current_user,
                           time_now=time_now
                           )


@views.route('/resultaten', methods=['GET', 'POST'])
@login_required
def uitslagen():
    return render_template("uitslagen.html",
                           results=results,
                           podium_pictures=podium_pictures,
                           user=current_user
                           )


@views.route('/voorspellingen', methods=['GET', 'POST'])
def voorspellingen():
    time_now = datetime.now()
    predictions = Prediction.query.order_by(Prediction.event).all()
    return render_template("voorspellingen.html",
                           startlist=startlist,
                           starttimes=starttimes,
                           time_now=time_now,
                           user=current_user,
                           predictions=predictions
                           )


@views.route('/stand', methods=['GET', 'POST'])
def stand():
    scores = {}
    users = User.query.order_by(User.name).all()
    for user in users:
        scores[user.name] = 0
    predictions = Prediction.query.order_by(Prediction.event).all()
    for prediction in predictions:
        for event in results:
            if prediction.event == event:
                if prediction.rider_one == results[event][0] or prediction.rider_two == results[event][0] or prediction.rider_three == \
                        results[event][0]:
                    scores[prediction.user_name] += 4
                if prediction.rider_one == results[event][1] or prediction.rider_two == results[event][1] or prediction.rider_three == \
                        results[event][1]:
                    scores[prediction.user_name] += 2
                if prediction.rider_one == results[event][1] or prediction.rider_two == results[event][1] or prediction.rider_three == \
                        results[event][1]:
                    scores[prediction.user_name] += 1
    return render_template("stand.html",
                           user=current_user,
                           scores=scores
                           )


@views.route('/delete-prediction', methods=['POST'])
def delete_prediction():
    prediction = json.loads(request.data)
    predictionId = prediction['predictionId']
    prediction = Prediction.query.get(predictionId)
    if prediction:
        if prediction.user_name == current_user.name:
            db.session.delete(prediction)
            db.session.commit()

    return jsonify({})

@views.route('/refresh_prediction', methods=['POST'])
def refresh_predictions():
    if request.method == ["POST"]:
        startlist, starttimes = get_startlist(year, tag)
        results, podium_pictures = get_result(year, tag)
    return render_template("refresh_prediction.html")
