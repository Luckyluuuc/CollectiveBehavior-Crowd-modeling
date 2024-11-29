from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import PedestrianAgent
from model import CrowdModel # type: ignore
from obstacle import Obstacle

def agent_portrayal(agent):
    if isinstance(agent, PedestrianAgent):
        if agent.unique_id == 0:
            return {
                "Shape": "circle",
                "Filled": "true",
                "r": 1,
                "Color": "red",
                "Layer": 0,
            }
        else:
            return {
                "Shape": "circle",
                "Filled": "true",
                "r": 1,
                "Color": "blue",
                "Layer": 0,
            }
    return {}

def grid_portrayal(model):
    portrayal = {}
    for cell in model.grid.coord_iter():
        (content, x, y) = cell
        if (x, y) == model.exit_pos:
            portrayal[(x, y)] = {"Shape": "rect", "w": 1, "h": 1, "Color": "green", "Layer": 1}
    return portrayal


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
        {"n_agents": 80, "width": 40, "height": 40, "obstacles": [], "exit_pos": (0,0)},
    )
    server.port = 8521
    server.launch()

if __name__ == "__main__":
    run_visualisation()