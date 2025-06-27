"""
Utility functions for production-ready Scientific Calculator application.
"""

import logging
import time
import functools
from typing import Any, Callable, Dict, Optional
import streamlit as st
import pandas as pd
import json
from config import ProductionConfig

# Configure logging
logging.basicConfig(
    level=getattr(logging, ProductionConfig.LOG_LEVEL),
    format=ProductionConfig.LOG_FORMAT
)
logger = logging.getLogger(__name__)

class CalculationError(Exception):
    """Custom exception for calculation errors."""
    pass

def log_calculation(func: Callable) -> Callable:
    """Decorator to log calculation attempts and results."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_name = func.__name__
        
        try:
            logger.info(f"Starting calculation: {function_name}")
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Calculation completed: {function_name} in {execution_time:.4f}s")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Calculation failed: {function_name} after {execution_time:.4f}s - {str(e)}")
            raise CalculationError(f"Calculation error in {function_name}: {str(e)}")
    
    return wrapper

def validate_input_range(value: float, min_val: float, max_val: float, param_name: str) -> bool:
    """Validate that input value is within acceptable range."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{param_name} must be a number")
    
    if value < min_val or value > max_val:
        raise ValueError(f"{param_name} must be between {min_val} and {max_val}")
    
    return True

def format_scientific_result(value: float, precision: int = 3) -> str:
    """Format numerical result for scientific display."""
    if value == 0:
        return "0.000"
    
    if abs(value) >= 1e-3 and abs(value) < 1e6:
        return f"{value:.{precision}f}"
    else:
        return f"{value:.{precision}e}"

def safe_calculation(calculation_func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """Safely execute calculation with error handling."""
    try:
        result = calculation_func(*args, **kwargs)
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def export_results_json(results: Dict[str, Any], filename: str = "calculation_results.json") -> str:
    """Export calculation results to JSON format."""
    try:
        # Add metadata
        export_data = {
            "metadata": {
                "application": ProductionConfig.APP_NAME,
                "version": ProductionConfig.APP_VERSION,
                "author": ProductionConfig.APP_AUTHOR,
                "watermark": ProductionConfig.WATERMARK_ID,
                "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
            },
            "results": results
        }
        
        json_str = json.dumps(export_data, indent=2)
        logger.info(f"Results exported to JSON format ({len(json_str)} characters)")
        return json_str
        
    except Exception as e:
        logger.error(f"JSON export error: {str(e)}")
        raise CalculationError(f"Failed to export results to JSON: {str(e)}")

def export_results_csv(results: Dict[str, Any], filename: str = "calculation_results.csv") -> str:
    """Export calculation results to CSV format."""
    try:
        # Create DataFrame with metadata
        df_data = {
            "Parameter": list(results.keys()),
            "Value": list(results.values()),
            "Timestamp": [time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())] * len(results),
            "Application": [ProductionConfig.APP_NAME] * len(results),
            "Watermark": [ProductionConfig.WATERMARK_ID] * len(results)
        }
        
        df = pd.DataFrame(df_data)
        csv_str = df.to_csv(index=False)
        logger.info(f"Results exported to CSV format ({len(csv_str)} characters)")
        return csv_str
        
    except Exception as e:
        logger.error(f"CSV export error: {str(e)}")
        raise CalculationError(f"Failed to export results to CSV: {str(e)}")

def display_error_message(error: str, context: str = "Calculation") -> None:
    """Display user-friendly error message."""
    st.error(f"❌ {context} Error")
    st.error(f"**Details:** {error}")
    st.info("💡 **Suggestions:**")
    st.info("• Check that all input parameters are within valid ranges")
    st.info("• Ensure all required fields are filled")
    st.info("• Try reducing the magnitude of large input values")
    st.info("• Contact support if the problem persists")

def display_success_message(calculation_type: str, execution_time: Optional[float] = None) -> None:
    """Display success message with optional performance info."""
    success_msg = f"✅ {calculation_type} completed successfully!"
    if execution_time:
        success_msg += f" ({execution_time:.3f}s)"
    st.success(success_msg)

def create_results_summary(results: Dict[str, Any]) -> pd.DataFrame:
    """Create a summary DataFrame of calculation results."""
    summary_data = []
    
    for key, value in results.items():
        # Format parameter name for display
        param_display = key.replace('_', ' ').replace('camelCase', ' ').title()
        
        # Determine value type and format
        if isinstance(value, str):
            try:
                # Try to parse scientific notation
                float_val = float(value)
                formatted_value = format_scientific_result(float_val)
                value_type = "Scientific"
            except (ValueError, TypeError):
                formatted_value = str(value)
                value_type = "Text"
        else:
            formatted_value = format_scientific_result(float(value))
            value_type = "Numeric"
        
        summary_data.append({
            "Parameter": param_display,
            "Value": formatted_value,
            "Type": value_type
        })
    
    return pd.DataFrame(summary_data)

def check_calculation_limits(params: Dict[str, Any]) -> Dict[str, bool]:
    """Check if calculation parameters are within production limits."""
    limits = ProductionConfig.get_calculation_limits()
    validation_results = {}
    
    for param_name, param_value in params.items():
        if param_name in limits:
            limit_config = limits[param_name]
            is_valid = (
                limit_config["min"] <= param_value <= limit_config["max"]
            )
            validation_results[param_name] = is_valid
            
            if not is_valid:
                logger.warning(
                    f"Parameter {param_name} ({param_value}) outside limits "
                    f"[{limit_config['min']}, {limit_config['max']}]"
                )
    
    return validation_results

def get_app_watermark() -> str:
    """Get application watermark for display."""
    return f"© {ProductionConfig.APP_AUTHOR} | {ProductionConfig.WATERMARK_ID}"

def log_user_interaction(interaction_type: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Log user interaction for analytics and debugging."""
    interaction_details = details if details is not None else {}
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "type": interaction_type,
        "details": interaction_details
    }
    
    logger.info(f"User interaction: {json.dumps(log_entry)}")

# Performance monitoring
class PerformanceMonitor:
    """Monitor application performance metrics."""
    
    def __init__(self):
        self.calculation_times = []
        self.error_count = 0
        self.success_count = 0
    
    def record_calculation(self, execution_time: float, success: bool) -> None:
        """Record calculation performance."""
        self.calculation_times.append(execution_time)
        
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        
        # Keep only recent measurements
        if len(self.calculation_times) > 1000:
            self.calculation_times = self.calculation_times[-500:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self.calculation_times:
            return {"status": "No data available"}
        
        avg_time = sum(self.calculation_times) / len(self.calculation_times)
        max_time = max(self.calculation_times)
        min_time = min(self.calculation_times)
        total_calculations = self.success_count + self.error_count
        success_rate = (self.success_count / total_calculations * 100) if total_calculations > 0 else 0
        
        return {
            "average_calculation_time": avg_time,
            "max_calculation_time": max_time,
            "min_calculation_time": min_time,
            "total_calculations": total_calculations,
            "success_rate": success_rate,
            "error_count": self.error_count
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()