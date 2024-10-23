from collections import defaultdict
import numpy as np
from config import SimConfig

class MetricsCollector:
    def __init__(self):
        self.clear_metrics()
        self.window_size = 50  # Size for moving averages
        
    def clear_metrics(self):
        self.metrics = defaultdict(list)
        self.interval_data = defaultdict(list)
        self.current_interval = 0
        self.total_packets = 0
        self.lost_packets = 0
        self.bytes_transmitted = 0
        self.current_window_metrics = {
            'throughput': [],
            'latency': [],
            'energy': [],
            'packet_loss': []
        }
        
    def update_metrics(self, time, bytes_sent, latency, energy, packets_lost=0):
        """Update all metrics with new data"""
        self.total_packets += 1
        self.lost_packets += packets_lost
        self.bytes_transmitted += bytes_sent
        
        # Store raw metrics with timestamps
        self.metrics['time'].append(time)
        self.metrics['throughput'].append(bytes_sent / (1024 * 1024))  # Convert to MB
        self.metrics['latency'].append(latency)
        self.metrics['energy'].append(energy)
        self.metrics['packet_loss'].append(self.lost_packets / max(1, self.total_packets))
        
        # Update interval metrics
        interval = int(time / SimConfig.METRIC_INTERVAL)
        if interval > self.current_interval:
            self._process_interval_metrics(interval)
            self.current_interval = interval
            
    def _process_interval_metrics(self, interval):
        """Process and store detailed metrics for the current interval"""
        if not self.metrics['time']:
            return
            
        start_idx = max(0, len(self.metrics['time']) - self.window_size)
        end_idx = len(self.metrics['time'])
        
        # Store basic interval data
        self.interval_data['time'].append(interval * SimConfig.METRIC_INTERVAL)
        
        # Enhanced throughput metrics
        throughput_values = self.metrics['throughput'][start_idx:end_idx]
        self.interval_data['avg_throughput'].append(np.mean(throughput_values))
        self.interval_data['peak_throughput'].append(np.max(throughput_values))
        self.interval_data['min_throughput'].append(np.min(throughput_values))
        
        # Enhanced latency metrics
        latency_values = self.metrics['latency'][start_idx:end_idx]
        self.interval_data['avg_latency'].append(np.mean(latency_values))
        self.interval_data['max_latency'].append(np.max(latency_values))
        self.interval_data['latency_std'].append(np.std(latency_values))
        
        # Enhanced energy metrics
        energy_values = self.metrics['energy'][start_idx:end_idx]
        self.interval_data['avg_energy'].append(np.mean(energy_values))
        self.interval_data['total_energy'].append(np.sum(energy_values))
        self.interval_data['energy_per_packet'].append(
            np.sum(energy_values) / max(1, len(energy_values))
        )
        
        # Enhanced packet loss metrics
        self.interval_data['packet_loss_rate'].append(
            self.lost_packets / max(1, self.total_packets)
        )
        self.interval_data['failure_count'].append(
            len([x for x in self.metrics['packet_loss'][start_idx:end_idx] if x > 0])
        )
        
        # Network utilization metrics
        self.interval_data['network_utilization'].append(
            len(throughput_values) / (SimConfig.SATELLITE_COUNT * SimConfig.MAX_QUEUE_SIZE)
        )
    
    def get_window_statistics(self):
        """Calculate detailed statistics for the current window"""
        stats = {}
        for metric in ['throughput', 'latency', 'energy', 'packet_loss']:
            if self.metrics[metric]:
                window_data = self.metrics[metric][-self.window_size:]
                stats[metric] = {
                    'mean': np.mean(window_data),
                    'std': np.std(window_data),
                    'min': np.min(window_data),
                    'max': np.max(window_data),
                    'median': np.median(window_data),
                    '95th_percentile': np.percentile(window_data, 95),
                    'count': len(window_data)
                }
        return stats
    
    def get_performance_summary(self):
        """Get a comprehensive performance summary"""
        return {
            'total_packets': self.total_packets,
            'lost_packets': self.lost_packets,
            'packet_loss_rate': self.lost_packets / max(1, self.total_packets),
            'total_bytes_transmitted': self.bytes_transmitted,
            'average_throughput': self.bytes_transmitted / (1024 * 1024 * SimConfig.SIM_TIME),  # MB/s
            'peak_throughput': max(self.metrics['throughput']) if self.metrics['throughput'] else 0,
            'average_latency': np.mean(self.metrics['latency']) if self.metrics['latency'] else 0,
            'total_energy_consumed': sum(self.metrics['energy']) if self.metrics['energy'] else 0,
            'network_utilization': len(self.metrics['throughput']) / (SimConfig.SATELLITE_COUNT * SimConfig.MAX_QUEUE_SIZE)
        }

