from random import randint

class Node():
    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right
        if data == None :
            raise ValueError("Node of None value")
        
    def height(self):
        if (self.left == None) and (self.right == None):
            return(0)
        elif ((self.left == None) and (self.right != None)) or ((self.left != None) and (self.right == None)):
            raise ValueError("Subtrees should have the same height.")
        elif self.left.height() != self.right.height() : #Les valeurs des arbres ne sont pas None, on peut accéder à left.height et right.height
            raise ValueError("Subtrees should have the same height.")
        else :
            return(self.left.height() + 1)
            
    def to_list(self):
        if (self.left == None) and (self.right == None):
            return([self.data])
        else :
            return([self.data] + self.left.to_list() + self.right.to_list())
                    
    def __contains__(self, item):
        if self.data == item :
            return(True)
        if self.left != None :
            return((item in self.left) or (item in self.right))
        return(False)
    
    def __len__(self):
        return(2**(self.height() + 1) - 1)
    
    def __getitem__(self, key):
        if (key >= len(self)) or (key < 0):
            raise IndexError("Complete tree index out of range.")
        else :
            if key == 0:
                return(self.data)
            if key <= (len(self) - 1)//2:
                return(self.left[key-1])
            else :
                return(self.right[key - 1 - len(self)//2])

def random_tree(n):
    if n == 1:
        return(Node(randint(1,1000)))
    else:
        return(Node(randint(1, 1000),
                    random_tree(n-1),
                    random_tree(n-1)))

if __name__ == "__main__":
    a1 = Node(92)
    a2 = Node(34, Node(23), Node(11))
    a3 = Node(28,
              Node(40, Node(33), Node(12)),
              Node(27, Node(7), Node(55)))
    """
    b1 = Node(28, Node(18))
    b2 = Node(49, None, Node(3))
    b3 = Node(36, 
              Node(34, Node(13), Node(44)), 
              Node(22))
    """
    c = random_tree(10)
    assert a1.to_list() == [92]
    assert a2.to_list() == [34,23,11]
    assert a3.to_list() == [28,40,33,12,27,7,55]

    assert 0 not in a1
    assert 33 in a3

    assert len(a1) == 1
    assert len(a2) == 3
    assert len(a3) == 7

    assert a1[0] == 92
    assert a2[2] == 11
    assert a3[5] == 7
    print("Tout s'est bien passé")


