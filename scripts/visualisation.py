import argparse
from random import gauss
import random
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
            "Shape": "rect",
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
            "Shape": "rect",
            "Filled": "false",
            "w": 1,
            "h": 1,
            "Color": "black",
            "Layer": 0,
        }
    return {}


def random_personality():
        personality = {}
        for trait in ['O', 'C', 'E', 'A', 'N']:
            mu = random.uniform(0, 1)
            sigma = random.uniform(-0.1, 0.1)
            personality[trait] = gauss(mu, sigma**2)
            # Personality[trait] = max(0, min(1, gauss(mu, abs(sigma))))
        return personality

def full_N():
    personality = {}
    for trait in ['O', 'C', 'E', 'A', 'N']:
        if trait == 'N':
            personality[trait] = 1
        else:
            mu = random.uniform(0, 1)
            sigma = random.uniform(-0.1, 0.1)
            personality[trait] = gauss(mu, sigma**2)
    return personality

def only_N():
    personality = {}
    for trait in ['O', 'C', 'E', 'A', 'N']:
        if trait == 'N':
            personality[trait] = 1
        else:
            personality[trait] = 0
    return personality


def run_visualisation(nb_agents=400, width=100, height=100, obstacles=[(20,40), (21,40), (20,39), (21,39)], exit_pos=[(50,0), (51,0), (52,0), (53,0), (0, 50), (0,51), (0,52), (0,53)], personality = only_N):
    """
    Lance le serveur de visualisation.
    TODO : Print les obstacles sur la grille.
    """
    grid = CanvasGrid(agent_portrayal, width, height, 1000, 1000)
    server = ModularServer(
        CrowdModel,
        [grid],
        "Simulation de Foule",
        {"n_agents": nb_agents, "width": width, "height": height, "obstacles": obstacles, "exit_pos": exit_pos, "personality_function": personality},
    )
    server.port = 8521
    server.launch()

if __name__ == "__main__":
    agents = int(input("Enter the number of agents (default 400): ") or 400)
    personality_choice = input(
        "Choose the personality function (random, fully N, only N; default 'random'): "
    ) or "random"

    # Set the personality function based on user input
    if personality_choice == "random":
        personality_function = random_personality
    elif personality_choice == "fully N":
        personality_function = full_N
    elif personality_choice == "only N":
        personality_function = only_N
    else:
        print("Invalid choice, defaulting to 'random'")
        personality_function = random_personality

    run_visualisation(
        nb_agents=agents,
        personality=personality_function,
    )