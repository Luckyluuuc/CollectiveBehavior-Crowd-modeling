import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Tuple

class DebugFuzzyModel:
    """Minimal fuzzy logic model with extensive debugging"""
    
    def __init__(self):
        self.pd_sim = None
        self.pv_sim = None
        print("Initializing DebugFuzzyModel...")
        self.define_fuzzy_model()

    def define_fuzzy_model(self) -> None:
        try:
            # Single input variable - utilisons un pas plus fin pour plus de précision
            openness = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Openness')
            print("Created Openness antecedent")
            
            # Single output variable
            distance = ctrl.Consequent(np.arange(0, 3.01, 0.01), 'Distance')
            print("Created Distance consequent")
            
            # Fonctions d'appartenance corrigées
            # Pour Openness :
            # - 'low' va de 0 à 0.6 avec chevauchement
            # - 'high' va de 0.4 à 1 avec chevauchement
            openness['low'] = fuzz.trapmf(openness.universe, [0, 0, 0.3, 0.6])
            openness['high'] = fuzz.trapmf(openness.universe, [0.4, 0.7, 1, 1])
            print("Defined openness membership functions")
            
            # Pour Distance :
            # - 'low' va de 0 à 2 avec chevauchement
            # - 'high' va de 1 à 3 avec chevauchement
            distance['low'] = fuzz.trapmf(distance.universe, [0, 0, 1, 2])
            distance['high'] = fuzz.trapmf(distance.universe, [1, 2, 3, 3])
            print("Defined distance membership functions")
            
            # Créons deux règles pour assurer une meilleure couverture
            rule1 = ctrl.Rule(openness['low'], distance['high'])
            rule2 = ctrl.Rule(openness['high'], distance['low'])
            print("Created rules")
            
            # Create control system with both rules
            control_system = ctrl.ControlSystem([rule1, rule2])
            print("Created control system")
            
            # Initialize simulation
            self.simulation = ctrl.ControlSystemSimulation(control_system)
            print("Initialized simulation")
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise

    def compute_distance(self, o: float) -> float:
        """Compute only distance based on openness"""
        try:
            # Assurons-nous que l'entrée est dans les limites
            o = max(0, min(1, o))  # Limite entre 0 et 1
            self.simulation.input['Openness'] = o
            self.simulation.compute()
            result = self.simulation.output['Distance']
            return result
            
        except Exception as e:
            print(f"Error in compute_distance: {str(e)}")
            raise RuntimeError(f"Error computing distance: {str(e)}")

# Test function améliorée
def test_model():
    print("Creating model...")
    model = DebugFuzzyModel()
    
    # Test systématique
    test_values = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    print("\nTesting specific values:")
    for o in test_values:
        try:
            result = model.compute_distance(o)
            print(f"Openness = {o:.1f} → Distance = {result:.2f}")
        except Exception as e:
            print(f"Test failed for o={o}: {str(e)}")
    
    # Test aléatoire
    print("\nTesting random values:")
    count = 0
    n_tests = 1000
    for i in range(n_tests):
        o = np.random.uniform(0, 1)
        try:
            result = model.compute_distance(o)
            count += 1
        except Exception as e:
            print(f"Test failed for o={o}: {str(e)}")
            
    print(f"Random tests completed: {count} successful, {n_tests - count} failed")

if __name__ == "__main__":
    test_model()

#________Brouillon__________


# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
# from typing import Optional, Tuple
# from dataclasses import dataclass

# @dataclass
# class FuzzyMembershipPoints:
#     """Configuration points for trapezoidal membership functions"""
#     # Tuples represent (a, b, c, d) points for trapezoidal membership functions

#     low: Tuple[float, float, float, float] = (0, 0, 0.25, 0.5)
#     medium: Tuple[float, float, float, float] = (0.25, 0.5, 0.75, 1.0)
#     high: Tuple[float, float, float, float] = (0.5, 0.75, 1, 1)

#     # just two membership function for output
#     low_out : Tuple[float, float, float, float] = (0, 0, 1, 2)
#     medium_out : Tuple[float, float, float, float] = (1, 2, 3, 3)

# class PersonalityFuzzyModel:
#     """
#     A fuzzy logic model that maps Big Five personality traits to behavioral parameters.
    
#     This model uses fuzzy logic to determine two behavioral parameters:
#     - P_d (Personal Distance): Represents preferred interpersonal distance
#     - P_v (Personal Velocity): Represents preferred movement speed
    
#     Attributes:
#         pd_sim: Control system simulation for Personal Distance
#         pv_sim: Control system simulation for Personal Velocity
#     """
    
#     def __init__(self):
#         """Initialize the fuzzy logic model with default membership functions."""
#         self.pd_sim: Optional[ctrl.ControlSystemSimulation] = None
#         self.pv_sim: Optional[ctrl.ControlSystemSimulation] = None
#         self.define_fuzzy_model()

#     def validate_input_range(self, value: float, name: str) -> None:
#         """
#         Validate that an input value is within the expected range [0, 1].
        
#         Args:
#             value: The input value to validate
#             name: Name of the parameter for error message
            
#         Raises:
#             ValueError: If the value is outside the valid range
#         """
#         if not 0 <= value <= 1:
#             raise ValueError(f"{name} must be between 0 and 1, got {value}")

