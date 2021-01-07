import numpy as np
import pandas as pd
from typing import List, Callable, Tuple, Any, NamedTuple, Dict, Union, Optional
from collections import defaultdict
import tqdm
from pathlib import Path
import logging
import time

from timeeval.datasets import Datasets
from timeeval.utils.metrics import roc


class Algorithm(NamedTuple):
    name: str
    function: Callable[[Union[np.ndarray, Path]], np.ndarray]
    data_as_file: bool


class Times(NamedTuple):
    pre: Optional[float]
    main: float
    post: Optional[float]

    def to_dict(self) -> Dict:
        return dict(self._asdict())


def timer(fn: Callable, *args, **kwargs) -> Tuple[Any, Times]:
    start = time.time()
    fn_result = fn(*args, **kwargs)
    end = time.time()
    duration = end - start
    return fn_result, Times(pre=None, main=duration, post=None)


class TimeEval:
    def __init__(self,
                 datasets: List[str],
                 algorithms: List[Algorithm],
                 dataset_config: Path):
        self.dataset_names = datasets
        self.algorithms = algorithms
        self.dataset_config = dataset_config

        self.results = defaultdict(dict)

    def _load_dataset(self, name) -> pd.DataFrame:
        return Datasets(name).load(self.dataset_config)

    def _get_dataset_path(self, name) -> Tuple[Path, Path]:
        return Datasets(name).get_path(self.dataset_config)

    def _run_algorithm(self, algorithm: Algorithm):
        for dataset_name in tqdm.tqdm(self.dataset_names, desc=f"Evaluating {algorithm.name}", position=1):
            if algorithm.data_as_file:
                dataset_file, label_file = self._get_dataset_path(dataset_name)
                self._run_from_data_file(algorithm, dataset_file, label_file, dataset_name)
            else:
                dataset = self._load_dataset(dataset_name)
                self._run_w_loaded_data(algorithm, dataset, dataset_name)

    def _run_from_data_file(self, algorithm: Algorithm, dataset_file: Path, label_file: Path, dataset_name: str):
        raise NotImplementedError()

    def _run_w_loaded_data(self, algorithm: Algorithm, dataset: pd.DataFrame, dataset_name: str):
        y_true = dataset.labels.values
        try:
            y_scores = algorithm.function(dataset.data.values)
            score, times = timer(roc, y_scores, y_true, plot=False)

            self._record_results(algorithm.name, dataset_name, score, times)

        except Exception as e:
            logging.error(f"Exception occured during the evaluation of {algorithm.name} on the dataset {dataset_name}:")
            logging.error(str(e))

    def _record_results(self, algorithm_name: str, dataset_name: str, score: float, times: Times):
        result = {
            "auroc": score,
            "times": times.to_dict()
        }
        self.results[algorithm_name][dataset_name] = result

    def run(self):
        assert len(self.algorithms) > 0, "No algorithms given for evaluation"

        for algorithm in tqdm.tqdm(self.algorithms, desc="Evaluating Algorithms", position=0):
            self._run_algorithm(algorithm)
