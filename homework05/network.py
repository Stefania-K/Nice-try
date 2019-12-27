from api_network import get_friends
import igraph
from igraph import Graph, plot
import numpy as np
import time

def get_network(user_id: int, as_edgelist=True) -> list:
    users_ids = get_friends(user_id, "id")
    edges = []
    matrix = [[0] * len(users_ids) for i in range(len(users_ids))]

    for i in range(len(users_ids)):
        friends = get_friends(users_ids[i],"id")
        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends:
                if as_edgelist:
                    edges.append((i, j))
                    print(edges)
                else:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        time.sleep(5)
    print("edges are ",edges)
    if as_edgelist:
        return edges
    return matrix


def plot_graph(user_id):
    surnames = get_friends(user_id, 'last_name')
    vertices = surnames
    edges = get_network(user_id, True)

    g = igraph.Graph(vertex_attrs={"shape": "circle",
                                   "label": vertices,
                                   "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }

    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, **visual_style)

get_network(127923722)
