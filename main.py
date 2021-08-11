import numpy as np

from agent import Agent
from evolution import Evolution
from config import CONFIG
from backup import save_generation, load_generation


def run(checkpoint=None):
    evolution = Evolution()
    if checkpoint is None:
        agents = evolution.generate_new_population(CONFIG['num_agents'])
        # agents of the previous generation
        prev_agents = []
        gen_num = 1
        best_fitness = 0
    else:
        num_alive = 2 * CONFIG['num_agents']
        checkpoint_path = f'./checkpoint/{checkpoint}'
        # players of the previous generation
        prev_agents = load_generation(checkpoint_path)
        # players of the current generation
        agents = evolution.generate_new_population(CONFIG['num_agents'], prev_agents)
        gen_num = int(checkpoint_path[checkpoint_path.rfind('/') + 1:]) + 1
        best_fitness = max(a._fitness for a in prev_agents)

    # money gained by agent
    fs = [0 for _ in range(CONFIG['num_agents'])]
    # money gained by prev agent
    prev_fs = [0 for _ in range(CONFIG['num_agents'])]
    # array of previous agents alive status
    prev_alive = [True for _ in range(CONFIG['num_agents'])]

    while True:
        evolution.calculate_fitness(agents, delta_xs)
        evolution.calculate_fitness(prev_players, prev_delta_xs)


if __name__ == '__main__':
    print(type(np.array([1, 2, 3])))
