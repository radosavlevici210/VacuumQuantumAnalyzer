import numpy as np
import math
from scipy import constants

class QuantumGeneticsCalculator:
    """
    Calculator for quantum genetic algorithm parameters and quantum biological effects.
    Based on quantum mechanics principles applied to genetic algorithms.
    """
    
    def __init__(self):
        # Physical constants
        self.hbar = constants.hbar  # Reduced Planck constant
        self.m_e = constants.m_e    # Electron mass
        self.k_b = constants.k      # Boltzmann constant
        
    def calculate_genetic_superposition(self, quantum_state_amplitude, population_size):
        """
        Calculate genetic superposition factor.
        
        Args:
            quantum_state_amplitude (float): Amplitude of quantum state (0-1)
            population_size (int): Size of the genetic population
            
        Returns:
            float: Genetic superposition value
        """
        try:
            # Superposition based on quantum state amplitude and population diversity
            diversity_factor = np.log(population_size) / 10
            superposition = quantum_state_amplitude * (1 - np.exp(-diversity_factor))
            return superposition
        except Exception as e:
            raise ValueError(f"Error calculating genetic superposition: {str(e)}")
    
    def calculate_quantum_coherence(self, coherence_time, temperature=300):
        """
        Calculate quantum coherence factor.
        
        Args:
            coherence_time (float): Coherence time in seconds
            temperature (float): Temperature in K
            
        Returns:
            float: Quantum coherence value
        """
        try:
            # Coherence decreases with temperature and time
            thermal_decoherence = np.exp(-self.k_b * temperature * coherence_time / self.hbar)
            coherence = coherence_time * thermal_decoherence * 1e8  # Scaling factor
            return coherence
        except Exception as e:
            raise ValueError(f"Error calculating quantum coherence: {str(e)}")
    
    def calculate_tunnel_probability(self, barrier_height, particle_energy, barrier_width=1e-9):
        """
        Calculate quantum tunneling probability.
        
        Args:
            barrier_height (float): Energy barrier height in eV
            particle_energy (float): Particle energy in eV
            barrier_width (float): Barrier width in meters
            
        Returns:
            float: Tunneling probability
        """
        try:
            if particle_energy >= barrier_height:
                return 1.0  # Classical case - particle has enough energy
            
            # Convert eV to Joules
            barrier_height_J = barrier_height * constants.eV
            particle_energy_J = particle_energy * constants.eV
            
            # Tunneling coefficient
            kappa = np.sqrt(2 * self.m_e * (barrier_height_J - particle_energy_J)) / self.hbar
            transmission = np.exp(-2 * kappa * barrier_width)
            
            return transmission
        except Exception as e:
            raise ValueError(f"Error calculating tunnel probability: {str(e)}")
    
    def calculate_quantum_leap_potential(self, tunnel_probability, superposition):
        """
        Calculate quantum leap potential.
        
        Args:
            tunnel_probability (float): Tunneling probability
            superposition (float): Genetic superposition
            
        Returns:
            float: Quantum leap potential
        """
        try:
            # Quantum leap based on tunneling and superposition
            leap_potential = tunnel_probability * superposition * np.sqrt(superposition)
            return leap_potential
        except Exception as e:
            raise ValueError(f"Error calculating quantum leap potential: {str(e)}")
    
    def calculate_fitness_gradient(self, selection_pressure, quantum_coherence):
        """
        Calculate fitness gradient in quantum genetic space.
        
        Args:
            selection_pressure (float): Selection pressure
            quantum_coherence (float): Quantum coherence
            
        Returns:
            float: Fitness gradient
        """
        try:
            # Gradient influenced by quantum effects
            if quantum_coherence > 1e-6:
                gradient = selection_pressure * quantum_coherence * 1e-2
            else:
                gradient = 0.0
            return gradient
        except Exception as e:
            raise ValueError(f"Error calculating fitness gradient: {str(e)}")
    
    def calculate_speciation_probability(self, mutation_rate, superposition, population_size):
        """
        Calculate probability of speciation events.
        
        Args:
            mutation_rate (float): Mutation rate (0-1)
            superposition (float): Genetic superposition
            population_size (int): Population size
            
        Returns:
            float: Speciation probability
        """
        try:
            # Speciation probability based on quantum effects and mutations
            quantum_factor = superposition * np.sqrt(mutation_rate)
            population_factor = 1 / np.sqrt(population_size)
            speciation_prob = quantum_factor * population_factor
            return min(speciation_prob, 1.0)
        except Exception as e:
            raise ValueError(f"Error calculating speciation probability: {str(e)}")
    
    def calculate_evolution_acceleration(self, quantum_leap_potential, fitness_gradient):
        """
        Calculate evolution acceleration factor.
        
        Args:
            quantum_leap_potential (float): Quantum leap potential
            fitness_gradient (float): Fitness gradient
            
        Returns:
            float: Evolution acceleration
        """
        try:
            # Acceleration due to quantum effects
            if fitness_gradient > 0:
                acceleration = quantum_leap_potential * fitness_gradient * 1e6
            else:
                acceleration = 0.0
            return acceleration
        except Exception as e:
            raise ValueError(f"Error calculating evolution acceleration: {str(e)}")
    
    def calculate_next_evolution_step(self, generation_count, evolution_acceleration):
        """
        Calculate the next significant evolution step.
        
        Args:
            generation_count (int): Current generation
            evolution_acceleration (float): Evolution acceleration
            
        Returns:
            int: Next evolution step generation
        """
        try:
            # Predict next major evolutionary step
            if evolution_acceleration > 1e-6:
                step_size = max(1, int(1 / evolution_acceleration))
            else:
                step_size = 100  # Default step size
            
            next_step = generation_count + step_size
            return next_step
        except Exception as e:
            raise ValueError(f"Error calculating next evolution step: {str(e)}")
    
    def calculate_all(self, population_size, quantum_state_amplitude, coherence_time,
                     barrier_height, particle_energy, selection_pressure,
                     mutation_rate, generation_count):
        """
        Calculate all quantum genetic parameters.
        
        Returns:
            dict: Dictionary containing all calculated values
        """
        try:
            # Perform all calculations
            genetic_superposition = self.calculate_genetic_superposition(
                quantum_state_amplitude, population_size
            )
            
            quantum_coherence = self.calculate_quantum_coherence(coherence_time)
            
            tunnel_probability = self.calculate_tunnel_probability(
                barrier_height, particle_energy
            )
            
            quantum_leap_potential = self.calculate_quantum_leap_potential(
                tunnel_probability, genetic_superposition
            )
            
            fitness_gradient = self.calculate_fitness_gradient(
                selection_pressure, quantum_coherence
            )
            
            speciation_probability = self.calculate_speciation_probability(
                mutation_rate, genetic_superposition, population_size
            )
            
            evolution_acceleration = self.calculate_evolution_acceleration(
                quantum_leap_potential, fitness_gradient
            )
            
            next_evolution_step = self.calculate_next_evolution_step(
                generation_count, evolution_acceleration
            )
            
            return {
                "geneticSuperposition": f"{genetic_superposition:.6f}",
                "quantumCoherence": f"{quantum_coherence:.3e}",
                "tunnelProbability": f"{tunnel_probability:.8f}",
                "quantumLeapPotential": f"{quantum_leap_potential:.6f}",
                "fitnessGradient": f"{fitness_gradient:.3e}",
                "speciationProbability": f"{speciation_probability:.4f}",
                "evolutionAcceleration": f"{evolution_acceleration:.8f}",
                "nextEvolutionStep": next_evolution_step
            }
            
        except Exception as e:
            raise ValueError(f"Error in quantum genetics calculations: {str(e)}")
