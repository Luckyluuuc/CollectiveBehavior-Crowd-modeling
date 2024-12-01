from mesa import Agent

class Trajectory(Agent):
    """
    A class to represent a trajectory of an agent, it will act as temporary obstacle
    """

    trajectory_counter = 0 # class variable to count the number of trajectories and give them unique id
    def __init__(self, model, agent_id):
        Trajectory.trajectory_counter += 1
        super().__init__(Trajectory.trajectory_counter, model)
        self.agent_id = agent_id

