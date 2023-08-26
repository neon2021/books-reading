from typing import List

class Pair:
    def __init__(self, element:str, priority:int):
        self.element = element
        self.priority = priority

    def __str__(self):
        return f'{{element={self.element},priority={self.priority}}}'

class DHeap:
    def __init__(self, pairs:List[Pair]) -> None:
        self.pairs = pairs

    def __str__(self):
        return ','.join([str(pair) for pair in self.pairs])

dheap_obj = DHeap([Pair('a',1), Pair('x',99)])
print('dheap_obj: ',dheap_obj)