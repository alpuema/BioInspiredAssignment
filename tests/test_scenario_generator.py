import pytest
from scenario.scenario_generator import Scenario

def test_generate_returns_expected_keys():
    config = {
        "type": "grid",  # <-- add this line!
        "grid_size": 3,
        "vehicles_per_hour": 1000,
        "accident_probability": 0.01,
        "random_seed": 42,
    }
    scenario = Scenario(config).generate()
    assert "nodes" in scenario
    assert "edges" in scenario
    assert "vehicles_per_hour" in scenario
    assert isinstance(scenario["nodes"], list)
    assert isinstance(scenario["edges"], list)