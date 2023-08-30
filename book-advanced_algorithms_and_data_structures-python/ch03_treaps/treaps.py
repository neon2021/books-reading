# work_date: 2023_08_29_Tue begin
# Table 3.1
class SortePriorityQueue:
    def __init__(self):
        pass

    # def top(self):
    #     pass

# Listing 3.1 Class Node and Treap
class Node:
    # ERR-20230829-01: refer to: https://segmentfault.com/a/1190000040864758
    # ERR-20230829-01: compilation nerror: def __init__(self, key:str, priority:float, left:Node=None, right:Node=None, parent:Node=None):
    def __init__(self, key:str, priority:float, left:"Node"=None, right:"Node"=None, parent:"Node"=None):
        self.key=key
        self.priority=priority
        self.left=left
        self.right=right
        self.parent=parent

    def setLeft(self, node:"Node"):
        self.left = node
        if node != None:
            node.parent = self

    def setRight(self, node:"Node"):
        self.right = node
        if node != None:
            node.parent = self

    def isRoot(self):
        return self.parent is None

class Treap:
    def __init__(self, root:Node=None):
        self.root = root

    def rightRotate(self, x:Node):
        if x is None or x.isRoot():
            raise Exception('cannot rotate null or root node')
        
        y = x.parent
        if y.left != x:
            raise Exception('x.parent.left is not x')
        
        p = y.parent
        if p is not None:
            if p.left == y:
                p.setLeft(x)
            else:
                p.setRight(x)
        else:
            self.root = x
        y.setLeft(x.right)
        x.setRight(y)

    def leftRotate(self, x:Node):
        if x is None or x.isRoot():
            raise Exception('cannot rotate null or root node')
        
        y = x.parent
        if y.right != x:
            raise Exception('x.parent.right is not x')
        
        p=y.parent
        if p is not None:
            if p.left == y:
                p.setLeft(x)
            else:
                p.setRight(x)
        else:
            self.root = x
        y.setRight(x.left)
        x.setLeft(y)

    def search(self, node:Node, targetKey:str)->Node:
        if node is None:
            return None
        
        if node.key == targetKey:
            return node
        elif targetKey<node.key:
            return search(node.left, targetKey)
        else:
            return search(node.right, targetKey)
# work_date: 2023_08_29_Tue end
# test editing ????

# work_date: 2023_08_30_Wed begin
# Listing 3.5
    def insert(self, key:str, priority:float):
        node = self.root
        parent = None
        newNode = Node(key, priority)
        while node is not None:
            print('t: node.key: ',node.key)
            parent = node
            # if node.key <= key: # error
            if key < node.key: # fixed
                print('t: left: ',node.left)
                node = node.left
            else:
                print('t: right: ',node.right)
                node = node.right
        if parent is None:
            self.root = newNode
            return
        elif key <= parent.key:
            parent.left = newNode
        else:
            parent.right = newNode
        newNode.parent = parent

        print('after newNode added: ',treap)

        while newNode.parent is not None and newNode.priority<newNode.parent.priority:
            if newNode==newNode.parent.left:
                self.rightRotate(newNode)
            else:
                self.leftRotate(newNode)
        if newNode.parent is None:
            self.root = newNode

    def traverse(self, layerIdx:int, node:Node)->str:
        if node is None:
            return '<null>'
        return f'{node.key}' \
                + f'\n{" "*layerIdx}L{layerIdx} ' + self.traverse(layerIdx+1, node.left) \
                + f'\n{" "*layerIdx}R{layerIdx} ' + self.traverse(layerIdx+1, node.right)

    def __str__(self):
        node = self.root
        return self.traverse(1, node)
            
    # def remove(self, key:str):
    #     node = self.search(treap.root, key)
    #     if node is None

if __name__ == '__main__':
    treap = Treap(Node('A',1))
    treap.insert('B',2)
    print(f'treap:\n{treap}')

    treap.insert('C',3)
    print(f'treap:\n{treap}')

# work_date: 2023_08_30_Wed end
