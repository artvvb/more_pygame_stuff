class pathnode:
	def __init__(self, loc, weight, delta):
		self.loc, self.weight, self.delta = loc, weight, delta
	def __eq__(self, loc):
		return self.loc == loc
	
def get_path(d_graph, src, max_weight, deltas):
	# graph is a dict indexed by location
	# nodes in graph must contain .loc and .weight members
	edge = [pathnode(src, 0, (0,0))]
	path = {src:pathnode(src, 0, (0,0))}
	
	while len(edge) > 0:
		edge.sort(key=lambda val:val.weight)
		temp = edge.pop(0)
		#adj = [ for delta in deltas if (temp.loc[0]+delta[0],temp.loc[1]+delta[1]) in d_graph]
		for delta in deltas:
			loc = (temp.loc[0]+delta[0],temp.loc[1]+delta[1])
			if not loc in d_graph:
				continue
			elif loc in path:
				continue
			elif loc in edge:
				i = edge.index(loc)
				if d_graph[loc] + temp.weight < edge[i].weight:
					edge[i].weight = d_graph[loc] + temp.weight
			elif d_graph[loc] + temp.weight <= max_weight:
				edge.append(pathnode(loc, d_graph[loc] + temp.weight, delta))
		if temp.weight <= max_weight:
			path[temp.loc] = temp
	return path
	
if __name__ == "__main__":
	import random
	g_deltanames = {
		( 0, 0):"*",
		( 1, 0):"L",
		(-1, 0):"R",
		( 0, 1):"U",
		( 0,-1):"D"
	}
	d_graph = {}
	RANDRANGE=(0,2)
	for y in range(4):
		for x in range(4):
			d_graph[(x,y)]=random.randint(RANDRANGE[0], RANDRANGE[1])
	deltas = [
		( 1, 0),
		(-1, 0),
		( 0, 1),
		( 0,-1)
	]
	for y in range(4):
		for x in range(4):
			print(d_graph[x,y], end=" ")
		print()
	path = get_path(d_graph, (0,0), (3,3), 2, deltas)
	print()
	for y in range(4):
		for x in range(4):
			if not (x,y) in path:
				print(" XX", end=" ")
			else:
				if path[(x,y)].weight < 10:
					print(" ", end = "")
				print(repr(path[(x,y)].weight)+g_deltanames[path[(x,y)].loc], end = " ")
		print()
	
