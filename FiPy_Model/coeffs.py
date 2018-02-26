"""
	This file contains the $g$ coefficients and plasma
	parameters for use in the alternate $Z$ equation
	developed by Staps.
	It has been written as a function.
"""

from variable_decl import *

## Plasma Parameters
e_p = 1.0 + (m_i*density + m_e*density) / (epsilon_0 * B**2)

# Neutrals density in use for CX friction
n_0 = CellVariable(name=r"$n_0$", mesh=mesh)
v_Ti = CellVariable(name=r"$v_{th,i}$", mesh=mesh)
v_Te = CellVariable(name=r"$v_{th,e}$", mesh=mesh)
rho_pi = CellVariable(name=r"$\rho_{\theta i}$", mesh=mesh)
rho_pe = CellVariable(name=r"$\rho_{\theta e}$", mesh=mesh)
omega_bi = CellVariable(name=r"$\omega_{bi}$", mesh=mesh)
omega_be = CellVariable(name=r"$\omega_{be}$", mesh=mesh)

## Collision Frequencies
nu_ei = CellVariable(name=r"$\nu_{ei}$", mesh=mesh)
nu_ii = CellVariable(name=r"$\nu_{ii}$", mesh=mesh)
nu_in0 = CellVariable(name=r"$\nu_{i0}$", mesh=mesh)
nu_eff = CellVariable(name=r"$\nu_{eff}$", mesh=mesh)
nu_ai = CellVariable(name=r"$\nu_{*i}$", mesh=mesh)
nu_ae = CellVariable(name=r"$\nu_{*e}$", mesh=mesh)

## Electron Anomalous Diffusion
D_an = CellVariable(name=r"$D_{an}$", mesh=mesh)
g_n_an = CellVariable(name=r"$g_n^{an}$", mesh=mesh)
g_T_an = CellVariable(name=r"$g_T^{an}$", mesh=mesh)
g_Z_an = CellVariable(name=r"$g_Z^{an}$", mesh=mesh)

## Charge Exchange Friction
g_n_cx = CellVariable(name=r"$g_n^{cx}$", mesh=mesh)
g_T_cx = CellVariable(name=r"$g_T^{cx}$", mesh=mesh)
g_Z_cx = CellVariable(name=r"$g_Z^{cx}$", mesh=mesh)

## Ion Bulk (Parallel) Viscosity
# Consolidated constant to reduce clutter, listed as N on reference
N = CellVariable(name="Consolidated Bulk Viscosity value", mesh=mesh)
# xi_p integral
xi_p = CellVariable(name=r"$\xi_\theta$", mesh=mesh)
# xi_t integral
xi_t = CellVariable(name=r"$\xi_\phi$", mesh=mesh)

g_n_bulk = CellVariable(name=r"$g_n^{\pi\parallel}$", mesh=mesh)
g_T_bulk = CellVariable(name=r"$g_T^{\pi\parallel}$", mesh=mesh)
g_Z_bulk = CellVariable(name=r"$g_Z^{\pi\parallel}$", mesh=mesh)

## Ion Orbit Loss
g_OL = CellVariable(name=r"$g^{OL}$", mesh=mesh)
f_OL = CellVariable(name=r"$f^{OL}$", mesh=mesh)

def update_g_coeffs():
	e_p = 1.0 + (m_i*density + m_e*density) / (epsilon_0 * B**2)

	# Neutrals density in use for CX friction
	n_0.setValue(4.0e17 * a_in0 * (temperature / 100.0)**(3.0/4.0))

	v_Ti.setValue((2.0 * charge * temperature / m_i)**(1.0/2.0))

	v_Te.setValue((2.0 * charge * temperature / m_e)**(1.0/2.0))

	rho_pi.setValue(m_i * v_Ti / (charge * B_theta))

	rho_pe.setValue(m_e * v_Te / (charge * B_theta))

	omega_bi.setValue(aspect**(3.0/2.0) * v_Ti / (q * R))

	omega_be.setValue(aspect**(3.0/2.0) * v_Te / (q * R))

	## Collision Frequencies
	nu_ei.setValue(((density) / (temperature))**(3.0/2.0))

	nu_ii.setValue(1.2 * (m_e / m_i)**(1.0/2.0) * nu_ei)

	nu_in0.setValue(a_in0 * omega_bi)

	nu_eff.setValue(nu_ii + nu_in0)

	nu_ai.setValue(nu_ii / omega_bi)	# nu_*i

	nu_ae.setValue(nu_ei / omega_be)	# nu_*e (not used as of now)

	## Consolidated constant to reduce clutter, listed as N on reference
	N.setValue(value = (nu_ai * aspect**(3.0/2.0) * nu_ei / nu_ii))

	## Electron Anomalous Diffusion
	D_an.setValue(((aspect)**2*(pi)**(1.0/2.0) / (2*a_m) * (rho_pe * temperature)/B))
	g_n_an.setValue(-charge*density*D_an)
	g_T_an.setValue(g_n_an * alpha_an)
	g_Z_an.setValue(g_n_an / rho_pi)

	## Charge Exchange Friction
	g_n_cx.setValue((-(m_i*n_0*neu_react_rate) / (B_theta**2)))
	g_T_cx.setValue(alpha_cx * g_n_cx)
	g_Z_cx.setValue(-g_n_cx / rho_pi)

	## Ion Bulk (Parallel) Viscosity
	# xi_p integral
	xi_p.setValue((4.0*N*(27.0*((N)**2 + Z**2)**2 - 7.0*((N)**2 - 3.0*Z**2)*(nu_ai)**(1.0/2.0))*(nu_ai)**(7.0/4)) / (189.0*pi*((N)**2 + Z**2)**3))
	# xi_t integral
	xi_t.setValue((2.0*N*(135.0*((N)**2 + Z**2)**2 - 7.0*(21.0*(N)**4 + 3.0*Z**2*(-5.0 + 7.0*Z**2) + (N)**2*(5.0 + 42.0*Z**2))*(nu_ai)**(1.0/2))*(nu_ai)**(7.0/4)) / (189.0*pi*((N)**2 + Z**2)**3))

	g_n_bulk.setValue(aspect**2*(pi)**(1.0/2) / (8*a_m) * density * m_i * rho_pi * (v_Ti)**2 * B_theta * xi_p)
	g_T_bulk.setValue(aspect**2*(pi)**(1.0/2) / (8*a_m) * density * m_i * rho_pi * (v_Ti)**2 * (B_theta*xi_p - B*xi_t))
	g_Z_bulk.setValue(aspect**2*(pi)**(1.0/2) / (4*a_m) * density * m_i * (v_Ti)**2 * B_theta*xi_p)

	## Ion Orbit Loss
	g_OL.setValue((charge * density * nu_eff * (aspect)**(1.0/2.0) * rho_pi))
	f_OL.setValue(numerix.exp(-(nu_ai + Z**4)**(1.0/2.0))/ (nu_ai + Z**4)**(1.0/2.0))

