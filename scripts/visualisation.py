from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import PedestrianAgent
from model import CrowdModel # type: ignore
from obstacle import Obstacle
from trajectory import Trajectory
from firesource import FireSource

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
            "r": 0.5,
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
    if isinstance(agent, FireSource):
        return {
            "Shape": "circle",
            "Filled": "true",
            "r": 1.5,
            "Color": "red",
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



def run_visualisation(nb_agents=80, width=40, height=40, obstacles=[], exit_pos=(0,0), fire_sources=[]):
    """
    Lance le serveur de visualisation.
    TODO : Print les obstacles sur la grille.
    """
    grid = CanvasGrid(agent_portrayal, width, height, 1000, 1000)

    server = ModularServer(
        CrowdModel,
        [grid],
        "Simulation de Foule",
        {"n_agents": nb_agents, "width": width, "height": height, "obstacles": obstacles, "exit_pos": exit_pos, "fire_sources" : fire_sources},
    )
    server.port = 8521
    server.launch()

if __name__ == "__main__":
    run_visualisation()