"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""

    # TODO: implement encoding and solving using PySAT
    cnf = CNF()

    index_map = {}
    value_index = {}

    for i in range(9):
        for j in range(9):
            for n in range(1,10):
                map = i*100 + j*10 + n
                index_map[f"{i}{j}{n}"] = map
                value_index[map] = f"{i}{j}{n}"
    
    for i in range(9):
        for n in range(1,10):
            row_fill = []
            for j in range(9):
                row_fill.append(index_map[f"{i}{j}{n}"])
            cnf.append(row_fill)

    for j in range(9):
        for n in range(1,10):
            column_fill = []
            for i in range(9):
                column_fill.append(index_map[f"{i}{j}{n}"])
            cnf.append(column_fill)

    for k in range(3):
        for l in range(3):
            for n in range(1,10):
                box_fill = []
                for i in range(3):
                    for j in range(3):
                            box_fill.append(index_map[f"{i+3*k}{j+3*l}{n}"])
                cnf.append(box_fill)
    
    for i in range(9):
        for j in range(9):
            n = grid[i][j]
            if n>=1 and n<=9:
                cnf.append([index_map[f"{i}{j}{n}"]])
    
    for i in range(9):
        for j in range(9):
            # atleast_one = []
            for n1 in range(1,10):
                # atleast_one.append(index_map[f"{i}{j}{n1}"])
                for n2 in range(n1+1,10):
                    atmost_one = []
                    atmost_one.append(-(index_map[f"{i}{j}{n1}"]))
                    atmost_one.append(-(index_map[f"{i}{j}{n2}"]))
                    cnf.append(atmost_one)
            # cnf.append(atleast_one)
        
    answer = [[0] * 9 for _ in range(9)]
    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        if solver.solve():
            model = solver.get_model()
        else:
            return [[]]
    
    for map in model:
        if map>0:
            value = value_index[map]
            n = int(value[2])
            j = int(value[1])
            i = int(value[0])
        
            answer[i][j] = n
    
    return answer