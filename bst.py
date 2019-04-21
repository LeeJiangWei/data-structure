import  queue

class Node:

    def __init__(self, key=None, left_child=None, right_child=None):
        self.__key = key
        self.__lc = left_child
        self.__rc = right_child

    def is_leaf(self):
        return (self.__lc is None) and (self.__rc is None)

    def left(self):
        return self.__lc

    def right(self):
        return self.__rc

    def set_left(self, left_child):
        self.__lc = left_child

    def set_right(self, right_child):
        self.__rc = right_child

    def set_key(self, key):
        self.__key = key

    def get_key(self):
        return self.__key


class BST:

    def __init__(self, root=None):
        self.__root = root
        self.__node_count = 0

    def __clear_help(self, root):
        if root is None:
            return
        self.__clear_help(root.left())
        self.__clear_help(root.right())
        del root

    def __insert_help(self, root, key):
        if root is None:
            return Node(key)
        if key < root.get_key():
            root.set_left(self.__insert_help(root.left(), key))
        else:
            root.set_right(self.__insert_help(root.right(), key))
        return root

    def __delete_min(self, root):
        if root.left() is None:
            return root.right()
        else:
            root.set_left(self.__delete_min(root.left()))
            return root

    def __get_min(self, root):
        if root.left() is None:
            return root
        else:
            return self.__get_min(root.right())

    def __remove_help(self, root, key):
        if root is None:
            return None
        elif key < root.get_key():
            root.set_left(self.__remove_help(root.left(), key))
        elif key > root.get_key():
            root.set_right(self.__remove_help(root.right(), key))
        elif root.left() is None:
            root = root.right()
        elif root.right() is None:
            root = root.left()
        else:
            temp = self.__get_min(root.right())
            root.set_key(temp.get_key())
            root.set_right(self.__delete_min(root.right()))
            del temp
        return root

    def __find_help(self, root, key):
        if root is None:
            return None
        if key < root.get_key():
            return self.__find_help(root.left(), key)
        elif key > root.get_key():
            return self.__find_help(root.right(), key)
        else:
            return root.get_key()

    def __print_help(self, root, level):
        if root is None:
            return
        self.__print_help(root.left(), level+1)
        for i in range(level):
            print(" ", end="")
        print(root.get_key())
        self.__print_help(root.right(), level+1)

    def __get_depth(self, root):
        if root is None:
            return 0
        return 1 + max(self.__get_depth(root.left()),
                       self.__get_depth(root.right()))

    def clear(self):
        self.__clear_help(self.__root)
        self.__root = None
        self.__node_count = 0

    def insert(self, key):
        self.__root = self.__insert_help(self.__root, key)
        self.__node_count += 1

    def remove(self, key):
        temp = self.__find_help(self.__root, key)
        if temp is not None:
            self.__root = self.__remove_help(self.__root, key)
            self.__node_count -= 1
        return temp

    def find(self, key):
        f = self.__find_help(self.__root, key)
        if f is None:
            print(key, "is not in this BST.")
        return f

    def size(self):
        return self.__node_count

    def print(self):
        if self.__root is None:
            print("The BST is empty.")
        else:
            self.__print_help(self.__root, 0)

    def __print_graph_help(self, que, num, m):

        for i in range(num):
            temp = que.get()

            for j in range(int(m/(num+1))):
                print(" ", end="")
            if temp is not None:
                print(temp.get_key(), end="")

                que.put(temp.left())
                que.put(temp.right())
            else:
                print(" ", end="")
                que.put(None)
                que.put(None)

        print("")

    # print the tree level by level, but still not perfect
    def print_graph(self):
        depth = self.depth()
        max_spaces = 2**depth * 2
        number = 1
        q = queue.Queue()
        q.put(self.__root)
        for i in range(depth+1):
            self.__print_graph_help(q, number, max_spaces)
            number *= 2

    def depth(self):
        return self.__get_depth(self.__root)-1

from numpy import random as nr

size = 4
keys = nr.randint(0, 20, [size])
tree = BST()

for i in range(size):
    tree.insert(i)
for i in range(1, size):
    tree.insert(-i)

tree.insert(0.5)
tree.insert(1.5)
# tree.print()

tree.print_graph()