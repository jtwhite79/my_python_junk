import pylab
import numpy

#--create a string variable with the name of the data file
file = "some_text.dat"


#--load the contents of data file to array named data
#--skip the first row, since it is a header
#--use only columns 0 and 5 of the data
#--opttionally, add delimiter=',' argument if file is comma delimited
data = numpy.loadtxt(file,skiprows=1,usecols=[0,5,9])


#--print the shape of data array 
print data.shape


#--create a new figure instance
fig = pylab.figure()

#--add a plot to the figure
plt = pylab.subplot(111)

#--add a second yaxis
plt2 = pylab.twinx() 

#--plot stage on the first axis
plt.plot(data[:,0],data[:,1],'b-') 
print plt.get_ylim()

#--precip on the second axis
plt2.plot(data[:,0],data[:,2],'k--')

#--reverse the order of the second axis to clear things up
ymin,ymax = plt2.get_ylim()
plt2.set_ylim(ymax,ymin)

#--label axes
plt.set_xlabel('total time')
plt.set_ylabel('stage (ft)')
plt2.set_ylabel('precip (ft3/day)')

#--'show' the figure to the screen
pylab.show()