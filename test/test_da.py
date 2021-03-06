"""Tests for module da on Domain Adaptation """

# Author: Remi Flamary <remi.flamary@unice.fr>
#
# License: MIT License

import numpy as np
from numpy.testing.utils import assert_allclose, assert_equal

import ot
from ot.datasets import get_data_classif
from ot.utils import unif


def test_sinkhorn_lpl1_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    otda = ot.da.SinkhornLpl1Transport()

    # test its computed
    otda.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert hasattr(otda, "cost_")
    assert hasattr(otda, "coupling_")

    # test dimensions of coupling
    assert_equal(otda.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = otda.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = otda.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = otda.fit_transform(Xs=Xs, ys=ys, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test unsupervised vs semi-supervised mode
    otda_unsup = ot.da.SinkhornLpl1Transport()
    otda_unsup.fit(Xs=Xs, ys=ys, Xt=Xt)
    n_unsup = np.sum(otda_unsup.cost_)

    otda_semi = ot.da.SinkhornLpl1Transport()
    otda_semi.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(otda_semi.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(otda_semi.cost_)

    # check that the cost matrix norms are indeed different
    assert n_unsup != n_semisup, "semisupervised mode not working"

    # check that the coupling forbids mass transport between labeled source
    # and labeled target samples
    mass_semi = np.sum(
        otda_semi.coupling_[otda_semi.cost_ == otda_semi.limit_max])
    assert mass_semi == 0, "semisupervised mode not working"


def test_sinkhorn_l1l2_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    otda = ot.da.SinkhornL1l2Transport()

    # test its computed
    otda.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert hasattr(otda, "cost_")
    assert hasattr(otda, "coupling_")
    assert hasattr(otda, "log_")

    # test dimensions of coupling
    assert_equal(otda.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = otda.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = otda.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = otda.fit_transform(Xs=Xs, ys=ys, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test unsupervised vs semi-supervised mode
    otda_unsup = ot.da.SinkhornL1l2Transport()
    otda_unsup.fit(Xs=Xs, ys=ys, Xt=Xt)
    n_unsup = np.sum(otda_unsup.cost_)

    otda_semi = ot.da.SinkhornL1l2Transport()
    otda_semi.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(otda_semi.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(otda_semi.cost_)

    # check that the cost matrix norms are indeed different
    assert n_unsup != n_semisup, "semisupervised mode not working"

    # check that the coupling forbids mass transport between labeled source
    # and labeled target samples
    mass_semi = np.sum(
        otda_semi.coupling_[otda_semi.cost_ == otda_semi.limit_max])
    mass_semi = otda_semi.coupling_[otda_semi.cost_ == otda_semi.limit_max]
    assert_allclose(mass_semi, np.zeros_like(mass_semi),
                    rtol=1e-9, atol=1e-9)

    # check everything runs well with log=True
    otda = ot.da.SinkhornL1l2Transport(log=True)
    otda.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert len(otda.log_.keys()) != 0


def test_sinkhorn_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    otda = ot.da.SinkhornTransport()

    # test its computed
    otda.fit(Xs=Xs, Xt=Xt)
    assert hasattr(otda, "cost_")
    assert hasattr(otda, "coupling_")
    assert hasattr(otda, "log_")

    # test dimensions of coupling
    assert_equal(otda.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = otda.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = otda.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = otda.fit_transform(Xs=Xs, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test unsupervised vs semi-supervised mode
    otda_unsup = ot.da.SinkhornTransport()
    otda_unsup.fit(Xs=Xs, Xt=Xt)
    n_unsup = np.sum(otda_unsup.cost_)

    otda_semi = ot.da.SinkhornTransport()
    otda_semi.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(otda_semi.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(otda_semi.cost_)

    # check that the cost matrix norms are indeed different
    assert n_unsup != n_semisup, "semisupervised mode not working"

    # check that the coupling forbids mass transport between labeled source
    # and labeled target samples
    mass_semi = np.sum(
        otda_semi.coupling_[otda_semi.cost_ == otda_semi.limit_max])
    assert mass_semi == 0, "semisupervised mode not working"

    # check everything runs well with log=True
    otda = ot.da.SinkhornTransport(log=True)
    otda.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert len(otda.log_.keys()) != 0


def test_emd_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    otda = ot.da.EMDTransport()

    # test its computed
    otda.fit(Xs=Xs, Xt=Xt)
    assert hasattr(otda, "cost_")
    assert hasattr(otda, "coupling_")

    # test dimensions of coupling
    assert_equal(otda.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = otda.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = otda.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = otda.fit_transform(Xs=Xs, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test unsupervised vs semi-supervised mode
    otda_unsup = ot.da.EMDTransport()
    otda_unsup.fit(Xs=Xs, ys=ys, Xt=Xt)
    n_unsup = np.sum(otda_unsup.cost_)

    otda_semi = ot.da.EMDTransport()
    otda_semi.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(otda_semi.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(otda_semi.cost_)

    # check that the cost matrix norms are indeed different
    assert n_unsup != n_semisup, "semisupervised mode not working"

    # check that the coupling forbids mass transport between labeled source
    # and labeled target samples
    mass_semi = np.sum(
        otda_semi.coupling_[otda_semi.cost_ == otda_semi.limit_max])
    mass_semi = otda_semi.coupling_[otda_semi.cost_ == otda_semi.limit_max]

    # we need to use a small tolerance here, otherwise the test breaks
    assert_allclose(mass_semi, np.zeros_like(mass_semi),
                    rtol=1e-2, atol=1e-2)


def test_mapping_transport_class():
    """test_mapping_transport
    """

    ns = 60
    nt = 120

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)
    Xs_new, _ = get_data_classif('3gauss', ns + 1)

    ##########################################################################
    # kernel == linear mapping tests
    ##########################################################################

    # check computation and dimensions if bias == False
    otda = ot.da.MappingTransport(kernel="linear", bias=False)
    otda.fit(Xs=Xs, Xt=Xt)
    assert hasattr(otda, "coupling_")
    assert hasattr(otda, "mapping_")
    assert hasattr(otda, "log_")

    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.mapping_.shape, ((Xs.shape[1], Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # check computation and dimensions if bias == True
    otda = ot.da.MappingTransport(kernel="linear", bias=True)
    otda.fit(Xs=Xs, Xt=Xt)
    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.mapping_.shape, ((Xs.shape[1] + 1, Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    ##########################################################################
    # kernel == gaussian mapping tests
    ##########################################################################

    # check computation and dimensions if bias == False
    otda = ot.da.MappingTransport(kernel="gaussian", bias=False)
    otda.fit(Xs=Xs, Xt=Xt)

    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.mapping_.shape, ((Xs.shape[0], Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # check computation and dimensions if bias == True
    otda = ot.da.MappingTransport(kernel="gaussian", bias=True)
    otda.fit(Xs=Xs, Xt=Xt)
    assert_equal(otda.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(otda.mapping_.shape, ((Xs.shape[0] + 1, Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(
        np.sum(otda.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(
        np.sum(otda.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = otda.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = otda.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # check everything runs well with log=True
    otda = ot.da.MappingTransport(kernel="gaussian", log=True)
    otda.fit(Xs=Xs, Xt=Xt)
    assert len(otda.log_.keys()) != 0


def test_linear_mapping():

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    A, b = ot.da.OT_mapping_linear(Xs, Xt)

    Xst = Xs.dot(A) + b

    Ct = np.cov(Xt.T)
    Cst = np.cov(Xst.T)

    np.testing.assert_allclose(Ct, Cst, rtol=1e-2, atol=1e-2)


def test_linear_mapping_class():

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    otmap = ot.da.LinearTransport()

    otmap.fit(Xs=Xs, Xt=Xt)
    assert hasattr(otmap, "A_")
    assert hasattr(otmap, "B_")
    assert hasattr(otmap, "A1_")
    assert hasattr(otmap, "B1_")

    Xst = otmap.transform(Xs=Xs)

    Ct = np.cov(Xt.T)
    Cst = np.cov(Xst.T)

    np.testing.assert_allclose(Ct, Cst, rtol=1e-2, atol=1e-2)


def test_otda():

    n_samples = 150  # nb samples
    np.random.seed(0)

    xs, ys = ot.datasets.get_data_classif('3gauss', n_samples)
    xt, yt = ot.datasets.get_data_classif('3gauss2', n_samples)

    a, b = ot.unif(n_samples), ot.unif(n_samples)

    # LP problem
    da_emd = ot.da.OTDA()     # init class
    da_emd.fit(xs, xt)       # fit distributions
    da_emd.interp()    # interpolation of source samples
    da_emd.predict(xs)    # interpolation of source samples

    np.testing.assert_allclose(a, np.sum(da_emd.G, 1))
    np.testing.assert_allclose(b, np.sum(da_emd.G, 0))

    # sinkhorn regularization
    lambd = 1e-1
    da_entrop = ot.da.OTDA_sinkhorn()
    da_entrop.fit(xs, xt, reg=lambd)
    da_entrop.interp()
    da_entrop.predict(xs)

    np.testing.assert_allclose(
        a, np.sum(da_entrop.G, 1), rtol=1e-3, atol=1e-3)
    np.testing.assert_allclose(b, np.sum(da_entrop.G, 0), rtol=1e-3, atol=1e-3)

    # non-convex Group lasso regularization
    reg = 1e-1
    eta = 1e0
    da_lpl1 = ot.da.OTDA_lpl1()
    da_lpl1.fit(xs, ys, xt, reg=reg, eta=eta)
    da_lpl1.interp()
    da_lpl1.predict(xs)

    np.testing.assert_allclose(a, np.sum(da_lpl1.G, 1), rtol=1e-3, atol=1e-3)
    np.testing.assert_allclose(b, np.sum(da_lpl1.G, 0), rtol=1e-3, atol=1e-3)

    # True Group lasso regularization
    reg = 1e-1
    eta = 2e0
    da_l1l2 = ot.da.OTDA_l1l2()
    da_l1l2.fit(xs, ys, xt, reg=reg, eta=eta, numItermax=20, verbose=True)
    da_l1l2.interp()
    da_l1l2.predict(xs)

    np.testing.assert_allclose(a, np.sum(da_l1l2.G, 1), rtol=1e-3, atol=1e-3)
    np.testing.assert_allclose(b, np.sum(da_l1l2.G, 0), rtol=1e-3, atol=1e-3)

    # linear mapping
    da_emd = ot.da.OTDA_mapping_linear()     # init class
    da_emd.fit(xs, xt, numItermax=10)       # fit distributions
    da_emd.predict(xs)    # interpolation of source samples

    # nonlinear mapping
    da_emd = ot.da.OTDA_mapping_kernel()     # init class
    da_emd.fit(xs, xt, numItermax=10)       # fit distributions
    da_emd.predict(xs)    # interpolation of source samples
