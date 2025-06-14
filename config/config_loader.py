import argparse
import yaml
import os

def load_yaml_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def parse_args(default_config_path):
    parser = argparse.ArgumentParser(description="Traffic Swarm Optimization Config")
    parser.add_argument('--config', type=str, default=default_config_path, help='Path to YAML config file')
    parser.add_argument('--objective', type=str, help='Objective to optimize (overrides config)')
    parser.add_argument('--optimizer', type=str, help='Optimizer algorithm (overrides config)')
    parser.add_argument('--sim_backend', type=str, help='Simulation backend (overrides config)')
    # Add more overrides as needed
    return parser.parse_args()

def merge_args_with_config(config, args):
    if args.objective:
        config['objectives']['selected'] = args.objective
    if args.optimizer:
        config['optimizer']['algorithm'] = args.optimizer
    if args.sim_backend:
        config['simulation']['backend'] = args.sim_backend
    return config

def validate_config(config):
    required_sections = ['scenario', 'simulation', 'optimizer', 'objectives']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Config error: Missing section '{section}'.")

def get_config():
    # Get path relative to this file's directory
    file_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(file_dir, 'default_config.yaml')
    args = parse_args(default_config_path)
    config_path = args.config
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} does not exist.")
    config = load_yaml_config(config_path)
    config = merge_args_with_config(config, args)
    validate_config(config)
    return config

if __name__ == "__main__":
    config = get_config()
    print("Loaded configuration:")
    import pprint
    pprint.pprint(config)