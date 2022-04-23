from random import random, randint

import numpy as np


class Agent:
    """Contains characteristics of an Agent"""
    def __init__(self, is_infected: bool = False, is_quarantined: bool = False):
        self.is_infected = is_infected
        self.is_quarantined = is_quarantined
        self.is_immune = False
        self.time_since_infection = 0


class CovidSimulatorEngine:
    """"Contain functions necessary to make simulations"""
    def __init__(self, board_size: tuple, agents_start: int, infected_start: int, speed: int,
                 incubation_time: int, convalescence_time: int, infection_probability: float,
                 infection_distance: int, death_probability: float, time_random: int):
        self.board_size = board_size
        self.board = np.zeros(board_size, dtype=Agent)

        self.agents_list = []
        self.agents_start = agents_start
        self.infected_start = infected_start

        self.infection_probability = infection_probability
        self.death_probability = death_probability

        self.infected_encountered = 0
        self.death_counter = 0
        self.speed = speed
        self.incubation_time = incubation_time
        self.convalescence_time = convalescence_time
        self.time_random = time_random

        adjacent = [(x, y) for x in range(-infection_distance, infection_distance + 1)
                    for y in range(-infection_distance, infection_distance + 1)]
        adjacent.remove((0, 0))
        self.adjacent = np.array(adjacent)

    def place_agents(self):
        """Places agents randomly on a board and infects specified amount of them"""
        agents_coords = set()
        while len(agents_coords) < self.agents_start:
            agents_coords.add((randint(0, self.board_size[0] - 1),
                               randint(0, self.board_size[1] - 1)))

        for coord_x, coord_y in agents_coords:
            agent = Agent()
            self.agents_list.append(agent)
            self.board[coord_x, coord_y] = agent

        for agent in self.agents_list[: self.infected_start]:
            agent.is_infected = True

    def move_agents(self):
        """Moves agents on a board"""
        new_board = np.zeros(self.board_size, dtype=Agent)
        for index, agent in np.ndenumerate(self.board):
            if agent:
                while True:
                    if agent.is_quarantined:
                        movement = index
                        new_board[movement[0], movement[1]] = agent
                        break
                    else:
                        movement = ((index[0] + randint(-self.speed, self.speed)) % self.board_size[0],
                                    (index[1] + randint(-self.speed, self.speed)) % self.board_size[1])
                        if not self.board[movement[0], movement[1]] and not new_board[movement[0], movement[1]]:
                            new_board[movement[0], movement[1]] = agent
                            break
        self.board = new_board
    
    def get_surrounding_infected(self, index: tuple, agent: Agent):
        """Returns amount of infected, not quarantined agents around a healthy one,
           returns None if agent is infected or immune"""
        if not agent.is_immune and not agent.is_infected:
            adjacent_indexes = (self.adjacent + index) % self.board_size
            adjacent_infected = len([True for row, col in adjacent_indexes
                                     if self.board[row, col]
                                     and self.board[row, col].is_infected
                                     and not self.board[row, col].is_quarantined])

            return adjacent_infected
        return None
        
    def check_if_infected(self, adjacent_infected) -> bool:
        """Randomly choose if Agent is infected, every adjacent_infected equals one chance to get infected"""
        for x in range(adjacent_infected):
            if random() <= self.infection_probability:
                return True
        return False

    def check_if_dead(self, agent: Agent) -> bool:
        """Randomly choose if Agent dies"""
        if agent.is_quarantined and not agent.is_immune:
            return random() <= self.death_probability

    def check_if_quarantined(self, agent: Agent) -> bool:
        """Checks if Agent should be quarantined"""
        if agent.is_infected and agent.time_since_infection >= (self.incubation_time +
                                                                randint(-self.time_random, self.time_random)):
            return True
        return False

    def has_recovered(self, agent: Agent) -> bool:
        """Checks if Agent has recovered"""
        if agent.time_since_infection >= (self.convalescence_time + randint(-self.time_random, self.time_random)):
            return True
        return False

    def remove_dead(self, index: tuple):
        """Removes dead from the board, counts the dead"""
        self.board[index[0], index[1]] = 0
        self.death_counter += 1

    def get_state_quantities(self) -> tuple:
        """Counts the states in a population and returns a tuple containing:
           (susceptible, quarantined, infected, immune)"""
        susceptible, quarantined, infected, immune = 0, 0, 0, 0
        for _, agent in np.ndenumerate(self.board):
            if agent:
                if agent.is_immune:
                    immune += 1
                elif agent.is_quarantined:
                    quarantined += 1
                elif agent.is_infected:
                    infected += 1
                else:
                    susceptible += 1
        return susceptible, quarantined, infected, immune, self.death_counter

    def turn(self):
        """Function used to advance in the simulation"""
        self.infected_encountered = 0
        for index, agent in np.ndenumerate(self.board):
            if not agent:
                continue

            if agent.is_infected:
                agent.time_since_infection += 1

            if self.check_if_quarantined(agent):
                agent.is_quarantined = True

            if self.check_if_dead(agent):
                self.remove_dead(index)

            if self.has_recovered(agent):
                agent.time_since_infection = 0
                agent.is_infected = False
                agent.is_quarantined = False
                agent.is_immune = True

            adjacent_infected = self.get_surrounding_infected(index, agent)
            if adjacent_infected is not None:
                self.infected_encountered += adjacent_infected
                if self.check_if_infected(adjacent_infected):
                    agent.is_infected = True

        self.move_agents()
