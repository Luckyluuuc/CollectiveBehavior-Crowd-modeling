import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Tuple

class FuzzyModel:
    """
    Enhanced fuzzy logic model for personality-based distance calculation
    with binary (high/low) output membership functions
    """
    def __init__(self):
        self.simulation = None
        print("Initializing FuzzyModel...")
        self.define_fuzzy_model()

    def define_fuzzy_model(self) -> None:
        try:
            # Define universes for each variable with fine granularity
            openness = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Openness')
            conscientiousness = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Conscientiousness')
            extraversion = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Extraversion')
            agreeableness = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Agreeableness')
            neuroticism = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Neuroticism')
            
            # Define output variables (0-3 range maintained for consistency)
            P_d = ctrl.Consequent(np.arange(0, 3.01, 0.01), 'P_d')
            P_v = ctrl.Consequent(np.arange(0, 3.01, 0.01), 'P_v')

            # Membership functions for input variables
            openness['low'] = fuzz.trapmf(openness.universe, [0, 0, 0.2, 0.4])
            openness['medium'] = fuzz.trapmf(openness.universe, [0.3, 0.4, 0.6, 0.7])
            openness['high'] = fuzz.trapmf(openness.universe, [0.6, 0.8, 1, 1])
            
            conscientiousness['low'] = fuzz.trapmf(conscientiousness.universe, [0, 0, 0.2, 0.4])
            conscientiousness['medium'] = fuzz.trapmf(conscientiousness.universe, [0.3, 0.4, 0.6, 0.7])
            conscientiousness['high'] = fuzz.trapmf(conscientiousness.universe, [0.6, 0.8, 1, 1])
            
            extraversion['low'] = fuzz.trapmf(extraversion.universe, [0, 0, 0.2, 0.4])
            extraversion['medium'] = fuzz.trapmf(extraversion.universe, [0.3, 0.4, 0.6, 0.7])
            extraversion['high'] = fuzz.trapmf(extraversion.universe, [0.6, 0.8, 1, 1])
            
            agreeableness['low'] = fuzz.trapmf(agreeableness.universe, [0, 0, 0.2, 0.4])
            agreeableness['medium'] = fuzz.trapmf(agreeableness.universe, [0.3, 0.4, 0.6, 0.7])
            agreeableness['high'] = fuzz.trapmf(agreeableness.universe, [0.6, 0.8, 1, 1])
            
            neuroticism['low'] = fuzz.trapmf(neuroticism.universe, [0, 0, 0.2, 0.4])
            neuroticism['medium'] = fuzz.trapmf(neuroticism.universe, [0.3, 0.4, 0.6, 0.7])
            neuroticism['high'] = fuzz.trapmf(neuroticism.universe, [0.6, 0.8, 1, 1])

            # P_d (Distance) - Only low and high
            P_d['low'] = fuzz.trapmf(P_d.universe, [0, 0, 1, 2])
            P_d['high'] = fuzz.trapmf(P_d.universe, [1, 2, 3, 3])

            # P_v (Value) - Only low and high
            P_v['low'] = fuzz.trapmf(P_v.universe, [0, 0, 1, 2])
            P_v['high'] = fuzz.trapmf(P_v.universe, [1, 2, 3, 3 ])

            rules = [

                # #--------The rule we agreed on---------
                # # ------Rules for P_v--------
                # # If high(O) and high(E) and medium(A) then high(P_v)
                # ctrl.Rule(openness['high'] & extraversion['high'] & agreeableness['medium'], P_v['high']),
                # # if high(N) then high(P_v)
                # ctrl.Rule(neuroticism['high'], P_v['high']),

                # # if high(C) and medium(A) then low(P_v)
                # ctrl.Rule(conscientiousness['low'] & agreeableness['medium'], P_v['low']),
                # #if high(A) then low(P_v)
                # ctrl.Rule(agreeableness['low'], P_v['low']),

                # # ------Rules for P_d--------
                # #if high(C) and high(A) then high(P_d)
                # ctrl.Rule(conscientiousness['high'] & agreeableness['high'], P_d['high']),
                # #if medium(O) and high(E) then low(P_d)
                # ctrl.Rule(openness['medium'] & extraversion['high'], P_d['low']),
                # #if high(0) then low(P_d)
                # ctrl.Rule(openness['high'], P_d['low']),


                # #________ the rule corrected by claude for better coverage________
                # # Original P_v rules
                # ctrl.Rule(openness['high'] & extraversion['high'] & agreeableness['medium'], P_v['high']),
                # ctrl.Rule(neuroticism['high'], P_v['high']),
                # ctrl.Rule(conscientiousness['low'] & agreeableness['medium'], P_v['low']),
                # ctrl.Rule(agreeableness['low'], P_v['low']),
                
                # # Complementary P_v rules pour assurer la couverture
                # ctrl.Rule(openness['low'] & extraversion['low'], P_v['low']),
                # ctrl.Rule(neuroticism['low'], P_v['low']),
                # ctrl.Rule(conscientiousness['medium'] & agreeableness['medium'], P_v['high']),
                
                # # Original P_d rules
                # ctrl.Rule(conscientiousness['high'] & agreeableness['high'], P_d['high']),
                # ctrl.Rule(openness['medium'] & extraversion['high'], P_d['low']),
                # ctrl.Rule(openness['high'], P_d['low']),
                
                # # Complementary P_d rules pour assurer la couverture
                # ctrl.Rule(conscientiousness['low'] & agreeableness['low'], P_d['low']),
                # ctrl.Rule(extraversion['low'] & openness['low'], P_d['high']),
                
                # # Rules for medium cases to ensure smooth transitions
                # ctrl.Rule(conscientiousness['medium'] & agreeableness['medium'], P_d['high']),
                # ctrl.Rule(openness['medium'] & extraversion['medium'], P_d['low']),
                
                # # Default rules pour éviter les cas non définis
                # ctrl.Rule(conscientiousness['medium'] & ~agreeableness['high'] & ~agreeableness['low'], P_d['low']),
                # ctrl.Rule(openness['medium'] & ~extraversion['high'] & ~extraversion['low'], P_v['low'])


                # second version of the improved rules
                # -------- Original P_v rules --------
                ctrl.Rule(openness['high'] & extraversion['high'] & agreeableness['medium'], P_v['high']),
                ctrl.Rule(neuroticism['high'], P_v['high']),
                ctrl.Rule(conscientiousness['low'] & agreeableness['medium'], P_v['low']),
                ctrl.Rule(agreeableness['low'], P_v['low']),

                # -------- Original P_d rules --------
                ctrl.Rule(conscientiousness['high'] & agreeableness['high'], P_d['high']),
                ctrl.Rule(openness['medium'] & extraversion['high'], P_d['low']),
                ctrl.Rule(openness['high'], P_d['low']),

                # -------- Additional coverage for P_v --------
                # Extreme cases
                ctrl.Rule(openness['low'] & extraversion['low'], P_v['low']),
                ctrl.Rule(openness['low'] & extraversion['medium'], P_v['low']),
                ctrl.Rule(openness['medium'] & extraversion['low'], P_v['low']),
                
                # Medium cases
                ctrl.Rule(openness['medium'] & extraversion['medium'] & agreeableness['medium'], P_v['high']),
                ctrl.Rule(openness['medium'] & extraversion['medium'] & agreeableness['low'], P_v['low']),
                
                # High neuroticism combinations
                ctrl.Rule(neuroticism['high'] & agreeableness['high'], P_v['high']),
                ctrl.Rule(neuroticism['high'] & agreeableness['low'], P_v['high']),
                
                # Low neuroticism combinations
                ctrl.Rule(neuroticism['low'] & agreeableness['high'], P_v['low']),
                ctrl.Rule(neuroticism['low'] & agreeableness['low'], P_v['low']),
                
                # Medium neuroticism default
                ctrl.Rule(neuroticism['medium'], P_v['low']),

                # -------- Additional coverage for P_d --------
                # Extreme cases
                ctrl.Rule(conscientiousness['low'] & agreeableness['low'], P_d['low']),
                ctrl.Rule(conscientiousness['low'] & agreeableness['medium'], P_d['low']),
                ctrl.Rule(conscientiousness['medium'] & agreeableness['low'], P_d['low']),
                
                # Medium cases
                ctrl.Rule(conscientiousness['medium'] & agreeableness['medium'], P_d['high']),
                
                # Openness combinations
                ctrl.Rule(openness['low'], P_d['high']),
                ctrl.Rule(openness['medium'], P_d['low']),
                
                # Default rules for remaining cases
                ctrl.Rule(extraversion['medium'] & ~openness['high'] & ~openness['low'], P_d['high']),
                ctrl.Rule(agreeableness['medium'] & ~conscientiousness['high'] & ~conscientiousness['low'], P_d['low']),
                
                # Fallback rules for complete coverage
                ctrl.Rule(~openness['high'] & ~openness['medium'] & ~openness['low'], P_v['low']),
                ctrl.Rule(~conscientiousness['high'] & ~conscientiousness['medium'] & ~conscientiousness['low'], P_d['low'])
            ]

            # Create and initialize control system
            control_system = ctrl.ControlSystem(rules)
            self.simulation = ctrl.ControlSystemSimulation(control_system)
            print("Fuzzy model initialization complete")

        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise

    def compute_parameters(self, o: float, c: float, e: float, a: float, n: float) -> Tuple[float, float]:
        """
        Compute both distance and value metrics based on all personality factors
        
        Args:
            o (float): Openness score (0-1)
            c (float): Conscientiousness score (0-1)
            e (float): Extraversion score (0-1)
            a (float): Agreeableness score (0-1)
            n (float): Neuroticism score (0-1)
            
        Returns:
            Tuple[float, float]: (distance metric, value metric)
        """
        try:
            # Ensure inputs are within bounds and correct if not
            inputs = {
                'Openness': max(0, min(1, o)),
                'Conscientiousness': max(0, min(1, c)),
                'Extraversion': max(0, min(1, e)),
                'Agreeableness': max(0, min(1, a)),
                'Neuroticism': max(0, min(1, n))
            }
            
            # Set inputs and compute
            for var_name, value in inputs.items():
                self.simulation.input[var_name] = value
                
            self.simulation.compute()
            
            # Get outputs
            p_d = self.simulation.output['P_d']
            p_v = self.simulation.output['P_v']

            # handeling output with none value
            if p_d is None:
                print("P_d is None, handeling it")
                p_d = 1.5
            if p_v is None:
                print("P_v is None, handeling it")
                p_v = 1.5
            
            return p_d, p_v

        except Exception as e:
            print(f"Error in compute_personality_metrics: {str(e)}")
            raise RuntimeError(f"Error computing metrics: {str(e)}")




