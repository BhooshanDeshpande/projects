# astar.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Clemson University and the authors.
#
# Author: Ioannis Karamouzas (ioannis@g.clemson.edu)
#


# Compute the optimal path from start to goal.
# The car is moving on a 2D grid and its orientation can be chosen from four different directions:
forward = [[-1, 0],  # 0: go north
           [0, -1],  # 1: go west
           [1, 0],  # 2: go south
           [0, 1]]  # 3: go east

# The car can perform 3 actions: -1: right turn and then move forward, 0: move forward, 1: left turn and then move
# forward
action = [-1, 0, 1]
action_name = ['R', 'F', 'L']
cost = [1, 1, 10]  # corresponding cost values

# GRID: 0 = navigable space, 1 = unnavigable space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
init = (4, 3, 0)  # (grid row, grid col, orientation)
goal = (2, 0, 1)  # (grid row, grid col, orientation)
heuristic = [[2, 3, 4, 5, 6, 7],  # Manhattan distance
             [1, 2, 3, 4, 5, 6],
             [0, 1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5, 6],
             [2, 3, 4, 5, 6, 7]]

from utils import (Value, OrderedSet, PriorityQueue)


# ----------------------------------------
# modify the code below
# ----------------------------------------
def get_orientation(parent_node, child_node):
    orientation = [child_node[0] - parent_node[0], child_node[1] - parent_node[1]]
    if orientation == forward[0]:
        return 0
    elif orientation == forward[1]:
        return 1
    elif orientation == forward[2]:
        return 2
    else:
        return 3


def find_children(grid, parent_node):
    child1 = (parent_node[0], parent_node[1] - 1, 0)
    child2 = (parent_node[0] - 1, parent_node[1], 0)
    child3 = (parent_node[0], parent_node[1] + 1, 0)
    child4 = (parent_node[0] + 1, parent_node[1], 0)
    children = [child1, child2, child3, child4]
    feasible_children = []
    for child in children:
        grid_x = int(child[0])
        grid_y = int(child[1])
        if 0 <= grid_x < 5 and 0 <= grid_y < 6:  # FILTER 1
            if grid[grid_x][grid_y] == 0:  # FILTER 2
                grid_orientation = int(get_orientation(parent_node, child))
                child = [grid_x, grid_y, grid_orientation]
                if get_action(parent_node, child) != 2 and get_action(parent_node, child) != -2:  # FILTER 3
                    feasible_children.append((grid_x, grid_y, grid_orientation))
        else:
            pass
    return feasible_children


def get_action(current_node, child_node):
    action = child_node[2] - current_node[2]
    if action == 3:
        return -1
    elif action == -3:
        return 1
    else:
        return action


def compute_path(grid, start, goal, cost, heuristic):
    closed_set = OrderedSet()
    open_set = PriorityQueue(order=min, f=lambda v: v.f)
    parent = [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
              [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
              [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
              [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]
    path = [['-' for row in range(len(grid[0]))] for col in range(len(grid))]
    x = start[0]
    y = start[1]
    theta = start[2]
    h = heuristic[x][y]
    g = 0
    f = g + h
    open_set.put(start, Value(f=f, g=g))
    cost_history = [[[float('inf') for row in range(len(grid[0]))] for col in range(len(grid))],
                    [[float('inf') for row in range(len(grid[0]))] for col in range(len(grid))],
                    [[float('inf') for row in range(len(grid[0]))] for col in range(len(grid))],
                    [[float('inf') for row in range(len(grid[0]))] for col in range(len(grid))]]
    # your code: implement A*
    while open_set:
        current_node, current_value = open_set.pop()
        p = current_node[0];
        q = current_node[1];
        r = current_node[2]
        if current_node == goal:
            print('\ngoal reached! \npath : ')
            closed_set.add(current_node)
            while current_node != start:
                last_node = current_node
                parent_node = parent[last_node[2]][last_node[0]][last_node[1]]
                action_taken = get_action(parent_node, last_node)
                path[goal[0]][goal[1]] = '*'
                path[parent_node[0]][parent_node[1]] = action_name[action_taken + 1]
                current_node = parent_node
            return path, closed_set
        closed_set.add(current_node)
        children = find_children(grid, current_node)
        for child in children:
            k = child[0];
            l = child[1];
            m = child[2]
            action = get_action(current_node, child)
            g = current_value.g + 1
            f = heuristic[k][l] + g + cost[action + 1]
            if child not in open_set or closed_set:
                open_set.put(child, Value(f=f, g=g))
            elif child in open_set:
                f_prev = open_set.get(child)
                if f < f_prev.f:
                    open_set.put(child, Value(f=f, g=g))
            if cost_history[m][k][l] <= f:
                pass
            else:
                parent[m][k][l] = p, q, r
                cost_history[m][k][l] = f
    return path, closed_set


if __name__ == "__main__":
    path, closed = compute_path(grid, init, goal, cost, heuristic)
    for i in range(len(path)):
        print(path[i])
    print("\nExpanded Nodes:")
    for node in closed:
        print(node)

"""
To test the correctness of your A* implementation, when using cost = [1, 1, 10] your code should return 

['-', '-', '-', 'R', 'F', 'R']
['-', '-', '-', 'F', '-', 'F']
['*', 'F', 'F', 'F', 'F', 'R']
['-', '-', '-', 'F', '-', '-']
['-', '-', '-', 'F', '-', '-'] 

In this case, the elements in your closed set (i.e. the expanded nodes) are: 
(4, 3, 0)
(3, 3, 0)
(2, 3, 0)
(2, 4, 3)
(1, 3, 0)      
(2, 5, 3)
(0, 3, 0)
(0, 4, 3)
(0, 5, 3)
(1, 5, 2)
(2, 5, 2)
(2, 4, 1)
(2, 3, 1)
(2, 2, 1)
(2, 1, 1)
(2, 0, 1)

"""
"""
Two data structures are provided for your open and closed lists: 

 1. OrderedSet is an ordered collection of unique elements.
 2. PriorityQueue is a key-value container whose `pop()` method always pops out
    the element whose value has the highest priority.

 Common operations of OrderedSet, and PriorityQueue
   len(s): number of elements in the container s
   x in s: test x for membership in s
   x not in s: text x for non-membership in s
   s.clear(): clear s
   s.remove(x): remove the element x from the set s;
                nothing will be done if x is not in s

 Unique operations of OrderedSet:
   s.add(x): add the element x into the set s
   s.pop(): return and remove the LAST added element in s;

 Example:
   s = Set()
   s.add((0,1,2))    # add a triplet into the set
   s.remove((0,1,2)) # remove the element (0,1,2) from the set
   x = s.pop()

 Unique operations of PriorityQueue:
   PriorityQueue(order="min", f=lambda v: v): build up a priority queue
       using the function f to compute the priority based on the value
       of an element
   s.put(x, v): add the element x with value v into the queue
                update the value of x if x is already in the queue
   s.get(x): get the value of the element x
            raise KeyError if x is not in s
   s.pop(): return and remove the element with highest priority in s;
            raise IndexError if s is empty
            if order is "min", the element with minimum f(v) will be popped;
            if order is "max", the element with maximum f(v) will be popped.
 Example:
   s = PriorityQueue(order="min", f=lambda v: v.f)
   s.put((1,1,1), Value(f=2,g=1))
   s.put((2,2,2), Value(f=5,g=2))
   x, v = s.pop()  # the element with minimum value of v.f will be popped
"""
