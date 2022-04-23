import re
import argparse

from covid_engine import CovidSimulatorEngine
from animation import Animation
from text import Text


def menu():
    text = Text()
    arguments = (["size", str, text.board_size, None],
                 ["agents", int, text.agents_start, None],
                 ["infected", int, text.infected_start, None],
                 ["--speed", int, text.speed, 20],
                 ["--incubation", int, text.incubation_time, 14],
                 ["--convalescence", int, text.convalescence_time, 20],
                 ["--infection_probability", float, text.infection_probability, 0.25],
                 ["--distance", int, text.infection_distance, 2],
                 ["--death_probability", float, text.death_probability, 0.02],
                 ["--time_random", int, text.time_random, 3],
                 ["--interval", int, text.interval, 50],
                 ["--steps", int, text.steps, 60])

    parser = argparse.ArgumentParser(description=text.description)
    for arg, arg_type, arg_help, arg_default in arguments:
        parser.add_argument(arg, type=arg_type, help=arg_help, default=arg_default)
    args = parser.parse_args()

    if not re.match(r"[1-9]\d*X[1-9]\d*$", args.size):
        print(text.error_board)
        return None
    
    board_size = str(args.size)
    board_size = (board_size.split("X"))

    if not 0 <= args.agents <= int(board_size[0]) * int(board_size[1]):
        print(text.error_agents)
        return None

    if not 0 <= args.infected <= args.agents:
        print(text.error_infected)
        return None

    if args.speed and not 0 <= args.speed:
        print(text.error_speed)
        return None

    if args.incubation and not 0 <= args.incubation:
        print(text.error_incubation)
        return None

    if args.convalescence and not 0 <= args.convalescence:
        print(text.error_convalescence)
        return None

    if args.infection_probability and not 0 <= args.infection_probability <= 1:
        print(text.error_infection_probability)
        return None

    if args.distance and not 0 <= args.distance:
        print(text.error_infection_distance)
        return None

    if args.death_probability and not 0 <= args.death_probability <= 1:
        print(text.error_death_probability)
        return None

    if args.time_random and not 0 <= args.time_random:
        print(text.error_time_random)
        return None

    if args.interval and not 0 <= args.interval:
        print(text.error_interval)
        return None

    if args.steps and not 0 <= args.steps:
        print(text.error_steps)
        return None

    engine = CovidSimulatorEngine(board_size=(int(board_size[0]), int(board_size[1])),
                                  agents_start=args.agents,
                                  infected_start=args.infected, speed=args.speed,
                                  incubation_time=args.incubation,
                                  convalescence_time=args.convalescence,
                                  infection_probability=args.infection_probability,
                                  infection_distance=args.distance,
                                  death_probability=args.death_probability,
                                  time_random=args.time_random)
    engine.place_agents()

    animation = Animation(engine,
                          interval=args.interval,
                          steps=args.steps)
    animation.animate()


menu()
