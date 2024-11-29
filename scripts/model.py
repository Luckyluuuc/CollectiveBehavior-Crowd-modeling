import random

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

        # Create agents only on empty cells
        empty_cells = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height) if self.grid.is_cell_empty((x, y))]
        for i in range(n_agents):
            if len(empty_cells) == 0:
                break
            agent = PedestrianAgent(i, self)
            cell_i = random.randint(0, len(empty_cells)-1)
            self.grid.place_agent(agent, empty_cells[cell_i])
            self.schedule.add(agent)
            empty_cells.pop(cell_i)

    def step(self):
        self.schedule.step()


if __name__ == "__main__":
    model = CrowdModel(0, 4, 4, [(2,2), (2,3)], (1,3))
    for _ in range(100):
        model.step()