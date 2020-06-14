from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db  = SQLAlchemy(app)

class City(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"City:{self.name}"

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_city = request.form['city']
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=02c0ca2f81c3769d84452840b85563b6'

    weather_data=[]

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city':city.name,
            'country':r['sys']['country'],
            'temperature':round(r['main']['temp']),
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        
        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)


if __name__ == "__main__":
    app.run(debug=True)