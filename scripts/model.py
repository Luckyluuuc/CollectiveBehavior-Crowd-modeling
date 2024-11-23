from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from agents import PedestrianAgent
from obstacle import Obstacle

class CrowdModel(Model):
    def __init__(self, n_agents, width, height, obstacles, exit_pos):
        super().__init__(seed=42)
        self.grid = MultiGrid(width, height, torus=False)  # Torus=False to avoid cycling edges

        # Fill the grid with some obstacles
        for i, (x,y) in enumerate(obstacles):
            assert(not self.grid.out_of_bounds((x,y)))
            obstacle = Obstacle(i, self)
            self.grid.place_agent(obstacle, (x, y))

        self.schedule = RandomActivation(self)
        self.exit = exit_pos  # Position(s) of the exit(s)

        # Create agents
        for i in range(n_agents):
            agent = PedestrianAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()


if __name__ == "__main__":
    model = CrowdModel(0, 4, 4, [(2,2), (2,3)], (1,3))