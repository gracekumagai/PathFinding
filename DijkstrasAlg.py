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
	for itr in coordinate: 
		#If outside the board
		if itr not in range(0, 34):
			return False
		for key in world.keys():
			if coordinate == key:
				if not world[key]['valid']:
					return False
	return True

def dijAlg(world, start, end):
	#where world is given in Q2, start is the start, end is at finish

	q = []
	
	#Direction of new path
	direct = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

	#Heap with coordinates(x,y) and distance from the start

	heap.heappush(q, (0, start))
	world[start]['dist'] = 0

	while q != []:
		v = heap.heappop(q)
		coordinate = v[1]

		#Identify nodes visited
		plt.scatter(coordinate[0], coordinate[1], marker = '*', color = '.75')


		for direction in direct:
			new_coordinate = (direction[0] + coordinate[0], direction[1] + coordinate[1])
			if isValid(new_coordinate, world):
				if direction in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
					dist = world[coordinate]['dist'] + np.sqrt(2)
				else:
					dist = world[coordinate]['dist'] + 1
				if dist < world[new_coordinate]['dist']:
					world[new_coordinate]['parent'] = coordinate
					world[new_coordinate]['dist'] = dist
				if world[new_coordinate]['visited'] != True:
					world[new_coordinate]['visited'] = True
					heap.heappush(q, (world[new_coordinate]['dist'], new_coordinate))

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

	#Create the world
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

	shortest_p, p = dijAlg(world, start, end)

	x_coord = [itr[0] for itr in p]
	y_coord = [itr[1] for itr in p]

	#Plot start and end points
	plt.plot([2],[2], marker='o', color = 'green')
	plt.plot([32],[32], marker='o', color = 'red')

	#Plot path
	plt.plot(x_coord, y_coord, color = 'cyan')
	plt.title("Question 2: Dijkstra's Algorithm")
	plt.show()