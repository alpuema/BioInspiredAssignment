import traci
from simulation.sim_interface import SimulationEngine
from simulation.sumo_scenario_builder import SumoScenarioBuilder

class SumoEngine(SimulationEngine):
    def __init__(self, config):
        self.config = config
        self.sumo_binary = config.get("sumo_binary", "sumo")
        self.step_length = config.get("step_length", 1.0)
        self.sumo_config_file = None
        self.metrics = {}

    def load_scenario(self, scenario):
        builder = SumoScenarioBuilder(scenario)
        self.sumo_config_file = builder.build()

    def run(self, control_params=None):
        sumo_cmd = [self.sumo_binary, "-c", self.sumo_config_file, "--step-length", str(self.step_length)]
        traci.start(sumo_cmd)
        step = 0
        travel_times = []
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            for veh_id in traci.simulation.getArrivedIDList():
                travel_times.append(traci.vehicle.getAccumulatedWaitingTime(veh_id))
            step += 1
        traci.close()
        self.metrics = {
            "avg_travel_time": sum(travel_times)/len(travel_times) if travel_times else 0.0,
            "steps": step
        }

    def get_metrics(self):
        return self.metrics