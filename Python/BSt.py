class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key

def insert(root, key):
    if root is None:
        return Node(key)
    elif root.value == key:
        return root
    elif root.value < key:
        root.right = search(root.right, key)
    else:
        root.left = search(root.left, key)
    return root
    
def search(root, key):
    if root.value is None:
        return None
    elif root.value == key:
        return root
    elif root.value < key:
        return search(root.right, key)
    else:
        return search(root.left, key)
    return root


def inorder(root):
    if root:
        inorder(root.left)
        print(root.value)
        inorder(root.right)

