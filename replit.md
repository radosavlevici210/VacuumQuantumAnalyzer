# Scientific Calculator - Vacuum Energy & Quantum Genetics

## Overview

This is a Streamlit-based scientific calculator application that performs specialized calculations in two domains: vacuum energy (from quantum field theory) and quantum genetics (quantum-inspired genetic algorithms). The application provides an interactive web interface for researchers and students to explore theoretical physics calculations.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **UI Components**: Tab-based interface with two main calculation modules
- **Layout**: Wide layout with sidebar for copyright information
- **Styling**: Built-in Streamlit components with custom configuration

### Backend Architecture
- **Language**: Python 3.11
- **Structure**: Modular design with separate calculator classes
- **Core Modules**:
  - `VacuumEnergyCalculator`: Handles quantum field theory calculations
  - `QuantumGeneticsCalculator`: Handles quantum genetic algorithm calculations
- **Scientific Libraries**: NumPy, SciPy, and Pandas for mathematical operations

### Calculation Engines
1. **Vacuum Energy Module** (`vacuum_energy.py`):
   - Calculates vacuum energy density using quantum field theory
   - Computes total vacuum energy for given volumes
   - Based on theoretical physics principles

2. **Quantum Genetics Module** (`quantum_genetics.py`):
   - Calculates genetic superposition factors
   - Computes quantum coherence in biological systems
   - Applies quantum mechanics to genetic algorithms

## Key Components

### Main Application (`app.py`)
- Streamlit interface with tabbed navigation
- Input parameter handling and validation
- Real-time calculation display
- Copyright protection and watermarking

### Scientific Calculators
- **VacuumEnergyCalculator Class**:
  - Uses physical constants from SciPy
  - Implements quantum field theory formulas
  - Error handling for invalid inputs

- **QuantumGeneticsCalculator Class**:
  - Combines quantum mechanics with genetic algorithms
  - Calculates superposition and coherence effects
  - Temperature-dependent decoherence modeling

### Configuration Files
- **Replit Configuration** (`.replit`): Defines Python 3.11 environment and deployment settings
- **Streamlit Configuration** (`.streamlit/config.toml`): Server configuration for headless operation
- **Project Dependencies** (`pyproject.toml`): Manages scientific Python packages

## Data Flow

1. **User Input**: Parameters entered through Streamlit interface
2. **Validation**: Input validation and error checking
3. **Calculation**: Processing through specialized calculator classes
4. **Results**: Real-time display of calculated values and visualizations
5. **Error Handling**: Graceful handling of calculation errors with user feedback

## External Dependencies

### Core Scientific Libraries
- **NumPy** (>=2.3.1): Numerical computing and array operations
- **SciPy** (>=1.16.0): Scientific computing and physical constants
- **Pandas** (>=2.3.0): Data manipulation and analysis

### Web Framework
- **Streamlit** (>=1.46.1): Interactive web application framework

### Additional Dependencies
- **Altair**: Data visualization (through Streamlit)
- **Cachetools**: Performance optimization
- **Blinker**: Event handling

## Deployment Strategy

### Replit Platform
- **Target**: Autoscale deployment on Replit
- **Runtime**: Python 3.11 with Nix package management
- **Port Configuration**: Application runs on port 5000
- **Environment**: Stable Nix channel 24_05 with required system packages

### Development Workflow
- **Run Button**: Configured for parallel workflow execution
- **Server Launch**: Automated Streamlit server startup
- **Port Forwarding**: Automatic port 5000 forwarding for web access

### System Requirements
- **OS Packages**: glibcLocales, libxcrypt, pkg-config, xsimd
- **Python Version**: 3.11 (specified in modules configuration)
- **Memory**: Sufficient for scientific computations with NumPy/SciPy

## Changelog
- June 27, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.