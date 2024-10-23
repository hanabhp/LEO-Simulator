# LEO Satellite Network Simulator

A comprehensive simulator for Direct-to-Device (D2D) Low Earth Orbit (LEO) satellite networks with dynamic failure handling and performance analysis.

## Analysis of Current Results

### Throughput Analysis
- Linear increase in cumulative throughput from 0 to ~70 MB/s over 3000s
- Regular intervals in bar plot indicate consistent packet transmission
- Slight variations in bar heights show impact of network conditions

### Latency Analysis
- Box plot shows median latency around 80ms
- Interquartile range (75-95ms) indicates stable performance
- Few outliers below 60ms and above 100ms
- Heatmap shows temporal patterns in latency variation

### Energy Consumption
- Baseline consumption ~1.5mW with regular variations
- Sharp drops indicate satellite failures
- Recovery periods visible after each drop
- Moving average window=50 smooths short-term fluctuations

### Packet Loss Rate
- Initial spike during network initialization
- Stabilizes around 7-8% loss rate
- Periodic variations correlate with satellite failures
- Gradual increase in baseline over time

### Normalized Metrics
- Clear correlation between energy and latency patterns
- Throughput shows steady growth
- Packet loss stabilizes after initial spike
- Energy shows most volatile behavior

## Directory Structure
```
leo_satellite_sim/
├── README.md
├── requirements.txt
├── config.py                 # Simulation parameters
├── models/
│   ├── __init__.py
│   ├── satellite.py         # Satellite implementation
│   ├── device.py           # D2D device implementation
│   └── packet.py           # Packet structure
├── utils/
│   ├── __init__.py
│   ├── metrics.py          # Performance metrics collection
│   └── visualization.py    # Plotting functions
├── output/                 # Generated plots directory
│   ├── throughput.png
│   ├── latency.png
│   ├── energy.png
│   ├── packet_loss.png
│   └── combined_metrics.png
└── run_simulation.py       # Main execution script
```

## Requirements

### Software Dependencies
- Python 3.8+
- SimPy 4.0+
- NumPy 1.20+
- Pandas 1.3+
- Matplotlib 3.4+
- Seaborn 0.11+

### Installation
```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/leo-satellite-sim.git
cd leo-satellite-sim
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the simulation:
```bash
python run_simulation.py
```

4. View results in the `output/` directory

## Configuration

Edit `config.py` to modify simulation parameters:

```python
class SimConfig:
    SIM_TIME = 3000          # Simulation duration (seconds)
    SATELLITE_COUNT = 5      # Number of satellites
    FAILURE_RATE = 300      # Average failure interval
    RECOVERY_TIME = 30      # Recovery duration
    # ... other parameters
```

## Output Files

The simulation generates several high-resolution plots:

1. `throughput.png` - Average throughput per interval
2. `latency.png` - Latency distribution and heatmap
3. `energy.png` - Energy consumption over time
4. `packet_loss.png` - Packet loss rate
5. `combined_metrics.png` - Normalized comparison of all metrics

## Visualization Options

To generate separate high-resolution plots, modify `utils/visualization.py`:

```python
DPI = 300  # Plot resolution
PLOT_FORMATS = ['png', 'pdf']  # Output formats
FIGURE_SIZES = {
    'throughput': (12, 8),
    'latency': (10, 6),
    'energy': (15, 5),
    'packet_loss': (10, 6),
    'combined': (15, 10)
}
```

## Citation

If you use this simulator in your research, please cite:

```bibtex
@article{pasandi2024orbit,
  title={Orbit Recovery: Real-Time Optimization for Resilient Direct-to-Device LEO Networks},
  author={Pasandi, Hannaneh B and Fraire, Juan A and Ratnasamy, Sylvia and Raviano, Herve},
  journal={arXiv preprint},
  year={2024}
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- UC Berkeley
- INRIA-Lyon
- Research supported by [funding organization]

## Contact

For questions or support, please contact:
- Name: [Your Name]
- Email: [Your Email]
- Organization: [Your Organization]
