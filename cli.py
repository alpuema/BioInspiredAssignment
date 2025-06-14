from config.config_loader import get_config
from scenario.scenario_generator import Scenario
from simulation.sumo_engine import SumoEngine

def main():
    config = get_config()
    scenario_cfg = config['scenario']
    sim_cfg = config['simulation']

    scenario = Scenario(scenario_cfg).generate()
    engine = SumoEngine(sim_cfg)
    engine.load_scenario(scenario)
    engine.run()
    metrics = engine.get_metrics()
    print("Simulation metrics:", metrics)

if __name__ == "__main__":
    main()