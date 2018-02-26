"""
	This file deals with all of the inputs for the system.

	Each possible input also has a default value, if nothing is set.
"""
import sys

# Import variables from job configuration file
config = __import__ (sys.argv[1].replace('.py',''))


parameter_sets = ["staps", "paquay", "g_grad", "gradient_model"]
diffusivity_models = ["d_zohm", "d_staps", "d_shear", "d_flow_shear"]


# -------------- Check Configuration Variables ------------
# Check the choice for numerical parameters
if (getattr(config, 'numerical_choice', "").lower() not in parameter_sets\
		or type(getattr(config, 'numerical_choice', None)) != str):
	try:
		config.numerical_choice =\
			raw_input("The set of parameters not properly chosen. Choose from the following: Staps, Paquay -> ")

		if config.numerical_choice.lower() not in parameter_sets:
			raise TypeError

	except (EOFError, TypeError):
		config.numerical_choice = "Paquay"
		print "Numerical choice defaulted to Paquay's set."


# Grid points
if (type(getattr(config, 'nx', None)) != int or\
		getattr(config, 'nx', None) <= 0):
	try:
		config.nx = int(input("nx (Grid number) not properly defined. Enter a positive integer value: "))

		if config.nx <= 0:
			raise ValueError

		print "nx set to " + str(config.nx)

	except (EOFError, NameError, SyntaxError, ValueError) as e:
		config.nx = 100
		print "nx defaulted to 100."


# Domain size
if (type(getattr(config, 'L', None)) != float or\
		getattr(config, 'L', None) <= 0.0):
	try:
		config.L = float(input("Length of domain not properly defined. Enter floating-point value: "))

		if config.L <= 0:
			raise NameError

		print "L set to " + str(config.L)

	except (NameError, SyntaxError, EOFError, ValueError):
		config.L = 4.0
		print "L defaulted to 4.0"


# Choice of the diffusivity model
if (getattr(config, 'D_choice', "").lower() not in diffusivity_models or\
		type(getattr(config, 'D_choice', None)) != str):
	try:
		config.D_choice = raw_input("The diffusivity model is not properly chosen. Choose from the following: Zohm, Staps, Shear -> ")

		if config.D_choice.lower() not in diffusivity_models:
			raise IndexError()

	except (IndexError, EOFError):
		config.D_choice = "d_staps"
		print "Diffusivity model defaulted to Staps'."


# Initial starting mode
if type(getattr(config, 'initial_H_mode', None) != bool):
	config.initial_H_mode = False
	print "Defaulted to starting in L--mode."


# Total number of time steps
if (type(getattr(config, 'total_time', None)) != int or\
		getattr(config, 'total_time', None) <= 0):
	try:
		config.total_time = int(input("Total number of time steps not properly defined. Enter integer value: "))

		if config.total_time <= 0:
			raise ValueError

		print "Total # of time steps set to " + str(config.total_time)

	except (NameError, SyntaxError, EOFError, ValueError):
		config.total_time = 100
		print "Total time steps defaulted to 100."


# Denominator of the delta t
if (type(getattr(config, 'timeStep_denom', None)) != float or\
		getattr(config, 'timeStep_denom', None) <= 0.0):
	try:
		config.timeStep_denom = float(input("The denomintor of the time step size is not properly defined. Enter floating-point value: "))

		if config.timeStep_denom <= 0:
			raise ValueError

		print "The denominator of the time step size is set to "\
				+ str(config.timeStep_denom)

	except (NameError, SyntaxError, EOFError, ValueError):
		config.timeStep_denom = 15.0
		print "The denominator of the time step size is defaulted to 15.0"


# Plot title
if getattr(config, 'plot_title', None) != str:
	try:
		config.plot_title = raw_input("Set the title of the plots: ")
	except:
		config.plot_title = ""


# If saving data is enabled, but not a directory, exit the run.
if (getattr(config, 'save_directory', None) == None and\
		(getattr(config, 'save_plots', False) == True or\
		getattr(config, 'save_TSVs', False) == True)):
	sys.exit("No directory specified for saving specified files. Exiting...")
