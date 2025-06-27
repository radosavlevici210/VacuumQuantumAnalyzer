#!/usr/bin/env python3
"""
Production deployment script for Scientific Calculator application.
This script ensures all production requirements are met before deployment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class ProductionValidator:
    """Validates production readiness of the application."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        
    def validate_files(self):
        """Check that all required files exist."""
        required_files = [
            'app.py',
            'config.py', 
            'utils.py',
            'vacuum_energy.py',
            'quantum_genetics.py',
            '.streamlit/config.toml',
            'README.md',
            'LICENSE-MIT',
            'LICENSE-BUSINESS',
            'LICENSE-PROPRIETARY', 
            'LICENSE-NDA'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.issues.append(f"Missing required files: {', '.join(missing_files)}")
        else:
            print("✓ All required files present")
    
    def validate_imports(self):
        """Test that all imports work correctly."""
        try:
            import streamlit
            import numpy
            import pandas
            import scipy
            print("✓ Core dependencies available")
        except ImportError as e:
            self.issues.append(f"Missing core dependency: {e}")
        
        try:
            from config import ProductionConfig
            from utils import safe_calculation
            from vacuum_energy import VacuumEnergyCalculator
            from quantum_genetics import QuantumGeneticsCalculator
            print("✓ Application modules import successfully")
        except ImportError as e:
            self.issues.append(f"Application import error: {e}")
    
    def validate_calculations(self):
        """Test that calculations work correctly."""
        try:
            from vacuum_energy import VacuumEnergyCalculator
            calc = VacuumEnergyCalculator()
            result = calc.calculate_all(6.62607015e-34, 299792458.0, 1.0, 1e20, 0.36, 2.7)
            if not result or 'vacuumEnergyDensity' not in result:
                self.issues.append("Vacuum energy calculation failed")
            else:
                print("✓ Vacuum energy calculations working")
        except Exception as e:
            self.issues.append(f"Vacuum energy calculation error: {e}")
        
        try:
            from quantum_genetics import QuantumGeneticsCalculator
            calc = QuantumGeneticsCalculator()
            result = calc.calculate_all(100, 0.85, 1e-9, 1.0, 0.5, 2.0, 0.01, 25)
            if not result or 'geneticSuperposition' not in result:
                self.issues.append("Quantum genetics calculation failed")
            else:
                print("✓ Quantum genetics calculations working")
        except Exception as e:
            self.issues.append(f"Quantum genetics calculation error: {e}")
    
    def validate_streamlit_config(self):
        """Check Streamlit configuration."""
        config_path = Path('.streamlit/config.toml')
        if config_path.exists():
            content = config_path.read_text()
            if 'headless = true' in content and 'port = 5000' in content:
                print("✓ Streamlit configuration correct")
            else:
                self.warnings.append("Streamlit configuration may need adjustment")
        else:
            self.issues.append("Missing Streamlit configuration")
    
    def validate_performance(self):
        """Test application performance."""
        try:
            import time
            from vacuum_energy import VacuumEnergyCalculator
            
            start_time = time.time()
            calc = VacuumEnergyCalculator()
            calc.calculate_all(6.62607015e-34, 299792458.0, 1.0, 1e20, 0.36, 2.7)
            execution_time = time.time() - start_time
            
            if execution_time > 5.0:
                self.warnings.append(f"Calculation time slow: {execution_time:.2f}s")
            else:
                print(f"✓ Performance acceptable: {execution_time:.3f}s")
        except Exception as e:
            self.warnings.append(f"Performance test failed: {e}")
    
    def run_validation(self):
        """Run all validation checks."""
        print("=== Production Validation ===")
        
        self.validate_files()
        self.validate_imports()
        self.validate_calculations()
        self.validate_streamlit_config()
        self.validate_performance()
        
        print("\n=== Validation Results ===")
        
        if self.issues:
            print("❌ CRITICAL ISSUES FOUND:")
            for issue in self.issues:
                print(f"  • {issue}")
            return False
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        print("✅ Application is production ready!")
        return True

def create_production_startup_script():
    """Create optimized startup script for production."""
    startup_script = """#!/bin/bash
# Production startup script for Scientific Calculator

echo "Starting Scientific Calculator in production mode..."

# Set production environment variables
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=5000
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Start the application
streamlit run app.py \\
    --server.headless true \\
    --server.port 5000 \\
    --server.address 0.0.0.0 \\
    --browser.gatherUsageStats false \\
    --logger.level error \\
    --client.showErrorDetails false
"""
    
    with open('start_production.sh', 'w') as f:
        f.write(startup_script)
    
    os.chmod('start_production.sh', 0o755)
    print("✓ Created production startup script")

def optimize_streamlit_config():
    """Optimize Streamlit configuration for production."""
    config_content = """[server]
headless = true
address = "0.0.0.0"
port = 5000
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[logger]
level = "error"

[client]
showErrorDetails = false
caching = true

[theme]
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
"""
    
    os.makedirs('.streamlit', exist_ok=True)
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    
    print("✓ Optimized Streamlit configuration")

def create_health_check():
    """Create health check endpoint for production monitoring."""
    health_check_script = """#!/usr/bin/env python3
import requests
import sys
import time

def check_health():
    try:
        response = requests.get('http://localhost:5000', timeout=10)
        if response.status_code == 200:
            print("✓ Application is healthy")
            return True
        else:
            print(f"❌ Application returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)
"""
    
    with open('health_check.py', 'w') as f:
        f.write(health_check_script)
    
    os.chmod('health_check.py', 0o755)
    print("✓ Created health check script")

def main():
    """Main deployment validation and setup."""
    print("Scientific Calculator - Production Deployment Setup")
    print("=" * 50)
    
    # Run validation
    validator = ProductionValidator()
    if not validator.run_validation():
        print("\n❌ Fix critical issues before deployment")
        sys.exit(1)
    
    # Create production files
    print("\n=== Setting Up Production Environment ===")
    optimize_streamlit_config()
    create_production_startup_script()
    create_health_check()
    
    print("\n=== Production Setup Complete ===")
    print("To start the application in production mode:")
    print("  ./start_production.sh")
    print("\nTo check application health:")
    print("  python health_check.py")
    print("\nApplication will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()