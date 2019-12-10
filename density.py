import numpy as np 
import snap 
import random 

def getMinAvgMax(graph):
	nodes = graph.GetNodes()
	edges = graph.GetEdges()
	InDegV = snap.TIntPrV()
	snap.GetNodeInDegV(graph, InDegV)
	sum_deg = 0
	max_deg = 0
	min_deg = 10000
	for item in InDegV:
		cur_deg = item.GetVal2()
		sum_deg += cur_deg
		min_deg = min(min_deg, cur_deg)
		max_deg = max(max_deg, cur_deg)
	avg_deg = sum_deg/nodes

	return (max_deg, min_deg, avg_deg)

if __name__ == '__main__':

	target_graph = "bio-SC-TS"

	### LOAD GRAPH ### 
	graph = snap.LoadEdgeList(snap.PUNGraph, target_graph + "/" + target_graph + ".txt", 0, 1, ' ')
	nodes = graph.GetNodes()
	edges = graph.GetEdges()
	InDegV = snap.TIntPrV()
	snap.GetNodeInDegV(graph, InDegV)
	sum_deg = 0
	max_deg = 0
	min_deg = 10000
	for item in InDegV:
		cur_deg = item.GetVal2()
		sum_deg += cur_deg
		min_deg = min(min_deg, cur_deg)
		max_deg = max(max_deg, cur_deg)
	avg_deg = sum_deg/nodes

	CfVec = snap.TFltPrV()
	Cf = snap.GetClustCf(graph, CfVec, -1)
	clus_coef = snap.GetClustCf(graph, -1)
    ### BASIC CHECKS OF GRAPHS ### 
	print("Nodes: ", graph.GetNodes())
	print("Edges: ", graph.GetEdges())
	print("Maximum Degree: ", max_deg)
	print("Minimum Degree: ", min_deg)
	print("Clustering Coefficient: ", clus_coef)
	print("Average degree: ", avg_deg)


	density = edges/(nodes * (nodes - 1))
	print("Density: ", density)

	initiator = np.array([[0,density,density],[density,0,density],[density,density,0]])

	matrix = initiator
	for i in range(5):
		matrix = np.kron(matrix, initiator)

	generated = snap.TUNGraph.New()
	for i in range(len(matrix)):
		generated.AddNode(i)

	for i in range(len(matrix)):
		for j in range(i, len(matrix)):
			rand = random.random()
			if matrix[i][j] < rand:
				generated.AddEdge(i, j)


	result_degree = snap.TIntV()
	snap.GetDegSeqV(generated, result_degree)
	arr = []
	for i in range(0, result_degree.Len()):
		arr.append((i, result_degree[i]))

	arr.sort(key= lambda x: -x[1], reverse=True)

	V = snap.TIntV()
	for i in range(len(matrix) - nodes):
		V.Add(arr[i][0])

	# V = snap.TIntV()
	# rand_nodes = random.sample(range(0, len(matrix)), len(matrix)-nodes)
	# for node in rand_nodes:
	# 	V.Add(node)

	while generated.GetEdges() < edges:
		rand_node_one = random.randint(0, nodes)
		rand_node_two = random.randint(0, nodes)
		if rand_node_two != rand_node_one:
			generated.AddEdge(rand_node_one, rand_node_two)

	snap.DelNodes(generated, V)
	max_gen_deg, min_gen_deg, avg_gen_deg = getMinAvgMax(generated)
	clus_gen_coef = snap.GetClustCf(generated, -1)
	CfVec_gen = snap.TFltPrV()
	Cf_gen = snap.GetClustCf(generated, CfVec_gen, -1)


	print("Generated Nodes: ", generated.GetNodes())
	print("Generated Edges: ", generated.GetEdges())
	print("Generated Maximum Degree: ", max_gen_deg)
	print("Generated Minimum Degree: ", min_gen_deg)
	print("Generated Clustering Coefficient: ", clus_gen_coef)
	print("Generated Average degree: ", avg_gen_deg)






