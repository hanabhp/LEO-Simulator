import os
import time
import sys
import logging
from datetime import datetime
import simpy
from config import SimConfig
from models import Satellite, D2DDevice
from utils import MetricsCollector, plot_all_metrics

def setup_logging():
    """Setup logging with both file and console handlers"""
    # Create logs directory
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create logger
    logger = logging.getLogger('LEOSimulation')
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers if any
    logger.handlers = []
    
    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(f'logs/simulation_{timestamp}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger, file_handler.baseFilename

def monitor_simulation_speed(env, start_time, logger):
    """Monitor the simulation execution speed and time dilation"""
    last_sim_time = 0
    last_real_time = start_time
    
    while True:
        yield env.timeout(SimConfig.PROGRESS_INTERVAL)
        
        current_real_time = time.time()
        current_sim_time = env.now
        
        # Calculate speeds
        real_time_delta = current_real_time - last_real_time
        sim_time_delta = current_sim_time - last_sim_time
        
        if real_time_delta > 0:
            simulation_speed = sim_time_delta / real_time_delta
            logger.debug(f"Simulation speed: {simulation_speed:.2f}x real-time")
        
        last_sim_time = current_sim_time
        last_real_time = current_real_time

def monitor_resources(env, satellites, metrics, logger):
    """Monitor system resources and simulation state"""
    while True:
        yield env.timeout(SimConfig.PROGRESS_INTERVAL)
        
        # Log satellite states
        for sat in satellites:
            queue_length = len(sat.queue)
            logger.debug(f"Satellite {sat.name}: Queue={queue_length}, "
                      f"Failed={sat.failed}, "
                      f"Processed={sat.total_packets}, "
                      f"Lost={sat.lost_packets}")

def run_simulation():
    try:
        # Setup logging
        logger, log_filename = setup_logging()
        start_time = time.time()
        
        # Clear previous output
        for directory in ['plots', 'logs']:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Initialize simulation
        env = simpy.Environment()
        metrics = MetricsCollector()
        
        # Create network components
        satellites = []
        devices = []
        
        logger.info(f"\nInitializing simulation for {SimConfig.SIM_TIME} seconds")
        logger.info(f"Time step: {SimConfig.TIME_STEP} seconds")
        logger.info(f"Packet rate: {SimConfig.PACKET_RATE} seconds")
        
        # Create satellites and devices
        for i in range(SimConfig.SATELLITE_COUNT):
            satellite = Satellite(env, f'Sat-{i}', metrics)
            satellites.append(satellite)
            device = D2DDevice(env, f'Device-{i}', satellite)
            devices.append(device)
            logger.debug(f"Created Satellite-{i} and Device-{i}")
        
        # Add monitoring processes
        env.process(monitor_simulation_speed(env, start_time, logger))
        env.process(monitor_resources(env, satellites, metrics, logger))
        
        def print_progress():
            last_progress = 0
            while True:
                yield env.timeout(SimConfig.PROGRESS_INTERVAL)
                current_time = env.now
                progress = (current_time / SimConfig.SIM_TIME) * 100
                elapsed_time = time.time() - start_time
                
                if progress > last_progress:
                    logger.info(f"\nProgress: {progress:.1f}%")
                    logger.info(f"Simulation time: {current_time:.1f}s")
                    logger.info(f"Real time elapsed: {elapsed_time:.1f}s")
                    logger.info(f"Speed: {current_time/elapsed_time:.1f}x real-time")
                    logger.info(f"Packets: {metrics.total_packets}")
                    if metrics.total_packets > 0:
                        logger.info(f"Loss rate: {metrics.lost_packets/metrics.total_packets*100:.2f}%")
                    last_progress = progress
        
        # Add progress monitoring
        env.process(print_progress())
        
        # Run simulation
        logger.info("\nStarting simulation...")
        env.run(until=SimConfig.SIM_TIME)
        
        # Calculate final statistics
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.info("\nSimulation completed:")
        logger.info(f"- Real time taken: {total_time:.2f} seconds")
        logger.info(f"- Simulation/real-time ratio: {SimConfig.SIM_TIME/total_time:.2f}x")
        logger.info(f"- Total packets transmitted: {metrics.total_packets}")
        logger.info(f"- Total packets lost: {metrics.lost_packets}")
        logger.info(f"- Final packet loss rate: {metrics.lost_packets/max(1, metrics.total_packets)*100:.2f}%")
        logger.info(f"- Average throughput: {metrics.bytes_transmitted/SimConfig.SIM_TIME/1024/1024:.2f} MB/s")
        
        # Generate plots
        logger.info("\nGenerating plots...")
        plot_all_metrics(metrics.metrics, metrics.interval_data)
        
        logger.info("\nPlots saved in 'plots' directory")
        logger.info(f"Logs saved in '{log_filename}'")
        
    except Exception as e:
        if 'logger' in locals():
            logger.error(f"Simulation failed: {str(e)}", exc_info=True)
        else:
            print(f"Logging setup failed. Error: {str(e)}")
        raise

if __name__ == "__main__":
    run_simulation()

