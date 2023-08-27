from abc import ABC, abstractmethod


class AlgorithmsBase(ABC):
    """
    Base class for algorithms
    """

    @property
    @abstractmethod
    def stocks_list_for_algo(self):
        pass

    @property
    @abstractmethod
    def result_csv_for_algo(self):
        pass

    @abstractmethod
    def start_back_testing(self):
        pass

    @abstractmethod
    def check_for_trades(self):
        pass
