"""
Based on the algorithm for generating random functions from the paper:
"Deep Learning for Symbolic Mathematics"
by Guillaume Lample and François Charton
https://arxiv.org/abs/1912.01412

"""

import random
from dataclasses import dataclass
from functools import cache
from typing import Optional

import numpy as np
import sympy as sp

from settings import INTEGRATION_VARIABLE_NAME

UNARY_OPERATORS = [
    "log",
    "exp",
    "sin",
    "cos",
    "tan",
    "sqrt",
    "asin",
    "acos",
    "atan",
]
BINARY_OPERATORS = ["+", "-", "*", "/", "**"]


@dataclass
class Node:
    value: Optional[str] = None
    children: Optional[list["Node"]] = None

    def is_leaf(self):
        return self.children is None

    def is_unary(self):
        return self.children is not None and len(self.children) == 1

    def is_binary(self):
        return self.children is not None and len(self.children) == 2

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        elif self.is_unary():
            return f"{self.value}({self.children[0].as_function()})"
        elif self.is_binary():
            return (
                f"({self.children[0].as_function()}) "
                f"{self.value} ({self.children[1].as_function()})"
            )
        else:
            raise ValueError("Invalid node type")

    def as_function(self):
        return sp.sympify(str(self))

    def as_simplified_function(self):
        return sp.simplify(self.as_function())


def get_unary_operator():
    return UNARY_OPERATORS[random.randint(0, len(UNARY_OPERATORS) - 1)]


def get_binary_operator():
    return BINARY_OPERATORS[random.randint(0, len(BINARY_OPERATORS) - 1)]


def get_number():
    rand = random.random()
    return int(-np.log(rand) + 1)


def get_number_or_variable():
    if random.random() < 0.5:
        return get_number()
    else:
        return INTEGRATION_VARIABLE_NAME


@cache
def number_of_subtrees(empty_nodes: int, internal_nodes: int) -> int:
    # In the literature, D(e,n) where
    # e is the number of empty nodes
    # n is the number of internal nodes
    if empty_nodes < 0 or internal_nodes < 0:
        raise ValueError("Empty nodes and internal nodes must be non-negative")
    if empty_nodes == 0:
        return 0
    if internal_nodes == 0:
        return 1
    return (
        number_of_subtrees(empty_nodes - 1, internal_nodes)
        + number_of_subtrees(empty_nodes, internal_nodes - 1)
        + number_of_subtrees(empty_nodes + 1, internal_nodes - 1)
    )


def probability_of_next_internal_node(
    empty_nodes: int,
    internal_nodes: int,
    position: int,
    arity: int,
) -> float:
    # In the literature, P(L(e,n)=(k,a)) where
    # e is the number of empty nodes
    # n is the number of internal nodes
    # k is the position of the next internal node (zero-indexed)
    # a is the arity of the next internal node
    #     (1 for unary, 2 for binary)
    if arity not in [1, 2]:
        raise ValueError("Arity must be 1 or 2")
    if arity == 1:
        return number_of_subtrees(
            empty_nodes - position, internal_nodes - 1
        ) / number_of_subtrees(empty_nodes, internal_nodes)
    else:
        return number_of_subtrees(
            empty_nodes - position + 1, internal_nodes - 1
        ) / number_of_subtrees(empty_nodes, internal_nodes)


def sample_position_and_arity(
    num_empty_nodes: int, num_internal_nodes: int
) -> tuple:
    positions = np.repeat(np.arange(num_empty_nodes), 2)
    arities = np.tile(np.array([1, 2]), num_empty_nodes)
    probabilities = np.array(
        [
            probability_of_next_internal_node(
                num_empty_nodes,
                num_internal_nodes,
                position,
                arity,
            )
            for position, arity in zip(positions, arities)
        ]
    )
    index = np.random.choice(
        len(probabilities),
        p=probabilities / probabilities.sum(),
    )
    return positions[index], arities[index]


def generate_unary_binary_tree(num_internal_nodes: int):
    top_node = Node()
    empty_nodes = [top_node]
    for node in range(num_internal_nodes):
        remaining_nodes = num_internal_nodes - node
        position, arity = sample_position_and_arity(
            len(empty_nodes), remaining_nodes
        )
        if arity == 1:
            new_node = Node()
            empty_nodes[position].children = [new_node]
            empty_nodes = empty_nodes[position + 1 :] + [new_node]
        else:
            new_nodes = [Node(), Node()]
            empty_nodes[position].children = new_nodes
            empty_nodes = empty_nodes[position + 1 :] + new_nodes
    return top_node


def populate_tree(node: Node):
    if node.is_leaf():
        node.value = get_number_or_variable()
    elif node.is_unary():
        node.value = get_unary_operator()
        populate_tree(node.children[0])
    elif node.is_binary():
        node.value = get_binary_operator()
        populate_tree(node.children[0])
        populate_tree(node.children[1])


def get_function_string(num_internal_nodes: int):
    tree = generate_unary_binary_tree(num_internal_nodes)
    populate_tree(tree)
    return str(tree.as_simplified_function())
