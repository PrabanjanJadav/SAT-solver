"""
Sokoban Solver using SAT (Boilerplate)
--------------------------------------
Instructions:
- Implement encoding of Sokoban into CNF.
- Use PySAT to solve the CNF and extract moves.
- Ensure constraints for player movement, box pushes, and goal conditions.

Grid Encoding:
- 'P' = Player
- 'B' = Box
- 'G' = Goal
- '#' = Wall
- '.' = Empty space
"""

from pysat.formula import CNF
from pysat.solvers import Solver

# Directions for movement
DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


class SokobanEncoder:
    def __init__(self, grid, T):
        """
        Initialize encoder with grid and time limit.

        Args:
            grid (list[list[str]]): Sokoban grid.
            T (int): Max number of steps allowed.
        """
        self.grid = grid
        self.T = T
        self.N = len(grid)
        self.M = len(grid[0])

        self.goals = []
        self.boxes = []
        self.player_start = None

        # TODO: Parse grid to fill self.goals, self.boxes, self.player_start
        self._parse_grid()

        self.max_player_value = (((self.N-1)*(self.N+1)+(self.M-1))*(self.T+1)+(self.T-1))+1
        self.num_boxes = len(self.boxes)
        self.cnf = CNF()

    def _parse_grid(self):
        """Parse grid to find player, boxes, and goals."""
        # TODO: Implement parsing logic
        b=0
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j]=='B':
                    self.boxes.append((b,i,j))
                    b+=1
                elif self.grid[i][j]=='G':
                    self.goals.append((i,j))
                elif self.grid[i][j]=='P':
                    self.player_start = (i,j)

    # ---------------- Variable Encoding ----------------
    def var_player(self, x, y, t):
        """
        Variable ID for player at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        return ((x*(self.N+1)+y)*(self.T+1)+t)+1

    def var_box(self, b, x, y, t):
        """
        Variable ID for box b at (x, y) at time t.
        """
        # TODO: Implement e
        # Encoding scheme
        return (((x*(self.N+1)+y)*(self.T+1)+t)*(self.num_boxes+1)+b)+self.max_player_value+1

    # ---------------- Encoding Logic ----------------
    def encode(self):
        """
        Build CNF constraints for Sokoban:
        - Initial state
        - Valid moves (player + box pushes)
        - Non-overlapping boxes
        - Goal condition at final timestep
        """
        # TODO: Add constraints for:
        # 1. Initial conditions
        # 2. Player movement
        # 3. Box movement (push rules)
        # 4. Non-overlap constraints
        # 5. Goal conditions
        # 6. Other conditions
        self.cnf.append([(self.var_player(self.player_start[0],self.player_start[1],0))])

        for b in self.boxes:
            self.cnf.append([self.var_box(b[0],b[1],b[2],0)])
            atleast_goal=[]
            for p in range(len(self.goals)):
                atleast_goal.append(self.var_box(b[0],self.goals[p][0],self.goals[p][1],self.T))
            self.cnf.append(atleast_goal)


        for i in range(self.N):
            for j in range(self.M):
                
                for k in range(self.T+1):
                    if self.grid[i][j]=='#':
                        self.cnf.append([-self.var_player(i,j,k)])

                    for p in range(len(self.boxes)):
                        self.cnf.append([-self.var_player(i,j,k), -self.var_box(p,i,j,k)])

                        for q in range(p+1,len(self.boxes)):
                            self.cnf.append([-self.var_box(p,i,j,k), -self.var_box(q,i,j,k)])

                        if self.grid[i][j]=='#':
                            self.cnf.append([-self.var_box(p,i,j,k)])

                        if k>=1:
                            if i>0 and i<self.N-1:
                                self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i+1,j,k-1), self.var_box(p,i-1,j,k), -self.var_player(i,j,k)])
                                self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i-1,j,k-1), self.var_box(p,i+1,j,k), -self.var_player(i,j,k)])

                            if j>0 and j<self.M-1:
                                self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i,j+1,k-1), self.var_box(p,i,j-1,k), -self.var_player(i,j,k)])
                                self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i,j-1,k-1), self.var_box(p,i,j+1,k), -self.var_player(i,j,k)])

                            if (i,j)==(0,0) or (i,j)==(0,self.M-1) or (i,j)==(self.N-1,0) or (i,j)==(self.N-1,self.M-1):
                                self.cnf.append([-self.var_box(p,i,j,k-1), self.var_box(p,i,j,k)]) 

                            else:
                                self.cnf.append([-self.var_box(p,i,j,k-1), self.var_box(p,i,j,k), self.var_player(i,j,k)])
                                if i==0:
                                    self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i+1,j,k-1),self.var_box(p,i,j,k), -self.var_player(i,j,k)])
                                if j==0:
                                    self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i,j+1,k-1),self.var_box(p,i,j,k), -self.var_player(i,j,k)])
                                if i==self.N-1:
                                    self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i-1,j,k-1),self.var_box(p,i,j,k), -self.var_player(i,j,k)])
                                if j==self.M-1:
                                    self.cnf.append([-self.var_box(p,i,j,k-1), -self.var_player(i,j-1,k-1),self.var_box(p,i,j,k), -self.var_player(i,j,k)])

                    for p in range(self.N):
                        for q in range(self.M):
                            if (p,q)!=(i,j):
                                self.cnf.append([-self.var_player(i,j,k), -self.var_player(p,q,k)]) 
                            for b in range(len(self.boxes)):
                                if (p,q)!=(i,j):
                                    self.cnf.append([-self.var_box(b,i,j,k), -self.var_box(b,p,q,k)]) 
                    
                    if k>=1:
                        next_mov = [-self.var_player(i,j,k-1), self.var_player(i,j,k)]
                        if i<self.N-1:
                            next_mov.append(self.var_player(i+1,j,k))
                        if i>0:
                            next_mov.append(self.var_player(i-1,j,k))
                        if j>0:
                            next_mov.append(self.var_player(i,j-1,k))
                        if j<self.M-1:
                            next_mov.append(self.var_player(i,j+1,k))
                        self.cnf.append(next_mov)
                
        return self.cnf


def decode(model, encoder):
    """
    Decode SAT model into list of moves ('U', 'D', 'L', 'R').

    Args:
        model (list[int]): Satisfying assignment from SAT solver.
        encoder (SokobanEncoder): Encoder object with grid info.

    Returns:
        list[str]: Sequence of moves.
    """
    N, M, T, max = encoder.N, encoder.M, encoder.T, encoder.max_player_value

    # TODO: Map player positions at each timestep to movement directions
    mov = []
    for m in model:
        if m>=1 and m<=max:
            mov.append(m)
    moves = []
    x = encoder.player_start[0]
    y = encoder.player_start[1]
    for t in range(T+1):
        if x<(N-1):
            if encoder.var_player(x+1,y,t) in mov:
                moves.append('D')
                x=x+1
        if x>0:
            if encoder.var_player(x-1,y,t) in mov:
                moves.append('U')
                x=x-1
        if y>0:
            if encoder.var_player(x,y-1,t) in mov:
                moves.append('L')
                y=y-1
        if y<(M-1):
            if encoder.var_player(x,y+1,t) in mov:
                moves.append('R')
                y=y+1
    
    return moves


def solve_sokoban(grid, T):
    """
    DO NOT MODIFY THIS FUNCTION.

    Solve Sokoban using SAT encoding.

    Args:
        grid (list[list[str]]): Sokoban grid.
        T (int): Max number of steps allowed.

    Returns:
        list[str] or "unsat": Move sequence or unsatisfiable.
    """
    encoder = SokobanEncoder(grid, T)
    cnf = encoder.encode()

    with Solver(name='g3') as solver:
        solver.append_formula(cnf)
        if not solver.solve():
            return -1

        model = solver.get_model()
        if not model:
            return -1

        return decode(model, encoder)


