from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import PedestrianAgent
from model import CrowdModel # type: ignore
from obstacle import Obstacle
from trajectory import Trajectory

def highest_trait(agent):
    """
    Takes an agent as input and returns the personality trait (O, C, E, A, N)
    with the highest value.
    """
    max_trait = max(agent.personality, key=agent.personality.get)
    return max_trait

def color_trait(agent):
    if highest_trait(agent) == "O" :
        return "blue"
    if highest_trait(agent) == "C" :
        return "purple"
    if highest_trait(agent) == "E":
        return "orange"
    if highest_trait(agent) == "A" :
        return "yellow"
    if highest_trait(agent) == "N" :
        return "green" 

def agent_portrayal(agent):
    if isinstance(agent, PedestrianAgent):
        color = ["red", "blue", "green", "yellow", "purple", "orange", "brown", "black"]
        return {
            "Shape": "circle",
            "Filled": "true",
            "r": 1.2,
            #"Color": color[agent.unique_id % len(color)],
            "Color": color_trait(agent),
            "Layer": 0,
        }
    
    if isinstance(agent, Obstacle):
        return {
            "Shape": "circle",
            "Filled": "true",
            "r": 1,
            "Color": "grey",
            "Layer": 0,
        }
    
    if isinstance(agent, Trajectory):
        colors = ["black", "blue", "green", "yellow", "purple", "orange", "brown", "black"]

        return {
            "Shape": "circle",
            "Filled": "false",
            "r": 0.1,
            "Color": colors[agent.agent_id % len(colors)],
            "Layer": 1  ,
        }
    return {}



def run_visualisation(nb_agents=400, width=100, height=100, obstacles=[], exit_pos=[(50,0), (0, 50)]):
    """
    Lance le serveur de visualisation.
    TODO : Print les obstacles sur la grille.
    """
    grid = CanvasGrid(agent_portrayal, width, height, 1000, 1000)
    server = ModularServer(
        CrowdModel,
        [grid],
        "Simulation de Foule",
        {"n_agents": nb_agents, "width": width, "height": height, "obstacles": obstacles, "exit_pos": exit_pos},
    )
    server.port = 8521  
    server.launch()

if __name__ == "__main__":
    agents = 1
    length = 10
    exits = [(5,0), (0,5)]
    exit_fire = [(5,0)]
    run_visualisation(nb_agents=agents, width=length, height=length, exit_pos=exits)