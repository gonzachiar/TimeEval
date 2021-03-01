from durations import Duration
from sklearn.model_selection import ParameterGrid

from timeeval import Algorithm
from timeeval.adapters import DockerAdapter
from .common import SKIP_PULL, DEFAULT_TIMEOUT


def knn(params=None, skip_pull: bool = SKIP_PULL, timeout: Duration = DEFAULT_TIMEOUT) -> Algorithm:
    return Algorithm(
        name="kNN-docker",
        main=DockerAdapter(image_name="mut:5000/akita/knn", skip_pull=skip_pull, timeout=timeout),
        param_grid=ParameterGrid(params or {}),
        data_as_file=True
    )
