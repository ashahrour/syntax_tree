#!/usr/bin/env python
#asasa   
#mistake
class Node(object):

    # A Node object is stored inside the _nodes dictionary of a Tree object.

    def __init__(self, identifier=None, tag=None, loc=None, next=None, prev=None, pos=None, features=None):

        self.identifier = identifier
        self.tag = tag
        self.loc = loc
        # self.word_form = tag # extra for now
        self.next = next
        self.prev = prev
        self.pos = pos
        self.features = features

        #: identifier of the parent :
        self._parent = None

        self.relation = None

        # identifier(s) of the child(ren) including self.identifier
        # Sorted based on the locations of words
        self._children = list()
        self.add_child(self.identifier)

    def __str__(self):
        print 'id = ',self.identifier
        print 'word_form = ',self.tag
        print 'location = ',self.loc
        print 'parent = ',self.parent
        print 'relation = ',self.relation
        print 'next = ',self.next
        print 'prev = ',self.prev
        print 'pos = ',self.pos
        print 'features = ',self.features
        print 'children = ',self.children
        return " "

    @property
    def parent(self):
        """return the value of _parent; see below for the setter"""
        return self._parent

    @parent.setter
    def parent(self, nid):
        """set the value of _parent; see above for the getter"""
        self._parent = nid

    @property
    def children(self):
        """return the value of _children; see below for the setter"""
        return self._children

    @children.setter
    def children(self, value):
        """set the value of _children; see above for the getter"""
        if value is None:
            self._children = list()
        elif isinstance(value, list):
            self._children = value
        elif isinstance(value, dict):
            self._children = list(value.keys())
        elif isinstance(value, set):
            self._children = list(value)
        else:
            pass


    def is_leaf(self):
        """return True if the the current node has no son"""
        if len(self.children) == 0:
            return True
        else:
            return False

    def is_root(self):
        """return True if self has no parent"""
        return self._parent == None

    # def update_parent(self, nid):
    #     # update parent pointer and remove child pointer form the parent
    #     self.parent = nid
    #
    # def update_children(self, nid, mode=ADD):
    #     """set _children recursively"""
    #     if nid is None:
    #         return
    #
    #     if mode is self.ADD:
    #         self._children.append(nid)
    #     elif mode is self.DELETE:
    #         if nid in self._children:
    #             self._children.remove(nid)
    #     elif mode is self.INSERT:  # deprecate to ADD mode
    #         print("WARNNING: INSERT is deprecated to ADD mode")
    #         self.update_children(nid)

    def add_child(self, nid): # TODO: add child in the proper location
        # add child and sort the list
        self._children.append(nid)
        # self._children.sort(key=int)

    def remove_child(self, nid):
        self._children.remove(nid)

if __name__ == '__main__':
    pass
    # n = Node("Harry", "harry")
    # n.parent = "test"
    # n.children = ["fdsa"]
    # # n._parent = "test2"
    # print n.parent
    # print n._parent
    # print n._children
