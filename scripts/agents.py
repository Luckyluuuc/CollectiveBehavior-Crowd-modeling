from mesa import Agent
from mesa.space import MultiGrid
from obstacle import Obstacle
from math import sqrt, exp


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


    def get_density(self, cell, alpha = 0.75, ra = 4):
        """
        Compute the density of pedestrians for a given cell.
        We consider that each neighboot in the neighboorood has it's own contribution to the density.
        But the further the neighboor is, the less it contributes to the density.

        To model this we use the following formula :
        contribution = exp(-0.5 * dist**4) 


        intput :
        - cell : tuple of int, the position of the cell
        - alpha : float, parameter to tune for increasing or deacreasing the importance of the density
        - ra : int, the radius of the neighborhood we consider to compute the density

        output :
        - density : float, the density of pedestrians in the neighborhood of the cell
        """

        density_score = 0

        neighbors = self.model.grid.get_neighborhood(
        pos=cell,
        moore=True,      
        include_center=False,
        radius=ra 
        ) 

        nb_neighbors = 0
        for neighbor_pos in neighbors:
            neigh_contents = self.model.grid.get_cell_list_contents(neighbor_pos)
            for agent in neigh_contents:
                if isinstance(agent, PedestrianAgent):
                    nb_neighbors += 1
                    dist = euclidean_dist(cell, agent.pos)
                    density_score += exp(-dist**2)

        # compute the real density 
        real_density = float(nb_neighbors)
        real_density = real_density / len(neighbors)# (((2*ra+1)**2)-1)# mesa consider the neighborhood as a square of size ra*
        real_density = real_density / 0.35**2  
        
        density_score =  density_score * alpha
        return density_score , real_density
    
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

    def score(self, next_cell, density:float = None):
        """
        Compute the satisfaction score considering the agent moving on the next_cell.
        """
        exit = self.model.exit
        # We compute the distance to the exit
        dist_to_exit = euclidean_dist(next_cell, exit)
        # We compute the density of the next cell
        if density is None: # gard rail in case there is code where density is not computed before
            density, _ = self.get_density(next_cell)
        
        #return (self.pd * dist_to_exit) + (self.pv * density)
        return dist_to_exit / (self.vel0 * exp(- density * (self.pv+1 )/(self.pd+1)))
    
    
    def step(self):

        if self.pos == self.model.exit:
            self.model.grid.remove_agent(self)  # L'agent "sort" de la grille
            self.model.schedule.remove(self)
        else:
            min_score = float('inf')
            best_cell = None
            density_of_best_cell = None
            for cell in self.get_cells_around():
                density, real_density = self.get_density(cell)
                score = self.score(cell, density)
                if score < min_score:
                    min_score = score
                    best_cell = cell
                    density_of_best_cell = real_density
            
            previous_cell = self.pos
            self.model.grid.move_agent(self, best_cell)
            if self.model.max_density_per_episode < density_of_best_cell:
                self.model.max_density_per_episode = density_of_best_cell

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

    


