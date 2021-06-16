# flaskweatherapplication
I have used flask framework beside some basic HTML5+CSS3.
Flask is a micro python based web-framework that helps to deal 
with the backend of different web application or websites.

To work with Flask we need to import the Flask(with capital 'F') Class from flask (with small 'f')
i.e, from Flask import flask.
Then intiate the application by using the statement given below:
app = Flask(__name__)

After running the code lets say on local host, then you need to 
put the name of intended city or country (who's weather you wants to know)
in url. for instance, http://127.0.0.1:5000/newyork or
                      http://127.0.0.1:5000/lahore
                      
Every time you enter a country or city name it will store in database right away.
by the way, i have connected my web-app with SQLAlchemy (SQLAchemy is ORM basically) database 
which is so easy and comfortable to work with. SQLAlchemy is offered only to python user.

Also when you click Cross sign , displayed on top right corner then that city 
or country will be deleted from the database.
