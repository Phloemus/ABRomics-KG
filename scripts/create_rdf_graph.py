import sys
import os

from modules.graph_creator.graph_creator import GraphCreator

if not os.path.exists("data/rdf"):
    os.makedirs("data/rdf")

gc = GraphCreator(reportDirectory = "data/public-reports", cacheDirectory = "data/cache")
gc.createGraph(templatePath = "modules/graph_creator/", outputPath = "data/rdf")

