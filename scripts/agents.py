from mesa import Agent
from mesa.space import MultiGrid
from obstacle import Obstacle
from math import sqrt, exp

def get_cells_around(grid:MultiGrid, loc):
    """
    Return the list of cell we consider as potential new destination for the next step.

    We consider (in first approximation) that the scoring function is enought to
    sort the neighbors and keep only the relevant ones.

    TO IMPROVE : prendre en compte la distance à l'arrivée (?)
    """

    # TO IMPROVE : Take diagonals into consideration
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    valid_neighbors = []

    for dir in directions:
        neighbor = (loc[0] + dir[0], loc[1] + dir[1])

        # Insures the neighbor is part of the grid
        if grid.out_of_bounds(neighbor):
            continue
        
        # Insures the neighbor is not an Obstacle
        neigh_contents = grid.get_cell_list_contents(neighbor)
        if any(isinstance(agent, Obstacle) for agent in neigh_contents):
            continue
        
        valid_neighbors.append(neighbor)

    return valid_neighbors


def euclidean_dist(pt1, pt2):
    """ Return euclidean distance between two points """
    return sqrt((pt1[0]- pt2[0])**2 + (pt1[1] - pt2[1])**2)


class PedestrianAgent(Agent):
    def __init__(self, unique_id, model, pd = 1, pv = 1):
        super().__init__(unique_id, model)
        self.vel0 = 1
        self.pd = pd
        self.pv = pv

    def get_density(self, cell):
        # TODO implement this function
        return 1

    def score(self, next_cell):
        """
        Compute the satisfaction score considering the agent moving on the next_cell.
        """
        exit = self.model.exit
        # We compute the distance to the exit
        dist_to_exit = euclidean_dist(next_cell, exit)
        # We compute the density of the next cell
        density = self.get_density(next_cell)
        

        return dist_to_exit / (self.vel0 * exp(- density * (self.pv+1 )/(self.pd+1)))
    
    def step(self):

        if self.pos == self.model.exit_pos:
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

    


