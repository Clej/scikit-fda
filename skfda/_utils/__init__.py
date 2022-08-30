from typing import TYPE_CHECKING

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submodules=[
        "constants",
    ],
    submod_attrs={
        "_utils": [
            "RandomStateLike",
            "_cartesian_product",
            "_check_array_key",
            "_check_estimator",
            "_classifier_get_classes",
            "_compute_dependence",
            "_DependenceMeasure",
            "_evaluate_grid",
            "_int_to_real",
            "_pairwise_symmetric",
            "_same_domain",
            "_to_grid",
            "_to_grid_points",
            "nquad_vec",
        ],
        '_warping': [
            "invert_warping",
            "normalize_scale",
            "normalize_warping",
        ],
    },
)

if TYPE_CHECKING:

    from ._utils import (
        RandomStateLike,
        _cartesian_product,
        _check_array_key,
        _check_estimator,
        _classifier_get_classes,
        _compute_dependence,
        _DependenceMeasure,
        _evaluate_grid,
        _int_to_real,
        _pairwise_symmetric,
        _same_domain,
        _to_grid,
        _to_grid_points,
        nquad_vec,
    )

    from ._warping import invert_warping, normalize_scale, normalize_warping
