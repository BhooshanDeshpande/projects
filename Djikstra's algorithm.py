G = {1:{1:0, 2:1, 3:12},
  2:{2:0, 3:9, 4:3},
  3:{3:0, 5:5},
  4:{3:4, 4:0, 5:13, 6:15},
  5:{5:0, 6:4},
  6:{6:0}}

def Dijkstra(G,v0,vf):
  ############################################ function definitions ####################################################
  def set_current(given_node):
    current_node = given_node;
    return current_node

  def add_node(given_node, visited_nodes):
    visited_nodes.append(given_node)
    return visited_nodes

  def remove_node(given_node, unvisited_nodes):
    unvisited_nodes.remove(given_node)
    return unvisited_nodes

  def get_connected_nodes(given_node):
    index = nodes.index(given_node)
    connected_nodes = list(distances[index].keys())
    connected_nodes = [element for element in connected_nodes if element not in visited_nodes]
    return connected_nodes

  def assign_val(given_node_list, cost):
    l = len(given_node_list)
    if len(cost) == 1:
      cost = [given_node_list, cost * l]
      return cost
    elif len(cost) == len(given_node_list):
      cost = [given_node_list, cost]
      return cost
    else:
      return print('Error in cost input matrix for the given nodes')

  def get_cost(given_node, connected_nodes):
    # cost=list(G[given_node].values())
    cost = []
    for i in connected_nodes:
      cost.append(G[given_node][i])
    min_cost = min(cost)
    return cost, min_cost

  ################################################ parameter_initiation ################################################
  v0 = 1
  #settting initial parameters
  nodes = list(G.keys())
  distances = list(G.values())
  current_node = set_current(v0)
  visited_nodes = [current_node]
  unvisited_nodes = nodes[:]
  unvisited_nodes.remove(current_node)
  least_cost_path = [current_node]
  total_cost = 0

  ############################################## main_script (loop)#####################################################

  while unvisited_nodes != []:
    # updating visited,unvisited nodes list
    visited_nodes = add_node(current_node, visited_nodes)
    print('current node', current_node)

    # getting connected,unconnected nodes list
    connected_nodes = get_connected_nodes(current_node)
    print('connected_nodes', connected_nodes)
    set1 = list(set(connected_nodes) | set(visited_nodes))
    unconnected_nodes = [element for element in nodes if element not in set1]
    # print('unconnected_nodes',unconnected_nodes)

    # getting costs for connected nodes
    path_costs, min_cost = get_cost(current_node, connected_nodes)
    print('path_costs', path_costs)

    # Assigning costs to all nodes
    cost_array = assign_val(connected_nodes, path_costs)
    assign_val(unconnected_nodes, [999])

    # selecting node with minimum cost
    # print(cost_array[0])
    minimum_cost_node = cost_array[0][cost_array[1].index(min(cost_array[1]))]

    # saving the cost of node selected and adding the least costs:
    total_cost += min_cost

    # setting current node=minimum_cost_node
    current_node = minimum_cost_node
    # print('hello')
    print('node selected', current_node)
    unvisited_nodes = remove_node(current_node, unvisited_nodes)
    # print('Nodes not in path',unvisited_nodes)
    print('------------------------------------------------------------')

    # save_least_cost_path
    least_cost_path.append(minimum_cost_node)
  ##################################### printing answers ###############################################################
  print('(The least cost path for given graph is:',least_cost_path,')')
  return 'The total cost for the least cost path is:',total_cost

#Execution
dis = Dijkstra(G,v0=1,vf=6)
print (dis)