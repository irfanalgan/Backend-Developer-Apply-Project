from app import app
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL

mysql = MySQL()
app.secret_key = "project"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "4208863kaan."
app.config["MYSQL_DB"] = "project"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql.init_app(app)