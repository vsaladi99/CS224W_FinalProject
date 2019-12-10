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

	target_graph = "bio-diseasome"

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

	# EigVals = 3
	# PEigV = snap.TFltV()
	# snap.GetEigVals(graph, EigVals, PEigV)
	# for item in PEigV:
	# 	print(item)


	kernels = [np.array([[0,1,1],[1,0,0],[1,0,0]]), np.array([[0,1,0],[1,0,1],[0,1,0]]), np.array([[0,1,0],[1,0,0],[0,0,0]])]
	kernels.append(np.array([[0,1,1,0],[1,0,0,0], [1,0,0,1], [0,0,1,0]]))
	kernels.append(np.array([[0,1,0,0],[1,0,1,0],[0,1,0,0],[0,0,0,0]]))
	kernels.append(np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]]))



	initiator = random.choice(kernels)
	matrix = initiator
	for i in range(4):
		kernel_choice = random.choice(kernels)
		matrix = np.kron(matrix, kernel_choice)

	print("initial generated size: ", len(matrix))

	generated = snap.TUNGraph.New()
	for i in range(len(matrix)):
		generated.AddNode(i)

	for i in range(len(matrix)):
		for j in range(i, len(matrix)):
			if matrix[i][j] == 1:
				generated.AddEdge(i, j)


	V = snap.TIntV()
	rand_nodes = random.sample(range(0, len(matrix)), len(matrix)-nodes)
	for node in rand_nodes:
		V.Add(node)

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

	# EigVals = 3
	# PEigV_gen = snap.TFltV()
	# snap.GetEigVals(generated, EigVals, PEigV_gen)
	# for item in PEigV_gen:
	# 	print(item)

	snap.DrawGViz(generated, snap.gvlNeato, "generated-kronecker-v3.png", "Kronecker", False)









    ###  Draw graph temporarily ### 
	# snap.DrawGViz(graph, snap.gvlNeato, target_graph + ".png", target_graph, False)

	### Structural Properties of Graph ### 
	# SCC = snap.GetMxScc(graph)
	# print("SCC Nodes: ", SCC.GetNodes())
	# print("SCC Edges: ", SCC.GetEdges())

	### PREFERENTIAL ATTACHMENT ### 
	# Rnd = snap.TRnd()
	# UGraph = snap.GenPrefAttach(nodes, int(avg_deg), Rnd)
	# snap.DrawGViz(UGraph, snap.gvlDot, "pref.png", "Pref Graph", False)