import numpy as np
import pandas as pd
from typing import Iterable


def generate_uniform_values(
    n_values: int,
    rng: np.random._generator.Generator,
    variation_percent: float = 0.2,
    scale: float = 1,
):
    """Generate `n_items` values from a uniform distribution and scales them to the range:
    `base` to `base` (1 + `variation_percent`).

    Args:
        n_values (int): number of values.
        rng (np.random._generator.Generator): random generator.
        variation_percent (float): the percent increase from the
            minimum value to the maximum value.
            E.g.: if the minimum value is 1 and the maximum value
            desired is 1.2, then variation_percent = 0.2.
        scale (float): minimum value.
        
    Returns:
        (np.array): of shape (n_values,) in the range described above.
    """
    values = rng.uniform(0, 100, (n_values,))
    min_value, max_value = min(values), max(values)
    return scale * (
        1 + variation_percent / (max_value - min_value) * (values - min_value)
    )

def generate_item_sizes(
    items: tuple,
    rng: np.random._generator.Generator,
    variation_percent: float = 0.2,
):
    """Randomly generates the item sizes from a uniform distribution
    as pd.DataFrame with cols `item` and `size`.

    Args:
        items (tuple): sorted tuple of all items considered.
        rng (np.random._generator.Generator): random generator.
        variation_percent (float): the percent increase from the
            minimum size to the maximum size.
            E.g.: if the minimum size is 1 and the maximum size
            desired is 1.2, then variation_percent = 0.2.
            NOTE: recall that the scale of the size is irrelevant,
            and thus we always set the minimum at 1.

    Returns:
        (pd.DataFrame): with cols `item` (int) and `size` (float)
    """
    sizes = generate_uniform_values(n_values=len(items), rng=rng, variation_percent=variation_percent)
    return pd.DataFrame({'item': items, 'size': sizes})

def generate_item_objectives(
    items: tuple,
    rng: np.random._generator.Generator,
    scale: float = 1000,
    variation_percent: float = 1,
):
    """Randomly generates the item sizes from a uniform distribution
    as pd.DataFrame with cols `item` and `size`.

    Args:
        items (tuple): sorted tuple of all items considered.
        rng (np.random._generator.Generator): random generator.
        scale (float): minimum objective.
        variation_percent (float): the percent increase from the
            minimum objective to the maximum objective.
            E.g.: if the minimum objective is 1 and the maximum objective
            desired is 1.2, then variation_percent = 0.2.

    Returns:
        (pd.DataFrame): with cols `item` (int), `objective` (float)
    """
    objective = generate_uniform_values(
        n_values=len(items),
        rng=rng,
        scale=scale,
        variation_percent=variation_percent)
    return pd.DataFrame({'item': items, 'objective': objective})

def generate_transfer_matrix(
    n_items: int,
    rng: np.random._generator.Generator,
    mean_loss: float = 0.15,
    std_loss: float = 0.03
 
):
    """Computes the transfer matrix T whose entry T[i][j]
    represents the demand that goes from the i-th item to the
    j-th item whenever the former is absent and the later is
    present.

    Each row contains 0 in the diagonal entry indicating that
    in the absence of an item, there is no transfer to that item.

    Each row adds up to a value between 0 and 1, indicating that
    there is loss in the demand in the absence of that item.
    
    Args:
        n_items (int): number of all items considered.
        rng (np.random._generator.Generator): random generator.
        mean_loss (float): average loss percent in the range 0 and 1.
            Default to 0.15
        std_loss (float): standard deviation of the loss, poportional
            to the average, also in the range 0 and 1. Default to 0.03.
 
    Returns:
        (np.array) of shape (len(items), len(items))
    """
    transfer_matrix = np.random.random((n_items, n_items))
    losses = np.random.normal(mean_loss, std_loss, (n_items,))
    for index, row in enumerate(transfer_matrix):
        row[index] = 0
        row /= sum(row)
        row *= 1 - losses[index] 
    return transfer_matrix

def compute_selection_objective(
    items: Iterable,
    all_items: tuple, 
    item_sizes: pd.DataFrame,
    initial_objectives: pd.DataFrame,
    transfer_matrix: np.array
) -> tuple:
    """Computes the total objective value of the selection in `items`
    from items in `item_sizes`, and the individual objective values for
    each item in the selection.

    NOTE: this is what differentiates this from the Knapsack problem
    because the objective is not linear on the items, but it also depends
    on the set of items selected, which compite among each other.

    Args:
        items (Iterable): items selected.
        item_sizes (pd.DataFrame): with cols `item` and `size`.
        initial_objectives (pd.DataFrame): the objectives of each item.
        transfer_matrix (np.array): of size (len(item_sizes), len(item_sizes))

    Returns:
        (pd.DataFrame): with cols `item` (int) and `objective`.
    """
    if len(items) == 0:
        return pd.DataFrame({'item': all_items}).assign(objective=0)


    objectives = {item: 0 for item in all_items}
    print(objectives)
    transfering = np.zeros((len(all_items),))
    for index, row in initial_objectives.iterrows():
        if row['item'] in items:
            objectives[row['item']] += row['objective']
        else:
            transfering += transfer_matrix[index,:] * row['objective']
        
    for index, row in initial_objectives.iterrows():
        if row['item'] in items:
            objectives[row['item']] += transfering[index]

    return pd.DataFrame(objectives.items(), columns=['item', 'objective'])