def test_model():
    """
    Comprehensive test suite for the EnhancedFuzzyModel
    Tests both systematic and random inputs for all personality factors
    """
    print("Creating enhanced fuzzy model...")
    try:
        model = FuzzyModel()
    except Exception as e:
        print(f"Failed to create model: {str(e)}")
        return


    # Random testing
    print("\nPerforming random tests:")
    successful_tests = 0
    failed_tests = 0
    n_tests = 1000

    for i in range(n_tests):
        # Generate random personality scores
        personality_scores = {
            'O': np.random.uniform(0, 1),
            'C': np.random.uniform(0, 1),
            'E': np.random.uniform(0, 1),
            'A': np.random.uniform(0, 1),
            'N': np.random.uniform(0, 1)
        }
        
        try:
            p_d, p_v = model.compute_personality_metrics(
                personality_scores['O'],
                personality_scores['C'],
                personality_scores['E'],
                personality_scores['A'],
                personality_scores['N']
            )
            successful_tests += 1
            
            # Print every 100th result for monitoring
            if i % 100 == 0:
                print(f"\nTest {i}:")
                print(f"Inputs: O={personality_scores['O']:.2f}, C={personality_scores['C']:.2f}, "
                      f"E={personality_scores['E']:.2f}, A={personality_scores['A']:.2f}, "
                      f"N={personality_scores['N']:.2f}")
                print(f"Outputs: P_d={p_d:.2f}, P_v={p_v:.2f}")
                
        except Exception as e:
            failed_tests += 1
            print(f"Test {i} failed: {str(e)}")
            print(f"Failed inputs: {personality_scores}")

    # Print test summary
    print("\nTest Summary:")
    print(f"Total tests: {n_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(successful_tests/n_tests)*100:.1f}%")

    # Verify output ranges
    if successful_tests > 0:
        print("\nVerifying output ranges...")
        test_extremes = [
            (0, 0, 0, 0, 0),  # All minimum
            (1, 1, 1, 1, 1),  # All maximum
            (0.5, 0.5, 0.5, 0.5, 0.5)  # All middle
        ]
        
        for inputs in test_extremes:
            try:
                p_d, p_v = model.compute_personality_metrics(*inputs)
                print(f"\nInputs: {inputs}")
                print(f"P_d={p_d:.2f}, P_v={p_v:.2f}")
                
                # Verify outputs are in expected ranges
                assert 0 <= p_d <= 3, f"P_d out of range: {p_d}"
                assert 0 <= p_v <= 3, f"P_v out of range: {p_v}"
                
            except Exception as e:
                print(f"Extreme test failed: {str(e)}")

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