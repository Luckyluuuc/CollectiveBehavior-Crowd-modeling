from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import PedestrianAgent
from model import CrowdModel # type: ignore
from obstacle import Obstacle
from trajectory import Trajectory
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
            "Shape": "/home/alexis-le-s/Cours/S5/Colletive_Behavior/CollectiveBehavior-Crowd-modeling/assets/wall.jpeg",
            "Filled": "true",
            "w": 1,
            "h": 1,
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
            "Shape": "/home/alexis-le-s/Cours/S5/Colletive_Behavior/CollectiveBehavior-Crowd-modeling/assets/exit.gif",
            "Filled": "false",
            "w": 4,
            "h": 4,
            "Color": "black",
            "Layer": 0,
        }
    return {}



def run_visualisation(nb_agents=50, width=70, height=70, obstacles=[(10,10)], exit_pos=[(50,0), (0, 50)]):
    """
    Run the visualization serve
    """
    # CHOICE OF MODELS FOR TESTS
    use_fuzzy = True 
    enable_emotions = True  
    enable_relationships = True  
    enable_clustering = True  

    grid = CanvasGrid(agent_portrayal, width, height, 1000, 1000)
    server = ModularServer(
        CrowdModel,
        [grid],
        "Simulation de Foule",
        {
            "n_agents": nb_agents,
            "width": width,
            "height": height,
            "obstacles": obstacles,
            "exit_pos": exit_pos,
            "use_fuzzy": use_fuzzy,
            "enable_emotions": enable_emotions,
            "enable_relationships": enable_relationships,
            "enable_clustering": enable_clustering,
        },
    )
    server.port = 8521  # Port par défaut
    server.launch()

if __name__ == "__main__":
    run_visualisation()

    

    """
    agents = 1
    length = 10
    exits = [(5,0), (0,5)]
    exit_fire = [(5,0)]
    run_visualisation(nb_agents=agents, width=length, height=length, exit_pos=exits)
    """