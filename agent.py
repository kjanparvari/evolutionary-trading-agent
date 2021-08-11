import numpy as np


class Agent:

    def __init__(self):
        from nn import NN
        # gained money for [train, validation, test] phases
        self._fitness = {
            "train": 0.,
            "validation": 0.,
            "test": 0.
        }
        self.nn = NN([3, 6, 12, 6, 3])

    @property  # train fitness
    def trf(self) -> float:
        return self._fitness["train"]

    @trf.setter
    def trf(self, value: float) -> None:
        self._fitness["train"] = value

    @property  # validation fitness
    def vlf(self) -> float:
        return self._fitness["validation"]

    @vlf.setter
    def vlf(self, value: float) -> None:
        self._fitness["validation"] = value

    @property  # test fitness
    def tsf(self) -> float:
        return self._fitness["test"]

    @tsf.setter
    def tsf(self, value: float) -> None:
        self._fitness["test"] = value

    def think(self, closes: list, data: np.ndarray) -> int:
        """
        gives input data to neural network and decide to buy, hold or sell
        :param closes: list of close data
        :param data: list of np arrays which contains custom inputs
        :return 1 for buy, 0 for hold and -1 for sell
        """
        result = self.nn.forward(data).argmax() - 1
        return result

    def copy(self):
        new_agent = Agent()
        new_agent.nn = self.nn.copy()
        new_agent.trf = self.trf
        new_agent.vlf = self.vlf
        new_agent.tsf = self.tsf
        return new_agent
