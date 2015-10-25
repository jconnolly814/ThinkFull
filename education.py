# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import csv
import numpy as np
#import statsmodels.api as sm

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

# Use Beautiful Soup to Parse the HTML
soup_data = BeautifulSoup(r.content)



# Select tables we are interested in
# pull all data with class tcont


soup_tag = soup_data('table')[6].tr.td
#for row in soup_tag:
    #print row
soup_table = soup_tag('table')[1].tr.td.div
#for row in soup_table:
    #print row
raw_table = soup_table('table')[0]
#for row in raw_table:
    #print row



col_name = []

for j in raw_table('tr'):
    if j.get('class', ['Null'])[0] == 'lheader':
        for td in j.find_all('td'):
            if td.get_text() != '':
                col_name.append(td.get_text())
        break


country_table = pd.DataFrame(columns=col_name)
#print country_table

edu_counter = 0
for j in raw_table('tr'):
    row_data = []
    if j.get('class', ['Null']) == 'tcont':
        row_data.append(j.find('td').get_text())
        for td in j.find_all('td')[1:]:
            if td.get('align'):
                row_data.append(td.get_text())
    else:
        row_data.append(j.find('td').get_text())
        for td in j.find_all('td')[1:]:
            if td.get('align'):
                row_data.append(td.get_text())
    if len(row_data) == len(col_name):
        country_table.loc[edu_counter] = row_data
        edu_counter += 1



sublistdf =country_table[['Total', 'Men', 'Women']]
numeric_country_table= pd.to_numeric(sublistdf , errors='coerce')
country_table[['Total', 'Men', 'Women']]= numeric_country_table[['Total', 'Men', 'Women']]

#print numeric_country_table


country_gdp = pd.DataFrame(
    columns=['country_name', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
             '2010'])


# convert school years to integers

con = lite.connect('education.db')
cur = con.cursor()



# create table to hold school data
with con:
    cur.execute("DROP TABLE IF EXISTS school_years")
    cur.execute('CREATE TABLE school_years (country_name, _Year, _Total, _Men, _Women)')

with con:
    cur.execute("DROP TABLE IF EXISTS gdp")
    cur.execute(
        'CREATE TABLE gdp (country_name text,  _1999 numeric, _2000 numeric, _2001 numeric, _2002 numeric, _2003 numeric, _2004 numeric, _2005 numeric, _2006 numeric, _2007 numeric, _2008 numeric, _2009 numeric, _2010 numeric)')

with open('E:\\ThinkFul\\ny\\ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', 'rU') as inputFile:
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    #print header
    inputReader = csv.reader(inputFile)
    gdp_row_num = 0
    for line in inputReader:
        row_data = [line[0]]
        row_data.extend(line[43:-5])
        country_gdp.loc[gdp_row_num] = row_data
        gdp_row_num += 1
        with con:
            cur.execute(
                'INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' +
                line[0] + '","' + '","'.join(line[43:-5]) + '");')



sublist_gdp_df = country_gdp[country_gdp.columns[1:-1]]
numeric_country_table= pd.to_numeric(sublist_gdp_df, errors='coerce')
country_gdp[country_gdp.columns[1:-1]]=numeric_country_table

country_table['GDP']=0


#print country_gdp['GDP']
#print country_gdp
#print country_table

gdplist =[]
for i in range(edu_counter):
    rowid = country_gdp[country_gdp['country_name'] == country_table['Country or area'][i]].index
    if len(rowid) > 0:
        row_index = rowid.tolist()[0]
        try:
            gdp = float(country_gdp[country_table['Year'][i]][row_index]) ##extracts year from country table they pull the year, row index from gdp table and assigns that value back to GDP col of the country tab;e
            gdplist.append(gdp)
        except ValueError:
            gdp ='nan'
            gdplist.append(gdp)

    else:
        gdp ='nan'
        gdplist.append(gdp)

#print gdplist
#print len(gdplist)
#print len(country_table['GDP'])

country_table['GDP']= gdplist


gdp = country_table['GDP'].map(lambda x: 0 if x =='nan'else float(x))
school_years = country_table['Year'].map(lambda x: int(x))
log_gdp = gdp.map(lambda x: np.log(x))

print len (gdp)
print len(log_gdp)
print len(school_years)

colors = np.random.rand(len(gdp))
plt.scatter(log_gdp, school_years, c=colors)
plt.show()


y = np.matrix(gdp).transpose()
x = np.matrix(school_years).transpose()

X = sm.add_constant(x)
model = sm.OLS(y,X)
results = model.fit()

y = np.matrix(log_gdp).transpose()
x = np.matrix(school_years).transpose()

X = sm.add_constant(x)
model2 = sm.OLS(y,X)
results2 = model2.fit()

sm.graphics.tsa.plot_acf(log_gdp) #Autocorrelation
plt.show()

sm.graphics.tsa.plot_pacf(log_gdp) #Partial Autocorrelation
plt.show()

