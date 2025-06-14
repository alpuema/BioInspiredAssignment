from abc import ABC, abstractmethod

class SimulationEngine(ABC):
    @abstractmethod
    def load_scenario(self, scenario):
        pass

    @abstractmethod
    def run(self, control_params=None):
        pass

    @abstractmethod
    def get_metrics(self):
        pass