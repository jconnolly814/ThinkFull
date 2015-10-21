import pandas as pd
from scipy import stats


data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = data.splitlines()
data = [i.split(', ') for i in data]

column_names = data[0]  # this is the first row
data_rows = data[1::]  # all of the folling rows


df = pd.DataFrame(data_rows, columns=column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

mean_alc = df['Alcohol'].mean()
median_alc = df['Alcohol'].median()
mode_alc = stats.mode(df['Alcohol'])

range_alc =max(df['Alcohol']) - min(df['Alcohol'])
std_alc = df['Alcohol'].std()
var_alc = df['Alcohol'].var()


print '\n'

print "Alcohol results are"
print "Mean = {0}".format(mean_alc)
print "Median = {0}".format(median_alc)
print "Mode = {0}".format(mode_alc)
print "Range = {0}".format(range_alc)
print "STD = {0}".format(std_alc)
print "Var = {0}".format(var_alc)


mean_tob = df['Tobacco'].mean()
meadian_tob = df['Tobacco'].median()
mode_tob = stats.mode(df['Tobacco'])

range_tob =max(df['Tobacco']) - min(df['Tobacco'])
std_tob = df['Tobacco'].std()
var_tob = df['Tobacco'].var()

print ' \n'
print "Tobacco results are"
print "Mean = {0}".format(mean_tob)
print "Median = {0}".format(meadian_tob)
print "Mode = {0}".format(mode_tob)
print "Range = {0}".format(range_tob)
print "STD = {0}".format(std_tob)
print "Var = {0}".format(var_tob)



