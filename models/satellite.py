import random
from collections import deque
from config import SimConfig

class Satellite:
    def __init__(self, env, name, metrics):
        self.env = env
        self.name = name
        self.metrics = metrics
        self.failed = False
        self.queue = deque(maxlen=SimConfig.MAX_QUEUE_SIZE)
        self.bytes_transmitted = 0
        self.total_packets = 0
        self.lost_packets = 0
        self.current_load = 0
        self.last_packet_time = 0
        
        # Start processes
        self.process = env.process(self.run())
        self.failure_process = env.process(self.failure_cycle())
        self.monitoring_process = env.process(self.monitor_health())
    
    def calculate_latency(self, packet):
        # Base propagation delay
        distance = 2 * SimConfig.ALTITUDE  # Round trip
        propagation_delay = distance / SimConfig.SPEED_OF_LIGHT * 1000  # ms
        
        # Queue-dependent processing delay
        queue_factor = len(self.queue) / SimConfig.MAX_QUEUE_SIZE
        processing_delay = SimConfig.PROCESSING_DELAY * 1000 * (1 + queue_factor * SimConfig.CONGESTION_FACTOR)
        
        # Size-dependent transmission delay
        size_factor = packet.size / SimConfig.PACKET_SIZE_MAX
        transmission_delay = processing_delay * size_factor
        
        # Add realistic jitter based on load
        load_factor = self.current_load / SimConfig.MAX_QUEUE_SIZE
        jitter = random.uniform(1, 5) * (1 + load_factor)
        
        # Calculate queuing delay
        queue_time = 0
        if packet.queue_entry_time is not None:
            queue_time = (self.env.now - packet.queue_entry_time) * 1000
        
        total_delay = propagation_delay + processing_delay + transmission_delay + jitter + queue_time
        return max(1, total_delay)  # Ensure minimum 1ms latency
    
    def calculate_energy(self, packet):
        # Base energy consumption
        energy = SimConfig.BASE_ENERGY
        
        # Size-dependent energy
        size_energy = packet.size * SimConfig.ENERGY_PER_BYTE
        
        # Load-dependent factor
        load_factor = 1 + (len(self.queue) / SimConfig.MAX_QUEUE_SIZE)
        
        # Add energy cost for processing
        processing_energy = SimConfig.PROCESSING_DELAY * SimConfig.BASE_ENERGY
        
        # Random variation based on conditions
        variation = random.uniform(0.9, 1.1)
        
        return (energy + size_energy + processing_energy) * load_factor * variation
    
    def monitor_health(self):
        """Monitor satellite health and performance"""
        while True:
            yield self.env.timeout(SimConfig.METRIC_INTERVAL)
            
            # Calculate current metrics
            queue_utilization = len(self.queue) / SimConfig.MAX_QUEUE_SIZE
            packet_rate = (self.total_packets) / max(1, self.env.now)
            
            # Log health status
            if queue_utilization > 0.9:
                print(f"WARNING: {self.name} queue near capacity ({queue_utilization:.2%})")
            
            # Update current load
            self.current_load = len(self.queue)
    
    def run(self):
        """Main packet processing loop"""
        while True:
            if not self.failed and self.queue:
                packet = self.queue.popleft()
                packet.processing_start_time = self.env.now
                
                # Simulate processing time
                yield self.env.timeout(SimConfig.PROCESSING_DELAY)
                
                # Calculate metrics
                latency = self.calculate_latency(packet)
                energy = self.calculate_energy(packet)
                self.bytes_transmitted += packet.size
                
                # Set completion time
                packet.completion_time = self.env.now
                
                # Update metrics
                self.metrics.update_metrics(
                    self.env.now,
                    packet.size,
                    latency,
                    energy
                )
                
                # Log packet transmission
                if self.env.now - self.last_packet_time >= SimConfig.METRIC_INTERVAL:
                    print(f"t={self.env.now:.1f}s: {self.name} sent {packet.size/1024:.1f}KB packet, "
                          f"latency={latency:.2f}ms, energy={energy:.3f}mW")
                    self.last_packet_time = self.env.now
            
            yield self.env.timeout(SimConfig.TIME_STEP)
    
    def failure_cycle(self):
        """Simulate satellite failures and recovery"""
        while True:
            yield self.env.timeout(random.expovariate(1.0/SimConfig.FAILURE_RATE))
            
            self.failed = True
            lost_packets = len(self.queue)
            self.lost_packets += lost_packets
            
            # Clear queue and update metrics
            self.queue.clear()
            self.metrics.update_metrics(
                self.env.now,
                0,
                SimConfig.MAX_LATENCY,  # Maximum latency during failure
                0,
                lost_packets
            )
            
            print(f"t={self.env.now:.1f}s: {self.name} FAILED - {lost_packets} packets lost")
            
            # Recovery period
            yield self.env.timeout(SimConfig.RECOVERY_TIME)
            self.failed = False
            print(f"t={self.env.now:.1f}s: {self.name} RECOVERED")
    
    def drop_low_priority_packets(self):
        """Drop lowest priority packets when queue is congested"""
        if len(self.queue) > SimConfig.MAX_QUEUE_SIZE * 0.9:
            num_to_drop = int(len(self.queue) * 0.1)  # Drop 10% of packets
            for _ in range(num_to_drop):
                if self.queue:
                    self.queue.popleft()
                    self.lost_packets += 1
    
    def send_packet(self, packet):
        """Handle incoming packets"""
        if not self.failed:
            packet.queue_entry_time = self.env.now
            
            # Check queue capacity
            if len(self.queue) < SimConfig.MAX_QUEUE_SIZE:
                self.queue.append(packet)
                self.total_packets += 1
            else:
                # Queue full - implement congestion control
                self.drop_low_priority_packets()
                self.lost_packets += 1
                self.metrics.update_metrics(
                    self.env.now, 0, SimConfig.MAX_LATENCY, 0, packets_lost=1
                )
                print(f"t={self.env.now:.1f}s: {self.name} dropped packet (queue full)")
        else:
            # Satellite failed - count as lost packet
            self.lost_packets += 1
            self.metrics.update_metrics(
                self.env.now, 0, SimConfig.MAX_LATENCY, 0, packets_lost=1
            )
            print(f"t={self.env.now:.1f}s: {self.name} dropped packet (failed)")

