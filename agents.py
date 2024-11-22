from mesa import Agent

class PedestrianAgent(Agent):
    def step(self):
        """Déplace l'agent vers la sortie s'il n'y est pas encore."""
        if self.pos == self.model.exit_pos:
            self.model.grid.remove_agent(self)  # L'agent "sort" de la grille
            self.model.schedule.remove(self)
        else:
            # Déplacer vers la sortie
            x, y = self.pos
            exit_x, exit_y = self.model.exit_pos
            dx = 1 if x < exit_x else -1 if x > exit_x else 0
            dy = 1 if y < exit_y else -1 if y > exit_y else 0
            new_position = (x + dx, y + dy)
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)
