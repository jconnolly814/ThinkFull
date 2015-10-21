import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

loansData = pd.read_csv("/Users/jenniferconnolly/Documents/ThinkFul/projects/multivar/LoanStats3d.csv")

loansData['income'] = loansData['annual_inc'].astype(int)[1]



loansData['interest']= loansData['int_rate'].map(lambda a: round(float(a.rstrip('%')) / 100, 4))[1]
y = loansData['interest']


X= loansData['income']
X =sm.add_constant(X)


print "\n model #1"

model = sm.OLS(y,X).fit()
print model.summary()

print '\n model #2'

loansData['homeOwn'] = pd.Categorical(loansData['home_ownership']).labels

X= loansData[['income','homeOwn']]
X =sm.add_constant(X)

model2 = sm.OLS(y,X).fit()
print model2.summary()


print '\nmodel #2 interaction homeownership'

income = loansData['income']
homeOwn= loansData['homeOwn']

loansData['interaction'] = income * homeOwn

X= loansData[['income','homeOwn','interaction']]
#X= loansData[['income','interaction']]
X =sm.add_constant(X)
model2a = sm.OLS(y,X).fit()
print model2a.summary()

xx1, xx2 = np.meshgrid(np.linspace(X.income.min(), X.income.max(), 100),
                       np.linspace(X.interaction.min(), X.interaction.max(), 100))
# plot the hyperplane by evaluating the parameters on the grid
Z = model2a.params[0] + model2a.params[1] * xx1 + model2a.params[2] * xx2

# create matplotlib 3d axes
fig = plt.figure(figsize=(12, 8))
ax = Axes3D(fig, azim=-115, elev=15)

# plot hyperplane
surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

# plot data points - points over the HP are white, points below are black
resid = y - model2a.predict(X)
ax.scatter(X[resid >= 0].income, X[resid >= 0].interaction, y[resid >= 0], color='black', alpha=1.0, facecolor='white')
ax.scatter(X[resid < 0].income, X[resid < 0].interaction, y[resid < 0], color='black', alpha=1.0)

# set axis labels
ax.set_xlabel('income')
ax.set_ylabel('interest')
ax.set_zlabel('interaction')
plt.show()

