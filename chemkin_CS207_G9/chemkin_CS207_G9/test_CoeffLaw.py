from chemkin_CS207_G9.CoeffLaw import *
import numpy as np


# ============ Tests on Results ============ #

T = np.e

a = np.zeros((2,7))
a[0,:] = np.e ** np.arange(0,-7,-1)
a[1,:] = ((-1) ** np.arange(0,7)) * a[0,:]
a[0,5], a[0,6] = np.e/6, 1/5
a[1,5], a[1,6] = -np.e/6, -1/5

nu = np.array([[1,-1],[0,0]])

prob = np.array([[1],[-1]])**np.arange(0,7)

tol = 1e-10

def test_backward_Cp():
    truth = np.sum(prob[:,:5], axis=1)
    res = BackwardLaw().Cp_over_R(a, T)
    assert( np.prod(np.abs(truth-res) < tol) )

def test_backward_H():
    truth = np.sum(prob[:,:6] / np.arange(1,7), axis=1)
    res = BackwardLaw().H_over_RT(a, T)
    assert( np.prod(np.abs(truth-res)< tol) )

def test_backward_S():
    truth = np.sum(prob[:,1:6] / np.arange(1,6), axis=1) + 1
    res = BackwardLaw().S_over_R(a, T)
    assert( np.prod(np.abs(truth-res) < tol) )

def test_backward_ke():
    p0, R = 2, 1/np.e
    H = np.sum(prob[:,:6] / np.arange(1,7), axis=1)
    S = np.sum(prob[:,1:6] / np.arange(1,6), axis=1) + 1
    truth = 2*np.exp(-H[0]+S[0])
    res = BackwardLaw(p0, R).equilibrium_coeffs(nu, a, T)
    assert( res[0]-truth<tol and res[1]-1/truth<tol )



# ============ Tests on Errors ============ #