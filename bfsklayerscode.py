#Below is code for regular BFS as well as code for layering a graph; a topic covered in algorithms class in theory, but we are not 
#given an oppertunity to fully code

####GENERAL HELPERS#####
def vector(p1, p2):
    #returns a vector/list which orginates at p1 and ends at p2
    return [p2[0]-p1[0], p2[1]-p1[1]]
def cross_product (v1, v2):
    #returns and computes the cross product from vectors v1 and v2
    return v1[0]*v2[1]-v1[1]*v2[0]
def dot_product (v1, v2): 
    #returns and computes the dot product from vectors v1 and v2
    return v1[0]*v2[0]+v1[1]*v2[1]
def bfs(start, adj):
    '''
    INPUT: Given a start node and an adjancency list, we can explore this graph 
    OUTPUT: After exploring the graph using BFS, we return a parent dictionary 
    which describes the shortest path from a node to start
    '''
    parent = {start: None}
    queue = [start]
    #we go through our queue until its empty
    while queue:
        new_queue = []
        #for each node in the queue, we check its neighbors and if we haven't seen, 
        #we add it to queue
        for u in queue:
            for v in adj[u]:
                if v not in parent:
                    parent[v] = u
                    new_queue.append(v)
        #replace queue with our new queue built up from neighbors 
        queue = new_queue 
    return parent

##### REGULAR SHORTEST PATH ######
def reg_get_path(parent, start, end):
    '''
    INPUT: a parent dictionary describing shortest path, a start node, and an end node
    OUTPUT: returns a list of dictionaries which describe the shortest path from start to end
    '''
    #initialize path 
    p = [end]
    while p[-1] is not None:
        p.append(parent[p[-1]])
    prepath = []  
    #p is now a built up shortest path in reverse order; now we reverse it 
    for i in range(len(p)-2, -1, -1):
        prepath.append(p[i])
    #prepath in order; we return path which is in order dictionary 
    path = []
    for p in range(len(prepath)-1):
        path.append({'start': prepath[p], 'end': prepath[p+1]})
    return path
def regular_adj(edges):
    '''
    INPUT: a list of dictionaries of the form [{'start': (1,3), 'end': (8,9)}...]
    OUTPUT: an adjacancy list of form {(1,3):(8,9), ...}
    '''
    adj = {}
    vert = set()
    #We go through the edges and add to adj list
    for dic in edges:
        vert.add(dic['start'])
        vert.add(dic['end'])
        if dic['start'] not in adj:
            adj[dic['start']] = [dic['end']]
        else:
            adj[dic['start']].append(dic['end'])
    #we go through terminal nodes and add them to the adj, having no out goin connections
    for v in vert:
        if v not in adj:
            adj[v] = []
    return adj 
##### K LEFTS SHORTEST PATH #######
def edges_adj_k(edges, k):
    '''
    INPUT: edges is a list of dictionaries of the form [{'start': (1,3), 'end': (8,9)}...]
    and k is the number of left turns we are allowed to take
    OUTPUT: an adjacancy list of form {((1,3), (8,9), 2):[((8,9), (7, 3), 1)], ...} which will
    represent k+1 copies of the H_0 graph
    
    NOTE: We break into multiple loops over edge to avoid double looping; 
    O(|edges|) instead of O(|edges|^2)      
    '''
    final_adj = {}
    #make the same graph k times 
    for i in range(k+1):
        pre_adj = {}
        #we know that all edges that end at some node will have all the edges that
        #come out of that node, in their adj list
        for edge in edges:
            if edge['end'] not in pre_adj: 
                pre_adj[edge['end']] = []    
        #thus we can just build adj for the end nodes to all edges coming out of it
        for edge in edges:
            if edge['start'] in pre_adj:
                pre_adj[edge['start']].append((edge['start'], edge['end'], i))
        #we now make a new dict which maps edges wich map to a certain end to all edges coming
        #out of that end 
        for edge in edges:
            final_adj[(edge['start'], edge['end'], i)] = pre_adj[edge['end']][:]
    return final_adj
