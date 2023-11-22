from dataclasses import dataclass
from itertools import product
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
np.random.seed(1)

NUM_STATIONS = 40
NUM_NEIGHBORHOODS = 60
NUM_SCENARIOS = 365


@dataclass
class StaticData:
    stations: list[int]
    neighborhoods: list[int]
    fixed_costs: list[int]
    travel_costs: dict[tuple[int, int], int]
    demand_penalty: int
    coords: np.ndarray


def make_static_data():
    # Download instance.
    import urllib.request

    url = "https://github.com/alessandrozocca/MO2023/raw/main/data/assignment2.pkl"
    response = urllib.request.urlopen(url)
    instance = pickle.loads(response.read())

    # Generate random permutation to shuffle stations and neighborhoods locations.
    permutation = np.random.permutation(range(NUM_STATIONS + NUM_NEIGHBORHOODS))

    stations = list(range(NUM_STATIONS))
    neighborhoods = list(range(NUM_NEIGHBORHOODS))
    fixed_costs = np.random.randint(5, 10, NUM_STATIONS).tolist()
    distances = instance["edge_weight"][permutation][:, permutation]
    travel_costs = {
        (i, j): distances[i, j + NUM_STATIONS] for i in stations for j in neighborhoods
    }
    coords = instance["node_coord"][permutation]

    return StaticData(
        stations=stations,
        neighborhoods=neighborhoods,
        fixed_costs=fixed_costs,
        travel_costs=travel_costs,
        demand_penalty=15,
        coords=coords,
    )


def generate_data(means: list, num_locations: int, num_samples: int = 365):
    data = np.zeros((num_samples, num_locations))  # Switch dimensions

    for j in range(num_samples):
        mean = means[j % 7]  # get mean using modulo
        data[j, :] = np.random.poisson(mean, num_locations)  # Switch indices

    return data


def make_demand_scenarios():
    means = [3, 4, 4, 4, 4, 3, 2]
    return generate_data(means, NUM_NEIGHBORHOODS, NUM_SCENARIOS)


# ---------------------------------------------------------------------
def read_elastic_net_data():
    """
    Returns a features matrix X and the target vector y.
    """
    wind_speed = pd.read_csv(
        "https://gist.githubusercontent.com/leonlan/dc606eee560edde18fd47339b7ad2954/raw/5ef38f264134ddd1be0331202616c78dd75be624/wind_speed.csv"
    ).dropna()
    X = wind_speed[
        ["IND", "RAIN", "IND.1", "T.MAX", "IND.2", "T.MIN", "T.MIN.G"]
    ].values
    y = wind_speed["WIND"].values
    return X, y
