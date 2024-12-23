import random
import numpy as np

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

# for the fuzzy logic
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from fuzzy import FuzzyModel
from grid_utils import MultiGridWithProperties


from agents import PedestrianAgent
from obstacle import Obstacle
from trajectory import Trajectory
from random import gauss
from math import sqrt
from exit import Exit
from math import sqrt, pi, exp


def euclidean_dist(pt1, pt2):
    """ Return euclidean distance between two points """
    return sqrt((pt1[0]- pt2[0])**2 + (pt1[1] - pt2[1])**2)


class CrowdModel(Model):
    def __init__(self, n_agents, width, height, obstacles, exit_pos):
        super().__init__(seed=42)
        self.grid = MultiGridWithProperties(width, height, torus=False)  # Torus=False to avoid cycling edges
        self.pd_sim = None
        self.pv_sim = None
        self.fuzzy_model = FuzzyModel() # Fuzzy model to compute Pd and Pv

        for pos in exit_pos:
            self.grid.set_cell_property(pos, 'is_exit', True)

        
        for i, (x, y) in enumerate(exit_pos):
            exit_agent = Exit(f"exit-{i}", self)
            self.grid.place_agent(exit_agent, (x, y))


        self.relationship_matrix = np.zeros((n_agents, n_agents)) # cf. Algorithm 6: Emotion Contagion Model
        self.clusters = {}  # keys are cluster ids, values are agents who are part of the cluster
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
            #self.grid.place_agent(agent, (8, 2))
            self.schedule.add(agent)
            self.clusters[i] = [agent]
            empty_cells.pop(cell_i)


    def theta(self, dori):
        """
        Algorithm 7: Emotion Contagion Algorithm
        Amplification function that dynamically modify the distance cut-off (cutxy)
        """
        if dori > self.cutori:
            return exp(-(dori/self.cutori)**2)
        return 1 + exp(-(dori/self.cutori)**2)


    def update_relationships(self):
        """
        Algorithm 6: Emotion Contagion Algorithm
        Update neighbors and density via relationship matrix (not explicitely written)
        """
        agents = list(self.schedule.agents)

        # Reset the relationships
        self.relationship_matrix = np.zeros_like(self.relationship_matrix)

        # Compute only the upper triangular part of the matrix (as it is symmetric)
        # In parallel, compute the density of each agent
        for i in range(len(agents)):
            agent1 = agents[i]

            for j in range(i+1, len(agents)):
                agent2 = agents[j]

                # Compute relative distances and velocities
                dxy = euclidean_dist(agent1.pos, agent2.pos)
                dori = euclidean_dist(np.arccos(agent1.vel), np.arccos(agent2.vel))

                # Case where there is a relation between the two agents
                if (dxy < self.cutxy * self.theta(dori)):
                    # Relationship matrix is filled with distances to then compute neighbors easily
                    self.relationship_matrix[agent1.unique_id, agent2.unique_id] = dxy

                    # Work on the assumption that agent densities are reset during step phase
                    agent1.p += 1
                    agent2.p += 1

        # Get the full matrix
        self.relationship_matrix = self.relationship_matrix + self.relationship_matrix.T


    def coll_clustering_algo(self):
        """
        Algorithm 1: Collective Clustering Algorithm
        """
        # Initialize cluster center
        # Agent's index is supposed to correspond with its unique id (cf initialization)
        agents = {agent.unique_id: agent for agent in self.schedule.agents}

        sorted_agents_density = sorted(agents.values(), key=lambda agent : agent.p, reverse=True)

        # Cluster initialization with the densest agent
        self.clusters = {}
        highest_density_agent = sorted_agents_density[0] 
        self.clusters[highest_density_agent.unique_id] = [highest_density_agent]
        highest_density_agent.neigh = highest_density_agent.unique_id

        for i in range(1, len(sorted_agents_density)):
            # Get agents in increasing density order
            agent = sorted_agents_density[i]

            # Get the agent with the closest distance to our current agent (avoiding the zeros distances)
            relation_dists = self.relationship_matrix[agent.unique_id]
            non_zero_dist = np.nonzero(relation_dists)[0]
            
            if len(non_zero_dist) == 0: # all distances are = 0 which means no relation at all
                self.clusters[agent.unique_id] = [agent]
                agent.neigh = agent.unique_id

            else:
                closest_agent_id = non_zero_dist[np.argmin(relation_dists[non_zero_dist])]
                closest_agent = agents[closest_agent_id]

                # Relationship and distance have already been compared in the relationships matrix update
                # only lacks the density to assess the neighbooring
                if closest_agent.p > agent.p:
                    # The density of the closest agent is higher also means it has already been treated by the algorithm
                    # Thus, its neigh value should be accurate
                    self.clusters[closest_agent.neigh].append(agent)
                    agent.neigh = closest_agent.neigh

                else:
                    self.clusters[agent.unique_id] = [agent]
                    agent.neigh = agent.unique_id


    def emotion_contagion(self):
        """
        Emotion contagion algorithm
        """
        for agent in self.schedule.agents:
            assert(isinstance(agent, PedestrianAgent))
            agent.update_emotions()



    def step(self):
        # Make the agent move
        self.remove_all_trajectories()
        self.max_density_per_episode = 0
        self.schedule.step()
        print("Max density per episode: ", self.max_density_per_episode)
        
        # Fill relationship matrix with distances from each relation
        self.update_relationships()

        # Update the clupdate_emotionsusters based on closest neighbor 
        self.coll_clustering_algo()

        # Apply the emotion contagion among the previously computed clusters
        self.emotion_contagion()
        

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