from chemkin_CS207_G9.math.ode_solver import solve_ivp
import numpy as np

tol = 1e-2
    
def test_solve_ivp():
    res_int = solve_ivp(
        fun=lambda t,y:y,
        jac=lambda t,y:np.array([[1,0],[0,1]]),
        t_span=(0,3),
        y0=np.array([1,3]),
        method='SIE')
    estim = res_int.sol(3)
    truth = np.array([1,3])*np.exp(3)
    diff = estim - truth
    assert( np.sqrt(np.sum(diff**2)) < tol*np.sqrt(np.sum(truth**2)))