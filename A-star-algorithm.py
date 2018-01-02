
import math

class Node:
    def __init__(self, value, point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other):
        return 0 if self.value == '.' else 1


def children(point, grid):
    x, y = point.point
    # print("x,y : ", x , y)
    #Find all possible links for the given x,y point
    #let's cater for some different special places/cases in the grid
    if(x<=0 and y<=0):                                          #if both coordinates equal to 0 then donot check point above or on left in grid
        links = [grid[d[0]][d[1]] for d in [(x, y + 1), (x + 1, y)]]
    elif(x<=0 and y>0 and y<len(grid[x])-1):                    #Donot check points on left (you are in firts column of grid)
        links = [grid[d[0]][d[1]] for d in [(x, y - 1), (x, y + 1), (x + 1, y)]]
    elif (x > 0 and x < len(grid)-1 and y <= 0):                #Donot check points above (you are in first row of grid)
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y + 1), (x + 1, y)]]
    elif(x>=len(grid)-1 and y>=len(grid[x])-1):                 #You are in last row and last column of grid
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1)]]
    elif (x >= len(grid) - 1 and y <=0):                        #Donot check below and left - you are in last row and first column
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y + 1)]]
    elif (x <=0 and y >= len(grid[x]) - 1):                     #Donot check above and right - you are in last column and first row
        links = [grid[d[0]][d[1]] for d in [(x, y - 1), (x + 1, y)]]
    elif (x >= len(grid) - 1 and y < len(grid[x]) - 1):         #Donot check below - you are in last row
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1)]]
    elif (x < len(grid) - 1 and y >= len(grid[x]) - 1):         #Donot check left - you are in last column
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x + 1, y)]]
    else:                                                       #for any other case
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
    # for link in links:
    #     print(link.point)
    return [link for link in links if link.value != '%']        #Return the links for the given point


def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1] - point2.point[1]) #this calculates the manhattan heuristic distance

def aStar(start, goal, grid):
    # create open and closed sets
    tag = "aStar: "
    openset = set()
    closedset = set()
    print( tag + "open and close set created")
    # Current point is the starting point
    current = start
    # Add the starting point to the open set
    openset.add(current)
    # While the open set is not empty
    while openset:
        print(tag + "inside while loop")
        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o: o.G + o.H)
        # If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        # Remove the item from the open set
        openset.remove(current)
        # Add it to the closed set
        closedset.add(current)
        # Loop through the node's children/siblings
        for node in children(current, grid):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue
            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                # Set the parent to our current item
                node.parent = current
                # Add it to the set
                openset.add(node)
    # Throw an exception if there is no path
    raise ValueError('No Path Found')


def next_move(pacman, food, grid):
    # Convert all the points to instances of Node
    print("creating nodes of grid")
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[x][y] = Node(grid[x][y], (x, y))
        print("nodes created")
    # Get the path
    path = aStar(grid[pacman[0]][pacman[1]], grid[food[0]][food[1]], grid)
    print("A star computed")
    # Output the path
    print (len(path) - 1)
    for node in path:
        x, y = node.point
        print(x, y)

if __name__ == '__main__':
    print("Enter pacman coordinates")
    pacman_x, pacman_y = [int(i) for i in input().strip().split()] # this gives the initial coordinates of pacman in the grid
    print(pacman_x, pacman_y)
    print("Enter food coordinates")
    food_x, food_y = [int(i) for i in input().strip().split()] #this gives the coordinates of the food(goal) in grid
    print(food_x, food_y)
    print("Enter grid size")
    x, y = [int(i) for i in input().strip().split()]  #this is the size of the grid
    print(x,y)


    print("create empty grid")             #Now you must enter weight for each block in the grid
    grid = []
    for i in range(0, x):
        print("Enter weights for blocks in row ", i, " (without spaces):")
        grid.append(list(input().strip())) #strip does nothing but, removes the the whitespace in your string. If you want to remove the extra whitepace from front and back of your string, you can use strip
        print("i : ", i)

    print("GRID with weights:")
    print(grid)
    print('no of rows: ', len(grid))
    print('no of columns: ', len(grid[0]))
    print("grid initialized")
    next_move((pacman_x, pacman_y), (food_x, food_y), grid)
