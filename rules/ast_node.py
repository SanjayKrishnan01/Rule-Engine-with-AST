class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.type == "operator":
            return f"({self.value} {self.left} {self.right})"
        else:
            return str(self.value)