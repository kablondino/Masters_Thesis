import matplotlib.pyplot as plt
import numpy
from matplotlib.ticker import FormatStrFormatter
import csv

import os
import sys

# Import DIRECTORY NAME in which to do the bidding
data_directory = sys.argv[1]


# Create list of files
file_list = []
big_data = []

# Function to remove first and last y-axis tick labels
def remove_yticks(*the_axes):
	for axis in the_axes:
		plt.setp(axis.get_yticklabels()[0], visible=False)
		plt.setp(axis.get_yticklabels()[-1], visible=False)

def min_max_ylim(the_big_data, the_column, the_axis):
	sum(the_big_data[:,the_column])

for filename in os.listdir('./'+str(data_directory)):
	file_list.append(filename)
	big_data.append(numpy.loadtxt(data_directory+'/'+filename, skiprows=1))


i = 0 # Looping counter
for filename in file_list:
	filename_sans_ext = os.path.splitext(filename)[0]

	data = numpy.loadtxt(data_directory+'/'+filename, skiprows=1)

	# The data
	x = data[:,0]
	density = data[:,1]
	temperature = data[:,2]
	Z = data[:,3]
	Diffusivity = data[:,4]

	# Generate the figure
	fig = plt.subplots(2, 1, sharex=True, squeeze=True, figsize=(12,12))[0]
	fig.subplots_adjust(hspace=0)

	# TOP PLOT
	ax_n = plt.subplot(2,1,1)
	density_plot = ax_n.plot(x, density, label=r"$n$", color='blue')
	ax_n.set_ylabel(r"$n$", fontsize='large', rotation=0, labelpad=20)
	ax_n.tick_params(axis='x', labelbottom='off') # Remove top plot's x-axis labels

	ax_T = ax_n.twinx()
	temp_plot = ax_T.plot(x, temperature, label=r"$T$", color='red')
	ax_T.set_ylabel(r"$T$", fontsize='large', rotation=0, labelpad=20)

	ax_T.set_yticks(numpy.linspace(ax_T.get_yticks()[0], ax_T.get_yticks()[-1],\
			len(ax_n.get_yticks())))

	ax_n.grid(True)
	ax_T.grid(True)
	ax_T.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

	# BOTTOM PLOT
	ax_Z = plt.subplot(2,1,2)
	Z_plot = ax_Z.plot(x, Z, label=r"$Z$", color='green')
	ax_Z.set_ylabel(r"$Z$", fontsize='large', rotation=0, labelpad=20)

	ax_D = ax_Z.twinx()
	D_plot = ax_D.plot(x, Diffusivity, label=r"$D$", color='orange')
	ax_D.set_ylabel(r"$D$", fontsize='large', rotation=0, labelpad=20)

	ax_Z.set_yticks(numpy.linspace(ax_Z.get_yticks()[0], ax_Z.get_yticks()[-1],\
			len(ax_D.get_yticks())))

	ax_Z.grid(True)
	ax_Z.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
	ax_D.grid(True)
	ax_D.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

	ax_Z.set_xlabel(r"$x$", fontsize='large')

	remove_yticks(ax_n, ax_T, ax_Z, ax_D)

	top_plot = density_plot + temp_plot
	top_labels = [l.get_label() for l in top_plot]
	ax_T.legend(top_plot, top_labels, loc='best', fontsize='medium')
	bottom_plot = Z_plot + D_plot
	bottom_labels = [l.get_label() for l in bottom_plot]
	ax_D.legend(bottom_plot, bottom_labels, loc='best')


	fig.suptitle(r"$\Gamma_c = -1.0\times 10^{18}~, ~~ D = 1 / (1 + 0.01\,Z^2 + 0.001\,(Z^\prime)^{-2})$" +"\n"+ "$t = " +str(filename_sans_ext)+ "$")
	fig.tight_layout(pad=0.2, w_pad=0.0)
	plt.subplots_adjust(top=0.9)

#	plt.savefig(data_directory +'/'+ filename_sans_ext +'.png')

	print str(i) + "\t| Saved " + str(filename_sans_ext) + ".png"
	i = i + 1
	plt.clf()

#plt.show()

