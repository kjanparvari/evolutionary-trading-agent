import os
from os.path import join
import pickle
from pathlib import Path
import shutil


# save agents of this generation in file
def save_generation(agents, gen_num):
    path = Path(join('checkpoint', str(gen_num)))
    try:
        shutil.rmtree(path)
    except OSError as e:
        pass

    path.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(agents):
        agent_path = join(path, str(i))
        with open(agent_path, 'wb') as file:
            pickle.dump(p, file)


# load agents from file
def load_generation(checkpoint_path):
    files = os.listdir(checkpoint_path)
    prev_agents = []
    for f in files:
        with open(join(checkpoint_path, f), 'rb') as file:
            p = pickle.load(file)
            prev_agents.append(p)

    return prev_agents
