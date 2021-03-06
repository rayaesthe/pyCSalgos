"""
test_l1min.py

Testing functions for analysisl1min.py

"""

# Author: Nicolae Cleju
# License: BSD 3 clause

import numpy as np
from sklearn.utils.testing import assert_raises
from sklearn.utils.testing import assert_true
from sklearn.utils.testing import assert_equal
from sklearn.utils.testing import assert_allclose

from ..generate import make_analysis_compressed_sensing_problem
from ..analysisl1min import AnalysisL1Min

m, N, n, l, numdata = 16, 25, 20, 18, 10
#rng = np.random.RandomState(47)

SolverClass = AnalysisL1Min

measurements, acqumatrix, data, operator, gamma, cosupport, realdata =\
    make_analysis_compressed_sensing_problem(m,n,N,l, numdata, np.inf, random_state=47)
tol = 1e-6

algorithms = ["nesta"]

def test_correct_shapes():
    stopvals = [1e-6]
    for algo in algorithms:
        for stopval in stopvals:
            yield subtest_correct_shapes, stopval, algo

def subtest_correct_shapes(stopval, algorithm):
    solver = SolverClass(stopval = stopval, algorithm=algorithm)
    # single vector
    recdata = solver.solve(measurements[:,0], acqumatrix, operator)
    assert_equal(recdata.shape, (n,))
    # multiple vectors
    recdata = solver.solve(measurements, acqumatrix, operator)
    assert_equal(recdata.shape, (n, numdata))


def test_tol():
    stopvals = [1e-6]
    for algo in algorithms:
        for stopval in stopvals:
            yield subtest_tol, stopval, algo

def subtest_tol(stopval, algorithm):
    solver = SolverClass(stopval = stopval, algorithm=algorithm)
    recdata = solver.solve(measurements, acqumatrix, operator)
    for i in range(data.shape[1]):
        assert_true(np.sum((measurements[:, i] - np.dot(acqumatrix, recdata[:,i])) ** 2) <= max(stopval, 1e-6))

def test_perfect_signal_recovery():
    stopvals = [1e-6]
    for algo in algorithms:
        for stopval in stopvals:
            yield subtest_perfect_signal_recovery, stopval, algo

def subtest_perfect_signal_recovery(stopval, algorithm):
    solver = SolverClass(stopval = stopval, algorithm=algorithm)
    recdata = solver.solve(measurements, acqumatrix, operator)
    assert_allclose(data, recdata, atol=1e-3)


# def test_solver_reaches_least_squares():
#     for algo in algorithms:
#         yield subtest_solver_reaches_least_squares, algo
#
# def subtest_solver_reaches_least_squares(algorithm):
#     n1 = 10
#     N1 = 8
#     X1 = rng.randn(n1, 3)
#     D1 = rng.randn(n1, N1)
#     for i in range(N1):
#         D1[:,i] = D1[:,i] / np.linalg.norm(D1[:,i])
#     solver = SolverClass(stopval = 1e-6, algorithm=algorithm)
#     coef = solver.solve(X1, D1)
#     lstsq = np.dot(np.linalg.pinv(D1), X1)
#     assert_allclose(coef, lstsq, atol=1e-10)


def test_bad_input():
    assert_raises(ValueError, SolverClass, stopval=-1)

    solver = SolverClass(stopval=1e-6, algorithm="nonexistent")
    assert_raises(ValueError, solver.solve, measurements, acqumatrix, operator)


# # TODO: to reanalyze, didn't figure out what it does
# def test_identical_regressors():
#     newD = D.copy()
#     newD[:, 1] = newD[:, 0]
#     gamma = np.zeros(N)
#     gamma[0] = gamma[1] = 1.
#     newy = np.dot(newD, gamma)
#     solver = SolverClass(stopval=1e-3, algorithm="l1magic")
#     assert_warns(RuntimeWarning, solver.solve, data=newy, dictionary=newD)
#     #assert_warns(RuntimeWarning, orthogonal_mp, newX, newy, 2)
#
#
# # TODO: to reanalyze, didn't figure out what it does
# def test_swapped_regressors():
#     gamma = np.zeros(N)
#     # X[:, 21] should be selected first, then X[:, 0] selected second,
#     # which will take X[:, 21]'s place in case the algorithm does
#     # column swapping for optimization (which is the case at the moment)
#     gamma[21] = 1.0
#     gamma[0] = 0.5
#     new_y = np.dot(D, gamma)
#     new_Xy = np.dot(D.T, new_y)
#     #gamma_hat = orthogonal_mp(X, new_y, 2)
#     gamma_hat = SolverClass(stopval=1e-3).solve(new_y, D)
#     assert_array_equal(np.flatnonzero(gamma_hat), [0, 21])
