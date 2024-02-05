# DO NOT EDIT THIS FILE!
# This file was automatically generated using the timeeval_experiments.generator from the template:
# timeeval_experiments/generator/templates/docker-algorithm.py.jinja
from durations import Duration
from typing import Any, Dict, Optional

from timeeval import Algorithm, TrainingType, InputDimensionality
from timeeval.adapters import DockerAdapter
from timeeval.params import ParameterConfig


_iforest_parameters: Dict[str, Dict[str, Any]] = {
 "bootstrap": {
  "defaultValue": "False",
  "description": "If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed.",
  "name": "bootstrap",
  "type": "boolean"
 },
 "max_features": {
  "defaultValue": 1.0,
  "description": "The number of features to draw from X to train each base estimator: `max_features * X.shape[1]`.",
  "name": "max_features",
  "type": "float"
 },
 "max_samples": {
  "defaultValue": None,
  "description": "The number of samples to draw from X to train each base estimator: `max_samples * X.shape[0]`. If unspecified (`None`), then `max_samples=min(256, n_samples)`.",
  "name": "max_samples",
  "type": "float"
 },
 "n_jobs": {
  "defaultValue": 1,
  "description": "The number of jobs to run in parallel. If -1, then the number of jobs is set to the number of cores.",
  "name": "n_jobs",
  "type": "int"
 },
 "n_trees": {
  "defaultValue": 100,
  "description": "The number of decision trees (base estimators) in the forest (ensemble).",
  "name": "n_trees",
  "type": "int"
 },
 "random_state": {
  "defaultValue": 42,
  "description": "Seed for random number generation.",
  "name": "random_state",
  "type": "int"
 },
 "verbose": {
  "defaultValue": 0,
  "description": "Controls the verbosity of the tree building process logs.",
  "name": "verbose",
  "type": "int"
 }
}


def iforest(params: Optional[ParameterConfig] = None, skip_pull: bool = False, timeout: Optional[Duration] = None) -> Algorithm:
    """Isolation Forest (iForest)

    Implementation of https://doi.org/10.1145/2133360.2133363.


    **Algorithm Parameters:**

    n_trees: int
        The number of decision trees (base estimators) in the forest (ensemble). (default: ``100``)
    max_samples: float
        The number of samples to draw from X to train each base estimator: `max_samples * X.shape[0]`. If unspecified (`null`), then `max_samples=min(256, n_samples)`. (default: ``None``)
    max_features: float
        The number of features to draw from X to train each base estimator: `max_features * X.shape[1]`. (default: ``1.0``)
    bootstrap: boolean
        If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed. (default: ``false``)
    random_state: int
        Seed for random number generation. (default: ``42``)
    verbose: int
        Controls the verbosity of the tree building process logs. (default: ``0``)
    n_jobs: int
        The number of jobs to run in parallel. If -1, then the number of jobs is set to the number of cores. (default: ``1``)

    Parameters
    ----------
    params : Optional[ParameterConfig]
        Parameter configuration for the algorithm
    skip_pull : bool
        Set to ``True`` to skip pulling the Docker image and use a local image instead.
        If the image is not present locally, this will raise an error.
    timeout : Optional[Duration]
        Set an individual execution and training timeout for this algorithm.
        This will overwrite the global timeouts set using :class:`~timeeval.ResourceConstraints`.

    Returns
    -------
    ~timeeval.Algorithm
        A correctly configured :class:`~timeeval.Algorithm` object for the Isolation Forest (iForest) algorithm.
    """
    return Algorithm(
        name="Isolation Forest (iForest)",
        main=DockerAdapter(
            image_name="ghcr.io/timeeval/iforest",
            tag="0.3.1",
            skip_pull=skip_pull,
            timeout=timeout,
            group_privileges="akita",
        ),
        preprocess=None,
        postprocess=None,
        param_schema=_iforest_parameters,
        param_config=params or ParameterConfig.defaults(),
        data_as_file=True,
        training_type=TrainingType.UNSUPERVISED,
        input_dimensionality=InputDimensionality("multivariate")
    )
