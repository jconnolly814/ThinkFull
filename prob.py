import collections
import scipy
import scipy.stats
import matplotlib.pyplot as plt
import os

testlist = [1, 4, 5, 6, 9, 9, 9]
x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

print "start testlist summary"
c = collections.Counter(testlist)
count_sum = sum(c.values())

for k, v in c.iteritems():
    print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

plt.boxplot(testlist)


plt.savefig(str('box_testlist.jpeg'))
plt.show()

plt.hist(testlist, histtype='bar')
plt.savefig(str('hist_testlist.jpeg'))
plt.show()

plt.figure()

graph1 = scipy.stats.probplot(testlist, dist="norm", plot=plt)

plt.savefig(str('qq_testlist.jpeg'))
plt.show()


print "start x data summary"
z = collections.Counter(x)
count_sum = sum(z.values())

for k, v in z.iteritems():
    print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

plt.boxplot(x)

plt.savefig(str('box_x.jpeg'))
plt.show()

plt.hist(x, histtype='bar')

plt.savefig(str('hist_x.jpeg'))
plt.show()

graph2 = scipy.stats.probplot(x, dist="norm", plot=plt)

plt.savefig(str('qq_x.jpeg'))
plt.show()


