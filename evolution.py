import numpy as np
from agent import Agent
import statistics
import random
import csv
from typing import List


class Evolution:

    def __init__(self):
        pass

    @staticmethod
    def calculate_fitness(agents: List[Agent]):
        for i, a in enumerate(agents):
            pass


    @staticmethod
    def crossover(parent1: Agent, parent2: Agent):
        child = parent1.copy()
        for layer_number in parent1.nn.weights.keys():
            if layer_number % 2 == 0:
                # child.nn.weights[layer_number] = parent1.nn.weights[layer_number].copy()
                # child.nn.biases[layer_number] = parent1.nn.biases[layer_number].copy()
                # else:
                child.nn.weights[layer_number] = parent2.nn.weights[layer_number].copy()
                child.nn.biases[layer_number] = parent2.nn.biases[layer_number].copy()
        return child

    @staticmethod
    def mutate(child: Agent):
        mutation_probability = .8
        noise_range = .3
        if random.random() < mutation_probability:
            for layer_number in child.nn.weights.keys():
                child.nn.weights[layer_number] += np.random.normal(0, noise_range, child.nn.weights[layer_number].shape)
                child.nn.biases[layer_number] += np.random.normal(0, noise_range, child.nn.biases[layer_number].shape)
        return child

    def generate_new_population(self, num_agents, prev_agents=None):
        # in first generation, we create random players
        if prev_agents is None:
            return [Agent() for _ in range(num_agents)]
        else:
            new_agents = []
            population_fitness = sum([agent.trf for agent in prev_agents])
            agent_probabilities = [agent.trf / population_fitness for agent in prev_agents]
            parents = []
            qt_parameter = 5
            p = 0.5
            while len(parents) != 2 * num_agents:
                candidate = np.random.choice(prev_agents, qt_parameter, replace=False).tolist()
                candidate.sort(key=lambda x: x.trf, reverse=True)
                for i in range(len(candidate)):
                    if random.random() < p * (1 - p) ** i:
                        parents.append(candidate[i])
                        break
            # parents = np.random.choice(prev_players, 2*num_players, p=agent_probabilities, replace=True)
            crossover_probability = 0.4
            for i in range(num_agents):
                if random.random() < crossover_probability:
                    new_agents.append(self.crossover(parents[i * 2], parents[i * 2 + 1]))
                else:
                    new_agents.append(parents[i * 2].copy())
            for i in range(num_agents):
                self.mutate(new_agents[i])
            return new_agents

    @staticmethod
    def next_population_selection(agents: list, num_agents: int):

        agents.sort(key=lambda x: x.trf, reverse=True)
        _mean = statistics.mean([agent.trf for agent in agents])
        with open('records.csv', 'a+', newline='') as _file:
            writer = csv.writer(_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([agents[0].trf, agents[len(agents) - 1].trf, _mean])
        return agents[: num_agents]
