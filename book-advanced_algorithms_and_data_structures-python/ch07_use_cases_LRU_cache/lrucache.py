from collections import deque

def moveNodeToFront(node, deque0: deque):
    willMoveToHead = node
    deque0.remove(willMoveToHead)
    deque0.insert(0, willMoveToHead)

def addFront(node, deque0: deque):
    deque0.insert(0, node)
    return node

def previous(node, deque0: deque):
    node_idx = deque0.index(node)
    if node_idx == 0:
        return None
    return deque0[node_idx-1] # deque0.get(node_idx-1)

def setNextAsNull(node, deque0: deque):
    pass

# Listing 7.1 LRU cache construction
class LRUCache:
    def __init__(self, maxElements):
        self.maxSize = maxElements
        self.hashTable = dict() # hashTable = new HashTable(maxElements)
        # refer to: https://www.geeksforgeeks.org/python-library-for-linked-list/
        self.elements = deque() # elements = new LinkeList()
        self.elementsTail = None
    
    def set(self, key, value):
        if key in self.hashTable:
            node = self.hashTable.get(key)
            node[1] = value # node.setValue(value)
            moveNodeToFront(node, self.elements) # elements.moveToFront(node)
            return False
        elif len(self.hashTable) >= self.maxSize: # self.getSize() >= self.maxSize
            self.evictOneEntry()
        newNode = addFront((key, value), self.elements) # newNode = elements.addFront(key, value)
        self.hashTable[key] = newNode
        if self.elementsTail is None:
            self.elementsTail = newNode
        return True
    
    # Listing 7.3 LRU cache evictOneEntry (private mehtod)
    def evictOneEntry(self):
        if len(self.hashTable)==0:
            return False
        node = self.elementsTail
        
        ## self.elementsTail = previous(node, self.elements)
        ## if self.elementsTail is not None:
        ##     setNextAsNull(self.elementsTail, self.elements)
        self.elements.pop()

        del self.hashTable[node[0]] # hashTable.delete(node.getKey())
        return True

    def get(self, key):
        node = self.hashTable[key]
        if node is None:
            return None
        else:
            return node[1] # return node.getValue()

if __name__=='__main__':
    lru_cache = LRUCache(3)
    print(f'lru_cache.elements: {lru_cache.elements}, lru_cache.hashTable: {lru_cache.hashTable}')

    for i in range(3):
        lru_cache.set(chr(ord('a')+i),1+i)
    print(f'after insert 3 chars, lru_cache.elements: {lru_cache.elements}, lru_cache.hashTable: {lru_cache.hashTable}')

    for i in range(1):
        lru_cache.set(chr(ord('x')+i),1+i)
    print(f'after insert "x", lru_cache.elements: {lru_cache.elements}, lru_cache.hashTable: {lru_cache.hashTable}')