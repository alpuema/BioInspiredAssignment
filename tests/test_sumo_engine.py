import pytest
from simulation.sumo_engine import SumoEngine

class DummyScenarioBuilder:
    def __init__(self, scenario):
        pass
    def build(self):
        return "dummy.sumocfg"

def test_sumo_engine_load(monkeypatch):
    engine = SumoEngine({"sumo_binary": "sumo"})
    monkeypatch.setattr("simulation.sumo_engine.SumoScenarioBuilder", DummyScenarioBuilder)
    engine.load_scenario({"nodes": [], "edges": [], "vehicles_per_hour": 10})
    assert engine.sumo_config_file == "dummy.sumocfg"