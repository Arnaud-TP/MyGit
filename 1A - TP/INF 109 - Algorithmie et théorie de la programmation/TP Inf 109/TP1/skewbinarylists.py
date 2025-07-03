from completetrees import Node

class SkewBinaryList():
    def __init__(self, hd = None, tl = None):
        self.head = hd
        self.next = tl

    def cons(self, item):
        if self.head == None :
            self.head = Node(item)
        elif self.next == None :
            self.next = SkewBinaryList(self.head)
            self.head = Node(item)
        else :
            if type(self.next) == Node:
                if self.head.height == self.next.height : 
                    self.head = Node(item,self.head,self.next)
                    self.next = None
                else :
                    self.next = SkewBinaryList(self.head,self.next)
                    self.head = Node(item)
            else : #if type(self.next) == SkewBinaryList:
                self.head = Node(item,self.head,self.next.head)
                self.next = self.next.next
        
    def to_list(self):
        if self.next == None:
            return(self.head.to_list())
        else:
            return(self.head.to_list() + self.next.to_list())
        
    def __contains__(self, item):
        if self.head == None :
            return(False)
        elif item in self.head :
            return(True)
        elif self.next == None :
            return(False)
        else :
            return(item in self.next)

    def __len__(self):
        if self.head == None :
            return(0)
        elif self.next == None :
            return(len(self.head))
        else :
            return(len(self.head) + len(self.next))

    def __getitem__(self, key):
        if 0 <= key < len(self):
            if key <= len(self.head) - 1:
                return(self.head[key])
            key = key-len(self.head)
            if type(self.next) == Node :
                return(self.next[key])
            else : #If type(self.next) == SkewBinaryList :
                if key <= len(self.next.head) - 1:
                    return(self.next.head[key])
                else :
                    return(self.next.next[key - len(self.next.head)])
                    
        raise IndexError("Skew binary list index out of range")

    def tail(self): #Complexité en O(1)
        if self.head == None :
            raise AssertionError("Skew Binary List must not be empty")
        if len(self.head) == 1:
            if self.next == None:
                return(SkewBinaryList())
            elif type(self.next) == Node:
                return(SkewBinaryList(self.next))
            else :
                return(SkewBinaryList(self.next.head, self.next.next))
        else :
            return(SkewBinaryList(self.head.left,SkewBinaryList(self.head.right,self.next)))
    
if __name__ == "__main__":
    a2 = Node(34, Node(23), Node(11))
    a3 = Node(28,
              Node(40, Node(33), Node(12)),
              Node(27, Node(7), Node(55)))
    s1 = SkewBinaryList(a2,a3)
    assert s1.to_list() == [34,23,11,28,40,33,12,27,7,55]
    s1.cons(9)
    assert s1.to_list() == [9,34,23,11,28,40,33,12,27,7,55]
    assert 8 not in s1
    assert 9 in s1
    assert len(s1) == 11
    assert s1[0] == 9
    assert s1[2] == 23
    assert s1[10] == 55
    s2 = s1.tail()
    assert s2.to_list() == [34,23,11,28,40,33,12,27,7,55]
    print("Exécution terminée")
