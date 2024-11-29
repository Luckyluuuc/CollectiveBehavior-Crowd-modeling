from mesa import Agent
from mesa.space import MultiGrid
from obstacle import Obstacle
from math import sqrt, exp

def get_cells_around(grid:MultiGrid, loc):
    """
    Return the list of cell we consider as potential new destination for the next step.

    We consider (in first approximation) that the scoring function is enought to
    sort the neighbors and keep only the relevant ones.

    TO IMPROVE : prendre en compte la distance à l'arrivée (= remove ceux qui nous font reculer)
    On suppose pour l'instant que la fonction de scoring est suffisante pour cela.
    """

    # TO IMPROVE : Take diagonals into consideration
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    valid_neighbors = []

    for dir in directions:
        neighbor = (loc[0] + dir[0], loc[1] + dir[1])

        # Insures the neighbor is part of the grid
        if grid.out_of_bounds(neighbor):
            continue
        
        # Insures the neighbor is not an Obstacle or an Agent
        if not grid.is_cell_empty(neighbor):
            continue
        
        valid_neighbors.append(neighbor)

    valid_neighbors.append(loc)
    
    return valid_neighbors


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
    def __init__(self, unique_id, model, personality, initial_pd=1, initial_pv=1):
        super().__init__(unique_id, model)
        self.personality = personality
        self.initial_pd = initial_pd
        self.initial_pv = initial_pv

        self.vel0 = 1
        self.preferences_vel_dist()

    def preferences_vel_dist(self):
        """Compute preference velocity Pv and preference distance Pd"""
        O, C, E, A, N = (self.personality['O'], self.personality['C'],
                         self.personality['E'], self.personality['A'],
                         self.personality['N'])
        
        # Calcul de Pd
        self.pd = pref_OEC(O) + pref_OEC(E) + pref_AN(A)
        
        # Calcul de Pv
        self.pv = pref_OEC(C) + prefV_E(E) + pref_AN(N)

    def get_density(self, cell):

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
                    density += exp(-dist/(100*ra))   # 1000 is a parameter, we'll need to tune it

        return density
    
    def update_emotions(self, cell, contagious_sources=[]):
        """Algorithm 2, p7 : Emotion Contagion Algorithm"""
        delta_pd = 0
        delta_pv = 0

        neighbors = self.model.grid.get_neighborhood(
        pos=cell,
        moore=True,      
        include_center=False,
        radius=1        
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
        dist_to_goal = euclidean_dist(self.pos, self.model.exit)
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
        exit = self.model.exit
        # We compute the distance to the exit
        dist_to_exit = euclidean_dist(next_cell, exit)
        # We compute the density of the next cell
        density = 1
        #density = self.get_density(next_cell)
        #return (self.pd * dist_to_exit) + (self.pv * density)
        return dist_to_exit / (self.vel0 * exp(- density * (self.pv+1 )/(self.pd+1)))
    
    
    def step(self):

        if self.pos == self.model.exit:
            self.model.grid.remove_agent(self)  # L'agent "sort" de la grille
            self.model.schedule.remove(self)
        else:
            min_score = float('inf')
            best_cell = None
            for cell in get_cells_around(self.model.grid, self.pos):
                score = self.score(cell)
                if score < min_score:
                    min_score = score
                    best_cell = cell
            
            self.model.grid.move_agent(self, best_cell)
            for agent in self.model.schedule.agents:
                if isinstance(agent, PedestrianAgent):
                    contagious_sources = [fire for fire in self.model.fire_sources if euclidean_dist(agent.pos, fire.pos) < 5]
                    # Emotion contagion
                    agent.update_emotions(agent.pos, contagious_sources) 

    


