from bottle import get, static_file, run
from jinja2 import template
import json
import pymysql as pms

_connection = None
COUNTRIES_PER_PAGE = 30


@get("/list_countries")
@get("/list_countries/<page>")
def get_list_countries(page="0"):
    limit_offset = COUNTRIES_PER_PAGE * int(page)
    try:
        with _connection.cursor() as cursor:
            sql = f"SELECT Name , Code2 FROM country LIMIT {COUNTRIES_PER_PAGE+1} OFFSET {limit_offset}"
            cursor.execute(sql)
            countries = cursor.fetchall()
            result = {
                "countries": countries[:COUNTRIES_PER_PAGE],
                "has_more": len(countries) == (COUNTRIES_PER_PAGE + 1)
            }

            return json.dumps(result)
    except Exception as ex:
        return json.dumps({'error': f'something is wrong with the DB, error: {ex}'})


@get("/country/<id>")
def get_country_details(id):
    try:
        with _connection.cursor() as cursor:
            sql = "SELECT * FROM country WHERE Code = '{}".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
            return json.dumps(result)
    except Exception as e:
        return json.dumps({'error': 'something is wrong with the DB ' + repr(e)})


@get("/add_language")
def add_language():
    with _connection.cursor() as cursor:
        sql = "INSERT INTO countryLanguage VALUES ('ISR', 'French', 'F', 5.3)"
        cursor.execute(sql)
        _connection.commit()
        return "done"


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root="js")


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root="css")


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root="images")


if __name__ == "__main__":
    _connection = pms.connect(host="localhost",
                              user="root",
                              password="root",
                              db="world",
                              charset="utf8",
                              cursorclass=pms.cursors.DictCursor)
    run(host="localhost", port=7000)
