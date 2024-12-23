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
                p_d = 1.5
            if p_v is None:
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