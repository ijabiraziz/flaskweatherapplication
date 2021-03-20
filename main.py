import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['DEBUG'] = True
# Create a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myweather.db'

"""Below Line help us to get notified before and after changes are 
committed to the database. These changes are only tracked if SQLALCHEMY_TRACK_MODIFICATIONS 
is enabled in the config. As we have make it False so we will not be notified."""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Generate a secret key. it also help with using flask messages inside your app
app.config['SECRET_KEY'] = 'thisisasecret'

db = SQLAlchemy(app)


# Create tables in database
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


"""this function will take the city is an argument and 
check if the city does exist.Also put the city in the url"""


def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weath' \
          f'er?q={city}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    r = requests.get(url).json()
    return r


@app.route('/')
def index_get():
    # fetch all the cities from database
    cities = City.query.all()

    weather_data = []

    """Now loop through all these Citiees"""
    for city in cities:
        # city.name come from the above url
        r = get_weather_data(city.name)
        print(r)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


@app.route('/<string:city>')
def index_post(city):
    err_msg = ''
    new_city = request.form.get('city')

    # Check if entered city actually exist
    if city:
        """check if the new_city actually exist in the database and if does
        then take out the first."""
        existing_city = City.query.filter_by(name=city).first()

        if not existing_city:
            """if there is no existing city then add it to the database"""
            new_city_data = get_weather_data(city)

            # cod == 200 come from the json
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=city)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not exist!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully!')

    return redirect(url_for('index_get'))


"""whichever the city name is passed to the link 
will be deleted both from the database and also from
the main page, which is home or home route."""


@app.route('/delete/<name>')
def delete_city(name):
    """Now search and actually remove the city from
    the database."""
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'{city.name} deleted Successfully ', 'success')
    return redirect(url_for('index_get'))


if __name__ == "__main__":
    app.run(debug=True)

"""We use to render_template only in the Get request
keyError: main error shows when the API doesn't get the 
the information about the specific city or the city that 
you asked for."""
