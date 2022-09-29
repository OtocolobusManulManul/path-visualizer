from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from anytree import RenderTree, NodeMixin #to generate ASCII trees for testing purposes
import pandas as pd


file_path = "../Downloads/miniweb-win32-20130309/miniweb/htdocs/" #you'll probably want to change this if you are running it on your own

def create_edge (state): return [[state.parent.name, state.name]]


def get_coords(edges, position, M):
    
    Xe, Ye = [], []
    for edge in edges:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

    return (Xe, Ye)


def display_graph (node):
    for pre, fill, node in RenderTree (node):
        print ("%s%s" % (pre, node.display()))
    print ("\n")

class state (NodeMixin):  # Add Node feature
    
    def display (self): return "<" + str(self.name) + "> k = " + str(self.k)

    def __init__ (self, node_index, K, Parent=None):
        self.parent = Parent
        self.name = node_index
        self.k = K

    left = None
    right = None

    def get_children(self): return [self.left, self.right]

    def assign_children (self, nodes): 
        self.left = nodes [0]
        self.right = nodes [1]
        return None 


def inc(x):
    x[0] += 1
    return x[0]

current_node_index = [1] # "reference type"
State = state (1, 1, Parent=None); State.name = 1
nodes = [State]
edges = []

n = 15 #this would be an off-by-one error for any node but the highest sequential node on any fiven level


while current_node_index [0] < n:
    
    [node.assign_children([state(inc(current_node_index), node.k*2, Parent=node), state(inc(current_node_index), node.k*2 + 1, Parent=node)]) for node in nodes] #
    nodes = [node.get_children() for node in nodes]
    nodes = sum(nodes, [])
    edges += [create_edge(node)[0] for node in nodes]

labels = list(range(1, current_node_index[0] + 1))

print("\nbinary tree: \n")
display_graph(State)

n = 11

#bfs
bfs_edges = [[x, x+1] for x in range (1, n)] #don't actually need to evaluate it to get path
bfs_order = list(range(1, n+1))

dls_edges = []
dls_order = [1]

node = State 
lvl = 3

def brother(node): return node.parent.right

def uncle(node): return brother(node.parent)

while node.name != n and node and lvl >= 0:  
    
    if node.left: 
        node = node.left
        lvl -= 1
    
    else:
        
        next_node = brother(node)

        if brother and (next_node != node):

            node = brother(node)       
        
        else:

            uncle = uncle (node)
            while (uncle == None):
                
                node = node.parent
                lvl += 1
                parent = node.parent
                
                if (parent == None): node = None
                else: uncle = uncle (node)
            
            lvl += 1
            node = uncle
    
    dls_order += [node.name]
    dls_edges += create_edge(node)


G = Graph(n=len(labels), edges=edges)
lay = G.layout_reingold_tilford(root=[1])

position = {k: lay[k] for k in labels}
Y = [lay[k][1] for k in labels]
M = max(Y)


Xn = [position[k][0] for k in labels]
Yn = [2*M-position[k][1] for k in labels]


dXe, dYe = get_coords(dls_edges, position, M)
bXe, bYe = get_coords(bfs_edges, position, M)
Xe, Ye = get_coords(edges, position, M)


fig = go.Figure()
fig.add_trace(go.Scatter(x=dXe,
                   y=dYe,
                   mode='lines',
                   line=dict(color='rgb(255,0,0)', width=8),
                   text = 'depth limited search',
                   hoverinfo="text",
                   name = "depth limited search"
                   ))
fig.add_trace(go.Scatter(x=bXe,
                   y=bYe,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=4),
                   text = "breadth first search",
                   name = "breadth first search",
                   hoverinfo='text'
                   ))
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(0,0,255)', width=4),
                   text = "edge",
                   name = "graph edges",
                   hoverinfo="text"
                   ))
fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='state space',
                  marker=dict(symbol='circle-dot',
                                size=36,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=2)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8
                  ))

def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k + 1][0], y=2*M-position[k + 1][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations

axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

fig.update_layout(title= 'binary tree search strategies (Reingold-Tilford Layout)',
              annotations=make_annotations(position, labels),
              font_size=12,
              showlegend=True,
              xaxis=axis,
              yaxis=axis,
              margin=dict(l=40, r=40, b=85, t=100),
              hovermode='closest',
              plot_bgcolor='rgb(248,248,248)'
              )

df1 = pd.DataFrame({"breadth first order":bfs_order})
df2 = pd.DataFrame({"depth limited search order":dls_order})

#fig.show()  
fig.write_html(file_path + "tree.html")


dataset = "<html><body>" + df1.to_html() + "<br></br>" + df2.to_html() + "</body></html>"

f = open(file_path + "treetable.html", "w")
f.write(dataset)
f.close()
