import abc
from pathlib import Path
from typing import List


class CustomDatasetsBase(abc.ABC):

    @abc.abstractmethod
    def get_dataset_names(self) -> List[str]:
        ...

    @abc.abstractmethod
    def get_path(self, dataset_name: str, train: bool) -> Path:
        ...

    @abc.abstractmethod
    def get_collection_names(self) -> List[str]:
        ...