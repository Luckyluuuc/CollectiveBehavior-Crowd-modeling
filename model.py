from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import PedestrianAgent

class CrowdModel(Model):
    def __init__(self, n_agents, width, height, exit_pos):
        self.grid = MultiGrid(width, height, torus=False)  # Torus=False pour éviter les bords cycliques
        self.schedule = RandomActivation(self)
        self.running = True
        self.exit_pos = exit_pos  # Position de la sortie

        # Crée des agents
        for i in range(n_agents):
            agent = PedestrianAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
