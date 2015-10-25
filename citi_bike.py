import requests
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt 
import collections
import sqlite3 as lite
import time
from dateutil.parser import parse
import datetime



r = requests.get('http://www.citibikenyc.com/stations/json')

text =r.text
json= r.json()
json_key= r.json().keys()

key_list = []
for station in r.json()['stationBeanList']:
	for k in station.keys():
		if k not in key_list:
			key_list.append(key_list)
print key_list

record= r.json()['stationBeanList'][0] #
print record


df = json_normalize(r.json()['stationBeanList'])# convert JSON datat to dataframe

# Let's look at the range of values for each attribute, starting with the available bikes:
df['availableBikes'].hist()
plt.show()

df['totalDocks'].hist()
plt.show()



#Challenge
total=len(r.json()['stationBeanList'])
#print total
count =collections.Counter(df['testStation'])
total_nontest = count[0]
#print total_nontest

df['testStation'].hist()
plt.show()

if total==total_nontest:
    print "There are no Test Stations"
else:
    test= total-total_nontest
    print "There are {0} test stations".format(test)


print 'The mean number of bikes is: {0}'.format(str(df['availableBikes'].mean()))
print 'The median number of bikes is: {0}'.format(str(df['availableBikes'].median()))

condition = (df['statusValue'] == 'In Service')
print 'The mean number number of bikes in service is:{0} '.format(str(df[condition]['availableBikes'].mean()))
print 'The median number number of bikes in service is:{0} '.format(str(df[condition]['availableBikes'].median()))

con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
    cur.execute ("DROP TABLE IF EXISTS citibike_reference")

    cur.execute(
        "CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )")

#prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist()
station_ids = ['_' + str(x) + ' INT' for x in station_ids]  #clean up for SQL

#create the table
#in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)

with con:
    cur.execute ("DROP TABLE IF EXISTS available_bikes")
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")

#take the string and parse it into a Python datetime object
exec_time = parse(r.json()['executionTime'])

with con:
	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

#iterate through the stations in the "stationBeanList"
id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

#loop through the stations in the station list
for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']

#iterate through the defaultdict to update the values in the database
with con:
    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
con.close() #close the database

### sleep for a minute and then perform the same task. do this for an hour

con = lite.connect('citi_bike.db')
cur = con.cursor()

print "Start hour long query"
for i in range(60):
    print i
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
    con.commit()

    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
    con.commit()

    time.sleep(60)

con.close() #close the database connection



## Analyzing the Result##

con = lite.connect('citi_bike.db')
cur = con.cursor()
df = pd.read_sql("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:]
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer

def keywithmaxval(d):
    # create a list of the dict's keys and values;
    v = list(d.values())
    k = list(d.keys())

    # return the key with the max value
    return k[v.index(max(v))]

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

plt.bar(hour_change.keys(), hour_change.values())
plt.show()
plt.savefig(str('bikedata.jpeg'))

con.close() #close the database connection

