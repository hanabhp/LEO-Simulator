import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from config import SimConfig

class Visualizer:
    def __init__(self, output_dir='plots'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style
        plt.style.use('seaborn')
        # Fix: Update colors dictionary to match exactly with metric names
        self.colors = {
            'throughput': '#2ecc71',
            'latency': '#e74c3c',
            'energy': '#3498db',
            'packet_loss': '#f1c40f',  # Added exactly as used in metrics
            'packet loss': '#f1c40f'   # Alternative format
        }
    
    def plot_throughput(self, interval_data):
        fig = plt.figure(figsize=SimConfig.FIGURE_SIZES['throughput'])
        plt.bar(interval_data['time'],
                interval_data['avg_throughput'],
                width=SimConfig.METRIC_INTERVAL * 0.8,
                color=self.colors['throughput'],
                alpha=0.7)
        plt.title('Average Throughput per Interval')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (MB/s)')
        plt.grid(True, alpha=0.3)
        self.save_plot(fig, 'throughput')
    
    def plot_latency(self, metrics):
        fig = plt.figure(figsize=SimConfig.FIGURE_SIZES['latency'])
        
        # Create subplots
        gs = plt.GridSpec(1, 2)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        
        # Boxplot
        sns.boxplot(data=pd.DataFrame({'Latency': metrics['latency']}),
                   y='Latency', ax=ax1, color=self.colors['latency'])
        ax1.set_title('Latency Distribution')
        ax1.set_ylabel('Latency (ms)')
        
        # Time series
        ax2.plot(metrics['time'], metrics['latency'],
                color=self.colors['latency'], alpha=0.5)
        ax2.set_title('Latency Over Time')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Latency (ms)')
        
        plt.tight_layout()
        self.save_plot(fig, 'latency')
        
        # Additional latency heatmap
        self.plot_latency_heatmap(metrics['latency'])
    
    def plot_latency_heatmap(self, latency_data):
        if len(latency_data) > 50:
            fig = plt.figure(figsize=(10, 6))
            n_samples = len(latency_data)
            n_cols = 50
            n_rows = n_samples // n_cols
            
            if n_rows > 0:
                data = np.array(latency_data[:n_rows * n_cols]).reshape(n_rows, n_cols)
                sns.heatmap(data, cmap='YlOrRd',
                           xticklabels=False, yticklabels=False)
                plt.title('Latency Heatmap\n(Columns represent time segments)')
                self.save_plot(fig, 'latency_heatmap')
    
    def plot_energy(self, metrics):
        fig = plt.figure(figsize=SimConfig.FIGURE_SIZES['energy'])
        
        time_array = np.array(metrics['time'])
        energy_array = np.array(metrics['energy'])
        
        # Calculate moving average
        window = min(50, len(energy_array))
        if window > 0:
            energy_ma = np.convolve(energy_array,
                                  np.ones(window)/window, mode='valid')
            time_ma = time_array[window-1:]
            plt.plot(time_ma, energy_ma, color=self.colors['energy'],
                    linewidth=1)
            
        plt.title('Energy Consumption (Moving Average)')
        plt.xlabel('Time (s)')
        plt.ylabel('Energy (mW)')
        plt.grid(True, alpha=0.3)
        self.save_plot(fig, 'energy')
    
    def plot_packet_loss(self, interval_data):
        fig = plt.figure(figsize=SimConfig.FIGURE_SIZES['packet_loss'])
        plt.plot(interval_data['time'],
                interval_data['packet_loss_rate'],
                color=self.colors['packet_loss'])
        plt.title('Packet Loss Rate Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Loss Rate')
        plt.grid(True, alpha=0.3)
        self.save_plot(fig, 'packet_loss')
    
    def plot_combined_metrics(self, interval_data):
        try:
            fig = plt.figure(figsize=SimConfig.FIGURE_SIZES['combined'])
            
            metrics_to_plot = {
                'Throughput': ('avg_throughput', 'throughput'),
                'Latency': ('avg_latency', 'latency'),
                'Energy': ('avg_energy', 'energy'),
                'Packet Loss': ('packet_loss_rate', 'packet_loss')
            }
            
            for label, (data_key, color_key) in metrics_to_plot.items():
                if data_key in interval_data and len(interval_data[data_key]) > 0:
                    data = interval_data[data_key]
                    normalized_data = data / np.max(data) if np.max(data) != 0 else data
                    plt.plot(interval_data['time'], normalized_data,
                            label=label, color=self.colors[color_key],
                            alpha=0.7)
            
            plt.title('Normalized Metrics Over Time')
            plt.xlabel('Time (s)')
            plt.ylabel('Normalized Value')
            plt.legend()
            plt.grid(True, alpha=0.3)
            self.save_plot(fig, 'combined_metrics')
            
        except Exception as e:
            print(f"Error in plot_combined_metrics: {str(e)}")
            raise
    
    def save_plot(self, fig, name):
        """Save plot with high resolution"""
        try:
            fig.savefig(f'{self.output_dir}/{name}.png',
                       dpi=SimConfig.DPI,
                       bbox_inches='tight')
            plt.close(fig)
        except Exception as e:
            print(f"Error saving plot {name}: {str(e)}")
            raise

def plot_all_metrics(metrics, interval_data):
    """Main function to generate all plots"""
    try:
        visualizer = Visualizer()
        visualizer.plot_throughput(interval_data)
        visualizer.plot_latency(metrics)
        visualizer.plot_energy(metrics)
        visualizer.plot_packet_loss(interval_data)
        visualizer.plot_combined_metrics(interval_data)
    except Exception as e:
        print(f"Error in plot_all_metrics: {str(e)}")
        raise

