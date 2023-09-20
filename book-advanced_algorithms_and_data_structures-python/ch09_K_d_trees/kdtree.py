import math
from typing import List
import datetime

# refer to: https://stackoverflow.com/a/62429374
#
# step 1: use sys.path to know the base path for importing modules
# step 2: add PYTHONPATH to env configuration in launch.json
#
import sys
print(f'sys.path: {sys.path}')
# first element of output is:
# 'book-advanced_algorithms_and_data_structures-python.ch09_K_d_trees'

# refer to: http://stackoverflow.com/a/7583738
#
# this solution could tackle with the module path that contains hyphens or underscores
#
# bpq_module = __import__("bounded_priority_queue")
# print(f'bpq_module: {bpq_module}')
# # import importlib
# # bpq_module = importlib.import_module("book-advanced_algorithms_and_data_structures-python.ch09_K_d_trees.bounded_priority_queue")
# bpq = bpq_module.BoundedPriorityQueue
# print(f'bpq: {bpq}')

from bounded_priority_queue import BoundedPriorityQueue
bpq = BoundedPriorityQueue(3)
print(f'bpq: {bpq}')

# Listing9.1 The KdTree class
GLOBAL_K = 2

class KdNode:
    def __init__(self, name:str, point:tuple, left:"KdNode", right:"KdNode", level:int):
        self.name = name
        self.point = point
        self.left = left
        self.right = right
        self.level = level

    def __str__(self):
        indent = self.level * '      '
        return f'\n{indent}\'{self.name}\'{self.point},level={self.level}'+ \
        (f'\n{indent}left={self.left},' if self.left else '')+ \
        (f'\n{indent}right={self.right},' if self.right else '')

class KdTree:
    def __init__(self, root:KdNode, k:int=GLOBAL_K):
        self.root = root
        self.k = k

    def __str__(self):
        return f'root={{{self.root}}},k={self.k}'

# Listing 9.2 Helper functions
def getNodeKey(node:KdNode)->float:
    '''Gets the value of the coordinate respecting to node.level

    Parameters
    ----------
    node : KdNode

    Returns
    -------
    float
        the value of the specific coordinate
    '''
    return getPointKey(node.point, node.level)

def getPointKey(point:tuple, level:int)->float:
    '''
    parameters: point - the coordinates of the point
                level - the level of the point's node in a tree
    returns: the value of the point's coordinate which is related to the point's level in the tree
    '''
    j = level % GLOBAL_K
    return point[j]

# refer to: https://stackoverflow.com/questions/1986152/why-doesnt-python-have-a-sign-function/41411231#41411231
#
# the code of cmp and sign from SO comments
def cmp(a, b):
    return (a>b)-(a<b)

def sign(x):
    return (x>0)-(x<0)

def compare(point:tuple, node:KdNode):
    '''
    parameters: point - 
                node  -
    returns:
        compare the value of the coordinate of point and node.point
        and the coordinate is calculated by the level of the node
    '''
    print(f'{five_dots}from reference docs, compare{five_dots}')
    return cmp(getPointKey(point, node.level), getNodeKey(node))

def splitDistance(point:tuple, node:KdNode):
    """ Calculate the shortest distance between the point and the splitting line of node

    Parameters
    ----------
    point   : tuple

    node    : KdNode which splits the rectangular area

    Returns
    -------
    float
        the shortest distance
    """
    return abs(getPointKey(point, node.level)-getNodeKey(node))

# Listing 9.3 The search method
def search(node:KdNode, target:tuple):
    if node is None:
        return None
    elif node.point == target:
        return node
    elif compare(target, node) < 0:
        return search(node.left, target)
    else:
        return search(node.right, target)

# Listing 9.4 The insert method
def insert(node:KdNode, name:str, newPoint:tuple, level:int=0):
    print(f'insert> newPoint={newPoint},level={level}')
    if node is None:
        return KdNode(name,newPoint,None,None,level)
    elif node.point == newPoint:
        return node
    elif compare(newPoint, node) < 0:
        node.left=insert(node.left,name,newPoint,node.level+1)
        return node
    else:
        node.right=insert(node.right,name,newPoint,node.level+1)
        return node

five_dots='.'*5
# Listing 9.5 Revised compare
def compare(point:tuple, node:KdNode):
    print(f'{five_dots}listing 9.5 compare{five_dots}')
    s = sign(getPointKey(point, node.level) - getNodeKey(node))
    if s == 0:
        return -1 if node.level % 2 == 0 else +1
    else:
        return s

# Listing 9.6 Balanced construction
def constructKdTree(points:List["tuple"], level:int=0):
    if len(points)==0:
        return None
    elif len(points)==1:
        return KdNode('',points[0], None, None, level)
    else:
        (median, left, right) = partition(points, level)
        left_tree = constructKdTree(left, level+1)
        right_tree = constructKdTree(right, level+1)
        return KdNode('',median, left_tree, right_tree, level)

