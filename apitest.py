from flask import Flask, jsonify, request, session, redirect, render_template
import psycopg2
import requests #it is used to request data from a url
app = Flask(__name__)

#connect to the db
con = psycopg2.connect(
            host = "127.0.0.1",
            database = "postgres",
            user = "postgres",
            password = "Ssnegi##5128"
)

#Current location information
res = requests.get('https://ipinfo.io/')
data = res.json()
cur_city = data['city']
cur_latitude = data['loc'].split(',')[0]
cur_longitude = data['loc'].split(',')[1]
cur_admin_name1 = data['region']
cur_pin_code = data['postal']




@app.route('/')
def index():
    return "This is to test the api for redcarpet go post_location or get_location"



#interview stage 1
@app.route('/post_location',methods=['POST'])
def post_location():
    global con,b,data
    cur = con.cursor()
    cur.execute("select * from locationdata where key='IN/%s' and latitude=%f and longitude=%f"%(cur_pin_code,float(cur_latitude),float(cur_longitude)))
    b = cur.fetchall()
    if b==[]:
        cur.execute("INSERT INTO locationdata VALUES('IN/%s','%s','%s',%f,%f,null);"%(cur_pin_code,cur_city,cur_admin_name1,float(cur_latitude),float(cur_longitude)))
        con.commit()
    return str(data)



#Interview Stage 2 where we are taking areas under 20 kilometers from a point(77.3710,28.5896)

#It is done by using the earthdistance
@app.route('/get_using_postgres',methods=['GET'])
def get_using_postgres():
    global con
    cur = con.cursor()
    cur.execute("with locationdata AS (select *,round(((point(longitude,latitude))<@>point(77.3710,28.5896))::numeric,3)*1.60934 as km from locationdata) select * from locationdata where km<20")
    b = cur.fetchall()
    return str(b)



#It is done by using the self calculation
#@app.route('/get_using_self',methods=['GET'])
#def get_using_self():
    


#interview Stage 3
@app.route('/<float:latitude>/<float:longitude>',methods=['get'])
def latitude_longitude(latitude,longitude):
    geojson = requests.get("https://gist.githubusercontent.com/ramsingla/6202001/raw/1dc42df3c6d8f4db95b7f7b65add1f520578ab33/map.geojson")
    raw = geojson.json()
    return str(latitude)
    




#running the app on LOCALHOST(i.e.->127.0.0.1:5000/)
if __name__ == "__main__":
    app.run(port = 5000,debug=True)


#close the connection
con.close()
