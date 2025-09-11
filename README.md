# Traffic Light Optimization using Ant Colony Optimization

This project implements traffic light signal optimization using Ant Colony Optimization (ACO) with SUMO simulation. The system is designed for research applications and provides clean, reproducible results.

## Features

- **Simple ACO Implementation**: Direct range sampling without complex bin systems
- **Interactive Interface**: User-friendly configuration with reasonable defaults
- **Multiple Traffic Patterns**: Supports balanced, random, commuter, commercial, and industrial patterns
- **Flexible Display Options**: Configurable plots, GUI, and verbosity levels
- **Train/Evaluate System**: Train on one scenario, then evaluate on multiple scenarios
- **Traffic Engineering Constraints**: Respects real-world timing constraints (green: 20-100s, yellow: 3-6s)
- **Smart Search Space**: Automatically classifies phase types and applies appropriate constraints
- **Reproducible Results**: Full seed control for consistent research outcomes
- **Performance Analysis**: Comprehensive evaluation and comparison tools
- **Optimization Visualization**: Progress tracking and results plotting

## Getting Started

### New Users

For beginners, start with the interactive menu:
```bash
python examples/menu_example.py
```

This provides a guided interface with:
- Quick Demo (2-3 minutes with preset values)
- Custom Configuration (step-by-step guidance)
- Sensitivity Analysis (find optimal settings)
- Learning Resources (understand the system)

### Main Optimization Tool

Run the complete optimization with visualization:
```bash
python main.py
```

### Quick Demonstration

For a guided demonstration of key features:
```bash
python examples/quick_start.py
```

### Interactive Configuration

For advanced users who want detailed control:
```bash
python examples/simple_aco_optimization.py
```

This enhanced interface provides:
- Grouped input sections (Scenario, Optimization, Display)
- Available options for every parameter
- Detailed descriptions of each setting
- Impact guidance for parameter choices
- Configuration summary before starting
- Runtime estimates based on selections

### Parameter Optimization

To find optimal parameter combinations:
```bash
python examples/sensitivity_example.py
```

Features guided parameter testing with statistical analysis and visualization.

### Advanced Training and Evaluation

For research applications:
```bash
python examples/train_evaluate.py
```

This workflow allows you to:
1. Train: Find optimal settings for a specific scenario
2. Evaluate: Test those settings on different scenarios
3. Compare: Analyze performance improvements statistically

## Implementation Notes

The system uses a simplified ACO approach that:
- Uses direct range sampling (20-100s green, 3-6s yellow phases)
- Eliminates complex bin arrays and mapping logic
- Reduces memory usage by 26x compared to previous implementations
- Maintains stable iteration performance
- Provides easier debugging and understanding
- Includes automatic optimization progress plotting

## Usage Examples

### Training Phase
Train ACO to find optimal traffic light settings:
```python
from src.optimization.simple_aco import run_traditional_aco_optimization

config = {
    'grid_size': 3,
    'n_vehicles': 50,
    'simulation_time': 600,
    'n_ants': 20,
    'n_iterations': 10
}

results = run_traditional_aco_optimization(config)
```

### Evaluation Phase  
Test trained settings on different conditions:
```python
eval_results = optimizer.evaluate(
    trained_settings_file="results/training_commuter_rush_hour_20250826_143022.json",
    eval_scenarios=["commuter", "realistic", "commercial"],
    eval_seeds=[1, 2, 3, 4, 5]
)
```

### Key Metrics
- **Improvement Percentage**: `(default_time - optimized_time) / default_time * 100`
- **Success Rate**: Percentage of tests showing positive improvement
- **Statistical Analysis**: Mean improvement ± standard deviation across multiple seeds

## Project Structure

```
my_grid_simulation/
├── main.py                    # Main entry point
├── examples/                  # Usage examples and demonstrations
│   ├── menu_example.py        # User-friendly guided menu for all levels
│   ├── quick_start.py         # Quick demonstration of key features
│   ├── simple_aco_optimization.py  # Step-by-step interactive configuration
│   ├── sensitivity_example.py # Parameter optimization with guidance
│   ├── simple_example.py      # Basic usage example
│   └── train_evaluate.py      # Advanced training/evaluation workflow
├── src/                       # Core functionality
│   ├── optimize.py           # Main optimization tool
│   ├── simplified_traffic.py # Traffic scenario generation
│   ├── traffic_patterns.py  # Traffic pattern definitions
│   ├── sensitivity_analysis.py # Parameter sensitivity testing
│   ├── config.py            # Configuration management
│   ├── optimization/        # ACO algorithm implementation
│   ├── utils/               # Utility functions
│   └── sumo_data/          # SUMO network and route files
└── results/                 # Generated results and visualizations
```

