import graph as gr
import numpy as np


#####################################
#
#   Calcul d'un arbre couvrant minimal
#   par l'algorithme de Kruskal
#   d'après Weis Data Structures & Algorithms in Java, p 324
#   
#   Utilise une structure "disjoint set" (union-find) qui fait son efficacité
#   avec une "compression de chemin"
#
#####################################



def compute(graph, xyc=[0,0], invert_distance=False) :

	n = graph.get_order()
	sorted_edges = get_sorted_edges_distance_to_center(graph, xyc, invert_distance=invert_distance)
	# sorted_edges = get_sorted_edges_orientation(graph)
	es = [(graph.get_vertice_index(s), graph.get_vertice_index(t)) for (s,t) in sorted_edges]

	s = [-1] * n  # dijSet
	edgesAccepted = []

	nbEdgesAccepted = 0
	while (nbEdgesAccepted < n - 1) and es :  # test si es vide : normalement pas necessaire mais utile si graphe non connexe
		(u,v) = es.pop(0)
		uset = find(s,u)
		vset = find(s,v)

		if ( uset != vset ) :
			#print('union')
			union(s,uset,vset)
			nbEdgesAccepted += 1
			edgesAccepted.append((u,v))
	return edgesAccepted

def find(s,u) :
	if ( s[u] < 0 ) :
		return u
	else :
		# return find(s,s[u]) # sans compression
		r = find(s,s[u]) 
		s[u] = r
		return r

def union(s,r1,r2) :
	s[r2] = r1

def get_sorted_edges_distance_to_center(graph, xyc, invert_distance=False):
	def distance_to_center(e) :
		(u,v) = e
		xu,yu = graph.get_xy(u)
		xv,yv = graph.get_xy(v)
		#distance to the xyc point

		d1 = (xu-xyc[0])*(xu-xyc[0]) + (yu-xyc[1])*(yu-xyc[1])
		d2 = (xv-xyc[0])*(xv-xyc[0]) + (yv-xyc[1])*(yv-xyc[1])
		d = np.mean((d1,d2))
		#d2 = (xu+xv-xyc[0])*(xu+xv-xyc[0]) + (yu+yv-xyc[1])*(yu+yv-xyc[1])
		if invert_distance:
			return -d
		return d
	return sorted(graph.get_edges(), key = distance_to_center)

def get_sorted_edges_orientation(graph):
	def orientation(e) :
		(u,v) = e
		return  gr.orientation(u,v)
	return sorted(graph.get_edges(), key = orientation)
    