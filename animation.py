import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class Animation:
    def __init__(self, engine, interval: int, steps: int):
        self.engine = engine
        self.interval = interval
        self.steps = steps

        self.figure, (self.R0_graph, self.axes_graph, self.axes_board) = plt.subplots(1, 3)
        self.figure.canvas.set_window_title('Covid simulator 9000')

        #  population graph
        self.axes_graph.set_title("Graph representation of population")

        self.axes_graph.set_xlim(0, self.steps)
        self.axes_graph.set_ylim(0, self.engine.agents_start)

        self.count_susceptible, = self.axes_graph.plot([], [], "g", label="susceptible")
        self.count_infected, = self.axes_graph.plot([], [], "r", label="infected")
        self.count_quarantined, = self.axes_graph.plot([], [], "m", label="quarantined")
        self.count_immune, = self.axes_graph.plot([], [], "b", label="immune")
        self.count_dead, = self.axes_graph.plot([], [], "black", label="dead")

        self.counts = [[], [], [], [], []]

        self.axes_graph.set_ylabel("Count")
        self.axes_graph.set_xlabel("Step")
        self.axes_graph.legend(loc="upper right")

        #  R0 graph
        self.R0_graph.set_title("R0 graph")
        self.R0_graph.set_ylabel("R0")
        self.R0_graph.set_xlabel("Step")

        self.R0_graph.set_xlim(0, self.steps)
        self.R0_graph.set_ylim(0, 5)

        self.points_R0, = self.R0_graph.plot([], [])
        self.R0 = []

        #  board
        self.axes_board.set_title("Board representation of population")

        self.axes_board.set_aspect(1)
        self.axes_board.set_xlim(0, engine.board_size[0])
        self.axes_board.set_ylim(0, engine.board_size[1])

        self.points_susceptible, = self.axes_board.plot([], [], "gs", markersize=1)
        self.points_infected, = self.axes_board.plot([], [], "rs", markersize=1)
        self.points_quarantined, = self.axes_board.plot([], [], "ms", markersize=1)
        self.points_immune, = self.axes_board.plot([], [], "bs", markersize=1)

    def animation_function(self, _):
        def graphs_animation():
            counts = self.engine.get_state_quantities()
            [x.append(y) for x, y in zip(self.counts, counts)]

            if counts[0] == 0:
                r0 = 0
            else:
                r0 = self.engine.infected_encountered / counts[0]
            self.R0.append(r0)

            frames = len(self.counts[0])

            self.count_susceptible.set_ydata(self.counts[0])
            self.count_susceptible.set_xdata(range(frames))

            self.count_quarantined.set_ydata(self.counts[1])
            self.count_quarantined.set_xdata(range(frames))

            self.count_infected.set_ydata(self.counts[2])
            self.count_infected.set_xdata(range(frames))

            self.count_immune.set_ydata(self.counts[3])
            self.count_immune.set_xdata(range(frames))

            self.count_dead.set_ydata(self.counts[4])
            self.count_dead.set_xdata(range(frames))

            self.points_R0.set_ydata(self.R0)
            self.points_R0.set_xdata(range(frames))

        def board_animation():
            susceptible, infected, immune, quarantined = [[], []], [[], []], [[], []], [[], []]
            for index, agent in np.ndenumerate(self.engine.board):
                if agent:
                    if agent.is_immune:
                        immune[0].append(index[0])
                        immune[1].append(index[1])
                    elif agent.is_quarantined:
                        quarantined[0].append(index[0])
                        quarantined[1].append(index[1])
                    elif agent.is_infected:
                        infected[0].append(index[0])
                        infected[1].append(index[1])
                    else:
                        susceptible[0].append(index[0])
                        susceptible[1].append(index[1])

            self.points_susceptible.set_xdata(susceptible[0])
            self.points_susceptible.set_ydata(susceptible[1])

            self.points_infected.set_xdata(infected[0])
            self.points_infected.set_ydata(infected[1])

            self.points_immune.set_xdata(immune[0])
            self.points_immune.set_ydata(immune[1])

            self.points_quarantined.set_xdata(quarantined[0])
            self.points_quarantined.set_ydata(quarantined[1])

        graphs_animation()
        board_animation()
        self.engine.turn()

    def animate(self):
        animation = FuncAnimation(self.figure, self.animation_function,
                                  interval=self.interval, frames=self.steps, repeat=False)
        plt.show()
