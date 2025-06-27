"""
Production configuration settings for Scientific Calculator application.
"""

import os
from typing import Dict, Any

class ProductionConfig:
    """Production configuration class."""
    
    # Application settings
    APP_NAME = "Scientific Calculator - Vacuum Energy & Quantum Genetics"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Ervin Remus Radosavlevici"
    WATERMARK_ID = "ErvinRemusOfficial™"
    
    # Server settings
    SERVER_HOST = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "5000"))
    
    # Calculation limits and defaults
    MAX_CUTOFF_FREQUENCY = 1e25
    MIN_CUTOFF_FREQUENCY = 1e10
    DEFAULT_CUTOFF_FREQUENCY = 1e20
    
    MAX_VOLUME = 1e10
    MIN_VOLUME = 1e-20
    DEFAULT_VOLUME = 1.0
    
    MAX_POPULATION_SIZE = 10000
    MIN_POPULATION_SIZE = 1
    DEFAULT_POPULATION_SIZE = 100
    
    # Performance settings
    CACHE_TTL = 3600  # 1 hour
    MAX_CONCURRENT_CALCULATIONS = 10
    CALCULATION_TIMEOUT = 30  # seconds
    
    # Security settings
    ENABLE_RATE_LIMITING = True
    MAX_REQUESTS_PER_MINUTE = 100
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Export settings
    MAX_EXPORT_SIZE = 10000  # Maximum number of records
    ALLOWED_EXPORT_FORMATS = ["json", "csv", "xlsx"]
    
    @classmethod
    def get_calculation_limits(cls) -> Dict[str, Any]:
        """Get calculation parameter limits."""
        return {
            "cutoff_frequency": {
                "min": cls.MIN_CUTOFF_FREQUENCY,
                "max": cls.MAX_CUTOFF_FREQUENCY,
                "default": cls.DEFAULT_CUTOFF_FREQUENCY
            },
            "volume": {
                "min": cls.MIN_VOLUME,
                "max": cls.MAX_VOLUME,
                "default": cls.DEFAULT_VOLUME
            },
            "population_size": {
                "min": cls.MIN_POPULATION_SIZE,
                "max": cls.MAX_POPULATION_SIZE,
                "default": cls.DEFAULT_POPULATION_SIZE
            }
        }
    
    @classmethod
    def get_app_info(cls) -> Dict[str, str]:
        """Get application information."""
        return {
            "name": cls.APP_NAME,
            "version": cls.APP_VERSION,
            "author": cls.APP_AUTHOR,
            "watermark": cls.WATERMARK_ID
        }