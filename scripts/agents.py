from mesa import Agent
from mesa.space import MultiGrid
from obstacle import Obstacle
from math import sqrt, exp


# for the fuzzy logic
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def euclidean_dist(pt1, pt2):
    """ Return euclidean distance between two points """
    return sqrt((pt1[0]- pt2[0])**2 + (pt1[1] - pt2[1])**2)


def pref_OEC(value):
    """
    To compute Pd and Pv for O E and C traits
    """
    seuil = 0.5
    if value < seuil:
        return 1 - value
    return 0

def pref_AN(value):
    """
    To compute Pd and Pv for A and N traits
    """
    seuil = 0.5
    facteur = 2
    if value >= seuil:
        return facteur * value - 1
    return 0

def prefV_E(value):
    """
    To compute Pv for E trait
    """
    seuil = 0.5
    if value >= seuil:
        return value
    return 0


class PedestrianAgent(Agent):
    def __init__(self, unique_id, model, personality, initial_pd=1, initial_pv=1, vel0=2):
        super().__init__(unique_id, model)
        self.personality = personality
        self.initial_pd = initial_pd
        self.initial_pv = initial_pv

        self.vel0 = vel0  # should belong to {1, 2, 3}
        self.fuzzy_preferences_vel_dist()

    def preferences_vel_dist(self):
        """Compute preference velocity Pv and preference distance Pd"""
        O, C, E, A, N = (self.personality['O'], self.personality['C'],
                         self.personality['E'], self.personality['A'],
                         self.personality['N'])
        
        # Calcul de Pd
        self.pd = pref_OEC(O) + pref_OEC(E) + pref_AN(A)
        
        # Calcul de Pv
        self.pv = pref_OEC(C) + prefV_E(E) + pref_AN(N)



    def fuzzy_preferences_vel_dist(self):
        """
        Calcule les propensions P_d (désobéissance) et P_v (marche rapide) à partir des scores OCEAN.

        Args:
            ocean_scores (dict): Dictionnaire contenant les scores OCEAN sous la forme :
                {
                    'O': float,  # Ouverture (0 à 1)
                    'C': float,  # Conscience (0 à 1)
                    'E': float,  # Extraversion (0 à 1)
                    'A': float,  # Agréabilité (0 à 1)
                    'N': float   # Névrosisme (0 à 1)
                }

        Returns:
            tuple: (P_d, P_v), où :
                - P_d est la propension à désobéir (float)
                - P_v est la propension à marcher vite (float)
        """
        # Étape 1 : Définir les variables d'entrée floues (O, E, A, C, N)
        psi_O = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'psi_O')  # Ouverture
        psi_E = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'psi_E')  # Extraversion
        psi_A = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'psi_A')  # Agréabilité
        psi_C = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'psi_C')  # Conscience
        psi_N = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'psi_N')  # Névrosisme

        # Étape 2 : Définir les variables de sortie floues (P_d et P_v)
        P_d = ctrl.Consequent(np.arange(0, 3.1, 0.1), 'P_d')  # Propension à désobéir
        P_v = ctrl.Consequent(np.arange(0, 3.1, 0.1), 'P_v')  # Propension à marcher vite

        # Étape 3 : Définir les ensembles flous pour chaque variable
        for var in [psi_O, psi_E, psi_A, psi_C, psi_N]:
            var['low'] = fuzz.trapmf(var.universe, [0, 0, 0.25, 0.5])  # Faible
            var['high'] = fuzz.trapmf(var.universe, [0.5, 0.75, 1, 1])  # Élevé

        P_d['low'] = fuzz.trapmf(P_d.universe, [0, 0, 1, 1.5])
        P_d['medium'] = fuzz.trapmf(P_d.universe, [1, 1.5, 2, 2.5])
        P_d['high'] = fuzz.trapmf(P_d.universe, [2, 2.5, 3, 3])

        P_v['low'] = fuzz.trapmf(P_v.universe, [0, 0, 1, 1.5])
        P_v['medium'] = fuzz.trapmf(P_v.universe, [1, 1.5, 2, 2.5])
        P_v['high'] = fuzz.trapmf(P_v.universe, [2, 2.5, 3, 3])

        # Étape 4 : Définir les règles floues
        rule1_pd = ctrl.Rule(psi_O['low'] & psi_E['low'], P_d['high'])  # Faible O et E -> P_d élevé
        rule2_pd = ctrl.Rule(psi_A['high'], P_d['low'])  # A élevé -> P_d faible

        rule1_pv = ctrl.Rule(psi_C['low'], P_v['high'])  # C faible -> P_v élevé
        rule2_pv = ctrl.Rule(psi_N['high'] & psi_E['high'], P_v['medium'])  # N et E élevés -> P_v moyen

        # Étape 5 : Créer les systèmes de contrôle flous
        pd_ctrl = ctrl.ControlSystem([rule1_pd, rule2_pd])
        pv_ctrl = ctrl.ControlSystem([rule1_pv, rule2_pv])

        pd_sim = ctrl.ControlSystemSimulation(pd_ctrl)
        pv_sim = ctrl.ControlSystemSimulation(pv_ctrl)

        # Étape 6 : Appliquer les scores OCEAN
        O, C, E, A, N = (self.personality['O'], self.personality['C'],
                         self.personality['E'], self.personality['A'],
                         self.personality['N'])
        
        pd_sim.input['psi_O'] = O
        pd_sim.input['psi_E'] = E
        pd_sim.input['psi_A'] = A

        pv_sim.input['psi_C'] = C
        pv_sim.input['psi_E'] = E
        pv_sim.input['psi_N'] = N

        # Calculer les sorties
        pd_sim.compute()
        pv_sim.compute()

        if pd_sim.output is None or P_d not in pd_sim.output:
            self.pd = 0.5
            print("pd is None")
        else:
            self.pd = pd_sim.output['P_d']


        if pv_sim.output is None or P_v not in pv_sim.output:
            self.pv = 0.5
            print("pv is None")
        else:
            self.pv = pv_sim.output['P_v']



    def get_cells_around(self):
        """
        Return the list of cell we consider as potential new destination for the next step.

        We consider (in first approximation) that the scoring function is enought to
        sort the neighbors and keep only the relevant ones.

        TO IMPROVE : prendre en compte la distance à l'arrivée (= remove ceux qui nous font reculer)
        On suppose pour l'instant que la fonction de scoring est suffisante pour cela.
        """
        grid = self.model.grid
        loc = self.pos
        speed = self.vel0

        directions = [(0, 1), (1,1), (1, 0), (-1,1), (-1, 0), (-1, -1), (0,-1), (1,-1)]
        valid_neighbors = []

        # For each direction, we go throught every cells our agent can reach according to its current velocity
        # If one cell on the way is not available, we consider our agent can not go further in this way, with respect
        # to the "one step" representation we assume

        for dir in directions:
            for i in range(1, speed+1):
                neighbor = (loc[0] + i*dir[0], loc[1] + i*dir[1])

                # Insures the neighbor is part of the grid
                if grid.out_of_bounds(neighbor):
                    break
                
                # Insures the neighbor is not an Obstacle or an Agent
                if not grid.is_cell_empty(neighbor):
                    break
                
                valid_neighbors.append(neighbor)

        valid_neighbors.append(loc)

        return valid_neighbors


    def get_density(self, cell):
        """
        Luc kind of things
        """

        density = 0
        ra = 2 # parameter to tune

        neighbors = self.model.grid.get_neighborhood(
        pos=cell,
        moore=True,      
        include_center=False,
        radius=1 #change the value here        
        ) 

        for neighbor_pos in neighbors:
            neigh_contents = self.model.grid.get_cell_list_contents(neighbor_pos)
            for agent in neigh_contents:
                if isinstance(agent, PedestrianAgent):
                    dist = euclidean_dist(cell, agent.pos)
                    density += exp(-dist)*100   # 1000 is a parameter, we'll need to tune it

        return  density
    
    def update_emotions(self, cell, contagious_sources=[]):
        """Algorithm 2, p7 : Emotion Contagion Algorithm"""
        delta_pd = 0
        delta_pv = 0

        neighbors = self.model.grid.get_neighborhood(
        pos=cell,
        moore=True,      
        include_center=False,
        radius=5        
        ) # J'ai recalculé les voisins ici, tout comme ça a été calculé dans get_density, mais est-ce que c'est pas un peu sale ?

        # Contagion from neighbors
        for neighbor in neighbors:
            if isinstance(neighbor, PedestrianAgent):
                dist = euclidean_dist(self.pos, neighbor.pos)
                delta_pd += exp((neighbor.pd - self.pd) / dist)
                delta_pv += exp((neighbor.pv - self.pv) / dist)

        # Contagion from other sources
        for source in contagious_sources:
            dist = euclidean_dist(self.pos, source.pos)
            delta_pd += exp(self.pd / dist)
            delta_pv += exp(self.pv / dist)

        # selective perception
        exits = self.model.exit # now exit is a list to handle multiple exits
        dist_to_exits = [euclidean_dist(self.pos, exit) for exit in exits]
        dist_to_goal = min(dist_to_exits)
        vel = self.vel0
        omega_d = exp(-0.05 * dist_to_goal)
        omega_v = exp(-2.0 * vel)

        # dampening factor
        zeta_d = self.initial_pd * 0.1
        zeta_v = self.initial_pv * 0.1

        # update of preferences
        self.pd += delta_pd * omega_d + zeta_d
        self.pv += delta_pv * omega_v + zeta_v

        # Normalisation
        total = self.pd + self.pv
        self.pd /= total
        self.pv /= total

    def score(self, next_cell):
        """
        Compute the satisfaction score considering the agent moving on the next_cell.
        """
        exits = self.model.exit # now exit is a list to handle multiple exits
        dist_to_exits = [euclidean_dist(next_cell, exit) for exit in exits]
        dist_to_exit = min(dist_to_exits)



        # We compute the density of the next cell
        density = self.get_density(next_cell)
        #return (self.pd * dist_to_exit) + (self.pv * density)
        return dist_to_exit / (self.vel0 * exp(- density * (self.pv+1 )/(self.pd+1)))
    
    
    def step(self):

        if self.pos in self.model.exit:
            self.model.grid.remove_agent(self)  # L'agent "sort" de la grille
            self.model.schedule.remove(self)
        else:
            min_score = float('inf')
            best_cell = None
            for cell in self.get_cells_around():
                score = self.score(cell)
                if score < min_score:
                    min_score = score
                    best_cell = cell
            
            previous_cell = self.pos
            self.model.grid.move_agent(self, best_cell)

            # Add a trajectory to the grid
            # first identify the direction
            dir_x = int((best_cell[0] - previous_cell[0]) / max(abs(best_cell[0] - previous_cell[0]), 1)) # max to avoid division by 0
            dir_y = int((best_cell[1] - previous_cell[1]) / max(abs(best_cell[1] - previous_cell[1]), 1))

            # Add the trajectory to the grid
            while previous_cell != best_cell:
                self.model.add_trajectory(previous_cell, self.unique_id)
                previous_cell = (previous_cell[0] + dir_x, previous_cell[1] + dir_y)

            for agent in self.model.schedule.agents:
                if isinstance(agent, PedestrianAgent):
                    contagious_sources = [fire for fire in self.model.fire_sources if euclidean_dist(agent.pos, fire.pos) < 5]
                    # Emotion contagion
                    agent.update_emotions(agent.pos, contagious_sources) 

    


