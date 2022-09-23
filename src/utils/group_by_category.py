'''
This helps us read a data file and format a given set of edges so the graph can be displated by https://csacademy.com/app/graph_editor/
'''

import json

FOUND_BEST_PATH = 'Found the optimal path'
FOUND_INEFFICIENT_PATH = 'Found a (non-optimal) path'
CORRECTLY_REPORTED_NO_PATH_EXISTS = 'Correctly reported no path exists'
FOUND_A_SOLUTION_WHEN_NONE_EXISTED = 'Found a solution when none existed'
ENDED_ON_WRONG_NODE = 'Ended on wrong node'
USED_EDGES_THAT_DONT_EXIST = 'Used edges that don\'t exist'
STARTED_WITH_THE_WRONG_NODE = 'Started with the wrong node'
INCORRECTLY_NO_PATH_EXISTS = 'Incorrectly reported no path exists'

if __name__ == '__main__':
    with open('data-82069690-2f52-4d35-b39a-f121af2ac8aa.json', 'r') as f:
        data = json.load(f)
    id = '067c9038-c6a4-4c7c-b626-1a27ffd6ffd0'

    by_category = {
        FOUND_BEST_PATH: 0,
        FOUND_INEFFICIENT_PATH: 0,
        CORRECTLY_REPORTED_NO_PATH_EXISTS: 0,
        FOUND_A_SOLUTION_WHEN_NONE_EXISTED: 0,
        ENDED_ON_WRONG_NODE: 0,
        USED_EDGES_THAT_DONT_EXIST: 0,
        STARTED_WITH_THE_WRONG_NODE: 0,
        INCORRECTLY_NO_PATH_EXISTS: 0
    }

    by_optimal_path_length = {
        2: (0, 0),
        3: (0, 0),
        4: (0, 0),
        5: (0, 0),
        6: (0, 0),
        7: (0, 0)
    }

    for entry in data:
        if entry["grade"][0] and "GPT-3 got the optimal solution" in entry["grade"][1]:
            by_category[FOUND_BEST_PATH] += 1
        elif entry["grade"][0] and "instead of the optimal" in entry["grade"][1]:
            by_category[FOUND_INEFFICIENT_PATH] += 1
        elif entry["grade"][0]:
            by_category[CORRECTLY_REPORTED_NO_PATH_EXISTS] += 1
        elif "There was no solution but GPT-3 found one" in entry["grade"][1]:
            by_category[FOUND_A_SOLUTION_WHEN_NONE_EXISTED] += 1
        elif "GPT-3's solution started with the wrong node" in entry["grade"][1]:
            by_category[STARTED_WITH_THE_WRONG_NODE] += 1
        elif "GPT-3 tried to used some edges that don't exist" in entry["grade"][1]:
            by_category[USED_EDGES_THAT_DONT_EXIST] += 1
        elif "GPT-3 ended up in the wrong place" in entry["grade"][1]:
            by_category[ENDED_ON_WRONG_NODE] += 1
        elif "There was a solution but GPT-3 thought there wasn't one" in entry["grade"][1]:
            by_category[INCORRECTLY_NO_PATH_EXISTS] += 1

        if entry["solution"]:
            (correct, total) = by_optimal_path_length[len(entry["solution"])]
            next_score = (correct + 1, total + 1) if entry["grade"][0] else (correct, total + 1)
            by_optimal_path_length[len(entry["solution"])] = next_score

    for (cat, count) in by_category.items():
        print(f"{cat}\t{count}")
    print("Total: ", sum(by_category.values()))

    for (path_len, (correct, total)) in by_optimal_path_length.items():
        print(f"{path_len}\t{correct / total}")
