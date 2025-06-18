from rdflib import Graph
from rdflib import compare

def merge(output_path, *sources):
    kg = Graph()

    for source in sources:
        print("Merging Start: {}".format(source))
        for file in source.iterdir():
            kg.parse(file, format="nt")
            kg.serialize(output_path, format="nt")

    print("Merging End!")

def isEqual(g1, g2):
    kg1 = Graph().parse(g1, format="nt")
    kg2 = Graph().parse(g2, format="nt")
    return compare.isomorphic(kg1, kg2)

def diff(g1, g2):
    kg1 = Graph().parse(g1, format="nt")
    kg2 = Graph().parse(g2, format="nt")
    return compare.graph_diff(kg1, kg2)