from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import CrowdModel # type: ignore

def agent_portrayal(agent):
    """Dessine un agent sous forme de cercle bleu."""
    return {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "blue",
        "Layer": 0,
    }

def run_visualisation():
    """Lance le serveur de visualisation."""
    grid = CanvasGrid(agent_portrayal, 40, 40, 1000, 1000)

    server = ModularServer(
        CrowdModel,
        [grid],
        "Simulation de Foule",
        {"n_agents": 80, "width": 40, "height": 40},
    )
    server.port = 8521
    server.launch()
