#!/usr/bin/env python3
"""
Clean Traffic Light Optimization Tool

This is the main optimization tool that combines simplified ACO algorithm
with flexible traffic pattern generation. It supports:

- Multiple traffic patterns (random, commuter, commercial, etc.)
- Seed-based reproducible optimization and evaluation
- Solution saving and loading for different scenarios
- Clean, easy-to-understand configuration

Author: Alfonso Rato
Date: August 2025
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Use package-relative imports so this works when imported as `src.optimize`
from .optimization.simple_aco import run_traditional_aco_optimization
from .simplified_traffic import (
    generate_network_and_routes, 
    save_optimized_solution, 
    load_solution,
    evaluate_solution_with_new_seed,
    list_available_patterns
)
from typing import List, Dict, Any, Optional, Tuple

# ============================================================================
# MAIN OPTIMIZATION INTERFACE
# ============================================================================

def run_complete_optimization(config):
    """
    Run complete optimization: generate scenario, optimize, and save results.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Results dictionary
    """
    print(" TRAFFIC LIGHT OPTIMIZATION")
    print("=" * 50)
    
    # Step 1: Generate scenario with specified traffic pattern
    print("\n Step 1: Generating Traffic Scenario")
    
    scenario_result = generate_network_and_routes(
        grid_size=config['grid_size'],
        n_vehicles=config['n_vehicles'], 
        sim_time=config['simulation_time'],
        pattern=config['traffic_pattern'],
        seed=config.get('seed')
    )
    
    if not scenario_result['success']:
        print(f" Scenario generation failed: {scenario_result['error']}")
        return {'success': False, 'error': 'Scenario generation failed'}
    
    print(f" Scenario generated with {config['traffic_pattern']} pattern")
    
    # Step 2: Run ACO optimization
    print("\n Step 2: Running ACO Optimization")
    
    aco_config = {
        'grid_size': config['grid_size'],
        'n_vehicles': config['n_vehicles'],
        'simulation_time': config['simulation_time'],
        'n_ants': config.get('n_ants', 20),
        'n_iterations': config.get('n_iterations', 10)
    }
    
    # Temporarily update paths for ACO to find generated files
    from .optimization import simple_aco as aco
    original_values = {}
    for key, value in aco_config.items():
        if hasattr(aco, key.upper()):
            original_values[key.upper()] = getattr(aco, key.upper())
            setattr(aco, key.upper(), value)
    
    optimization_result = run_traditional_aco_optimization(aco_config)
    
    # Restore original values
    for key, value in original_values.items():
        setattr(aco, key, value)
    
    if not optimization_result['success']:
        print(f" Optimization failed: {optimization_result['error']}")
        return {'success': False, 'error': 'Optimization failed'}
    
    print(f" Optimization completed! Best cost: {optimization_result['best_cost']:.1f}")
    
    # Step 3: Save results
    print("\n Step 3: Saving Results")
    
    # Prepare metadata
    metadata = {
        'grid_size': config['grid_size'],
        'n_vehicles': config['n_vehicles'],
        'simulation_time': config['simulation_time'],
        'traffic_pattern': config['traffic_pattern'],
        'seed': config.get('seed'),
        'n_ants': aco_config['n_ants'],
        'n_iterations': aco_config['n_iterations'],
        'optimization_duration': optimization_result['duration'],
        'best_cost': optimization_result['best_cost']
    }
    
    # Create results directory
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save optimized solution
    save_result = save_optimized_solution(
        optimization_result['best_solution'],
        metadata,
        results_dir
    )
    
    # Combine all results
    complete_result = {
        'success': True,
        'scenario': scenario_result,
        'optimization': optimization_result,
        'saved_solution': save_result,
        'metadata': metadata
    }
    
    print_summary(complete_result)
    
    return complete_result


# ============================================================================
# SIMPLE WRAPPER CLASS FOR EXAMPLES
# ============================================================================

class ACOTrafficOptimizer:
    """
    Thin wrapper to provide a simple interface expected by examples.

    Note: SUMO files are expected to be generated beforehand (via
    simplified_traffic.create_traffic_scenario or generate_network_and_routes).
    This class maps high-level parameters to the underlying ACO function.
    """

    def __init__(
        self,
        sumo_config: Optional[str] = None,
        n_ants: int = 20,
        n_iterations: int = 10,
        alpha: float = 1.0,
        beta: float = 2.0,
        rho: float = 0.5,
        verbose: bool = True,
        scenario_vehicles: int = None,  # Allow passing actual vehicle count
        simulation_time: int = None,  # Allow passing simulation time
        show_plots: bool = True,  # Show optimization progress plots
        show_sumo_gui: bool = False,  # Launch SUMO GUI with results
        compare_baseline: bool = True,  # Compare against baseline uniform timing
    ) -> None:
        # Stored for completeness; current ACO doesn't use beta directly
        self.sumo_config = sumo_config
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.verbose = verbose
        self.scenario_vehicles = scenario_vehicles
        self.simulation_time = simulation_time
        self.show_plots = show_plots
        self.show_sumo_gui = show_sumo_gui
        self.compare_baseline = compare_baseline

    def optimize(self) -> Tuple[Dict[str, Dict[str, int]], float, List[Dict[str, float]], Optional[Dict]]:
        """
        Run optimization and return (best_solution_dict, best_cost, optimization_data, baseline_comparison).

        best_solution_dict maps phase identifiers to timing info for simple display.
        optimization_data is a list of {'best_cost': value} per iteration.
        baseline_comparison contains comparison against uniform 30s/4s timing (if enabled).
        """
        # Build config for underlying optimizer
        config = {
            'n_ants': self.n_ants,
            'n_iterations': self.n_iterations,
            # Map alpha -> stop_penalty used in cost function
            'stop_penalty': self.alpha,
            # Provide some stability params derived from rho (evaporation)
            'evaporation_rate': max(0.01, min(0.9, self.rho)),
            # Pass through actual vehicle count if available
            'n_vehicles': self.scenario_vehicles or 30,  # Default to 30 if not provided
            # Pass through simulation time if available
            'simulation_time': self.simulation_time,
        }

        results = run_traditional_aco_optimization(
            config=config, 
            show_plots_override=self.show_plots,
            show_gui_override=self.show_sumo_gui,
            compare_baseline=self.compare_baseline,
            sumo_config_file=self.sumo_config
        )
        if not results.get('success'):
            raise RuntimeError(results.get('error', 'Optimization failed'))

        # Convert best solution list + phase types into a friendly dict
        durations: List[int] = results.get('best_solution') or []
        phase_types: List[bool] = results.get('phase_types') or [True] * len(durations)
        best_cost: float = float(results.get('best_cost', float('inf')))

        solution_dict: Dict[str, Dict[str, int]] = {}
        for idx, dur in enumerate(durations):
            key = f'phase_{idx}'
            if idx < len(phase_types) and not phase_types[idx]:
                solution_dict[key] = {'yellow': int(dur)}
            else:
                solution_dict[key] = {'green': int(dur)}

        # Build optimization_data as list of dicts with best_cost per iteration
        cost_history: List[float] = results.get('cost_history') or []
        optimization_data = [{'best_cost': float(c)} for c in cost_history]
        
        # Get baseline comparison results
        baseline_comparison = results.get('baseline_comparison')

        return solution_dict, best_cost, optimization_data, baseline_comparison

def evaluate_existing_solution(solution_file, new_seed, config=None):
    """
    Evaluate an existing solution with a new traffic seed.
    
    Args:
        solution_file: Path to saved solution file
        new_seed: New random seed for traffic generation
        config: Optional configuration overrides
    
    Returns:
        Evaluation results
    """
    print(" SOLUTION RE-EVALUATION")
    print("=" * 50)
    
    # Load existing solution
    solution_data = load_solution(solution_file)
    if not solution_data:
        return {'success': False, 'error': 'Could not load solution'}
    
    print(f" Loaded solution from: {os.path.basename(solution_file)}")
    print(f"   Original seed: {solution_data['metadata'].get('seed')}")
    print(f"   New seed: {new_seed}")
    
    # Use configuration overrides or original values
    eval_config = solution_data['metadata'].copy()
    if config:
        eval_config.update(config)
    
    # Generate new scenario
    scenario_result = generate_network_and_routes(
        grid_size=eval_config['grid_size'],
        n_vehicles=eval_config.get('n_vehicles', 30),
        sim_time=eval_config.get('simulation_time', 600),
        pattern=eval_config.get('traffic_pattern', 'commuter'),
        seed=new_seed
    )
    
    if not scenario_result['success']:
        return {'success': False, 'error': 'New scenario generation failed'}
    
    print(f" New scenario generated with seed {new_seed}")
    
    # Here you would apply the solution and evaluate performance
    # For now, return the setup information
    
    result = {
        'success': True,
        'original_solution': solution_data,
        'new_scenario': scenario_result,
        'evaluation_seed': new_seed,
        'message': 'Solution loaded and new scenario generated. Ready for evaluation.'
    }
    
    return result

def print_summary(results):
    """Print a summary of optimization results."""
    print("\n OPTIMIZATION SUMMARY")
    print("=" * 50)
    
    metadata = results['metadata']
    
    print(f"  Scenario: {metadata['grid_size']}x{metadata['grid_size']} grid")
    print(f" Vehicles: {metadata['n_vehicles']}")
    print(f" Simulation: {metadata['simulation_time']}s")
    print(f" Pattern: {metadata['traffic_pattern']}")
    print(f" Seed: {metadata.get('seed', 'None')}")
    print()
    print(f" ACO Config: {metadata['n_ants']} ants × {metadata['n_iterations']} iterations")
    print(f"  Duration: {metadata['optimization_duration']:.1f} seconds")
    print(f" Best Cost: {metadata['best_cost']:.1f}")
    print()
    print(f" Solution saved: {results['saved_solution']['solution_file']}")
    print()
    print(" Optimization completed successfully!")

