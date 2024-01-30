import pandas as pd


def compute_selection_size(selection: tuple, item_sizes: pd.DataFrame) -> float:
    """Computes the sum of the sizes of the item in the selection.

    Args:
        selection (tuplep[int]): items in the selection.
        item_sizes (pd.DataFrame): with cols `item` (int) and `size` (float)

    Returns:
        (float): sum of the sizes of the items in the selection.
    """
    return (item_sizes[item_sizes["item"].isin(selection)]["size"].sum(),)


def compute_fitness_increase(
    this_objective: float,
    prev_objective: float,
    this_size: float,
    prev_size: float,
    fitness_type: str,
):
    """Computes the increase in objective or the ration of increase in objective per unit
    of increase in size.

    Args:
        this_objective (float): current selection objective.
        prev_objective (float): objective of the source selection.
        this_size (float): current selection size.
        prev_size (float): size of the source selection.
        fitness_type (str): either `objective` or `objective_per_size`. Default to later.

    Returns:
        (float): increase in fitness.

    Raises:
        (ValueError): if fitness_type is neither `objective` or `objective_per_size`.
        (ValueError): if this_size <= prev_size.
    """
    if fitness_type not in ["objective", "objective_per_size"]:
        raise ValueError(
            "fitness_type must be either `objective` or `objective_per_size`, "
            f"{fitness_type} is not allowed."
        )

    objective_increase = this_objective - prev_objective
    if fitness_type == "objective" or objective_increase == 0:
        return objective_increase

    size_increase = this_size - prev_size

    if size_increase <= 0:
        raise ValueError(
            f"this_size: {this_size} <= prev_size: {prev_size}, please check the computations"
        )

    return objective_increase / size_increase


def forward_greedy_selection(
    all_items: tuple,
    item_sizes: pd.DataFrame,
    capacity: float,
    compute_total_objective,
    base_selection: tuple = None,
    fitness: str = "objective_per_size",
):
    """Selects items based one at a time based on which one improved the fitness
    the most with respect to the current selection.

    Args:
        all_items (tuple): list of all items to consider.
        item_sizes (pd.DataFrame): with cols `item` (int) and `size` (float).
        capacity (float): maximum total selection size supported.
        compute_total_objective (function): takes a selection of items `tuple[int]`
            and returns a the total objective of the selection `float`.
        base_selection (tuple): custom initial selection. Default to None, which is
            interpreted as the empty selection.
        fitness (str): either `objective` or `objective_per_size`. Default to later.

    Returns:
        (tuple[tuple[int], pd.DataFrame]): the best selection based on the fitness used,
            and a frame with all the attempted solutions with cols:
                - `selection`: tuple[int]
                - `from`: tuple[int]
                - `size`: float
                - `objective`: float
                - `fitness` float

    Raises:
        (ValueError): if fitness is not `objective` or `objective_per_size`.
    """
    if fitness not in ["objective", "objective_per_size"]:
        raise ValueError(
            "fitness must be either `objective` or `objective_per_size`, "
            f"{fitness} is not allowed."
        )

    # Sets up the initial custom selection.
    if base_selection is None:
        base_selection = tuple()

    curr_selection = base_selection

    # Defines the history data for every selection attempted and saves it into a dictionary.
    history = {
        curr_selection: {
            "selection": curr_selection,
            "from": None,
            "size": compute_selection_size(curr_selection, item_sizes),
            "objective": compute_total_objective(curr_selection),
        }
    }

    history[curr_selection]["fitness"] = compute_fitness_increase(
        history[curr_selection]["objective"],
        0,
        history[curr_selection]["size"],
        0,
        fitness,
    )

    # Define the loop to keep increasing the selection until the capacity is filled.
    while history[curr_selection]["size"] <= capacity:

        # Computes all feasible selections with one more item.
        feasible_selections = {}
        for item in all_items:
            if item not in curr_selection:
                attempted_selection = tuple(sorted(list(curr_selection) + [item]))
                attempted_size = compute_selection_size(attempted_selection, item_sizes)
                if attempted_size <= capacity and attempted_selection not in history:
                    feasible_selections[attempted_selection] = attempted_size

        # Early exit if there are no new feasible selections.
        if len(feasible_selections) == 0:
            break

        # Placeholder.
        max_fitness = 0

        # Searches for best feastible new selection.
        for selection in feasible_selections:

            # Fill in the history of attempts.
            history[selection] = {
                "selection": selection,
                "from": curr_selection,
                "size": feasible_selections[selection],
                "objective": compute_total_objective(selection),
            }

            history[selection]["fitness"] = compute_fitness_increase(
                history[selection]["objective"],
                history[curr_selection]["objective"],
                history[selection]["size"],
                history[curr_selection]["size"],
                fitness,
            )

            # Updates the max selection for this iteration.
            if max_fitness < history[selection]["fitness"]:
                max_selection = selection

        curr_selection = max_selection

    return curr_selection, pd.DataFrame(history).T.reset_index(drop=True)
