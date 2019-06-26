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
    return """This is to test the api for redcarpet go post_location or get_location

                    following are the links you can go for---
                    
                        127.0.0.1:5000/post_location
                        127.0.0.1:5000/get_using_postgres/(float for distance range)
                        127.0.0.1:5000/get_using_self/(float for distance range)
                        127.0.0.1:5000/(float for latitude)/(float for longitude)
                        127.0.0.1:5000/feed_geojson

                                                        """
                                                                                                    #       -------------------  table locationdata ------------------------------
                                                                                                    #      | pin_code    city     admin_name1    latitude    longitude   accuracy|

                                                                                                    #      |(varchar)  (varchar)   (varchar)     (float)      (float)   (integer)|





                                       #      ---------------------Interview stage 1-------------------------------


                                       
@app.route('/post_location',methods=['POST'])
def post_location():
    global con,b,data
    cur = con.cursor()
    cur.execute("select * from locationdata where key='IN/%s' and latitude=%f and longitude=%f;"%(cur_pin_code,float(cur_latitude),float(cur_longitude)))
    b = cur.fetchall()
    if b==[]:
        cur.execute("INSERT INTO locationdata VALUES('IN/%s','%s','%s',%f,%f,null);"%(cur_pin_code,cur_city,cur_admin_name1,float(cur_latitude),float(cur_longitude)))
        con.commit()
    return str(data)






                                      #     -----------------------------Interview Stage 2-------------------------



#It is done by using the earthdistance
@app.route('/get_using_postgres/<float:distance>/',methods=['GET'])
def get_using_postgres(distance):
    global con,cur_latitude,cur_longitude
    cur = con.cursor()
    cur.execute("with locationdata AS (select *,round(((point(longitude,latitude))<@>point(%f,%f))::numeric,3) *1.60934 as km from locationdata) select * from locationdata where km<%f;"%(float(cur_longitude),float(cur_latitude),distance))
    b = cur.fetchall()
    return str(b)



#It is done by using the self calculation
@app.route('/get_using_self/<float:distance>/',methods=['GET'])
def get_using_self(distance):
    global con
    from math import radians, sin, cos, acos
    slat = radians(float(cur_latitude))
    slon = radians(float(cur_longitude))
    store = {}
    cur = con.cursor()
    cur.execute("select * from locationdata where admin_name1='New Delhi'")
    b = cur.fetchall()
    for i in b:
        elat = radians(float(i[3]))
        elon = radians(float(i[4]))
        dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
        if dist<=distance:
            store[i[1]] = dist
    return(str(store))
    

                            #              ------------------------------Interview Stage 3-----------------------------



@app.route('/<float:latitude>/<float:longitude>',methods=['get'])
def latitude_longitude(latitude,longitude):
    global con
    cur = con.cursor()
    cur.execute("with region AS (select *,round(((point(longitude,latitude))<@>point(%f,%f))::numeric,3) *1.60934 as km from locationdata) select admin_name1 from region where km = (select min(km) from region)"%(float(cur_longitude),float(cur_latitude)))
    b = cur.fetchall()
    b={b[0][0]}
    return(str(b))





                        #               ---------------------------- FEEDING DATA FROM GEOJSON.IO INTO THE DATABASE ------------------------




@app.route('/feed_geojson/',methods=['get'])
def feed_geojson():
    global con
    #This is to feed the geojson.io's json data in the databases geojson and geojson_coordinates                                
    geojson = requests.get("https://gist.githubusercontent.com/ramsingla/6202001/raw/1dc42df3c6d8f4db95b7f7b65add1f520578ab33/map.geojson") #fetching the json data


    raw = geojson.json()                                                                           #                          -------     ------  TABLE GEOJSON  ------   ---------------
    features = raw['features']
    for i in features:                                                                        #                               |     name        type          parent          shape      |
        name = i['properties']['name']                                                         #                              |(VARCHAR 100) (VARCHAR 100)   (VARCHAR 100)  (VARCHAR 100)|
        type_ = i['properties']['type']
        parent = i['properties']['parent']                                                                                                  
        shape = i['geometry']['type']
        cur = con.cursor()
        cur.execute("select * from geojson where name='%s' and type='%s' and parent='%s' and shape='%s';"%(name,type_,parent,shape))
        b = cur.fetchall()                                                                                                      


        if b==[]:                                                                                                   #                ------  TABLE GEOJSON_COORDINATES  -------------
            cur = con.cursor()
            cur.execute("INSERT INTO geojson VALUES('%s','%s','%s','%s');"%(name,type_,parent,shape))               #                |   longitude        latitude       name        |
            con.commit()
                                                                                                                        #            |    (float)         (float)     (varchar 100)  |
        for j in features:
            cor = j['geometry']['coordinates'][0]
            for k in cor:
                cur = con.cursor()
                cur.execute("select * from geojson_coordinates where longitude=%f and latitude=%f and name='%s'"%(k[0],k[1],name))
                b = cur.fetchall()
                if b==[]:
                    cur.execute("INSERT INTO geojson_coordinates VALUES(%f,%f,'%s');"%(k[0],k[1],name))
                    con.commit()
                    
    return "DATA FEEDED IN THE DATABASE GEOJSON AND GEOJSON_COORDINATE SUCCESSFULLY"




#running the app on LOCALHOST(i.e.->127.0.0.1:5000/)
if __name__ == "__main__":
    app.run(port = 5000,debug=True)


#close the connection
con.close()
