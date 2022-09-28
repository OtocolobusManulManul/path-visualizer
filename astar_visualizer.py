from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from anytree import Node, RenderTree #to generate ASCII trees for testing purposes


#used with the help of:
#https://www.researchgate.net/publication/320386988_Tutorial_Igraph_with_Python
#https://pypi.org/project/anytree/
#https://plotly.com/python/tree-plots/

#we just need to check to make sure that the state doesn't already exist
#if it does it will never need to be moved around in the graph,
#since A* will have generated the statespace from a previous
#state with a lower hueristic, thus hashes just needs to check
#if the state already exists

def is_valid (state, hashes, current_node_index): #index 0 = cats, index 1 = cats
    
    right = state.right
    left = state.left
    state_hash = hash_statespace(state)

    #print(state.display())

    if state_hash in hashes: return False
    elif (right[0] < right[1] and right[0] != 0) or (left[0] < left[1] and left[0] != 0): return False
    elif right[0] < 0 or right[1] < 0 or left[0] < 0 or left[1] < 0: return False

    current_node_index[0] += 1
    state.node_index = current_node_index[0]
    hashes += [state_hash]

    return True


def hash_statespace (state): 

    #print (state.display())

    state_hash = ""
    for x in state.left + state.right + [1 if state.side else 0]:
        state_hash += str(x)

    #print(state_hash)
    return state_hash


class statespace: 
    
    def display(self, short = False): 
        if not short: return "A*: " + str(self.astar) + ", left: " + str(self.left) + " right: " + str(self.right) + " Boat: " + str("right" if self.side else "left")
        else: return str(self.node_index) + " <A*:" + str(self.astar) + "> " + "<L:" + str(self.left) + "> <R:" + str(self.right) + "> <B: " + str("right" if self.side else "left") + ">"

    parent = None
    node_index = None

    def __init__ (self, left_shore, right_shore, boat, true_cost):
        self.children = []
        self.cost = true_cost
        self.side = boat
        self.left = left_shore
        self.right = right_shore
        self.side = boat #False (0) = left
                         #True (1) = right
    
        self.astar = sum(self.left) + true_cost 

    def append_children (self, state): self.children += [state]

    
def trip (state, dogs, cats):

    right = state.right
    left = state.left
    cost = state.cost
    boat = state.side
    shore = 1 if boat else -1
    
    new_right = [right[0] + (cats * shore * -1), right[1] + (dogs * shore * -1)] #; print (new_right)
    new_left =  [left[0] + (cats * shore), left[1] + (dogs * shore)] #; print (new_left)

    new_state = statespace (new_left, new_right, not boat, cost + 1)
    #print(new_state.display())

    return new_state


current_node_index = [0]
priority_queue = []
root_state = statespace ([3,3], [0,0], False, 0)
State = root_state
hashes = [hash_statespace(State)]
eval_path = []
root_state.node_index = 0


while sum(State.right) != 6:

    eval_path += [State]

    for action in [[0,2], [0,1], [1,0], [2,0], [1,1]]:
        
        branch = trip (State, *action)
        #print(branch.display())

        if is_valid (branch, hashes, current_node_index):
            State.append_children (branch)
            branch.parent = State
            priority_queue += [branch]

    priority_queue = sorted (priority_queue, key = lambda astar: astar.astar, reverse=True)
    print ("queue:", ", ".join(["node: " + str(x.node_index) + " A*: " + str(x.astar) for x in priority_queue][::-1]))
    
    State = priority_queue.pop()


eval_path += [State]
print ("reached goal space on node", State.node_index, "with", State.cost, "trips")


def display_graph(node):
    for pre, fill, node in RenderTree(node):
        print("%s%s" % (pre, node.name))
    print("\n")


def create_edge(state): return [[state.parent.node_index, state.node_index]] 


solution_path = []
while State.parent:
    solution_path.insert(0, State)
    State = State.parent

solution_path.insert(0, State) 
solution_edges = []


node = None
for solution_node in solution_path:
    node = Node(solution_node.display(), parent=node)
    if node.parent != None: solution_edges += create_edge(solution_node)


print("\ntree for solution path:\n")
display_graph(node.root)


print("\nevaluation path\n")
print([x.node_index for x in eval_path])


evaluation_edges = []
for node_index in range(len(eval_path) - 1):
    evaluation_edges += [[eval_path[node_index].node_index, eval_path[node_index + 1].node_index]]


state = root_state
node = Node(state.display(short=True), parent=None)
full_solution_root= node
labels = [state.node_index]
v_text = [state.display()]
edges = []
vertices = []

while state:    
    if len(state.children) != 0:
        state = state.children.pop()
        node = Node(state.display(short=True), parent = node)
        labels += [state.node_index]
        v_text += [state.display()]
        if node.parent != None: 
            edges += create_edge(state)
            
    else:
        state = state.parent
        node = node.parent


print("\ntree for full state generation  path:\n")
display_graph(full_solution_root)


G = Graph(n=len(labels), edges=edges)
lay = G.layout_reingold_tilford(root=[0])

position = {k: lay[k] for k in labels}
Y = [lay[k][1] for k in labels]
M = max(Y)


Xn = [position[k][0] for k in labels]
Yn = [2*M-position[k][1] for k in labels]
eXe= []
eYe= []
sYe= []
sXe= []
Xe = []
Ye = []
labels = sorted(labels)

for edge in solution_edges:
    sXe+=[position[edge[0]][0],position[edge[1]][0], None]
    sYe+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

for edge in edges:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

for edge in evaluation_edges:
    eXe+=[position[edge[0]][0],position[edge[1]][0], None]
    eYe+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]


fig = go.Figure()
fig.add_trace(go.Scatter(x=sXe,
                   y=sYe,
                   mode='lines',
                   line=dict(color='rgb(255,0,0)', width=8),
                   text = 'optimal solution path',
                   hoverinfo="text",
                   name = "solution path"
                   ))
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=6),
                   text = "statespace generation path",
                   name = "state generation path",
                   hoverinfo='text'
                   ))
fig.add_trace(go.Scatter(x=eXe,
                   y=eYe,
                   mode='lines',
                   line=dict(color='rgb(0,0,255)', width=4),
                   text = "A* evaluation path",
                   name = "state evaluation path",
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
                  text=v_text,
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
                x=pos[k][0], y=2*M-position[k][1],
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

fig.update_layout(title= 'A* missionaries and cannibal (Reingold-Tilford Layout)',
              annotations=make_annotations(position, v_text),
              font_size=12,
              showlegend=True,
              xaxis=axis,
              yaxis=axis,
              margin=dict(l=40, r=40, b=85, t=100),
              hovermode='closest',
              plot_bgcolor='rgb(248,248,248)'
              )

fig.write_html("../Downloads/miniweb-win32-20130309/miniweb/htdocs/astar.html")


