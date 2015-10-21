import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from numpy import loadtxt, where
from pylab import scatter, show, legend, xlabel, ylabel

# Function for log regression: equations : p(x) = 1/(1 + e^(intercept + 0.087423(FicoScore) ? 0.000174(LoanAmount))
def logistic_function(FicoScore, LoanAmount, threshold, coeff, ):
    interest_rate = -(coeff[2]) - (coeff[1]*FicoScore) -(coeff[0]*LoanAmount)
    prob = (1 / (1+ interest_rate**(coeff[2] + coeff[1] * FicoScore + coeff[0] * LoanAmount)))
    lines=plt.plot()
    if prob > threshold:
        p = 1
    else:
        p = 0
    return prob, p


loansData = pd.read_csv('/Users/jenniferconnolly/Documents/ThinkFul/projects/graphs/loansData_clean.csv')

CleanIR = loansData['Interest.Rate'].map(lambda a: round(float(a.rstrip('%')) / 100, 4))
t = CleanIR[0:5]
# print t

CleanLL = loansData['Loan.Length'].map(lambda a: round(int(a.rstrip('months'))))
u = CleanLL[0:5]
# print u

CleanFR_a = loansData['FICO.Range'].map(lambda a: a.split('-')[0])
v = CleanFR_a[0:5]
# print v

loansData['IR_TF'] = (CleanIR.map(lambda x: 0 if x < .12 else 1))

loansData['intercept'] = 1.0

df = pd.DataFrame(loansData)

df['FICO.SCORE'] = (CleanFR_a.astype(int))

ind_vars = ['Amount.Funded.By.Investors', 'FICO.SCORE', 'intercept']
print ind_vars

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])
result = logit.fit()
print result
coeff = result.params
print coeff
threshold = 0.7

prob = logistic_function(720, 10000,threshold ,coeff)[0]
predict =logistic_function(720, 10000,threshold ,coeff)[1]


print prob
print predict



print "The probability of getting a 12% or less interest loan of $10,000 with a 720 FICO score is: {0}% ".format(float(prob * 100))

if predict ==1:
    print "You will likely get your loan funded if the threshold is 70%"
else:
    print "You loan will likely not be funded if the threshold is 70%"

