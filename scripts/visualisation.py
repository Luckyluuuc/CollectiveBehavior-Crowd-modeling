from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import PedestrianAgent
from model import CrowdModel # type: ignore
from obstacle import Obstacle
from trajectory import Trajectory
from firesource import FireSource
from exit import Exit

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
            "Shape": "rect",
            "Filled": "true",
            "w": 1,
            "h": 1,
            "Color": "red",
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
    
    elif isinstance(agent, Exit):
        return {
            "Shape": "rect",
            "Filled": "false",
            "w": 1,
            "h": 1,
            "Color": "black",
            "Layer": 0,
        }
    return {}





def run_visualisation(nb_agents=400, width=100, height=100, obstacles=[(20,40), (21,40), (20,39), (21,39)], exit_pos=[(50,0), (0, 50)], fire_sources=[]):
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