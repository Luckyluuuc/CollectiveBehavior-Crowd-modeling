from mesa import Agent

class Obstacle(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)