# TODO: 2023_09_15 FRI
#
# Book: Finally, line #7, where we call partition: it’s possible to find a median in linear time, and we can also partition an array of n elements around a pivot with O(n) swaps (or create two new arrays, also with O(n) total assignments).
#
# the code below uses sort function, so its performance will be not efficient
def partition(points:List[tuple], level:int=0):
    idx = level % GLOBAL_K
    # refer to: https://docs.python.org/3/howto/sorting.html
    points.sort(key=lambda p: p[idx])
    n = len(points)

    # if n=3, then left_part_size= (n-1)/2 = 1, median_index = left_part_size = 1 and right_part_size = n-left_part_size-1 = 1
    # if n=4, then left_part_size= (n-1)/2 = 1, median_index = left_part_size = 1 and right_part_size = n-left_part_size-1 = 2
    # if n=5, then left_part_size= (n-1)/2 = 2, median_index = left_part_size = 2 and right_part_size = n-left_part_size-1 = 2
    median_index = (int)((n-1)/2) # TODO: float to int
    return points[median_index], \
            points[:median_index],\
            points[median_index+1:]

    return median, \
        [p for p in points if p[idx]<median], \
        [p for p in points if p[idx]>median]

# Listing 9.7 The findMin method
def find_min(node:KdNode, coordinateIndex:int)->KdNode:
    if node is None:
        return None
    # elif node.level == coordinateIndex:
    elif node.level % GLOBAL_K == coordinateIndex: # refer to cs.cmu.edu PDF
        if node.left is None:
            return node
        else:
            return find_min(node.left, coordinateIndex)
    else:
        left_min = find_min(node.left, coordinateIndex)
        right_min = find_min(node.right, coordinateIndex)
        # return min(node, left_min, right_min) 
        # refer to: https://www.geeksforgeeks.org/find-minimum-in-k-dimensional-tree/
        return min([node, left_min, right_min],
            key=lambda x:float('inf') if x is None else x.point[coordinateIndex])

# refer to: https://www.geeksforgeeks.org/find-minimum-in-k-dimensional-tree/
# comment two methods: min2, min
#
# def min2(one:KdNode, two:KdNode)->KdNode:
#     if one is None:
#         return two
#     elif two is None:
#         return one
#     else:
#         coordinateIndex = one.level % GLOBAL_K
#         return one if one.point[coordinateIndex] < two.point[coordinateIndex] \
#                 else two


# def min(min:KdNode, left:KdNode, right:KdNode)->KdNode:
#     if min is None and left is None and right is None:
#         raise Exception("ERROR: all nodes are None")
#     return min2(min2(min, left),right)

# Listing 9.8 The remove method
def remove(node: KdNode, point:tuple)->KdNode:
    if node is None:
        return None
    elif node.point == point:
        if node.right is not None:
            # min_node = find_min(node.right, node.level)
            min_node = find_min(node.right, node.level % GLOBAL_K) # refer to cs.cmu.edu PDF
            new_right = remove(node.right, min_node.point)
            return KdNode('', min_node.point, node.left, new_right, node.level)
        elif node.left is not None:
            # min_node = find_min(node.left, node.level)
            min_node = find_min(node.left, node.level % GLOBAL_K) # refer to cs.cmu.edu PDF
            new_right = remove(node.left, min_node.point)
            return KdNode('', min_node.point, None, new_right, node.level)
        else:
            return None
    elif compare(point, node) < 0:
        node.left = remove(node.left, point)
        return node
    else:
        node.right = remove(node.right, point)
        return node

# Listing 9.9 The nearestNeighbor method
def nearest_neighbor(node:KdNode, target:tuple, nnDist=float('inf'), nn=None)->tuple:
    if node is None:
        return (nnDist, nn)
    else:
        dist = distance(node.point, target)
        if dist < nnDist:
            nnDist, nn = dist, node.point
        if compare(target, node) < 0:
            closeBranch = node.left
            farBranch = node.right
        else:
            closeBranch = node.right
            farBranch = node.left
        # Explanation on 20/09/2023:
        #
        # The two nearest_neighbor called below are very tricky.
        #
        # When the shortest distance between target and node is shorter than the nnDist found in closeBranch,
        # we should continue to check the farBranch for avoiding to miss another closer point might be in the farBranch
        #
        nnDist, nn = nearest_neighbor(closeBranch, target, nnDist, nn)
        if splitDistance(target, node) < nnDist:
            nnDist, nn = nearest_neighbor(farBranch, target, nnDist, nn)
        return nnDist, nn

