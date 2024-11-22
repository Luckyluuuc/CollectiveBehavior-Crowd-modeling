from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import PedestrianAgent

class CrowdModel(Model):
    """Modèle pour la simulation de foule."""
    def __init__(self, n_agents, width, height):
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Crée des agents
        for i in range(n_agents):
            agent = PedestrianAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """Avance la simulation d'un pas."""
        self.schedule.step()
