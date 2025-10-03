class Queue:
    def __init__(self):
        self.queue = []
        self.explored = {}

    def enqueue(self, node):
        self.queue.append(node)

    def dequeue(self):
        return self.queue.pop(0)
    
    def explore(self, node, parent, link):
        self.explored[node] = {"parent": parent, "link": link}

    def get_path(self, current_node):
        p = Path()
        while True:
            p.add_step(current_node, self.explored[current_node]["link"])
            current_node = self.explored[current_node]["parent"]
            if self.explored[current_node]["parent"] is None:
                break
        p.add_step(current_node, None)
        return p

class Path:
    def __init__(self):
        self._path = []
    
    def add_step(self, node, link):
        # self._path.insert(0, {"node": node, "link": link})
        self._path.insert(0, Node(node, link))
    
    def nodes(self):
        return [i.node for i in self._path]
    
    # todo: add iterator
    


class Node:
    def __init__(self, node, link):
        self.node = node
        self.link = link # group that connects the node with the prev node
    
    def __repr__(self):
        return f"{self.node} via {self.link}" 

    def __str__(self):
        return self.node