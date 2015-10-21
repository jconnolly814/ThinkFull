import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix

import matplotlib.pyplot as plt
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
# Drop null rows
loansData.dropna(inplace=True)


a=loansData['Interest.Rate'][0:5]
b =loansData['Loan.Length'][0:5]
c = loansData['FICO.Range'][0:5]
#print c

CleanIR = loansData['Interest.Rate'].map(lambda a: round(float(a.rstrip('%')) / 100, 4))
t=CleanIR[0:5]
#print t

CleanLL = loansData['Loan.Length'].map(lambda a: round(int(a.rstrip('months'))))
u= CleanLL[0:5]
#print u

CleanFR_a = loansData['FICO.Range'].map(lambda a: a.split('-')[0])
v= CleanFR_a[0:5]
#print v

df = pd.DataFrame(loansData)
df['FICO.SCORE']= (CleanFR_a.astype(int))

#print df

hist = df['FICO.SCORE'].plot(kind ='hist')
plt.show()


j=scatter_matrix(df, alpha=0.05, figsize=(10,10))
plt.show()
k= pd.scatter_matrix(df, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()


#df.to_csv('C:\Users\JConno02\projects\graphs\loansData_clean.csv', header=True, index=False)

intrate = CleanIR
loanamt = df['Amount.Requested']
fico = df['FICO.SCORE']



y = np.matrix(intrate).transpose()
print y
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

x = np.column_stack([x1,x2])
print x

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

output = f.summary()

print output