## Mathematical Background

See `MATHEMATICAL_FORMULATION.md` for complete mathematical details including:
- Decision variables and search space
- Objective function: `f(x) = T_total + α × T_max_stop`  
- ACO algorithm with pheromone updates
- Traffic engineering constraints
- Computational complexity analysis

## Configuration

Key parameters in `examples/train_evaluate.py`:
```python
config = {
    # Simulation
    "grid_size": 3,           # 2-5 recommended
    "n_vehicles": 50,         # 20-100 recommended  
    "simulation_time": 1200,  # 300-1800 seconds
    "traffic_pattern": "commuter",  # "random", "realistic", "commuter", "commercial"
    
    # ACO Algorithm
    "n_ants": 50,            # 20-100 ants
    "n_iterations": 10,      # 5-20 iterations
    "evaporation_rate": 0.3, # 0.1-0.5
    "alpha": 30.0,           # Stop time penalty weight
    
    # Critical Settings
    "use_traffic_engineering": True,  # ESSENTIAL - enables proper search space
    "use_default_start": True,        # Start from SUMO's proven defaults
    "use_coordination": True,         # Coordinate adjacent traffic lights
}
```

## Repository Structure

```
├── examples/
│   ├── train_evaluate.py          # Main train/evaluate system
│   ├── simple_aco_optimization.py # Legacy single optimization
│   └── analyze_sumo_defaults.py   # Analysis tool
├── src/
│   ├── optimization/
│   │   └── aco.py                 # Core ACO algorithm
│   ├── utils/                     # Utility functions
│   ├── config.py                  # Configuration management
│   └── traffic_patterns.py       # Traffic pattern generation
├── results/                       # Output directory (auto-created)
├── MATHEMATICAL_FORMULATION.md    # Complete mathematical details
└── README.md                      # This file
```

## Research Applications

### Scenario Generalization Study
Train on one traffic pattern, evaluate on others:
```python
# Train on commuter pattern with morning rush hour characteristics
results = optimizer.train("commuter_morning", seed=42)

# Evaluate on different patterns
optimizer.evaluate(results_file, 
                  scenarios=["commuter", "commercial", "realistic"],
                  seeds=[1,2,3,4,5])
```

### Seed Sensitivity Analysis
Test robustness across different random conditions:
```python
# Train with multiple seeds
for seed in [10, 20, 30, 40, 50]:
    results = optimizer.train(f"sensitivity_test_{seed}", seed)
    
# Cross-evaluate all combinations
```

### Parameter Sensitivity
Modify ACO parameters and compare results:
```python
optimizer.config["evaporation_rate"] = 0.1  # Low evaporation
results_low = optimizer.train("param_test_low", 42)

optimizer.config["evaporation_rate"] = 0.5  # High evaporation  
results_high = optimizer.train("param_test_high", 42)
```

## Analysis Tools

### Default Analysis
Understand what SUMO's defaults actually are:
```bash
python examples/analyze_sumo_defaults.py
```

Shows:
- Actual phase durations in SUMO's defaults
- Phase type classification (green vs yellow)
- Why original ACO couldn't find optimal solutions
- Recommendations for search space

### Results Analysis
All results are saved as JSON files with comprehensive metadata:
- Training configuration and performance
- Evaluation results across scenarios/seeds
- Statistical summaries
- Improvement percentages

## Academic Usage

This implementation is designed for research with:
- **Reproducible Results**: Full seed control
- **Statistical Validation**: Multi-seed evaluation
- **Comparative Analysis**: Default vs optimized performance
- **Mathematical Documentation**: Complete formulation
- **Clean Code**: Well-documented, research-grade implementation

Perfect for traffic engineering research, metaheuristic algorithm studies, and SUMO-based optimization projects.

## Requirements

- Python 3.8+
- SUMO 1.8+
- NumPy, Matplotlib
- `SUMO_HOME` environment variable set

## Citation

If you use this code in your research, please cite:
```
Traffic Light Optimization using Ant Colony Optimization
Author: Alfonso Rato, 2025
Implementation with traffic engineering constraints and train/evaluate methodology
```