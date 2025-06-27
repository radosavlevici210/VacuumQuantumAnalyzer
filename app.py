import streamlit as st
import numpy as np
import pandas as pd
from vacuum_energy import VacuumEnergyCalculator
from quantum_genetics import QuantumGeneticsCalculator

# Set page configuration
st.set_page_config(
    page_title="Scientific Calculator - Vacuum Energy & Quantum Genetics",
    page_icon="⚛️",
    layout="wide"
)

# Add copyright notice
st.sidebar.markdown("""
---
© Ervin Remus Radosavlevici  
All rights reserved.

This software, its content, code, and all features are protected under international copyright law.

Watermark ID: ErvinRemusOfficial™  
Ownership is non-transferable and non-tradable without signed, written permission from Ervin Remus Radosavlevici.

Unauthorized reproduction, resale, modification, or use for AI model training is strictly forbidden.  
Includes embedded watermark and creation timestamp for verification.

Violations will result in legal action.
""")

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
            try:
                calculator = VacuumEnergyCalculator()
                results = calculator.calculate_all(
                    planck_constant, speed_of_light, volume, 
                    cutoff_frequency, extraction_factor, temperature
                )
                
                # Display results in a formatted way
                st.success("Calculations completed successfully!")
                
                # Create metrics display
                col2a, col2b = st.columns(2)
                
                with col2a:
                    st.metric("Vacuum Energy Density", f"{results['vacuumEnergyDensity']:.3e} J/m³")
                    st.metric("Total Vacuum Energy", f"{results['totalVacuumEnergy']:.3e} J")
                    st.metric("Harvestable Energy", f"{results['harvestableEnergy']:.3e} J")
                    st.metric("Power Output", f"{results['powerOutput']:.3e} W")
                
                with col2b:
                    st.metric("Extraction Efficiency", f"{results['extractionEfficiency']:.2f}%")
                    st.metric("Vacuum Resistance", f"{results['vacuumResistance']:.3e} Ω")
                    st.metric("Energy Yield/Second", f"{results['energyYieldPerSecond']:.3e} J/s")
                    st.metric("Feasibility Index", f"{results['feasibilityIndex']:.2f}")
                
                # Export functionality
                if st.button("Export Results as JSON"):
                    st.json(results)
                
                # Download as CSV
                df = pd.DataFrame([results])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="vacuum_energy_results.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")
                st.error("Please check your input parameters and try again.")

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
            try:
                calculator = QuantumGeneticsCalculator()
                results = calculator.calculate_all(
                    population_size, quantum_state_amplitude, coherence_time,
                    barrier_height, particle_energy, selection_pressure,
                    mutation_rate, generation_count
                )
                
                # Display results in a formatted way
                st.success("Calculations completed successfully!")
                
                # Create metrics display
                col2a, col2b = st.columns(2)
                
                with col2a:
                    st.metric("Genetic Superposition", f"{results['geneticSuperposition']:.6f}")
                    st.metric("Quantum Coherence", f"{results['quantumCoherence']:.3e}")
                    st.metric("Tunnel Probability", f"{results['tunnelProbability']:.8f}")
                    st.metric("Quantum Leap Potential", f"{results['quantumLeapPotential']:.6f}")
                
                with col2b:
                    st.metric("Fitness Gradient", f"{results['fitnessGradient']:.3e}")
                    st.metric("Speciation Probability", f"{results['speciationProbability']:.4f}")
                    st.metric("Evolution Acceleration", f"{results['evolutionAcceleration']:.8f}")
                    st.metric("Next Evolution Step", f"{results['nextEvolutionStep']}")
                
                # Export functionality
                if st.button("Export Results as JSON", key="quantum_json"):
                    st.json(results)
                
                # Download as CSV
                df = pd.DataFrame([results])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="quantum_genetics_results.csv",
                    mime="text/csv",
                    key="quantum_csv"
                )
                
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")
                st.error("Please check your input parameters and try again.")

# Footer with additional information
st.markdown("---")
st.markdown("""
### About This Calculator
This scientific calculator performs advanced calculations for:
- **Vacuum Energy**: Theoretical calculations based on quantum field theory
- **Quantum Genetics**: Quantum mechanical effects in genetic algorithms

All calculations use established scientific formulas and constants. Results are provided in scientific notation for precision.
""")

# Performance note
st.info("💡 **Performance Note**: All calculations are performed in real-time with high precision using NumPy and SciPy libraries.")
