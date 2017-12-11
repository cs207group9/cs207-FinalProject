import numpy as np
import scipy.interpolate
import warnings

def solve_ivp(
        fun, jac, t_span, y0, method='SIE', 
        max_step=np.inf, rtol=1e-3, atol=1e-6, 
        interpolater=scipy.interpolate.CubicSpline,
        **options):
    '''solves an ivp problem, can be used in a similar manner as scipy.integrate.solve_ivp
    this solver is made for implicit methods, so `jac` (jacobian) is required

    currently supports methods:
        SIE:            semi-implicit extrapolation, an easy-implementing method. 
                        it's accurate to O(h), with addaptive stepsize control.
                        its accuracy and time consumption are not good.

    INPUTS:
        fun:            fun(t,y) gives dy/dt, returning in n array
        jac:            jac(t,y) gives dfun/dy, returning in n*n array
        t_span:         2-tuple of float, i.e. (time_init, time_bound)
        y0:             n array, y value at t_span[0]
        method:         str, solver method, defaults 'SIE'
        max_step:       int, max_step in t_span division, defaults np.inf
        rtol:           float, relative error tolerance, defaults 1e-3
        atol:           float, absolute error tolerance, defaults 1e-6
        interpolater:   scipy.interpolate type, for density output, defaults CubicSpline
        options:        other keyword options for the specified solver method

    OUTPUTS:
        output_sol:     DenseOutput object
                        output_sol.sol(t) gives y(t) by interpolation of `interpolater`

    '''

    if method == 'SIE':
        solver = SemiImplicitExtrapolation(fun, jac)

    t_sol, y_sol = solver.solve(
        y0, t_span[0], t_span[1], max_step, rtol, atol, **options)
    output_sol = DenseOutput(interpolater).fit(t_sol, y_sol)

    return output_sol



class SemiImplicitExtrapolation:

    '''semi-implicit extrapolation ode solver

    ATTRIBUTES:
        fun:    fun(t,y) gives dy/dt, returning in n array
        jac:    jac(t,y) gives dfun/dy, returning in n*n array

    METHODS:
        judge_err:          given estimated y and yhat, judge if the error is within atol and rtol
        take_step:          propogate y by a step of size h, also return a flag indicating convergence
        solve_step_fixed:   solve the ode on n-division of t_span, also return a flag indicating convergence
        solve:              iterate on n_step and each time calls `solve_step_fixed`,
                            at the meantime evaluate the solutions until it meets `judge_err`,
                            return the final time grid and the ys,
                            errs when it cannot converge within max_step,
                            warns when it cannot converge to required accuracy within max_step
    '''

    def __init__(self, fun, jac):
        self.fun = fun
        self.jac = jac

    def judge_err(self, yhat, y, atol, rtol):
        '''prob: norm(yhat-y) < atol + rtol * norm(yhat)
        the norm here is taken as 2-norm on vector'''
        diff_norm = np.sqrt(np.sum((yhat-y)**2))
        yhat_norm = np.sqrt(np.sum(yhat**2))
        return (diff_norm < atol+rtol*yhat_norm)

    def take_step(self, h, t, y):
        '''solve: (1-h*jac).(y'-y)=h*fun
        in an implicit manner'''
        mat_left = np.eye(len(y)) - h * self.jac(t+h, y)
        vec_right = h * self.fun(t+h, y)

        flag = True
        try:
            y_step = np.linalg.solve(mat_left, vec_right)
            y_new = y + y_step
        except np.linalg.LinAlgError: # singular matrix
            y_new = y
            flag = False

        return y_new, flag

    def solve_step_fixed(self, y0, t_start, t_end, n_step):

        n_dim = len(y0)
        h = (t_end - t_start) / n_step
        t_sol = np.arange(t_start, t_end+h, h)
        y_sol = np.zeros((n_dim, n_step+1))
        y_sol[:,0] = y0

        flag = True
        for i in range(1, n_step+1):
            t = t_sol[i]
            y_now = y_sol[:,i-1]
            y_new, flag = self.take_step(h, t, y_now)
            if flag:
                y_sol[:,i] = y_new
            else:
                break

        return t_sol, y_sol, flag

    def solve(self, y0, t_start, t_end, max_step=np.inf, rtol=1e-3, atol=1e-6):

        # just to start with
        n_step = 128
        flag_first = False
        while (n_step < max_step):
            t_sol, y_sol, flag_first \
                = self.solve_step_fixed(y0, t_start, t_end, n_step)
            n_step *= 2
            if flag_first:
                break
        if not flag_first:
            raise np.linalg.LinAlgError('Evaluation cannot converge within max_step.')

        flag_sol = False
        while (n_step < max_step):
            t_sol_new, y_sol_new, flag_new \
                = self.solve_step_fixed(y0, t_start, t_end, n_step)
            n_step *= 2
            if not flag_new:
                continue
            if self.judge_err(y_sol_new[:,-1], y_sol[:,-1], atol, rtol):
                flag_sol = True
                break
            t_sol, y_sol = t_sol_new, y_sol_new

        if not flag_sol:
            warnings.warn('''The ode solver has reached its max_step, '''
                          '''but the solution has not converged to the required accuracy.''')

        return t_sol, y_sol


class DenseOutput:
    '''the output class of solve_ivp
    creates an interplation of what was returned by solver methods'''

    def __init__(self, interpolater):
        self.interp = interpolater
        self.t = None
        self.y = None
        self.f = None

    def fit(self, t_sol, y_sol):
        self.t = t_sol
        self.y = y_sol
        self.f = self.interp(t_sol, y_sol.T)
        return self

    def sol(self, t):
        return self.f(t).T
