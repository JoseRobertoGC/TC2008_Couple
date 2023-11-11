from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from graficas import get_chart_modules


from model import CarModel

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "gray", "w": 1, "h": 1}
    
    if hasattr(agent, 'color'):
        portrayal["Color"] = agent.color
        portrayal["Layer"] = 2
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
    elif hasattr(agent, 'cell_type'):
        if agent.cell_type == "street":
            portrayal["Color"] = "grey"  # Calles pueden ser grises
        elif agent.cell_type == "sidewalk":
            portrayal["Color"] = "lightgrey"  # Aceras pueden ser más claras
        elif agent.cell_type == "grass":
            portrayal["Color"] = "green"  # Zonas verdes
        elif agent.cell_type == "building":
            portrayal["Color"] = "brown"  # Edificios

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart_modules = get_chart_modules()


model_params = {
    "width": 10,
    "height": 10,
    "n_agents": 3,
    "free_cell_percentage": 80,
    "max_time": 100
}

server = ModularServer(
    CarModel,
    [grid, *chart_modules],  
    "Car Simulation",
    model_params
)
server.port = 8521 

if _name_ == "_main_":
    server.launch()