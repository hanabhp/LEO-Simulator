class SimConfig:
    # Time settings
    SIM_TIME = 3000          # 50 minutes
    TIME_STEP = 0.01         # 10ms steps for granular simulation
    METRIC_INTERVAL = 1.0    # Collect metrics every second
    PROGRESS_INTERVAL = 10   # Print progress every 10 seconds
    
    # Network parameters
    SATELLITE_COUNT = 20     # Increased from 5 to 20 satellites
    FAILURE_RATE = 300      # One failure every 5 minutes
    RECOVERY_TIME = 15      # 15 seconds recovery
    
    # Packet parameters
    PACKET_SIZE_MIN = 10240  # 10KB
    PACKET_SIZE_MAX = 102400 # 100KB
    PACKET_RATE = 0.1       # Packet every 100ms
    
    # Queue parameters
    MAX_QUEUE_SIZE = 75     # Increased queue size
    PROCESSING_DELAY = 0.01 # 10ms processing delay
    
    # Energy parameters
    BASE_ENERGY = 0.5       # Base energy consumption (mW)
    ENERGY_PER_BYTE = 0.00001 # Energy per byte adjusted
    
    # Network conditions
    CONGESTION_FACTOR = 1.5
    JITTER_RANGE = 0.005    # 5ms max jitter
    
    # Satellite parameters
    ALTITUDE = 550          # km
    SPEED_OF_LIGHT = 299792 # km/s
    
    # Visualization parameters
    DPI = 300
    PLOT_FORMATS = ['png']
    FIGURE_SIZES = {
        'throughput': (12, 8),
        'latency': (15, 6),
        'energy': (15, 5),
        'packet_loss': (12, 6),
        'combined': (15, 8)
    }
    
    # Performance thresholds
    MAX_LATENCY = 100       # Maximum acceptable latency (ms)
    TARGET_PACKET_LOSS = 0.05  # Target packet loss rate (5%)
    MIN_THROUGHPUT = 1.0    # Minimum throughput (MB/s)
