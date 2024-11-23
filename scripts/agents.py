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
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.vel0 = 1
        self.pd = 1
        self.pv = 1

    def score(self, next_cell):
        """
        Compute the satisfaction score considering the agent moving on the next_cell.
        """

        grid = self.model.grid
        
        # Don't want to go on an already occupied cell
        if grid.get_cell_list_contents(self.pos):
            return -1
        
        exit = self.model.exit

        # Euclidean distance
        dist_exit = euclidean_dist(exit, next_cell)

        # TO IMPROVE : changer la valeur de radius (distance à laquelle on considère les voisins)
        # Get all the neighbors of the observed cell
        neighbors = grid.get_neighborhood(
        next_cell,
        moore=True, # Do not consider diagonals
        include_center=False,
        radius=3) # Consider cell that are far by 3 cells of next_cell

        density = 0
        for cell in neighbors:
            nb_occupants = sum(1 for object in grid.get_cell_list_contents(cell) if isinstance(object, PedestrianAgent))
            
            # The further the cell is from next_cell, the less its density will impact next_cell density
            density += nb_occupants / euclidean_dist(cell, next_cell)  # non-zero thanks to second function line

        # Scoring function extracted from the scientific paper
        return (dist_exit/self.vel0) * exp((density * (self.pv + 1) / (self.pd + 1))**2)

