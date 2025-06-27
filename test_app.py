"""
Test script to identify production issues in the application.
"""
import sys
import traceback

def test_imports():
    """Test all module imports."""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit imported")
    except Exception as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        from config import ProductionConfig
        print("✓ Config imported")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from utils import (
            safe_calculation, validate_input_range, display_error_message,
            export_results_json, performance_monitor
        )
        print("✓ Utils imported")
    except Exception as e:
        print(f"✗ Utils import failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        from vacuum_energy import VacuumEnergyCalculator
        from quantum_genetics import QuantumGeneticsCalculator
        print("✓ Calculator modules imported")
    except Exception as e:
        print(f"✗ Calculator import failed: {e}")
        return False
    
    return True

def test_calculations():
    """Test calculation functionality."""
    print("\nTesting calculations...")
    
    try:
        from vacuum_energy import VacuumEnergyCalculator
        calc = VacuumEnergyCalculator()
        result = calc.calculate_all(6.62607015e-34, 299792458.0, 1.0, 1e20, 0.36, 2.7)
        print("✓ Vacuum energy calculations work")
        print(f"  Sample result: {result['vacuumEnergyDensity']}")
    except Exception as e:
        print(f"✗ Vacuum energy calculation failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        from quantum_genetics import QuantumGeneticsCalculator
        calc = QuantumGeneticsCalculator()
        result = calc.calculate_all(100, 0.85, 1e-9, 1.0, 0.5, 2.0, 0.01, 25)
        print("✓ Quantum genetics calculations work")
        print(f"  Sample result: {result['geneticSuperposition']}")
    except Exception as e:
        print(f"✗ Quantum genetics calculation failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_utils():
    """Test utility functions."""
    print("\nTesting utilities...")
    
    try:
        from utils import safe_calculation, validate_input_range, export_results_json
        from vacuum_energy import VacuumEnergyCalculator
        
        # Test safe calculation
        calc = VacuumEnergyCalculator()
        result = safe_calculation(calc.calculate_all, 6.62607015e-34, 299792458.0, 1.0, 1e20, 0.36, 2.7)
        if result["success"]:
            print("✓ Safe calculation works")
        else:
            print(f"✗ Safe calculation failed: {result['error']}")
            return False
        
        # Test validation
        validate_input_range(1.0, 0.1, 10.0, "test_param")
        print("✓ Input validation works")
        
        # Test export
        test_data = {"param1": "1.234e-05", "param2": "2.567e+08"}
        json_result = export_results_json(test_data)
        if "metadata" in json_result:
            print("✓ JSON export works")
        else:
            print("✗ JSON export missing metadata")
            return False
        
    except Exception as e:
        print(f"✗ Utils test failed: {e}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("=== Production Issue Testing ===")
    
    success = True
    success &= test_imports()
    success &= test_calculations()
    success &= test_utils()
    
    if success:
        print("\n✓ All tests passed - Application appears to be working correctly")
    else:
        print("\n✗ Some tests failed - Issues found")
    
    print("=== Test Complete ===")