#     def define_fuzzy_model(self) -> None:
#         """
#         Define the fuzzy logic model with input/output variables, membership functions, and rules.
        
#         This function creates:
#         1. Input variables (Big Five traits)
#         2. Output variables (Personal Distance and Velocity)
#         3. Membership functions for all variables
#         4. Fuzzy rules
#         5. Control systems for simulation
        
#         The model is stored in self.pd_sim and self.pv_sim for later use.
#         """
#         try:
#             # Define input ranges for personality traits (0 to 1)
#             input_range = np.arange(0, 1.1, 0.1)
            
#             # Step 1: Define input variables (antecedents)
#             personality_traits = {
#                 'psi_O': ctrl.Antecedent(input_range, 'Openness'),
#                 'psi_E': ctrl.Antecedent(input_range, 'Extraversion'),
#                 'psi_A': ctrl.Antecedent(input_range, 'Agreeableness'),
#                 'psi_C': ctrl.Antecedent(input_range, 'Conscientiousness'),
#                 'psi_N': ctrl.Antecedent(input_range, 'Neuroticism')
#             }
            
#             # Step 2: Define output variables (consequents)
#             output_range = np.arange(0, 3.1, 0.1)
#             P_d = ctrl.Consequent(output_range, 'Personal_Distance')
#             P_v = ctrl.Consequent(output_range, 'Personal_Velocity')
            
#             # Step 3: Define membership functions
#             trait_memberships = FuzzyMembershipPoints()
#             output_memberships = FuzzyMembershipPoints(
#                 low=(0, 0, 1, 1.5),
#                 medium=(1, 1.5, 2, 2.5),
#                 high=(2, 2.5, 3, 3)
#             )
            
#             # Apply membership functions to personality traits
#             for trait in personality_traits.values():
#                 trait['low'] = fuzz.trapmf(trait.universe, trait_memberships.low)
#                 trait['high'] = fuzz.trapmf(trait.universe, trait_memberships.high)
            
#             # Apply membership functions to output variables
#             for output in [P_d, P_v]:
#                 output['low'] = fuzz.trapmf(output.universe, output_memberships.low)
#                 output['medium'] = fuzz.trapmf(output.universe, output_memberships.medium)
#                 output['high'] = fuzz.trapmf(output.universe, output_memberships.high)
            
#             # Step 4: Define rules
#             pd_rules = [
#                 # Low Openness leads to high Personal Distance
#                 ctrl.Rule(
#                     personality_traits['psi_O']['low'], P_d['high']
#                 ),
#                 # High Agreeableness leads to low Personal Distance
#                 ctrl.Rule(
#                     personality_traits['psi_A']['high'], self.P_d['low']

#                 )
#             ]
            
#             pv_rules = [
#                 # Low Conscientiousness leads to high Personal Velocity
#                 ctrl.Rule(
#                     self.personality_traits['psi_C']['low'], self.P_v['high']
#                 ),
#                 # High Neuroticism and Extraversion lead to medium Personal Velocity
#                 ctrl.Rule(
#                     self.personality_traits['psi_N']['high'] & self.personality_traits['psi_E']['high'], 
#                     self.P_v['medium']
#                 )
#             ]
            
#             # Step 5: Create control systems
#             pd_ctrl = ctrl.ControlSystem(pd_rules)
#             pv_ctrl = ctrl.ControlSystem(pv_rules)
            
#             # Initialize simulations
#             self.pd_sim = ctrl.ControlSystemSimulation(pd_ctrl)
#             self.pv_sim = ctrl.ControlSystemSimulation(pv_ctrl)
            
#         except Exception as e:
#             raise RuntimeError(f"Failed to initialize fuzzy logic model: {str(e)}")
    
#     def compute_parameters(self, o: float, c: float, e: float, a: float, n: float) -> Tuple[float, float]:
#         """
#         Compute Personal Distance and Velocity based on Big Five personality traits.
        
#         Args:
#             o: Openness score [0-1]
#             e: Extraversion score [0-1]
#             a: Agreeableness score [0-1]
#             c: Conscientiousness score [0-1]
#             n: Neuroticism score [0-1]
            
#         Returns:
#             Tuple[float, float]: Personal Distance and Personal Velocity values
            
#         Raises:
#             ValueError: If any input is outside the valid range [0-1]
#         """
#         # Validate all inputs
#         for value, name in zip([o, c, e, a, n], ['Openness', 'Conscientiousness','Extraversion', 'Agreeableness', 'Neuroticism']):
#             self.validate_input_range(value, name)
        
#         try:
#             # Set inputs for Personal Distance simulation
#             self.pd_sim.input['Openness'] = o
#             self.pd_sim.input['Extraversion'] = e
#             self.pd_sim.input['Agreeableness'] = a
            
#             # Set inputs for Personal Velocity simulation
#             self.pv_sim.input['Conscientiousness'] = c
#             self.pv_sim.input['Neuroticism'] = n
#             self.pv_sim.input['Extraversion'] = e
            
#             # Compute outputs
#             self.pd_sim.compute()
#             self.pv_sim.compute()
            
#             return (self.pd_sim.output['Personal_Distance'],
#                     self.pv_sim.output['Personal_Velocity'])
                    
#         except Exception as e:
#             raise RuntimeError(f"Error computing parameters: {str(e)}")