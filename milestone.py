from scipy.io import mmread 
import numpy as np
import snap 
import random
# from sklearn.preprocessing import normalize
# import graphviz 


def makeEdgeListFromA(A, name):
	with open(name, "w+") as file:
		for r in range(len(A)):
			for c in range(len(A[r])):
				if A[r][c] == True:
					file.write(str(r) + " " + str(c) + "\n")

graph = snap.LoadEdgeList(snap.PUNGraph, "bio-SC-TS/bio-SC-TS.txt", 0, 1, ' ')

print("Nodes of loaded graph: ", graph.GetNodes())
print("Edges of loaded graph: ", graph.GetEdges())






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

