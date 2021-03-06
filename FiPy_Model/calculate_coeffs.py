"""
	This file contains the $g$ coefficients and plasma
	parameters for use in the alternate $Z$ equation
	developed by Staps.
	It has been written as a function as to be called within
	the solving loop.
"""

from variable_decl import *

import scipy.special		# For the Faddeeva (plasma dispersion) function
import numpy


# ASSUMES density is in m^-3 and temperature is in eV
def calculate_coeffs():
	# Thermal velocities (most probable)
	v_Ti.setValue(numerix.sqrt(2.0 * charge * temperature / m_i))	# [m/s]
	v_Te.setValue(numerix.sqrt(2.0 * charge * temperature / m_e))	# [m/s]

	# Neutrals density in use for CX friction, NEEDS CHANGE!
	# The commented version cannot be properly computed
#	n_0.setValue((-0.1*config.Gamma_c / v_Ti) * numerix.exp(\
#			-numerix.sqrt(sigma_ion*cx_rate) * density[0]\
#			* numerix.exp(x * density.grad[0]/density)))		# [m^-3]
	# NEED dynamic definition!
	n_0.setValue((-0.1*config.Gamma_c / v_Ti) / (1.0 +\
			numerix.exp(1.0e3*(x-0.02))))						# [m^-3]

	# Poloidal gyro-(Larmor) radii
	rho_pi.setValue(m_i * v_Ti / (charge * B_theta))			# [m]
	rho_pe.setValue(m_e * v_Te / (charge * B_theta))			# [m]

	# Transition frequency
	omega_t.setValue(v_Ti / (q*R))

	# Banana orbit bounce frequencies
	omega_bi.setValue(numerix.sqrt(aspect**3) * omega_t)		# [s^-1]
	omega_be.setValue(numerix.sqrt(aspect**3) * v_Te / (q * R))	# [s^-1]

	# Banana width
	w_bi.setValue(numerix.sqrt(aspect) * rho_pi)				# [m]

	# Collision frequencies within electrons and ions
	nu_ei.setValue(4.2058e-11*(density)\
			/ numerix.sqrt(temperature**3))						# [s^-1]
	nu_ii.setValue(1.2 * numerix.sqrt(m_e / m_i) * nu_ei)		# [s^-1]

	# Collision frequency of trapped ions and neutrals, DEPRICATED
	#nu_in0.setValue(a_in0 * omega_bi)							# [s^-1]

	# Effective detrapping frequency, DEPRICATED
	#nu_eff.setValue(nu_ii + nu_in0)								# [s^-1]

	# Effective collision frequencies
	nu_ai.setValue(nu_ii / omega_bi)	# nu_*i
	nu_ae.setValue(nu_ei / omega_be)	# nu_*e (not used as of now)


	## Electron Anomalous Diffusion
	D_an.setValue(aspect**2 * numerix.sqrt(pi) * rho_pe * (temperature/charge)\
			/ (2*a_m * B))
	g_n_an.setValue(charge * density * D_an)					# [A m^-2]
	g_T_an.setValue(g_n_an * alpha_an)							# [A m^-2]
	g_Z_an.setValue(g_n_an / rho_pi)							# [A m^-1]

	Gamma_an.setValue(g_n_an * density.grad[0]\
			/ density + g_T_an * temperature.grad[0] / temperature\
			+ g_Z_an * Z)							# [m^-2 s^-1]


	## Charge Exchange Friction
	ionization_rate.setValue(5.0e-14 * (100.0 * temperature)\
			**(-1.0/4.0))	# Itoh 1989							# [m^3 s^-1]

	# Rozhansky cx rate
#	cx_rate.setValue(1.985e-14 * numerix.sqrt(temperature))		# [m^3 s^-1]

	cx_rate.setValue(1.0e-14 * (100*temperature)\
			**(1.0 / 3.0))	# Itoh 1989							# [m^3 s^-1]

	g_n_cx.setValue((-(m_i * n_0 * cx_rate * density\
			* (temperature/charge)) / (B_theta**2))\
			* ((B_theta**2 / (aspect * B_phi)**2) + 2.0))		# [A m^-2]
	g_T_cx.setValue(alpha_cx * g_n_cx)							# [A m^-2]
	g_Z_cx.setValue(g_n_cx / rho_pi)							# [A m^-1]

	Gamma_cx.setValue(g_n_cx * density.grad[0] / density\
			+ g_T_cx * temperature.grad[0] / temperature\
			+ g_Z_cx*Z)											# [m^-2 s^-1]


	## Ion Bulk (Parallel) Viscosity
	plasma_disp.setValue(numpy.imag(1j * numerix.sqrt(pi)\
			* scipy.special.wofz(Z + 1j*nu_ii / omega_t)))
#	plasma_disp.setValue(numerix.sqrt(pi) * numerix.exp(-Z**2))
	D_bulk.setValue(aspect**2 * rho_pi * temperature\
			/ ((x - a_m) * B * numerix.sqrt(pi)))				# [m^2 s^-1]

	Gamma_bulk.setValue(density * D_bulk * (density.grad[0] / density\
#			+ 1.2*temperature.grad[0] / temperature\
			+ Z / rho_pi) * plasma_disp)						# [m^-2 s^-1]


	## Ion Orbit Loss
	g_ol.setValue(-charge * density * nu_ii * nu_ai * rho_pi)	# [A m^-2]
	radical_ol = numerix.sqrt(nu_ai + (Z)**4 + ((x) / w_bi)**4)

	Gamma_ol.setValue(g_ol * numerix.exp(-radical_ol)\
			/ (charge * radical_ol))							# [m^-2 s^-1]

