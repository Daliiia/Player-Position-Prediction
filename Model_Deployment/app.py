from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction',methods=('GET', 'POST'))
def prediction():
    if request.method == 'POST':
        shooting = int(request.form['shooting'])
        tackling = int(request.form['tackling'])
        crossing = int(request.form['crossing'])
        intercepting = int(request.form['intercepting'])
        aggressive = int(request.form['aggressive'])
        impulse = int(request.form['impulse'])
        assisting = int(request.form['assisting'])
        power = int(request.form['power'])
        height = int(request.form['height'])
        print(shooting,tackling,crossing,intercepting,aggressive,impulse,assisting,power,height)
        input=np.array([[height,shooting,aggressive,impulse,crossing,assisting,tackling,intercepting,power]])
        model=joblib.load('FinalModel.sav')
        scaler=joblib.load('scaler.sav')
        input=scaler.transform(input)
        print(model.get_booster().feature_names)
        prediction=model.predict(input)
        if prediction == 0:
            output='Forward'
        if prediction == 1:
            output='Midfielder'
        if prediction == 2:
            output = 'Defender'

    return render_template('prediction.html',output=output)