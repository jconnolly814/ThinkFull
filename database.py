import sqlite3 as lite
import pandas as pd

# Here you connect to the database. The `connect()` method returns a connection object.
con = lite.connect('C:\Users\JConno02\projects\sqlite\getting_started.db')
# Select all rows and print the result set one row at a time
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cities ")
    cur.execute("DROP TABLE IF EXISTS weather ")

    cur.execute("CREATE TABLE cities (name TEXT, state TEXT)")
    cur.execute(
        "CREATE TABLE weather (city TEXT, year INTEGER, warm_month TEXT, cold_month TEXT, average_high INTEGER)")

    cur.execute("INSERT INTO cities VALUES('Houston', 'TX')")
    cur.execute("INSERT INTO cities VALUES('New York City','NY')")
    cur.execute("INSERT INTO cities VALUES('Boston', 'MA')")
    cur.execute("INSERT INTO cities VALUES('Chicago', 'IL')")
    cur.execute("INSERT INTO cities VALUES('Miami', 'FL')")
    cur.execute("INSERT INTO cities VALUES('Dallas', 'TX')")
    cur.execute("INSERT INTO cities VALUES('Seattle', 'WA')")
    cur.execute("INSERT INTO cities VALUES('Portland', 'OR')")
    cur.execute("INSERT INTO cities VALUES('San Francisco', 'CA')")
    cur.execute("INSERT INTO cities VALUES('Los Angeles', 'CA')")

    cur.execute("INSERT INTO weather VALUES('New York City', 2013 ,'July', 'January', 62)")
    cur.execute("INSERT INTO weather VALUES('Boston', 2013, 'July','January',59)")
    cur.execute("INSERT INTO weather VALUES('Chicago', 2013, 'July','January',59)")
    cur.execute("INSERT INTO weather VALUES('Miami', 2013, 'August','January',84)")
    cur.execute("INSERT INTO weather VALUES('Dallas', 2013, 'July','January',77)")
    cur.execute("INSERT INTO weather VALUES('Seattle', 2013, 'July','January',61)")
    cur.execute("INSERT INTO weather VALUES('Portland', 2013, 'July','December',63)")
    cur.execute("INSERT INTO weather VALUES('San Francisco', 2013,'September','December',64)")
    cur.execute("INSERT INTO weather VALUES('Los Angeles', 2013,'September','December', 75)")
    cur.execute("SELECT name, state, warm_month FROM cities INNER JOIN weather ON name = city ORDER BY  warm_month")
    # cur.execute("SELECT city, state,warm_month FROM weather ORDER BY  warm_month")
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)

july_df = df[df['warm_month'].isin(['July'])]
nm_state = july_df.loc[:, ['name', 'state']]

count = len(nm_state)
index = count - 1
tracker = index
partb = ''

while tracker > -1:
    if tracker == index:
        b = (nm_state.iloc[int(tracker)][:2])
        bb = b.values
        for value in bb:
            y = bb[0]
            z = bb[1]
        start = "The cities that are warmest in July are: {0} {1}".format(y, z)
        tracker -= 1
    else:
        b = (nm_state.iloc[int(tracker)][:2])
        bb = b.values
        partc = partb.replace("and ", ",")
        for value in bb:
            y = bb[0]
            z = bb[1]

        partb = "{0} and {1} {2}".format(partc, y, z)
        final = "{0}{1}".format(start, partb)

        tracker -= 1
print "{0}.".format(final)
