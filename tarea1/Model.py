from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random
import math

class CellAgent(Agent):
    def _init_(self, unique_id, model, cell_type="sidewalk"):
        super()._init_(unique_id, model)
        self.cell_type = cell_type
        if cell_type == "street":
            self.color = "grey"
        elif cell_type == "sidewalk":
            self.color = "lightgrey"
        elif cell_type == "grass":
            self.color = "green"
        else:
            self.color = "white"

    def step(self):
        pass

class CarAgent(Agent):
    def _init_(self, unique_id, model, color="purple"):
        super()._init_(unique_id, model)
        self.color = color
        self.moves = 0
        self.collisions = 0
        self.step_count = 0
        self.horizontal_direction = 1  # Comienza moviéndose hacia la derecha para el carro amarillo

    def move_blue(self):
        # Movimiento más lento y en una sola dirección
        if self.model.schedule.steps % 3 == 0:
            next_move = (self.pos[0], (self.pos[1] + 1) % self.model.grid.height)
            if self.is_move_valid(next_move):
                self.model.grid.move_agent(self, next_move)
                self.moves += 1

    def move_purple(self):
        # Movimiento en zigzag
        if self.step_count % 2 == 0:
            next_move = ((self.pos[0] + self.horizontal_direction) % self.model.grid.width, self.pos[1])
        else:
            next_move = (self.pos[0], (self.pos[1] - 1) % self.model.grid.height)

        if self.is_move_valid(next_move):
            self.model.grid.move_agent(self, next_move)
            self.moves += 1
            self.step_count += 1
            if self.step_count % 2 == 0:
                self.horizontal_direction *= -1

    def move_yellow(self):
        # Movimiento aleatorio
        current_x, current_y = self.pos
        move_choice = random.choice(["forward", "left", "right", "stay", "backward"])
        if move_choice == "forward":
            next_move = (current_x, (current_y + 1) % self.model.grid.height)
        elif move_choice == "left":
            next_move = ((current_x - 1) % self.model.grid.width, current_y)
        elif move_choice == "right":
            next_move = ((current_x + 1) % self.model.grid.width, current_y)
        elif move_choice == "backward":
            next_move = (current_x, (current_y - 1) % self.model.grid.height)
        elif move_choice == "stay":
            next_move = (current_x, current_y)  # No se mueve

        if self.is_move_valid(next_move):
            self.model.grid.move_agent(self, next_move)
            self.moves += 1

    def is_move_valid(self, next_move):
        # Verifica si la celda está vacía o no tiene otros carros
        return self.model.grid.is_cell_empty(next_move) or not any(isinstance(agent, CarAgent) for agent in self.model.grid.get_cell_list_contents(next_move))

    def step(self):
        if self.color == "blue":
            self.move_blue()
        elif self.color == "purple":
            self.move_purple()
        elif self.color == "yellow":
            self.move_yellow()

        # Colisiones solo para el carro amarillo
        if self.color == "yellow":
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for mate in cellmates:
                if isinstance(mate, CarAgent) and mate is not self:
                    self.collisions += 1
                    mate.collisions += 1
                    self.model.n_collisions += 1

class ObstacleAgent(Agent):
    def _init_(self, unique_id, model):
        super()._init_(unique_id, model)

    def step(self):
        pass

def compute_average_speed(model):
    agent_speeds = [agent.moves for agent in model.schedule.agents if isinstance(agent, CarAgent)]
    average_speed = sum(agent_speeds) / len(agent_speeds) if agent_speeds else 0
    return average_speed

class CarModel(Model):
    def _init_(self, width, height, n_agents, free_cell_percentage, max_time):
        super()._init_()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.max_time = max_time
        self.running = True
        self.n_moves = 0
        self.n_collisions = 0
        self.current_id = 0

        for x in range(width):
            for y in range(height):
                if x == 2 or x == 5:
                    cell_type = "street"
                elif x % 4 == 0:
                    cell_type = "grass"
                elif y % 4 == 0:
                    cell_type = "building"
                else:
                    cell_type = "sidewalk"
                cell_agent = CellAgent(self.next_id(), self, cell_type)
                self.grid.place_agent(cell_agent, (x, y))
                self.schedule.add(cell_agent)

        for _ in range(int((width * height) * (free_cell_percentage / 100))):
            x, y = self.random_empty_cell()
            obstacle = ObstacleAgent(self.next_id(), self)
            self.grid.place_agent(obstacle, (x, y))

        colors = ["purple", "blue", "yellow"]
        for i in range(n_agents):
            color = colors[i % len(colors)]  # Asignación de color basada en el índice
            x, y = self.random_empty_cell()
            car_agent = CarAgent(self.next_id(), self, color)
            self.grid.place_agent(car_agent, (x, y))
            self.schedule.add(car_agent)

        self.datacollector = DataCollector(
            model_reporters={
                "Number of Collisions": lambda m: m.n_collisions,
                "Average Speed": compute_average_speed,
                "Total Movements": lambda m: m.n_moves
            }
        )

    def step(self):
        self.schedule.step()
        self.n_moves = sum(agent.moves for agent in self.schedule.agents if isinstance(agent, CarAgent))
        self.n_collisions = sum(agent.collisions for agent in self.schedule.agents if isinstance(agent, CarAgent))
        self.datacollector.collect(self)
        if self.schedule.steps >= self.max_time:
            self.running = False

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def random_empty_cell(self):
        cell_list = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height) if len(self.grid.get_cell_list_contents((x, y))) <= random.randint(0, 2) and isinstance(self.grid.get_cell_list_contents((x, y))[0], CellAgent)]
        return random.choice(cell_list) if cell_list else None

if _name_ == "_main_":
    pass