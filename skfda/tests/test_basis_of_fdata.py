"""Tests of BasisOfFData."""

import unittest

import numpy as np

from skfda.representation.basis import BasisOfFData, FDataBasis, Fourier
from skfda.representation.grid import FDataGrid


class TestBasis(unittest.TestCase):
    """Tests for BasisOfFData."""

    def test_grid(self):
        """Test a datagrid toy example."""
        grid_points = np.array([0, 1, 2])
        sample = FDataGrid(
            data_matrix=np.array([[1, 2, 3], [4, 5, 6]]),
            grid_points=np.array([[0, 1, 2]]),
        )

        data_basis = FDataBasis(
            basis=BasisOfFData(fdata=sample),
            coefficients=np.array([[1, 0], [0, 1], [1, 1]]),
        )

        evaluated = [
            np.array([1, 2, 3]),
            np.array([4, 5, 6]),
            np.array([5, 7, 9]),
        ]

        np.testing.assert_equal(data_basis(grid_points)[..., 0], evaluated)

    def test_basis(self):
        """Test a databasis toy example."""
        basis = Fourier(n_basis=3)
        coeficients = np.array(
            [
                [2, 1, 0],
                [3, 1, 0],
                [1, 2, 9],
            ],
        )

        data_basis = FDataBasis(
            basis=BasisOfFData(
                fdata=FDataBasis(basis=basis, coefficients=coeficients),
            ),
            coefficients=coeficients,
        )

        combined_basis = FDataBasis(
            basis=basis,
            coefficients=coeficients @ coeficients,
        )

        eval_points = np.linspace(0, 1, 100)
        np.testing.assert_almost_equal(
            data_basis(eval_points),
            combined_basis(eval_points),
        )

    def test_not_linearly_independent_too_many(self):
        """
        Test that a non linearly independent basis raises an error.

        In this case, the number of samples is greater than the number
        of sampling points or base functions in the underlying base.
        """
        sample = FDataGrid(
            data_matrix=np.array(
                [[1, 2, 3], [2, 4, 6], [15, 4, -2], [1, 28, 0]],
            ),
            grid_points=np.array([[0, 1, 2]]),
        )

        with self.assertRaises(ValueError):
            BasisOfFData(fdata=sample)

        sample = FDataBasis(
            basis=Fourier(n_basis=3),
            coefficients=np.array(
                [
                    [0, 1, 0],
                    [1, 0, 0],
                    [0, 0, 1],
                    [1, 1, 1],
                ],
            ),
        )

        with self.assertRaises(ValueError):
            BasisOfFData(fdata=sample)

    def test_not_linearly_independent_range(self):
        """
        Test that a non linearly independent basis raises an error.

        In this case, the number of samples is valid but the given
        samples are not linearly independent.
        """
        sample = FDataGrid(
            data_matrix=np.array([[1, 2, 3], [2, 4, 6]]),
            grid_points=np.array([[0, 1, 2]]),
        )

        with self.assertRaises(ValueError):
            BasisOfFData(fdata=sample)

        sample = FDataBasis(
            basis=Fourier(n_basis=3),
            coefficients=np.array(
                [
                    [2, 1, 0],
                    [3, 1, 0],
                    [1, 2, 0],
                ],
            ),
        )

        with self.assertRaises(ValueError):
            BasisOfFData(fdata=sample)

    def test_derivative_grid(self):
        """Test the derivative of a basis constructed from a FDataGrid."""
        base_functions = FDataGrid(
            data_matrix=np.array([[1, 2, 3], [1, 1, 5]]),
            grid_points=np.array([[0, 1, 2]]),
        )
        # The derivative of the first function is always 1
        # The derivative of the second function is 0 and then 4

        basis = BasisOfFData(fdata=base_functions)

        coefs = np.array([[1, 0], [0, 1], [1, 1]])
        derivate_basis, derivative_coefs = basis.derivative_basis_and_coefs(
            coefs=coefs,
            order=1,
        )

        derivative = FDataBasis(
            basis=derivate_basis,
            coefficients=derivative_coefs,
        )

        eval_points = np.array([0.5, 1.5])

        # Derivative of the original functions sampled in the given points
        # and multiplied by the coefs
        derivative_evaluated = np.array([[1, 1], [0, 4], [1, 5]])
        np.testing.assert_equal(
            derivative(eval_points)[..., 0],
            derivative_evaluated,
        )

    def test_derivative_basis(self):
        """Test the derivative of a basis constructed from a FDataBasis."""
        basis_coef = np.array(
            [
                [2, 1, 0, 10, 0],
                [3, 1, 99, 15, 99],
                [0, 2, 9, 22, 0],
            ],
        )

        base_functions = FDataBasis(
            basis=Fourier(n_basis=5),
            coefficients=basis_coef,
        )

        basis = BasisOfFData(fdata=base_functions)

        coefs = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [2, 1, 5]])
        derivate_basis, derivative_coefs = basis.derivative_basis_and_coefs(
            coefs=coefs,
            order=1,
        )

        derivative = FDataBasis(
            basis=derivate_basis,
            coefficients=derivative_coefs,
        )

        eval_points = np.linspace(0, 1, 100)

        # Derivative of the original functions
        basis_derivative, coefs_derivative = Fourier(
            n_basis=5,
        ).derivative_basis_and_coefs(coefs=coefs @ basis_coef)

        derivative_on_the_basis = FDataBasis(
            basis=basis_derivative,
            coefficients=coefs_derivative,
        )

        np.testing.assert_almost_equal(
            derivative(eval_points),
            derivative_on_the_basis(eval_points),
        )

    def test_linearly_dependent_derivatives(self):
        """
        Construct a basis whose derivative is not a basis.

        An error should be raised
        """
        base_functions = FDataGrid(
            data_matrix=np.array([[1, 2, 3], [1, 3, 5]]),
            grid_points=np.array([[0, 1, 2]]),
        )
        # The derivative of the first function is 1
        # The derivative of the second function is 2
        # Therefore, the derivative of the basis is not a basis

        # The basis is linearly independent
        base = BasisOfFData(fdata=base_functions)

        # Its derivative is not linearly independent
        with self.assertRaises(ValueError):
            base.derivative_basis_and_coefs(np.ndarray([1, 1]))


if __name__ == "__main__":
    unittest.main()
