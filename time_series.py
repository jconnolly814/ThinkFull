import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


df = pd.read_csv("/Users/jenniferconnolly/Documents/ThinkFul/projects/multivar/LoanStats3d.csv",header=0, low_memory=False)

# converts string to datetime object in pandas:
df['issue_d_format'] = pd.to_datetime(df['issue_d'])
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

print loan_count_summary


plt.plot(loan_count_summary)
plt.ylabel("Number of Loans")
plt.xlabel("Month")
plt.show()

### data is not stationary; transform by getting the difference
loan_count_sum_diff = loan_count_summary.diff()
plt.plot(loan_count_sum_diff)
plt.ylabel("Number of Loans")
plt.xlabel("Difference")
plt.show()

sm.graphics.tsa.plot_acf(loan_count_summary) #Autocorrelation

plt.show()

sm.graphics.tsa.plot_pacf(loan_count_summary) #Partial Autocorrelation

plt.show()

sm.graphics.tsa.plot_acf(loan_count_sum_diff) #Autocorrelation

plt.show()

sm.graphics.tsa.plot_pacf(loan_count_sum_diff) #Partial Autocorrelation

plt.show()

### Yes there are autocorrelated structures
# The autocorrelations is quickly decaying but with persistent partial autocorrelations therefore the model is best
# served by an MA terms to match the lags of significant autocorrelations.