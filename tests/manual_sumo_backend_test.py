from scenario.scenario_generator import Scenario
from simulation.sumo_engine import SumoEngine

# 1. Load minimal scenario config (hardcoded or from YAML)
scenario_config = {
    "type": "grid",
    "grid_size": 2,
    "vehicles_per_hour": 100,
    "accident_probability": 0.0,
    "random_seed": 123,
}
scenario = Scenario(scenario_config).generate()

# 2. Initialize SUMO engine with config
sumo_engine_config = {
    "sumo_binary": "sumo",  # or "sumo-gui" to visualize, if installed
    "step_length": 1.0
}
engine = SumoEngine(sumo_engine_config)

# 3. Load the scenario/build files
engine.load_scenario(scenario)

# 4. Run the simulation
engine.run()

# 5. Retrieve and print metrics
metrics = engine.get_metrics()
print("Simulation metrics:", metrics)