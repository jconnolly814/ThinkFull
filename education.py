# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import csv
import numpy as np
import statsmodels.api as sm

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

# Use Beautiful Soup to Parse the HTML
soup_data = BeautifulSoup(r.content)



# Select tables we are interested in
# pull all data with class tcont


soup_tag = soup_data('table')[6].tr.td
soup_table = soup_tag('table')[1].tr.td.div
raw_table = soup_table('table')[0]



col_name = []

for child in raw_table('tr'):
    if child.get('class', ['Null'])[0] == 'lheader':
        for td in child.find_all('td'):
            if td.get_text() != '':
                col_name.append(td.get_text())
        break


country_table = pd.DataFrame(columns=col_name)
print country_table

edu_row_num = 0
for child in raw_table('tr'):
    row_curr = []
    if child.get('class', ['Null']) == 'tcont':
        row_curr.append(child.find('td').get_text())
        for td in child.find_all('td')[1:]:
            if td.get('align'):
                row_curr.append(td.get_text())
    else:
        row_curr.append(child.find('td').get_text())
        for td in child.find_all('td')[1:]:
            if td.get('align'):
                row_curr.append(td.get_text())
    if len(row_curr) == len(col_name):
        country_table.loc[edu_row_num] = row_curr
        edu_row_num += 1


country_table[['Total', 'Men', 'Women']] = country_table[['Total', 'Men', 'Women']].convert_objects(
    convert_numeric=True)
print country_table

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

with open('/Users/jenniferconnolly/Documents/ThinkFul/ny/ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', 'rU') as inputFile:
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    print header
    inputReader = csv.reader(inputFile)
    gdp_row_num = 0
    for line in inputReader:
        row_curr = [line[0]]
        row_curr.extend(line[43:-5])
        country_gdp.loc[gdp_row_num] = row_curr
        gdp_row_num += 1
        with con:
            cur.execute(
                'INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' +
                line[0] + '","' + '","'.join(line[43:-5]) + '");')

country_gdp[country_gdp.columns[1:-1]] = country_gdp[country_gdp.columns[1:-1]].convert_objects(convert_numeric = True)

country_table['GDP'] = np.nan
for i in range(edu_row_num):
    find_index = country_gdp[country_gdp['country_name'] == country_table['Country or area'][i]].index
    if len(find_index) > 0:
        row_index = find_index.tolist()[0]
        country_table['GDP'][i] = country_gdp[country_table['Year'][i]][row_index]
edu_gdp = country_table[np.isfinite(country_table['GDP'])][['Country or area', 'Total', 'GDP']]
edu_gdp['log_GDP'] = np.log(edu_gdp['GDP'])

edu_gdp.plot(kind='scatter', x='Total', y='log_GDP')
plt.show()

gdp = country_table['GDP'].map(lambda x: float(x))
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


#So now you have the GDP for the countries and the school life expectancy, try and match them up.
# See if there is any correlation between the GDP numbers and the life expectancy.
# You may need to do a log-transform of the GDP to get a scale you can use to compare the widely distributed countries.
# If there's a correlation, why do you think that is? Also explain why there may not be a correlation. Write up a blogpost
# and share your insights with the world!


