import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import os

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')



loansData.dropna(inplace=True)
loansData.boxplot(column='Amount.Funded.By.Investors')
plt.show()

loansData.dropna(inplace=True)
loansData.boxplot(column='Amount.Requested')
plt.show()


df = pd.DataFrame(loansData)
AFBI= df.loc[:, ['Amount.Funded.By.Investors']]
AR= df.loc[:, ['Amount.Requested']]


box = AFBI.plot(kind ='box')
plt.savefig(str('box_AFBI_loansData.jpeg'))
plt.show()

hist = AFBI.plot(kind ='hist')
plt.savefig(str('hist_AFBI_loansData.jpeg'))
plt.show()

plt.figure()
graph = stats.probplot(loansData['Amount.Funded.By.Investors'], dist="norm", plot=plt)
plt.savefig(str('qq_AFBI_loansData.jpeg'))
plt.show()


box = AR.plot(kind ='box')
plt.savefig(str('box_AR_loansData.jpeg'))
plt.show()

hist = AR.plot(kind ='hist')
plt.savefig(str('hist_AR_loansData.jpeg'))
plt.show()

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.savefig(str('qq_AR_loansData.jpeg'))
plt.show()