def distance(point1:tuple, point2:tuple):
    return math.sqrt( \
        sum( \
            [ (point1[i]-point2[i])**2 for i in range(0,GLOBAL_K)] \
        ) \
    )

# Listing 9.10 The nNearestNeighbor method
def nNearestNeighbor(node:KdNode, target:tuple, n:int)->BoundedPriorityQueue:
    # pq = BoundedPriorityQueue(n)
    pq = BoundedPriorityQueue(k=n)
    # pq.insert((float('inf'),None))
    pq.add((float('inf'),None))
    print(f'nNearestNeighbor> target:{target}, pq.heap: {pq.heap}')
    pq = n_nearest_neighbor(node, target, pq)
    # nnnDist, _ = pq.peek()
    nnnDist = pq.max()
    print(f'nNearestNeighbor> target:{target}, pq.heap: {pq.heap}, nnnDist:{nnnDist}')
    if nnnDist == float('inf'):
        # pq.top()
        pq.extract_max()
    return pq

def n_nearest_neighbor(node:KdNode, target:tuple, pq:BoundedPriorityQueue)->BoundedPriorityQueue:
    print(f'n_nearest_neighbor> target:{target}, pq.heap: {pq.heap}')
    if node is None:
        print(f'n_nearest_neighbor> returning pq')
        return pq
    else:
        dist = distance(node.point, target)
        # pq.insert((dist, node.point))
        pq.add((dist, node.point))
        if compare(target, node) < 0:
            closeBranch = node.left
            farBranch = node.right
        else:
            closeBranch = node.right
            farBranch = node.left
        print(f'n_nearest_neighbor> target:{target}, pq.heap: {pq.heap}, closeBranch.point:{closeBranch.point if closeBranch is not None else "none"}')
        pq = n_nearest_neighbor(closeBranch,target,pq)
        # nnnDist, _ = pq.peek()
        nnnDist = pq.max()
        print(f'n_nearest_neighbor> nnnDist:{nnnDist}')
        if splitDistance(target, node) < nnnDist:
            pq=n_nearest_neighbor(farBranch, target, pq)
        return pq

if __name__ == '__main__':
    kd_node_root=KdNode('A',(0,5),None,None,0)
    kd_tree_1 = KdTree(kd_node_root)

    for name_and_point in [('B',(-1,6)),('C',(1,-1))]:
        name = name_and_point[0]
        p = name_and_point[1]
        kd_node_1=KdNode(name,p,None,None,0)
        print(f'kd_node_1: {kd_node_1}')
        insert(kd_node_root,name,p)

    print(f'\nfinal: kd_tree_1: {kd_tree_1}')

    kd_tree_2_root_node = constructKdTree([(0,5),(1,-1),(-1,6),(-0.5,0),(2,5),(2.5,3),(-1, 1),(-1.5,-2)])
    print(f'\nfinal: kd_tree_2_root_node: {kd_tree_2_root_node}')

    remove(kd_tree_2_root_node, (2.5,3))
    print(f'\nafter remove (1,-1): kd_tree_2_root_node:\n {kd_tree_2_root_node}')

    # refer to kdtrees paska13 pdf
    kd_tree_3_root_node=KdNode('A',(34,90),None,None,0)
    insert(kd_tree_3_root_node,'',(10,75))
    insert(kd_tree_3_root_node,'',(70,80))

    # build subtree of (10,75)
    insert(kd_tree_3_root_node,'',(25,10))
    insert(kd_tree_3_root_node,'',(20,50))

    # build subtree of (70,80)
    insert(kd_tree_3_root_node,'',(80,40))
    insert(kd_tree_3_root_node,'',(50,90))
    insert(kd_tree_3_root_node,'',(70,30))
    insert(kd_tree_3_root_node,'',(90,60))
    
    # build subtree of (70,30)
    insert(kd_tree_3_root_node,'',(50,25))
    # insert(kd_tree_3_root_node,'',(35,50))
    insert(kd_tree_3_root_node,'',(60,10))
    print('kd_tree_3_root_node:\n',kd_tree_3_root_node)
    #
    # show the tree in a coordinate graph, refer to: kdtees_draw_by_myself-show_a_tree_in_a_coordinate_graph.png
    
    found_closest_point = nearest_neighbor(kd_tree_3_root_node,(40,50))
    print('found_closest_point: ',found_closest_point)

    # the output result refers to the figure kdtrees_paska13_pdf-p44-nnsearch_example_ii.jpeg
    #
    # description: each element is a tuple that represents a found node, and the tuple's first element is distance between the found node and the target, and the second element is the postion of the found node.
    found_n_closest_points = nNearestNeighbor(kd_tree_3_root_node,(40,50),3)
    print('n: ',3,', found_n_closest_points: ',found_n_closest_points.heap)

    print('now: ',datetime.datetime.now())