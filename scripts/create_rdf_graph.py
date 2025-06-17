import sys
from modules.graph_creator.graph_creator import GraphCreator

sys.path.append("modules/graph_creator")

## THIS DIRECTORY DOESN'T SEEM TO EXIST... I don't know where python search the files 
gc = GraphCreator("../../data/public-reports")
gc.createGraph()
