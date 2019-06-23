class node(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

tree = [node("grandmother", [ node("daughter", [ node("granddaughter"), node("grandson")]), node("son", [ node("granddaughter"), node("grandson")]) ])];

def familyValues(targetName, siblings = []):
    family = []
    for sibling in siblings:
        if sibling.value == targetName:
            family.append(sibling)
            family = family + sibling.children
            break
        else:
            children = familyValues(targetName, sibling.children)
            if len(children) > 0:
                children.append(sibling)
                family = children

    return family

myFamily = familyValues('daughter', tree)
for sibling in myFamily:
    print(sibling.value)
