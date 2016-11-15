import numpy as np
import matplotlib.pyplot as plt
import random
import heapq as heap


def draw(): 
    world = {}
    for i in range(34):
        for j in range(34):
            world[(i,j)] = {'visited':False, 'dist':np.inf, 'valid':True, 'F':np.inf}
            #Shape A
            if i in range(6,13) and j in range(4,11):
                if j >= 14-i:
                    world[(i,j)]['valid'] = False
            #Shape C
            if i in range(14,18) and j in range(11,16):
                world[(i,j)]['valid'] = False
            #Shape D
            if i in range(9,13) and j in range(16,21):
                world[(i,j)]['valid'] = False
            #Shape E
            if i in range(18,25) and j in range(16,20):
                world[(i,j)]['valid'] = False
            #Shape B
            if i in range(20, 29) and j in range(6,20):
                if j <= 13*i/8 - 212/8:
                	world[(i,j)]['valid'] = False
            #Shape F
            if (i in range(12,29) and j in range(25,29)) or (i in range(25,29) and j in range(22,26)):
                world[(i,j)]['valid'] = False
    return world

def isValid(coordinate, world):
	#isValid determines if coordinates are valid for the given world
	for itr in coordinate: 
		#If outside the board
		if itr not in range(0, 34):
			return False
		for key in world.keys():
			if coordinate == key:
				if not world[key]['valid']:
					return False
	return True

def H(coordinate, target):
	#Function H represents the Heuristic value for A* 
	#The Heuristic Value = distance from a given node (or coordinate) to target 
	x_dist = coordinate[0] - target[0]
	y_dist = coordinate[1] - target[1]
	diag_dist = np.sqrt((x_dist)**2 + (y_dist)**2)

	return diag_dist

def aStarAlg(world, start, end):
	#where world is given in Q2, start is the start, end is at finish
	
	q = []
	
	#Direction of new path
	direct = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

	#Heap with coordinates(x,y) and distance from the start
	heap.heappush(q, (0, start))

	world[start]['dist'] = 0	
	#Where F is the total distance (distance travelled + heuristic value)
	world[start]['F'] = 0

	while q != []:
		v = heap.heappop(q)
		coordinate = v[1]

		if coordinate == end:
			break

		#Identify nodes visited
		plt.scatter(coordinate[0], coordinate[1], marker = '*', color = '.75')

		#The code above is almost identical to Q2, below I update the code for Q3
		for direction in direct:
			new_coordinate = (direction[0] + coordinate[0], direction[1] + coordinate[1])
			if isValid(new_coordinate, world):
				if direction in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
					dist = world[coordinate]['dist'] + np.sqrt(2)
					F = dist + H(new_coordinate, end)
				else:
					dist = world[coordinate]['dist'] + 1
					F = dist + H(new_coordinate, end)
				if F < world[new_coordinate]['F']:
					world[new_coordinate]['parent'] = coordinate
					world[new_coordinate]['dist'] = dist
					world[new_coordinate]['F'] = F
				if world[new_coordinate]['visited'] != True and coordinate != new_coordinate:
					world[new_coordinate]['visited'] = True
					heap.heappush(q, (world[new_coordinate]['F'], new_coordinate))

	#To find shortest path - backtrack through parents of nodes
	itr = end
	p = [end]
	shortest_p = world[end]['dist']

	while itr != start:
		itr = world[itr]['parent']
		p.append(itr)

	print 'Distance of the shortest path is %f' %(shortest_p)
	return shortest_p, p


if __name__ == '__main__':
	world = draw()

	#Create coords
	coordinates = []
	for key in world.keys():
		if world[key]['valid'] != True:
			coordinates.append(key)

	x_coord = []
	for keys in coordinates:
		x_coord.append(keys[0])

	y_coord = []
	for keys in coordinates:
		y_coord.append(keys[1])

	#Plot world
	plt.axis([0, 33, 0, 33])
	plt.scatter(x_coord, y_coord, color = 'magenta')

	#Initalize start and end points (from diagram in 2)
	start = (2,2)
	end = (32, 32)

	shortest_p, p = aStarAlg(world, start, end)

	x_coord = [itr[0] for itr in p]
	y_coord = [itr[1] for itr in p]

	#Plot path
	plt.plot(x_coord, y_coord, color = 'cyan')

	#Plot start and end points
	plt.plot([2],[2], marker='o', color = 'green')
	plt.plot([32],[32], marker='o', color = 'red')

	plt.title("Question 3: A* Algorithm")
	plt.show()