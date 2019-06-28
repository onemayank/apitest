NAME:MAYANK NEGI
EMAIL_ID : MAY17SEPT@GMAIL.com
phone number : 9599797402,9650759121(around 2pm to 5 pm)

question source--> https://pastebin.com/Rn1W4fb1

					Interview Stage 1:

In stage 1 I created a database named as locationdata in which I loaded the .csv file from the link (https://github.com/sanand0/pincode/blob/master/data/IN.csv)

Then I created a  post api for the link 127.0.0.1:5000/post_location which run for the POST method only and returns JSON data of current location

To fetch the current location I import the requests in my python file and fetch the current address from ipinfo.io which returned me the json data of my location

	
					Interview Stage 2:

In this I made two api with GET METHOD

One which uses postgresql module named as earthdistance 
The other is my own algorithm to find the nearest location to me

					
					Interview Stage 3:

In this I made an api with GET METHOD

url for this api is 127.0.0.1/latitude/longitude --->(Latitude and longitude are the float values)
using the latitude and longitude of the current location I searched the region of that latitude nad longitude

					DATABASES CREATED:

1----> locationdata (Column Name-->pin_code, city, admin_name1, latitude, longitude, accuracy)
2----> geojson (Column Name-->name, type, parent, shape)
3----> geojson_coordinates(Column Name-->longitude, latitude, name)



