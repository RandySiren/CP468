from collections import deque
# heap queue for A* algorithm
import heapq
# deque = double ended queue, used to represent stacks and queues with O(1) insert/remove operations on both ends
from queue import PriorityQueue
# Priority Queue for best first search

class Node():
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
      return self.f < other.f

    def __gt__(self, other):
      return self.f > other.f

def main():
    maze, start, goal = read_maze("maze.txt")
    print("Maze Before search:")
    displayMaze(maze)
    # breadth first search
    # goal, exp, parentMap, path = bfs(maze, start)

    # depth first search
    # goal, exp, parentMap, path = dfs(maze, start)

    # best first search
    # goal, exp, parentMap, path = best_first_search(maze, start, goal)

    # A*
    path, exp = Astar(maze, start, goal)
    # Location of the goal, total nodes expanded, and parent map of graph vertices
    cost = len(path)-1
    print("\nSearch finished\n")
    print("Cost:", cost)
    print("Exp:", exp)
    print("Path:", path)
    # Displaying maze again will show which locations on the grid the search visited
    print("\nNew Maze After Search:")
    displayMaze(maze)


def read_maze(filename):
    fv = open("maze.txt", "r")
    line = fv.readline()
    # row - current row of text file, startP - location of "P", goal - location of "."
    row = 0
    startP = (0, 0)
    goal = (0, 0)
    maze = []
    while line != '':
        maze.append([])
        for c, char in enumerate(line):
            if char.lower() == "p":
                startP = (row, c)
            elif char == ".":
                goal = (row, c)
            if char in "% .P":
                maze[row].append(char)
        line = fv.readline()
        row += 1
    return maze, startP, goal


def adj(maze, parentMap, loc):
    # Helper function for returning adjacent locations in the maze
    row, col = loc
    adj_p = []
    for offx, offy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nRow = row + offx
        nCol = col + offy
        # Make sure we don't go out of bounds
        if nRow >= 0 and nRow < len(maze) and nCol >= 0 and nCol < len(maze[0]):
            # If we have not already visited this location
            if (nRow, nCol) not in parentMap:
                adj_p.append((nRow, nCol))
                parentMap[(nRow, nCol)] = (row, col)
    return adj_p

def manhattan(start, goal):
    # Heuristic function
    return abs(start[0] - goal[0]) + abs(start[1]-goal[1])


def getPath(maze, pMap, start, goal):
    # Helper function to get the path in order after finding the goal in the maze
    curr = goal
    path = []
    while curr != None:
        if curr != start:
            maze[curr[0]][curr[1]] = '.'
        path.insert(0, curr)
        curr = pMap[curr]
    return path


def return_path(current_node, maze):
    path = []
    current = current_node
    while current is not None:
        maze[current.pos[0]][current.pos[1]] = '.'
        path.append(current.pos)
        current = current.parent
    return path[::-1]

def best_first_search(maze, start, goal):
    pq = PriorityQueue(100)
    parentMap = {}
    row, col = start
    parentMap[start] = None
    exp = 1
    pq.put((0, start))
    while not pq.empty():
        weight, location = pq.get()
        adj_p = adj(maze, parentMap, location)
        for nRow, nCol in adj_p:
           # If we found our goal
            if maze[nRow][nCol] == '.':
                path = getPath(maze, parentMap, start, (nRow, nCol))
                # Return the goal, total nodes expanded, and map of parent nodes to extract path
                return (nRow, nCol), exp, parentMap, path
            elif maze[nRow][nCol] == ' ':
                pq.put((manhattan((nRow, nCol), goal), (nRow, nCol)))
                exp += 1
    return(-1, -1), -1, -1


def dfs(maze, start):  # Iterative depth first search using a stack
    stack = deque()
    exp = 1
    # Total nodes expanded starts at 1
    row, col = start
    # Position of "P"
    # Dictionary to check if we have already visited a location
    parentMap = {}
    # Dictionary storing parents of every child node we visit
    parentMap[start] = None
    stack.append(start)
    while len(stack) > 0:
        loc = stack.pop()
        adj_p = adj(maze, parentMap, loc)
        for nRow, nCol in adj_p:
            # Adjacent locations in grid to check
            if maze[nRow][nCol] == '.':
                # Return the goal, total nodes expanded, and map of parent nodes to extract path
                path = getPath(maze, parentMap, start, (nRow, nCol))
                return (nRow, nCol), exp, parentMap, path
            elif maze[nRow][nCol] == ' ':
                stack.append((nRow, nCol))
                exp += 1
    # This line will only be reached in error, such as there being no goal
    return(-1, -1), -1, -1


def bfs(maze, start):  # Iterative breadth first search using a queue
    q = deque()
    exp = 1
    # Total nodes expanded starts at 1
    row, col = start
    # Position of "P"
    parentMap = {}
    # Dictionary storing parents of every child node we visit
    parentMap[start] = None
    q.append(start)
    while len(q) > 0:
        loc = q.popleft()
        adj_p = adj(maze, parentMap, loc)
        # Adjacent locations in grid to check
        for nRow, nCol in adj_p:
            if maze[nRow][nCol] == '.':
                path = getPath(maze, parentMap, start, (nRow, nCol))
                # Return the goal, total nodes expanded, and map of parent nodes to extract path
                return (nRow, nCol), exp, parentMap, path
            elif maze[nRow][nCol] == ' ':
                q.append((nRow, nCol))
                exp += 1
    return(-1, -1), -1, -1  # Error


def Astar(maze, start, end):
    # Create start and end nodes
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize lists
    open_list = []
    closed_list = []

    exp = 1

    # Generate heap and push start
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # while open_list heap is not empty
    while len(open_list) > 0:

        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Reached end
        if current_node == end_node:
            return return_path(current_node, maze), exp

        # Generate children nodes
        children = []
        for new_position in ((0, -1), (0, 1), (-1, 0), (1, 0)):

            node_position = (current_node.pos[0] + new_position[0], current_node.pos[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] not in " .P":
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = manhattan(child.pos, end_node.pos)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child.pos == open_node.pos and child.g > open_node.g]) > 0:
                continue

            heapq.heappush(open_list, child)
            exp += 1
    return None


def displayMaze(maze):  # Helper function that prints a 2d maze array
    for i, row in enumerate(maze):
        for j, c in enumerate(row):
            print(c, end='')
        # print(" ", i)
        print()


if __name__ == '__main__':
    main()