def k_lefts_adj(adj):
    '''
    INPUT: an adjacancy list describing a path
    OUTPUT: output is an adjacancy list which takes out left turns on graph copies with
    the same k. (Ex
    return an adj of form {((1,1), (2,4), k): [((2,4), (1,6), k-1), ((2,4), (3,9)), k], ...} w/o lefts
    '''
    real_adj = {}
    #loop over all edges in adj
    for edge1 in adj:
        real_link = []
        #loop over all edges that connect to edge1
        for edge2 in adj[edge1]:
            #compute the dot and cross product between these edges 
            v1, v2 = vector(edge1[0], edge1[1]), vector(edge2[0], edge2[1])
            cross, dot = cross_product(v1, v2), dot_product(v1, v2)
            #if its a not a left turn or u-turn, we keep it in the adj
            if (cross==0 and dot>=0) or (cross>0):
                real_link.append(edge2)
            #if we take a left turn, then we will add that edge with one less k
            elif cross<0 and edge2[2]>0:
                real_link.append((edge2[0], edge2[1], edge2[2]-1))
        #add this list to the adj we will later return 
        real_adj[edge1] = real_link[:]
    return real_adj
def k_left_get_path(parent, end):
    '''
    INPUT: a parent dictionary which outlines the shortes path from a node to a start node 
    which we defined in an earlief BFS; an end edge/node where we would like to terminate at
    OUTPUT: a list of dictionaries which describes the path from one node state to another
    '''
    #parent is of form {((2,4), (1,2), k): ((1,1), (2,4), k),...} 
    #return none if its not in our BFS path
    if end not in parent:
        return None
    #traverse through the parent dictionary; parent(x), parent(parent(x)), ...
    p = [end]
    while p[-1] is not None: #parent of the last edge will be None 
        p.append(parent[p[-1]])
    #reverse this path to get proper ordering 
    prepath = []  
    for i in range(len(p)-2, -1, -1):
        prepath.append(p[i])
    #path is now in order path; but needs to be reformatted 
    #its of form [((4,3), (4,1), k), ((4,1), (5,6), k-1), ...]
    path = []
    for p in prepath:
        path.append({'start': p[0], 'end': p[1]})
    return path

####HELPER END#####
    
def shortest_path(edges, start, end):
    """
    Finds a shortest path from start to end using the provided edges

    INPUT:
        edges: a list of dictionaries, where each dictionary has two items. 
        start: a tuple representing our initial location.
        end: a tuple representing the target location.

    OUTPUT:
        A list containing the edges taken in the resulting path if one exists, None if there is no path
        with format [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    #we get our adjanceny list and run it through BFS
    adj = regular_adj(edges)
    parent = bfs(start, adj)
    #if our end not in parent, it was not found in our BFS
    if end not in parent:
        return None
    #get path from start to end
    path = reg_get_path(parent, start, end)
    return path


def shortest_path_k_lefts(edges, start, end, k):
    """
    Finds a shortest path with no more than k left turns that 
        goes from start to end using the provided edges

    INPUT:
        edges: a list of dictionaries
        start: a tuple representing our initial location.
        end: a tuple representing the target location.
        k: the max number of allowed left turns.

    OUTPUT:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    #create adjacancy list with k+1 copies of graph
    preadj = edges_adj_k(edges, k)
    #for each left turn, decrease its k value by one
    adj = k_lefts_adj(preadj)
    '''
    -we don't have to run BFS over every starting edge, we need only do this for the 
    level with value k since we would use all k left turns if need be and if there is 
    a path which uses less than k left turns, we can still find an equivalant path starting
    from level k. 
    -we collect all such starting edges in start_edges
    -we collect all end edges, regardless of their level, in end_edge'''
    start_edge = []
    for edge in adj:
        if edge[0]==start and edge[2]==k:
            start_edge.append(edge) 
    end_edge = []
    for edge in adj:
        if edge[1]==end:
            end_edge.append(edge)
    #looping over all relevant start edges and end edges, we find the minumum length path
    #len(edges) is an upper bound to the length of shortest path
    min_length = len(edges)
    for strt in start_edge :
        parent = bfs(strt, adj) #we need to run bfs for every start edge
        #we can have multiple edges which lead to the target/end node
        for endd in end_edge:
            #for a specific start and end edge, we find a path 
            k_left_path = k_left_get_path(parent, endd)
            if k_left_path != None:
                #if the path is valid (ie not None), we keep track of the shortest one
                if len(k_left_path)<=min_length:
                    min_length=len(k_left_path)
                    min_path = k_left_path
    #it is impossible to have a path of len(edges) since we ignore eqiv node when turning left
    #on graph copies
    if min_length==len(edges):
        return None
    return min_path