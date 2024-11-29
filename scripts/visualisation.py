from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import PedestrianAgent
from model import CrowdModel # type: ignore
from obstacle import Obstacle
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
    return {}



def run_visualisation():
    """
    Lance le serveur de visualisation.
    TODO : Print les obstacles sur la grille.
    """
    grid = CanvasGrid(agent_portrayal, 40, 40, 1000, 1000)

    server = ModularServer(
        CrowdModel,
        [grid],
        "Simulation de Foule",
        {"n_agents": 80, "width": 40, "height": 40, "obstacles": [(20,30)], "exit_pos": (0,0), "fire_sources" : [(5,5), (20,25)]},
    )
    server.port = 8521
    server.launch()

if __name__ == "__main__":
    run_visualisation()