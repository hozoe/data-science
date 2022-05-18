import networkx as nx
import argparse
import json

from networkx.classes.graph import Graph

def load_dict(json_file):
    with open(json_file,'r') as f:
        pony_dict = json.load(f)
    return pony_dict

def to_graph(pony_dict):
    for k, d in pony_dict.items():
        for ik in d:
            d[ik] = {'weight': d[ik]}
    G = nx.Graph(pony_dict)
    # G = nx.Graph(pony)
    #for edge in G.edges:
    #print(G.size())
    return G

''' find the nodes with the max number of neighbors that have weight > 0 '''
def most_connected_by_num(G,pony_dict):
    num_dict = {key: 0 for key in dict.fromkeys(pony_dict)}
    for node in G.nodes():
        for neighbor in G.neighbors(node):
        # if len(list(G.neighbors(node)))!=0:
            if G.edges[(node,neighbor)]['weight']>0:
                num_dict[node] += 1
    weighted = list(num_dict.values())
    return sorted(num_dict, key=num_dict.get, reverse=True)[:3]
    # print(max(weighted))
    # nodes = list(num_dict.keys())
    # most = nodes[weighted.index(max(weighted))]
    # return most
    #return max(G.degree().items(), key = lambda x: x[1])

def most_connected_by_weight(G,pony_dict):
    weight_dict = {key: 0 for key in dict.fromkeys(pony_dict)}
    for node in G.nodes():
        for neighbor in G.neighbors(node):
        # if len(list(G.neighbors(node)))!=0:
            weight_dict[node]+= G.edges[(node,neighbor)]['weight']
    return sorted(weight_dict, key=weight_dict.get, reverse=True)[:3]
    # weights = list(weight_dict.values())
    # print(max(weights))
    # nodes = list(weight_dict.keys())
    # most = nodes[weights.index(max(weights))]
    # return most

def most_connected_by_betweenness(G):
    valid_edges = list(filter(lambda e: e[2] > 0, (e for e in G.edges.data('weight'))))
    keep_edges = list(e[:2] for e in valid_edges)
    G.remove_edges_from(keep_edges)
    betweenness_dict = nx.degree_centrality(G)
    # print(([(a,b) for a, b, attrs in G.edges(data=True) if attrs["weight"] == 0]))
    return sorted(betweenness_dict, key=betweenness_dict.get, reverse=True)[:3]
    

# graph = to_graph('/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw9/submission_template/data/interaction_network.json')
# print(most_connected_by_num(graph,'/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw9/submission_template/data/interaction_network.json'))
# print(most_connected_by_weight(graph,'/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw9/submission_template/data/interaction_network.json'))
# print(most_connected_by_betweenness(graph))
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',help='interaction-network.json')
    parser.add_argument('-o',help='stats.json')
    args = parser.parse_args()

    input_file = args.i
    output = args.o
    pony_dict = load_dict(input_file)
    graph = to_graph(pony_dict)
    keys = ["most_connected_by_num", "most_connected_by_weight", "most_connected_by_betweenness"]
    res = {}
    res["most_connected_by_num"] = most_connected_by_num(graph,pony_dict)
    res["most_connected_by_weight"] = most_connected_by_weight(graph,pony_dict)
    res["most_connected_by_betweenness"] = most_connected_by_betweenness(graph)
    
    with open(output,'w') as f:
        json.dump(res,f,indent=4)

if __name__ == "__main__":
    main()