from abc import ABC, abstractmethod
import numpy as np
from typing import Any

class ImageProcessing(ABC):
    @abstractmethod
    def run(self, image: np.ndarray) -> Any:
        pass