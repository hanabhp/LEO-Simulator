import random
from config import SimConfig
from .packet import Packet

class D2DDevice:
    def __init__(self, env, name, satellite):
        self.env = env
        self.name = name
        self.satellite = satellite
        self.packets_sent = 0
        self.bytes_sent = 0
        self.last_sent_time = 0
        self.env.process(self.generate_traffic())
    
    def generate_traffic(self):
        """Generate network traffic with variable packet sizes and rates"""
        while True:
            # Variable packet generation interval
            yield self.env.timeout(random.expovariate(1.0/SimConfig.PACKET_RATE))
            
            # Generate packet with random size
            size = random.randint(SimConfig.PACKET_SIZE_MIN, SimConfig.PACKET_SIZE_MAX)
            packet = Packet(size, self.env.now)
            
            # Update statistics
            self.packets_sent += 1
            self.bytes_sent += size
            
            # Send packet to satellite
            self.satellite.send_packet(packet)
            
            # Log traffic generation periodically
            if self.env.now - self.last_sent_time >= SimConfig.METRIC_INTERVAL:
                throughput = self.bytes_sent / (1024 * 1024 * max(1, self.env.now))  # MB/s
                print(f"t={self.env.now:.1f}s: {self.name} generated {self.packets_sent} packets, "
                      f"throughput={throughput:.2f} MB/s")
                self.last_sent_time = self.env.now

