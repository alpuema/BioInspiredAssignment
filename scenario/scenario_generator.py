import random

class Scenario:
    def __init__(self, config):
        self.type = config['type']
        self.grid_size = config.get('grid_size', 5)
        self.vehicles_per_hour = config.get('vehicles_per_hour', 1000)
        self.accident_probability = config.get('accident_probability', 0.02)
        self.random_seed = config.get('random_seed', 42)
        random.seed(self.random_seed)

    def generate(self):
        if self.type == "grid":
            return self._generate_grid()
        else:
            raise NotImplementedError(f"Scenario type '{self.type}' not implemented.")

    def _generate_grid(self):
        nodes = []
        edges = []
        # Create grid nodes
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                nodes.append((i, j))
        # Create edges between adjacent nodes (4-connected)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i < self.grid_size - 1:
                    edges.append(((i, j), (i + 1, j)))
                if j < self.grid_size - 1:
                    edges.append(((i, j), (i, j + 1)))
        # This is a simple grid, you can expand to add directions, weights, etc.
        scenario = {
            "nodes": nodes,
            "edges": edges,
            "vehicles_per_hour": self.vehicles_per_hour,
            "accident_probability": self.accident_probability,
            "random_seed": self.random_seed
        }
        return scenario

# Example usage
if __name__ == "__main__":
    # Simulate getting config from the loader
    import sys
    sys.path.append("../config")
    from config.config_loader import get_config

    config = get_config()
    scenario_cfg = config['scenario']
    scenario_gen = Scenario(scenario_cfg)
    scenario = scenario_gen.generate()
    print("Generated scenario:")
    import pprint
    pprint.pprint(scenario)