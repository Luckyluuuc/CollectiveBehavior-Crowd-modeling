import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

# for the fuzzy logic
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from fuzzy import FuzzyModel



from agents import PedestrianAgent
from obstacle import Obstacle
from trajectory import Trajectory
from random import gauss
from firesource import FireSource
from math import sqrt


def euclidean_dist(pt1, pt2):
    """ Return euclidean distance between two points """
    return sqrt((pt1[0]- pt2[0])**2 + (pt1[1] - pt2[1])**2)

class CrowdModel(Model):
    def __init__(self, n_agents, width, height, obstacles, exit_pos, fire_sources):
        super().__init__(seed=42)
        self.grid = MultiGrid(width, height, torus=False)  # Torus=False to avoid cycling edges
        self.pd_sim = None
        self.pv_sim = None
        self.fuzzy_model = FuzzyModel()


        # Fill the grid with some obstacles
        for i, (x,y) in enumerate(obstacles):
            assert(not self.grid.out_of_bounds((x,y)))
            obstacle = Obstacle(i, self)
            self.grid.place_agent(obstacle, (x, y))

        self.schedule = RandomActivation(self)
        self.exit = exit_pos  # Position(s) of the exit(s)

         # Fill the grid with some fire sources
        self.fire_sources = []  # List to stock them
        for i, pos in enumerate(fire_sources):
            fire = FireSource(i + 1000, self, pos)
            self.grid.place_agent(fire, pos)
            self.fire_sources.append(fire)  

        # Create agents only on empty cells
        empty_cells = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height) if self.grid.is_cell_empty((x, y))]
        for i in range(n_agents):
            if len(empty_cells) == 0:
                break
            personality = {}
            for trait in ['O', 'C', 'E', 'A', 'N']:
                mu = self.random.uniform(0, 1)
                sigma = self.random.uniform(-0.1, 0.1)
                personality[trait] = gauss(mu, sigma**2)
                #personality[trait] = max(0, min(1, gauss(mu, abs(sigma))))
            
            agent = PedestrianAgent(i, self, personality)
            cell_i = random.randint(0, len(empty_cells)-1)
            self.grid.place_agent(agent, empty_cells[cell_i])
            self.schedule.add(agent)
            empty_cells.pop(cell_i)


    def step(self):

        self.remove_all_trajectories()
        self.schedule.step()


    def add_trajectory(self, pos, agent_id): 
        """
        Add a trajectory to the grid
        """
        trajectory = Trajectory(self, agent_id)
        self.grid.place_agent(trajectory, pos)
        self.schedule.add(trajectory)

        assert trajectory.pos is not None, "creation of an agent without position"


    def remove_all_trajectories(self):
        """
        Remove all trajectories object from the grid
        """
        for agent in self.schedule.agents:
            if isinstance(agent, Trajectory) and agent.pos is not None: #TODO understand why pos is none sometimes
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)
        Trajectory.trajectory_counter = 0

        



if __name__ == "__main__":
    model = CrowdModel(0, 4, 4, [(2,2), (2,3)], (1,3))
    for _ in range(100):
        model.step()