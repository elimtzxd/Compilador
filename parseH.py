import nltk
from nltk.tree import Tree
import pickle
import json




def tree_to_json(tree):
    result = {}
    result['name'] = tree.label()
    result['children'] = []

    for subtree in tree:
        if isinstance(subtree, nltk.Tree):
            child = tree_to_json(subtree)
            result['children'].append(child)
        else:
            leaf = {'name': subtree}
            result['children'].append(leaf)

    return result
def tree_to_json2(tree):
    result = {}
    result['name'] = tree.label()

    if isinstance(tree, nltk.Tree) and len(tree) > 0:
        result['children'] = []

        for subtree in tree:
            if isinstance(subtree, nltk.Tree):
                child = tree_to_json2(subtree)
                result['children'].append(child)
            else:
                leaf = {'name': subtree}
                result['children'].append(leaf)
    else:
        result['children'] = []

    return result

def convert_to_json(tree):
    json_tree = tree_to_json2(tree)
    # Guardar el árbol serializado en un archivo
    file_path = "tree_data.json"
    with open(file_path, "w") as file:
        json.dump(json_tree,file)

# Serializar el árbol utilizando pickle
#serialized_tree = pickle.dumps(tree)
#json_tree = tree._pprint_flat("", "()", False)
##################################
#      Example    ###############

