# algorithm visualizer

two short python scripts that generate interactive graphs that can be used to help visualize the control flow of a couple search algorithms.

at a later date I will probably turn this into a more generalized tool that can be used to visualize the statespaces and traversal path of any algorithm and perhaps program memory, using tools like ctypes and reclass. I should also probably redo astar_visualizer at some point, given that I can make the code much better now that I am familiar with the libraries.


since I think this actually has some potential to be interesting I think I might keep with it. I guess the road map would be something along the lines of:

### todo:
  - modularize the graphing and tree functionalities
    - ideally a user would be able to implement the funcionality on preexisting code by providing a function reference, and specifying which objects need to be turned into nodes.
  - implement more options for graph display and perhaps a localized viewer using chromium libraries or something (no more webserver) 
  - create ctypes compatiable anytree node objects so it can visualize the execution state of an algorithm in C++ by passing constructor addresses to and a function pointer. 
  - make the graphs it generates look less bad

## to cover dependancies  run 

```
pip install lxml igraph plotly anytree pandas
```


## tested on:
  
  - Microsoft Windows 10 Pro Version 10.0.19044 Build 19044 and python 3.10.4



## resources used:

  - https://www.researchgate.net/publication/320386988_Tutorial_Igraph_with_Python

  - https://pypi.org/project/anytree/

  - https://plotly.com/python/tree-plots/



