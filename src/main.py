from gpt3_api import execute
from random import shuffle, choice
from collections import deque
import re

def format_node_name(node):
    return node  # no op for now, but we might want to try named nodes


def format_solution(solution):
    if not solution or solution == no_path_reason:
        return no_path_reason
    return ','.join(str(n) for n in solution)


def other(edge, fr):
    if edge[0] == fr:
        return edge[1]
    else:
        return edge[0]


no_path_reason = 'There is no path.'


class RandomGraph:
    def __init__(self, node_count, edge_count):
        assert (node_count < 100)
        assert (edge_count < node_count * (node_count - 1) / 2)
        edges = [(a, b) for a in range(1, node_count + 1) for b in range(1, node_count + 1) if a < b]
        shuffle(edges)

        self.nodes = list(range(1, node_count + 1))
        self.edges = edges[:edge_count]
        self.neighbors_of_node = {
            node: [other(edge, node) for edge in self.edges if node in edge] for node in self.nodes
        }
        self.from_location = choice(self.nodes)
        self.to_location = choice([node for node in self.nodes if node != self.from_location])
        self.solution = self.solve()
        self.raw_gpt_answer = self.gpt_solve()['choices'][0]['text']
        self.gpt3_solution = self.extract_gpt_answer(self.raw_gpt_answer)

    def extract_gpt_answer(self, answer):
        stripped = answer.strip()
        if stripped == no_path_reason:
            return None
        numbers = [int(s) for s in re.findall(r'(\d+)', answer)]
        return numbers

    def gpt_solve(self):
        return execute(self.to_gpt3_string(), max_tokens=1000)

    def solve(self):
        q = deque([(self.from_location, [])])
        seen = set()
        while len(q):
            (top, path) = q.popleft()
            if top in seen:
                continue
            seen.add(top)
            if top == self.to_location:
                return [format_node_name(n) for n in path + [top]]
            for n in self.neighbors_of_node[top]:
                q.append((n, path + [top]))

        return None

    def grade_gpt_answer(self):
        if not self.gpt3_solution:
            if not self.solution:
                return (True, "There was no solution and GPT-3 correctly figured it out!")
            return (False, "There was a solution but GPT-3 thought there wasn't one")

        if not len(self.gpt3_solution):
            return (False, "GPT-3 returned an answer we couldn't parse.")

        gpt_solution = self.gpt3_solution[:]
        cur = self.from_location
        is_correct_length = self.solution and len(gpt_solution) == len(self.solution)
        bad_edges = []
        for node in gpt_solution[1:]:
            if node not in self.neighbors_of_node[cur]:
                bad_edges.append((cur, node))

            cur = node

        if not self.solution:
            return (False,
                    f"There was no solution but GPT-3 found one. Their solution was {len(gpt_solution)} nodes and included the following {len(bad_edges)} incorrect edges: {'|'.join((str(be) for be in bad_edges))}")
        if gpt_solution[0] != self.from_location:
            return (
                False,
                f"GPT-3's solution started with the wrong node: {gpt_solution[0]} instead of {self.from_location}")
        if len(bad_edges):
            return (False, "GPT-3 tried to used some edges that don't exist. They are: " + '|'.join(
                (str(be) for be in bad_edges)))
        if cur != self.to_location:
            return (False, f"GPT-3 ended up in the wrong place! ({cur} instead of {self.to_location})")

        if is_correct_length:
            return (True, f"GPT-3 got the optimal solution of {len(gpt_solution)} steps!")

        return (True,
                f"GPT-3 found a solution -- though it took {len(gpt_solution)} steps instead of the optimal {len(self.solution)} steps")

    def to_gpt3_string(self):
        newline = '\n'
        return f'''
You are solving a graph problem where you need to find a path in the graph.
The graph has {len(self.nodes)} nodes, numbered from 1 to {len(self.nodes)}.
        
The graph has {len(self.edges) * 2} bidirectional edges. Here they are:
{newline.join(f'An edge from node {format_node_name(edge[0])} to {format_node_name(edge[1])}' for edge in self.edges)}
{newline.join(f'An edge from node {format_node_name(edge[1])} to {format_node_name(edge[0])}' for edge in self.edges)}
        
You are currently on node {format_node_name(self.from_location)}. 
You would like to find the optimal path to node {format_node_name(self.to_location)}.
        
Output the list of nodes you visit on this path in order, separated by commas. If there is no path, instead print "{no_path_reason}" 

Your solution should start with node {format_node_name(self.from_location)} and end with node {format_node_name(self.to_location)}. 

Do not include any extra text.
            
            '''


if __name__ == '__main__':
    graph = RandomGraph(6, 8)

    print(graph.to_gpt3_string())

    print("correct answer: ", graph.solution)

    print("gpt answer: ", graph.raw_gpt_answer)

    print(graph.grade_gpt_answer())
