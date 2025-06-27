#!/usr/bin/env python3
"""
Production monitoring and optimization for Scientific Calculator.
Monitors performance, handles errors, and ensures system reliability.
"""

import time
import psutil
import logging
import json
from datetime import datetime
from pathlib import Path

class ProductionMonitor:
    """Monitors application performance and system health."""
    
    def __init__(self):
        self.setup_logging()
        self.metrics = {
            'start_time': time.time(),
            'requests_processed': 0,
            'errors_count': 0,
            'avg_response_time': 0,
            'memory_usage': [],
            'cpu_usage': []
        }
    
    def setup_logging(self):
        """Configure production logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('production.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ProductionMonitor')
    
    def record_request(self, execution_time, success=True):
        """Record a request for monitoring."""
        self.metrics['requests_processed'] += 1
        
        if not success:
            self.metrics['errors_count'] += 1
        
        # Update average response time
        current_avg = self.metrics['avg_response_time']
        request_count = self.metrics['requests_processed']
        self.metrics['avg_response_time'] = (
            (current_avg * (request_count - 1) + execution_time) / request_count
        )
        
        self.logger.info(f"Request processed in {execution_time:.3f}s - Success: {success}")
    
    def collect_system_metrics(self):
        """Collect system performance metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        self.metrics['cpu_usage'].append(cpu_percent)
        self.metrics['memory_usage'].append(memory.percent)
        
        # Keep only last 100 measurements
        if len(self.metrics['cpu_usage']) > 100:
            self.metrics['cpu_usage'] = self.metrics['cpu_usage'][-100:]
            self.metrics['memory_usage'] = self.metrics['memory_usage'][-100:]
    
    def get_health_status(self):
        """Get current health status."""
        uptime = time.time() - self.metrics['start_time']
        error_rate = (self.metrics['errors_count'] / 
                     max(self.metrics['requests_processed'], 1) * 100)
        
        status = {
            'status': 'healthy',
            'uptime_seconds': uptime,
            'requests_processed': self.metrics['requests_processed'],
            'error_rate_percent': error_rate,
            'avg_response_time_ms': self.metrics['avg_response_time'] * 1000,
            'timestamp': datetime.now().isoformat()
        }
        
        # Determine health status
        if error_rate > 10:
            status['status'] = 'degraded'
        if error_rate > 25:
            status['status'] = 'unhealthy'
        
        return status
    
    def save_metrics(self):
        """Save metrics to file."""
        metrics_file = Path('metrics.json')
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)

# Global monitor instance
monitor = ProductionMonitor()