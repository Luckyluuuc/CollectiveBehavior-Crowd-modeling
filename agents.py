from mesa import Agent

class PedestrianAgent(Agent):
    """Agent représentant un piéton dans une foule."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = model.random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

    def step(self):
        """Déplace l'agent dans une direction aléatoire (oui Alexis random lol)."""
        x, y = self.pos
        dx, dy = self.direction
        new_position = (x + dx, y + dy)

        # Vérifie si la cellule est vide et dans les limites parce que c'est facile comme ça
        if self.model.grid.out_of_bounds(new_position) or not self.model.grid.is_cell_empty(new_position):
            self.direction = self.model.random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        else:
            self.model.grid.move_agent(self, new_position)
