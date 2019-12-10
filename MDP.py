import numpy as np 
import snap 
import mdptoolbox as mdp 
import random 




def getNextAttachment(Graph):
	InDegV = snap.TIntPrV()
	snap.GetNodeInDegV(Graph, InDegV)
	rand = random.random()

def makeEdgeListFromA(A, name):
	with open(name, "w+") as file:
		for r in range(len(A)):
			for c in range(len(A[r])):
				if A[r][c] == True:
					file.write(str(r) + " " + str(c) + "\n")



if __name__ == '__main__':

	target_graph = "bio-SC-TS"

	### LOAD GRAPH ### 
	graph = snap.LoadEdgeList(snap.PUNGraph, target_graph + "/" + target_graph + ".txt", 0, 1, ' ')
	nodes = graph.GetNodes()
	edges = graph.GetEdges()
	InDegV = snap.TIntPrV()
	snap.GetNodeInDegV(graph, InDegV)
	sum_deg = 0
	for item in InDegV:
		sum_deg += item.GetVal2()
	avg_deg = sum_deg/nodes
    
    ### BASIC CHECKS OF GRAPHS ### 
	print("Nodes: ", graph.GetNodes())
	print("Edges: ", graph.GetEdges())

    ###  Draw graph temporarily ### 
	# snap.DrawGViz(graph, snap.gvlNeato, target_graph + ".png", target_graph, False)

	### Structural Properties of Graph ### 
	SCC = snap.GetMxScc(graph)
	print("SCC Nodes: ", SCC.GetNodes())
	print("SCC Edges: ", SCC.GetEdges())

	### PREFERENTIAL ATTACHMENT ### 
	Rnd = snap.TRnd()
	UGraph = snap.GenPrefAttach(nodes, int(avg_deg), Rnd)
	snap.DrawGViz(UGraph, snap.gvlDot, "pref.png", "Pref Graph", False)

