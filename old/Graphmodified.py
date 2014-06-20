from collections import deque

class Edge(object):
    def __init__(self, u, v, w):
        self.u = u
        self.v = v  
        self.w = w
    def __repr__(self):
        return "%s->%s:%s" % (self.u, self.v, self.w)
 
class FlowNetwork(object):
    def __init__(self, N):
        self.adj = tuple([] for i in range(N))
        self.flow = {}
        self.N = N
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge  #redge is not defined in Edge class lol
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def find_path(self, source, sink, path, min_capacity=0):
##        if source == sink:
##            return path
##        for edge in self.get_edges(source):
##            residual = edge.capacity - self.flow[edge]
##            if residual > 0 and edge not in path:
##                result = self.find_path( edge.sink, sink, path + [edge]) 
##                if result != None:
##                    return result
        #implement BFS... at least
        tree = {source: None}
        queue = deque()
        queue.appendleft(source)
        
        while queue:
            v = queue.pop()
            for edge in self.get_edges(v):
                residual = edge.w - self.flow[edge]
                if residual > min_capacity and edge.v not in tree:
                    tree[edge.v] = edge
                    queue.appendleft(edge.v)
                    if edge.v == sink:
                        path = [edge]
                        while path[-1] != None:
                            path.append(tree[path[-1].u])
                        path.pop()
                        path.reverse()
                        return path
        return None
        
            
    def max_flow(self, source, sink):
        edges = []
        for adj in self.adj:
            edges.extend(adj)
        min_capacity = max(edges, key=lambda e: e.w).w
        while min_capacity > 0:
            path = self.find_path(source, sink, [], min_capacity=min_capacity)
            while path != None:
                residuals = [edge.w - self.flow[edge] for edge in path]
                flow = min(residuals)
                for edge in path:
                    self.flow[edge] += flow
                    self.flow[edge.redge] -= flow
                path = self.find_path(source, sink, [])
            min_capacity //= 2
        return self.flow

    def min_cut(self, source, sink):
        flow = self.max_flow(source, sink)
        #do a bfs over non-full edges
        
        visited = set()
        queue = deque()
        queue.appendleft(source)
        while queue:
            u = queue.pop()
            if u in visited:
                continue
            visited.add(u)
            for e in self.get_edges(u):
                if flow[e] < e.w:
                    queue.appendleft(e.v)
                    
        unvisited = set(range(self.N)) - visited
        return (visited, unvisited)
            
