from mesa import Agent

class FireSource(Agent):
    """A source of external influence (e.g., fire)."""
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
