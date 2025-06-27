import streamlit as st
import numpy as np
import pandas as pd
import time
import logging
from vacuum_energy import VacuumEnergyCalculator
from quantum_genetics import QuantumGeneticsCalculator
from config import ProductionConfig
from utils import (
    log_calculation, safe_calculation, validate_input_range,
    display_error_message, display_success_message, export_results_json,
    export_results_csv, create_results_summary, check_calculation_limits,
    log_user_interaction, performance_monitor, CalculationError
)

# Set page configuration
st.set_page_config(
    page_title=ProductionConfig.APP_NAME,
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for performance monitoring
if 'performance_stats' not in st.session_state:
    st.session_state.performance_stats = {
        'total_calculations': 0,
        'successful_calculations': 0,
        'failed_calculations': 0
    }

# Add copyright notice and app info
st.sidebar.markdown(f"""
---
### Application Info
**Version:** {ProductionConfig.APP_VERSION}  
**Author:** {ProductionConfig.APP_AUTHOR}  
**Watermark:** {ProductionConfig.WATERMARK_ID}

---
### Copyright Notice
© Ervin Remus Radosavlevici  
All rights reserved.

This software, its content, code, and all features are protected under international copyright law.

Watermark ID: ErvinRemusOfficial™  
Ownership is non-transferable and non-tradable without signed, written permission from Ervin Remus Radosavlevici.

Unauthorized reproduction, resale, modification, or use for AI model training is strictly forbidden.  
Includes embedded watermark and creation timestamp for verification.

Violations will result in legal action.

---
### License Options
- **MIT License**: Educational use
- **Business License**: Commercial use
- **Proprietary License**: Full rights
- **NDA License**: Confidential research

Contact for licensing information.

---
### Performance Monitor
""")

# Add performance statistics
if st.session_state.performance_stats['total_calculations'] > 0:
    success_rate = (st.session_state.performance_stats['successful_calculations'] / 
                   st.session_state.performance_stats['total_calculations'] * 100)
    
    st.sidebar.metric("Total Calculations", st.session_state.performance_stats['total_calculations'])
    st.sidebar.metric("Success Rate", f"{success_rate:.1f}%")
    st.sidebar.metric("Failed Calculations", st.session_state.performance_stats['failed_calculations'])
    
    # Performance stats from monitor
    perf_stats = performance_monitor.get_performance_stats()
    if "average_calculation_time" in perf_stats:
        st.sidebar.metric("Avg Calc Time", f"{perf_stats['average_calculation_time']:.3f}s")

st.sidebar.markdown("---")

# Main title
st.title("⚛️ Scientific Calculator")
st.subheader("Vacuum Energy & Quantum Genetic Algorithm Calculations")

# Create tabs for different calculation types
tab1, tab2 = st.tabs(["🌌 Vacuum Energy", "🧬 Quantum Genetics"])

with tab1:
    st.header("Vacuum Energy Calculations")
    
    # Create two columns for input and results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        # Input parameters for vacuum energy calculations
        planck_constant = st.number_input(
            "Planck Constant (J⋅s)", 
            value=6.62607015e-34, 
            format="%.2e",
            help="Fundamental physical constant"
        )
        
        speed_of_light = st.number_input(
            "Speed of Light (m/s)", 
            value=299792458.0, 
            format="%.2e",
            help="Speed of light in vacuum"
        )
        
        volume = st.number_input(
            "Volume (m³)", 
            value=1.0, 
            min_value=0.0,
            help="Volume of space to analyze"
        )
        
        cutoff_frequency = st.number_input(
            "Cutoff Frequency (Hz)", 
            value=1e20, 
            format="%.2e",
            min_value=0.0,
            help="Maximum frequency for calculations"
        )
        
        extraction_factor = st.slider(
            "Extraction Factor", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.36,
            help="Efficiency factor for energy extraction"
        )
        
        temperature = st.number_input(
            "Temperature (K)", 
            value=2.7, 
            min_value=0.0,
            help="Background temperature"
        )
        
        calculate_vacuum = st.button("Calculate Vacuum Energy", type="primary")
    
    with col2:
        st.subheader("Results")
        
        if calculate_vacuum:
            start_time = time.time()
            log_user_interaction("vacuum_energy_calculation", {
                "volume": volume,
                "cutoff_frequency": cutoff_frequency,
                "extraction_factor": extraction_factor,
                "temperature": temperature
            })
            
            try:
                # Validate input parameters
                limits = ProductionConfig.get_calculation_limits()
                validate_input_range(cutoff_frequency, limits["cutoff_frequency"]["min"], 
                                   limits["cutoff_frequency"]["max"], "Cutoff Frequency")
                validate_input_range(volume, limits["volume"]["min"], 
                                   limits["volume"]["max"], "Volume")
                
                # Perform calculation with error handling
                calculator = VacuumEnergyCalculator()
                calculation_result = safe_calculation(
                    calculator.calculate_all,
                    planck_constant, speed_of_light, volume, 
                    cutoff_frequency, extraction_factor, temperature
                )
                
                execution_time = time.time() - start_time
                
                if calculation_result["success"]:
                    results = calculation_result["result"]
                    
                    # Update performance stats
                    st.session_state.performance_stats['total_calculations'] += 1
                    st.session_state.performance_stats['successful_calculations'] += 1
                    performance_monitor.record_calculation(execution_time, True)
                    
                    display_success_message("Vacuum Energy Calculation", execution_time)
                    
                    # Create results summary
                    results_df = create_results_summary(results)
                    
                    # Display results in tabs
                    res_tab1, res_tab2, res_tab3 = st.tabs(["📊 Results", "📈 Summary", "📁 Export"])
                    
                    with res_tab1:
                        # Create metrics display
                        col2a, col2b = st.columns(2)
                        
                        with col2a:
                            st.metric("Vacuum Energy Density", f"{results['vacuumEnergyDensity']} J/m³")
                            st.metric("Total Vacuum Energy", f"{results['totalVacuumEnergy']} J")
                            st.metric("Harvestable Energy", f"{results['harvestableEnergy']} J")
                            st.metric("Power Output", f"{results['powerOutput']} W")
                        
                        with col2b:
                            st.metric("Extraction Efficiency", f"{results['extractionEfficiency']}%")
                            st.metric("Vacuum Resistance", f"{results['vacuumResistance']} Ω")
                            st.metric("Energy Yield/Second", f"{results['energyYieldPerSecond']} J/s")
                            st.metric("Feasibility Index", f"{results['feasibilityIndex']:.2f}")
                    
                    with res_tab2:
                        st.subheader("Calculation Summary")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Performance info
                        st.info(f"⚡ Calculation completed in {execution_time:.4f} seconds")
                        st.info(f"🔬 {len(results)} parameters calculated")
                    
                    with res_tab3:
                        st.subheader("Export Options")
                        
                        # JSON export
                        if st.button("📄 Export as JSON", key="vacuum_json"):
                            json_data = export_results_json(results, "vacuum_energy_results.json")
                            st.download_button(
                                label="Download JSON File",
                                data=json_data,
                                file_name="vacuum_energy_results.json",
                                mime="application/json"
                            )
                        
                        # CSV export
                        if st.button("📊 Export as CSV", key="vacuum_csv"):
                            csv_data = export_results_csv(results, "vacuum_energy_results.csv")
                            st.download_button(
                                label="Download CSV File",
                                data=csv_data,
                                file_name="vacuum_energy_results.csv",
                                mime="text/csv"
                            )
                        
                        # Display raw JSON for copy-paste
                        with st.expander("View Raw JSON"):
                            st.json(results)
                
                else:
                    # Handle calculation error
                    st.session_state.performance_stats['total_calculations'] += 1
                    st.session_state.performance_stats['failed_calculations'] += 1
                    performance_monitor.record_calculation(execution_time, False)
                    
                    display_error_message(calculation_result["error"], "Vacuum Energy Calculation")
                    
            except ValueError as e:
                execution_time = time.time() - start_time
                st.session_state.performance_stats['total_calculations'] += 1
                st.session_state.performance_stats['failed_calculations'] += 1
                performance_monitor.record_calculation(execution_time, False)
                
                display_error_message(str(e), "Input Validation")
                
            except Exception as e:
                execution_time = time.time() - start_time
                st.session_state.performance_stats['total_calculations'] += 1
                st.session_state.performance_stats['failed_calculations'] += 1
                performance_monitor.record_calculation(execution_time, False)
                
                display_error_message(f"Unexpected error: {str(e)}", "System Error")

with tab2:
    st.header("Quantum Genetic Algorithm Calculations")
    
    # Create two columns for input and results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        # Input parameters for quantum genetics calculations
        population_size = st.number_input(
            "Population Size", 
            value=100, 
            min_value=1,
            help="Size of the genetic population"
        )
        
        quantum_state_amplitude = st.slider(
            "Quantum State Amplitude", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.85,
            help="Amplitude of quantum superposition"
        )
        
        coherence_time = st.number_input(
            "Coherence Time (s)", 
            value=1e-9, 
            format="%.2e",
            min_value=0.0,
            help="Time quantum coherence is maintained"
        )
        
        barrier_height = st.number_input(
            "Energy Barrier Height (eV)", 
            value=1.0, 
            min_value=0.0,
            help="Energy barrier for quantum tunneling"
        )
        
        particle_energy = st.number_input(
            "Particle Energy (eV)", 
            value=0.5, 
            min_value=0.0,
            help="Energy of the particle attempting tunneling"
        )
        
        selection_pressure = st.slider(
            "Selection Pressure", 
            min_value=0.0, 
            max_value=5.0, 
            value=2.0,
            help="Intensity of natural selection"
        )
        
        mutation_rate = st.slider(
            "Mutation Rate", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.01,
            help="Probability of genetic mutation"
        )
        
        generation_count = st.number_input(
            "Current Generation", 
            value=25, 
            min_value=1,
            help="Current generation number"
        )
        
        calculate_quantum = st.button("Calculate Quantum Genetics", type="primary")
    
    with col2:
        st.subheader("Results")
        
        if calculate_quantum:
            start_time = time.time()
            log_user_interaction("quantum_genetics_calculation", {
                "population_size": population_size,
                "quantum_state_amplitude": quantum_state_amplitude,
                "coherence_time": coherence_time,
                "barrier_height": barrier_height,
                "particle_energy": particle_energy,
                "selection_pressure": selection_pressure,
                "mutation_rate": mutation_rate,
                "generation_count": generation_count
            })
            
            try:
                # Validate input parameters
                limits = ProductionConfig.get_calculation_limits()
                validate_input_range(population_size, limits["population_size"]["min"], 
                                   limits["population_size"]["max"], "Population Size")
                
                if not 0 <= quantum_state_amplitude <= 1:
                    raise ValueError("Quantum State Amplitude must be between 0 and 1")
                if not 0 <= mutation_rate <= 1:
                    raise ValueError("Mutation Rate must be between 0 and 1")
                if coherence_time <= 0:
                    raise ValueError("Coherence Time must be positive")
                
                # Perform calculation with error handling
                calculator = QuantumGeneticsCalculator()
                calculation_result = safe_calculation(
                    calculator.calculate_all,
                    population_size, quantum_state_amplitude, coherence_time,
                    barrier_height, particle_energy, selection_pressure,
                    mutation_rate, generation_count
                )
                
                execution_time = time.time() - start_time
                
                if calculation_result["success"]:
                    results = calculation_result["result"]
                    
                    # Update performance stats
                    st.session_state.performance_stats['total_calculations'] += 1
                    st.session_state.performance_stats['successful_calculations'] += 1
                    performance_monitor.record_calculation(execution_time, True)
                    
                    display_success_message("Quantum Genetics Calculation", execution_time)
                    
                    # Create results summary
                    results_df = create_results_summary(results)
                    
                    # Display results in tabs
                    res_tab1, res_tab2, res_tab3 = st.tabs(["📊 Results", "📈 Summary", "📁 Export"])
                    
                    with res_tab1:
                        # Create metrics display
                        col2a, col2b = st.columns(2)
                        
                        with col2a:
                            st.metric("Genetic Superposition", f"{results['geneticSuperposition']}")
                            st.metric("Quantum Coherence", f"{results['quantumCoherence']}")
                            st.metric("Tunnel Probability", f"{results['tunnelProbability']}")
                            st.metric("Quantum Leap Potential", f"{results['quantumLeapPotential']}")
                        
                        with col2b:
                            st.metric("Fitness Gradient", f"{results['fitnessGradient']}")
                            st.metric("Speciation Probability", f"{results['speciationProbability']}")
                            st.metric("Evolution Acceleration", f"{results['evolutionAcceleration']}")
                            st.metric("Next Evolution Step", f"{results['nextEvolutionStep']}")
                    
                    with res_tab2:
                        st.subheader("Calculation Summary")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Performance info
                        st.info(f"⚡ Calculation completed in {execution_time:.4f} seconds")
                        st.info(f"🧬 {len(results)} genetic parameters calculated")
                    
                    with res_tab3:
                        st.subheader("Export Options")
                        
                        # JSON export
                        if st.button("📄 Export as JSON", key="quantum_json_export"):
                            json_data = export_results_json(results, "quantum_genetics_results.json")
                            st.download_button(
                                label="Download JSON File",
                                data=json_data,
                                file_name="quantum_genetics_results.json",
                                mime="application/json",
                                key="quantum_json_download"
                            )
                        
                        # CSV export
                        if st.button("📊 Export as CSV", key="quantum_csv_export"):
                            csv_data = export_results_csv(results, "quantum_genetics_results.csv")
                            st.download_button(
                                label="Download CSV File",
                                data=csv_data,
                                file_name="quantum_genetics_results.csv",
                                mime="text/csv",
                                key="quantum_csv_download"
                            )
                        
                        # Display raw JSON for copy-paste
                        with st.expander("View Raw JSON"):
                            st.json(results)
                
                else:
                    # Handle calculation error
                    st.session_state.performance_stats['total_calculations'] += 1
                    st.session_state.performance_stats['failed_calculations'] += 1
                    performance_monitor.record_calculation(execution_time, False)
                    
                    display_error_message(calculation_result["error"], "Quantum Genetics Calculation")
                    
            except ValueError as e:
                execution_time = time.time() - start_time
                st.session_state.performance_stats['total_calculations'] += 1
                st.session_state.performance_stats['failed_calculations'] += 1
                performance_monitor.record_calculation(execution_time, False)
                
                display_error_message(str(e), "Input Validation")
                
            except Exception as e:
                execution_time = time.time() - start_time
                st.session_state.performance_stats['total_calculations'] += 1
                st.session_state.performance_stats['failed_calculations'] += 1
                performance_monitor.record_calculation(execution_time, False)
                
                display_error_message(f"Unexpected error: {str(e)}", "System Error")

# Footer with additional information
st.markdown("---")
st.markdown(f"""
### About This Calculator
**{ProductionConfig.APP_NAME}**  
Version {ProductionConfig.APP_VERSION} | {ProductionConfig.WATERMARK_ID}

This professional-grade scientific calculator performs advanced calculations for:
- **Vacuum Energy**: Theoretical calculations based on quantum field theory
- **Quantum Genetics**: Quantum mechanical effects in genetic algorithms

All calculations use established scientific formulas and constants from peer-reviewed literature. Results are provided in scientific notation for maximum precision and accuracy.

### Technical Specifications
- **High-Precision Computing**: NumPy and SciPy libraries
- **Real-Time Processing**: Sub-second calculation times
- **Production-Ready**: Input validation and error handling
- **Export Capabilities**: JSON and CSV formats with metadata
- **Performance Monitoring**: Built-in analytics and logging
""")

# License and usage information
st.info("""
**📜 Licensing Information**  
This software is available under multiple licensing options:
- MIT License for educational use
- Business License for commercial applications  
- Proprietary License for full rights
- NDA License for confidential research

Contact the author for licensing inquiries and custom development.
""")

# Technical support and contact
st.markdown(f"""
---
**© {ProductionConfig.APP_AUTHOR}** | **Watermark ID:** {ProductionConfig.WATERMARK_ID}  
All rights reserved. Unauthorized use is prohibited.
""")
