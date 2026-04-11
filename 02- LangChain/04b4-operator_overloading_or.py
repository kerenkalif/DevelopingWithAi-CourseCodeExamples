class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return (f"{self.value} --> {self.next if self.next else "END"}")

    def __or__(self, other):
        print(f"DEBUG: {self} --> {other}")
        self.next = other
        return other

n1 = Node("Requirements")
n2 = Node("Design")
n3 = Node("Coding")
n4 = Node("Testing")
#n1 | n2  | n3 | n4
n1 | n2
n2 | n3
n3 | n4
print(n1)
