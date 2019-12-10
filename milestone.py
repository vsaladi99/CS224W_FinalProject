print("Fuck you")
from scipy.io import mmread 
import numpy as np
print("I got fucked")
import snap 
print("eee")
import random

# from sklearn.preprocessing import normalize
# import graphviz 

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

def makeEdgeListFromA(A, name):
	with open(name, "w+") as file:
		for r in range(len(A)):
			for c in range(len(A[r])):
				if A[r][c] == True:
					file.write(str(r) + " " + str(c) + "\n")

# graph = snap.LoadEdgeList(snap.PUNGraph, "bio-SC-TS/bio-SC-TS.txt", 0, 1, ' ')

# print("Nodes of loaded graph: ", graph.GetNodes())
# print("Edges of loaded graph: ", graph.GetEdges())


target_graph = 'ENZYMES_g123'
print(target_graph)
G = snap.LoadEdgeList(snap.PUNGraph, "Archive/"+target_graph + "/" + target_graph + ".txt", 0, 1, ' ')
print("Loaded {} with {} nodes".format(target_graph, G.GetNodes()))
max_deg, min_deg, avg_deg = getMinAvgMax(G)
clus_coef = snap.GetClustCf(G, -1)
diam = snap.GetBfsFullDiam(G, 10, False)

print(" Nodes: ", G.GetNodes())
print(" Edges: ", G.GetEdges())
print(" Maximum Degree: ", max_deg)
print(" Minimum Degree: ", min_deg)
print(" Clustering Coefficient: ", clus_coef)
print(" Average degree: ", avg_deg)
print("Diameter: ", diam)


generated = snap.LoadEdgeList(snap.PUNGraph, "Archive/attempt0.txt", 0, 1, '\t')
print("Loaded {} with {} nodes".format("Generated graph", generated.GetNodes()))
max_gen_deg, min_gen_deg, avg_gen_deg = getMinAvgMax(generated)
clus_gen_coef = snap.GetClustCf(generated, -1)
diam_gen = snap.GetBfsFullDiam(generated, 100, False)

print("Generated Nodes: ", generated.GetNodes())
print("Generated Edges: ", generated.GetEdges())
print("Generated Maximum Degree: ", max_gen_deg)
print("Generated Minimum Degree: ", min_gen_deg)
print("Generated Clustering Coefficient: ", clus_gen_coef)
print("Generated Average degree: ", avg_gen_deg)
print("Generated Diameter: ", diam_gen)








##########################  RANDOM EIGENVECTOR SHIT #####################
# EigValV = snap.TFltV()
# EigVecV = snap.TFltVFltV()
# snap.GetEigVec(graph, 10, EigValV, EigVecV)

# eigenvalues = []

# for item in EigValV:
# 	eigenvalues.append(item)


# A = np.zeros((516, 516))

# for eigenvalue in eigenvalues:
# 	v = np.random.rand(516,1)
# 	outer = np.matmul(v, np.transpose(v))
# 	A += eigenvalue*outer


# A = A/np.max(A)
# A = A > 0.5
# edges = []

# for r in range(len(A)):
# 	for c in range(len(A[r])):
# 		if A[r][c] == 1:
# 			edges.append((r,c))

# while len(edges) > graph.GetEdges():
# 	thing = random.randint(0, len(edges)-1)
# 	r, c = edges[thing]
# 	edges.remove(edges[thing])
# 	A[r][c] = 0

# print(len(edges))
# print(np.sum(A))

# makeEdgeListFromA(A, "temp.txt")

# generated = snap.LoadEdgeList(snap.PUNGraph, "temp.txt", 0, 1)

# snap.DrawGViz(generated, snap.gvlNeato, "temp.png", "kys", False)


##########################  RANDOM EIGENVECTOR SHIT #####################

# GraphClustCoeff = snap.GetClustCf (generated, -1)
# print("Clustering coefficient: %f" % GraphClustCoeff)


# result = snap.GetTriadsAll(graph)
# print("closed triads", result[0])
# print("open triads", result[2])





# eigenvalues = []

# i = 0
# for item in EigValV:
#     i += 1
#     print("Eigenvalue %d: %.6f" % (i, item))
#     eigenvalues.append(item)
#     if i >2:
#     	break

# eigenvectors = []

# i = 0
# for v in EigVecV:
#     i += 1
#     print("=== Eigenvector: %d ===" % (i))
#     eigenvectors.append(v)
#     if i > 2:
#     	break

# P = np.zeros((3, 516))
# for i in range(len(eigenvectors)):
# 	P[i] = eigenvectors[i]

# P = np.transpose(P)
# print(P.shape)

# D = np.zeros((3, 3))
# for i in range(3):
# 	D[i][i] = eigenvalues[i]

# print(np.linalg.pinv(P).shape)
# shithead = np.matmul(P, np.matmul(D, np.linalg.pinv(P)))

# print(shithead)

# P = np.concatenate((eigenvectors[0], eigenvectors[1], eigenvectors[2]), axis=1)
# print(len(P))

