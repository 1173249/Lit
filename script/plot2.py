from __future__ import division
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot

def func(x,a,b):
    return a*x + b

def func2(x,a,b,c):
    return a*x*x + b*x + c
xData = numpy.array([675,726,792])

yData = numpy.array([1411,2040, 780])

trialX = numpy.linspace(xData[1],xData[-1],1000)

# Fit a polynomial
fitted = numpy.polyfit(xData, yData, 10)[::-1]
y = numpy.zeros(len(trialX))
for i in range(len(fitted)):
    y += fitted[i]*trialX**i

# Fit an exponential
popt, pcov = curve_fit(func2, xData, yData)
print popt
yEXP = func2(trialX, *popt)

pyplot.figure()
pyplot.plot(xData, yData, label='Data', marker='o')
pyplot.plot(trialX, yEXP, 'r-',ls='--', label="Exp Fit")
#pyplot.plot(trialX,   y, label = '10 Deg Poly')
pyplot.legend()
pyplot.show()
