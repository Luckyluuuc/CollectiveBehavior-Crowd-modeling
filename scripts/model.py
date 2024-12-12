import random
import numpy as np

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from agents import PedestrianAgent
from obstacle import Obstacle
from trajectory import Trajectory
from random import gauss
from firesource import FireSource
from math import sqrt, pi, acos, exp


def euclidean_dist(pt1, pt2):
    """ Return euclidean distance between two points """
    return sqrt((pt1[0]- pt2[0])**2 + (pt1[1] - pt2[1])**2)


class CrowdModel(Model):
    def __init__(self, n_agents, width, height, obstacles, exit_pos, fire_sources):
        super().__init__(seed=42)
        self.grid = MultiGrid(width, height, torus=False)  # Torus=False to avoid cycling edges

        self.relationship_matrix = np.identity(n_agents) # cf. Algorithm 6: Emotion Contagion Model
        self.cutxy = 50
        self.cutori = pi/3

        # Fill the grid with some obstacles
        for i, (x,y) in enumerate(obstacles):
            assert(not self.grid.out_of_bounds((x,y)))
            obstacle = Obstacle(i, self)
            self.grid.place_agent(obstacle, (x, y))

        self.schedule = RandomActivation(self)
        self.exit = exit_pos  # Position(s) of the exit(s)
        self.max_density_per_episode = 0 

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
                # Personality[trait] = max(0, min(1, gauss(mu, abs(sigma))))
            agent = PedestrianAgent(i, self, personality)
            cell_i = random.randint(0, len(empty_cells)-1)
            self.grid.place_agent(agent, empty_cells[cell_i])
            self.schedule.add(agent)
            empty_cells.pop(cell_i)


    def theta(self, dori):
        """
        Algorithm 7: Emotion Contagion Algorithm
        Amplification function that dynamically modify the distance cut-off (cutxy)
        """
        if dori > self.cutori:
            return exp(-(dori/self.cutori)**2)
        return 1 + exp(-(dori/self.cutori)**2)


    def step(self):
        # Make the agent move
        self.remove_all_trajectories()
        self.max_density_per_episode = 0
        self.schedule.step()
        print("Max density per episode: ", self.max_density_per_episode)
        

        # Algorithm 6: Emotion Contagion Algorithm
        # Update relationship matrix
        agents = list(self.schedule.agents)

        # Compute only the upper triangular part of the matrix (as it is symmetric)
        # In parallel, compute the density of each agent
        for i in range(len(agents)):
            for j in range(i+1, len(agents)):
                agent1 = agents[i]
                agent2 = agents[j]

                # Compute relative distances and velocities
                dxy = euclidean_dist(agent1.loc, agent2.loc)
                dori = abs(acos(agent1.vel) - acos(agent2.vel))

                # Compute the relation between the two agents according to dxy and dori
                relation = 1 if (dxy < self.cutxy * self.theta(dori)) else 0

                self.relationship_matrix[agent1.unique_id, agent2.unique_id] = relation

                # Work on the assumption that agent densities are reset during step phase
                agent1.p += relation
                agent2.p += relation

        # Get the full matrix
        self.relationship_matrix = self.relationship_matrix + self.relationship_matrix.T
        


    def add_trajectory(self, pos, agent_id): 
        """
        Add a trajectory to the grid
        """
        trajectory = Trajectory(self, agent_id)
        self.grid.place_agent(trajectory, pos)

        assert trajectory.pos is not None, "creation of an agent without position"


    def remove_all_trajectories(self):
        """
        Remove all trajectories object from the grid
        """
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                for agent in self.grid.get_cell_list_contents((x, y)):
                    if isinstance(agent, Trajectory): 
                        self.grid.remove_agent(agent)
        Trajectory.trajectory_counter = 0

        



if __name__ == "__main__":
    model = CrowdModel(0, 4, 4, [(2,2), (2,3)], (1,3))
    for _ in range(100):
        model.step()