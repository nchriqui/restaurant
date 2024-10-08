import json

import pytest

from similarity import (binarize_recipes,
                        binarize_recipes_data_limited_ingredients,
                        binarize_recipes_data_origines, calculate_scores,
                        compute_nearest_neighbors)

RECIPES_COUNT = 7
INGREDIENTS_COUNT = 6


@pytest.fixture
def inputs_recipes_data():
    return {"1": [1, 2, 3], "2": [4, 5], "3": [3, 4, 6], "4": [6], "5": [1], "7": [5]}


@pytest.fixture
def input_binarized_data():
    return {
        "1": [1, 1, 1, 0, 0, 0],
        "2": [0, 0, 0, 1, 1, 0],
        "3": [0, 0, 1, 1, 0, 1],
        "4": [0, 0, 0, 0, 0, 1],
        "5": [1, 0, 0, 0, 0, 0],
        "7": [0, 0, 0, 0, 1, 0],
    }


@pytest.fixture
def output_scores():
    return {
        "1": {"1": 0, "2": 5, "3": 4, "4": 4, "5": 2, "7": 4},
        "2": {"1": 5, "2": 0, "3": 3, "4": 3, "5": 3, "7": 1},
        "3": {"1": 4, "2": 3, "3": 0, "4": 2, "5": 4, "7": 4},
        "4": {"1": 4, "2": 3, "3": 2, "4": 0, "5": 2, "7": 2},
        "5": {"1": 2, "2": 3, "3": 4, "4": 2, "5": 0, "7": 2},
        "7": {"1": 4, "2": 1, "3": 4, "4": 2, "5": 2, "7": 0},
    }


@pytest.fixture
def k3_nn_out():
    return {
        "1": {"nearest_N": [5, 3, 4]},
        "2": {"nearest_N": [7, 3, 4]},
        "3": {"nearest_N": [4, 2, 1]},
        "4": {"nearest_N": [3, 5, 7]},
        "5": {"nearest_N": [1, 4, 7]},
        "7": {"nearest_N": [2, 4, 5]},
    }


@pytest.fixture
def input_recipes_limited():
    return {"1": [10, 20, 30], "2": [4, 30], "3": [6, 10, 30], "4": [6], "7": [1200]}


@pytest.fixture
def input_binarized_limited():
    return {
        "1": [0, 0, 1, 1, 1, 0],
        "2": [1, 0, 0, 0, 1, 0],
        "3": [0, 1, 1, 0, 1, 0],
        "4": [0, 1, 0, 0, 0, 0],
        "7": [0, 0, 0, 0, 0, 1],
    }


@pytest.fixture
def output_scores_limited():
    return {
        "1": {"1": 0, "2": 3, "3": 2, "4": 4, "7": 2},
        "2": {"1": 3, "2": 0, "3": 3, "4": 3, "7": 1},
        "3": {"1": 2, "2": 3, "3": 0, "4": 2, "7": 2},
        "4": {"1": 4, "2": 3, "3": 2, "4": 0, "7": 2},
        "7": {"1": 2, "2": 1, "3": 2, "4": 2, "7": 0},
    }


@pytest.fixture
def input_recipes_origines():
    return {
        "8": [["Boisson", "Viande"], "Afrique"],
        "2": [["Poisson", "Céréales"], "Europe"],
        "3": [["Boisson", "Poisson", "Viande", "Céréales"], "Afrique"],
        "4": [["Poisson"], "Asie"],
        "7": [["Poisson"], "Europe"],
    }


@pytest.fixture
def input_binarized_origines():
    return {
        "8": ([1, 1, 0, 0], [0, 1, 0]),
        "2": ([0, 0, 1, 1], [1, 0, 0]),
        "3": ([1, 1, 1, 1], [0, 1, 0]),
        "4": ([0, 0, 1, 0], [0, 0, 1]),
        "7": ([0, 0, 1, 0], [1, 0, 0]),
    }


@pytest.fixture
def a():
    return 4


def testa(a):
    assert 4 == a


def test_binarize_recipes(inputs_recipes_data, input_binarized_data):
    recipes_binarised = binarize_recipes(
        inputs_recipes_data,
        recipes_count=RECIPES_COUNT,
        ingredients_count=INGREDIENTS_COUNT,
        save=False,
    )
    assert recipes_binarised == input_binarized_data


def test_calculate_scores(input_binarized_data, output_scores):
    scores = calculate_scores(input_binarized_data, False)
    print(scores)
    assert scores == output_scores


def test_compute_nearest_neighbors(output_scores, k3_nn_out):
    mins = compute_nearest_neighbors(output_scores, 3, False)
    assert mins == k3_nn_out


def test_binarize_recipes_data_limited_ingredients(
    input_recipes_limited, input_binarized_limited, mocker
):
    mocker.patch(
        "similarity.extract_all_ingredients_with_chosen_type",
        return_value=[4, 6, 10, 20, 30, 1200],
    )

    recipes_binarized = binarize_recipes_data_limited_ingredients(
        input_recipes_limited, False
    )
    assert recipes_binarized == input_binarized_limited


def test_binarize_recipes_data_origines(
    input_recipes_origines, input_binarized_origines, mocker
):
    mocker.patch(
        "similarity.extract_all_cuisines", return_value=["Europe", "Afrique", "Asie"]
    )
    mocker.patch(
        "similarity.extract_all_types",
        return_value=["Boisson", "Viande", "Poisson", "Céréales"],
    )

    recipes_binarized = binarize_recipes_data_origines(input_recipes_origines, False)
    assert recipes_binarized == input_binarized_origines


if __name__ == "__main__":
    pytest.main()
