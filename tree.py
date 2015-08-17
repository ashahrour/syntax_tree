import re
import sys
from node import Node


class NodeIDAbsentError(Exception):
    """Exception throwed if a node's identifier is unknown"""


class DuplicatedNodeIdError(Exception):
    """Exception throwed if an identifier already exists in a tree."""

feat_names = ['pos', 'prc0', 'prc1', 'prc2', 'prc3', 'per', 'asp', 'stt', 'cas',
              'vox', 'mod', 'gen', 'num', 'enc0', 'rat']


def getFeatures(line, feat_names):
    feat_vals = [''] * len(feat_names)
    for i in range(len(feat_names)):
        regex_patt = r'(' + re.escape(feat_names[i]) + r')(:)(\S*)'
        match = re.search(regex_patt, line)
        feat_vals[i] = match.group(3)

    return feat_vals


class Tree(object):
    """Tree objects are made of Node(s) stored in _nodes dictionary."""

    def __init__(self):

        # dictionary, identifier: Node object
        self._nodes = {}
        # identifier of the root node (currently 0)
        self.root = '0'
        # number of nodes
        self.node_count = 0

        self['ROOT'] = Node('ROOT', 'ROOT', 'ROOT')
        self['BOS'] = Node('BOS', 'BOS', 'BOS', next='EOS')
        self['EOS'] = Node('EOS', 'EOS', 'EOS', prev='BOS')
        # make BOS a child of ROOT
        self['BOS'].parent = 'ROOT'
        self['ROOT'].add_child('BOS')
        # make EOS a child of ROOT
        self['EOS'].parent = 'ROOT'
        self['ROOT'].add_child('EOS')

    def __getitem__(self, key):
        """Return _nodes[key]"""
        try:
            return self._nodes[key]
        except KeyError:
            raise NodeIDAbsentError("Node '%s' is not in the tree" % key)

    def __len__(self):
        """Return len(_nodes)"""
        return len(self._nodes)

    def __setitem__(self, key, item):
        """Set _nodes[key]"""
        self._nodes.update({key: item})

    def __str__(self):
        for nid in self._nodes:
            print self[nid]
        return " "

    def update_parent(self, nid, parent_id):
        # update parent pointer
        self[nid].parent = parent_id
        # remove child pointer form the parent
        self[parent_id].remove_child(nid)

    # def set_children(self, nid, children_ids):
    #     self[nid].children = children_ids
    #
    # def add_child(self, nid, child_id):
    #     self[nid].add_child(child_id)
    #
    # def remove_child(self, nid, child_id):
    #     self[nid].remove_child(child_id)

    def add_node(self, node, parent=None, rel=None):
        """
        Add a new node to tree under a specific parent.
        The 'node' argument refers to an instance of Class::Node
        """
        if not isinstance(node, Node):
            raise OSError("First parameter must be object of Class::Node.")

        if node.identifier in self._nodes:
            raise DuplicatedNodeIdError("Can't create new node "
                                        "with ID '%s'" % node.identifier)

        # if parent == '0':
        #     self.roots.append(node.identifier)

        self._nodes.update({node.identifier: node})  # add the node to the _nodes dictionary
        self.node_count +=1
        self[node.identifier].parent = parent  # child's pointer to parent
        self[node.identifier].relation = rel  # child's relation with parent
        # if parent != '0':
        #     self[parent].add_child(node.identifier) # parent's pointer to child

    def contains(self, nid):
        """Check if the tree contains node of given id"""
        return True if nid in self._nodes else False

    def create_node(self, id=None, tag=None, pos=None, parent=None, rel=None, features=None):
        """Create a child node for given parent node."""
        #  (identifier, tag, loc, next, prev, pos, features)
        node = Node(id, tag, id, str(int(id)+1), str(int(id)-1), pos, features)  # TODO: EOS, BOS
        self.add_node(node, parent, rel)
        return node

    def read_tree_catib(self, sen_arr):
        # format = ['id', 'tag', 'POS_Catib', 'POS_Catibex', 'parent', 'relation', 'features']
        for word_line in sen_arr:
            word_arr = word_line.split('\t')
            # print word_arr[0], word_arr[1]
            if not word_arr[6].startswith('Nil'):
                word_features = getFeatures(word_arr[6], feat_names)
            else:
                word_features = ['Nil']*len(feat_names)
            features = dict(zip(feat_names, word_features))
            self.create_node(word_arr[0], word_arr[1], word_arr[2], word_arr[4], word_arr[5], features)

        # create pointers to children
        for nid in self._nodes: # TODO: children list should be sorted
            parent_id = self[nid].parent
            if parent_id != '0':
                self[parent_id].add_child(nid)  # parent's pointer to child

    def read_tree_catibex_gold(self, sen_arr):
        # format = ['id', 'tag', 'POS_Catibex', 'parent', 'relation', 'POS_catib', 'features']
        for word_line in sen_arr:
            word_arr = word_line.split('\t')
            # print word_arr[0], word_arr[1], word_arr[6]
            feat = word_arr[6].replace('[', '').replace(']', '').split(',')
            features = {'WORD': feat[0].replace('WORD:', ''),
                        'LEXEME': feat[1].replace('LEXEME:', ''),
                        'pos': feat[-1].replace('\n', ''),  # catib/penn/bw
                        'catibex': word_arr[2],
                        'full_features': word_arr[6].replace('\n','')}
            # print word_arr[0], features
            #                 id=None,    tag=None,     pos=None, parent=None,   rel=None,    features=None
            self.create_node(word_arr[0], word_arr[1], word_arr[5], word_arr[3], word_arr[4], features)

        # create pointers to children
        for nid in self._nodes:  # TODO: children list should be sorted
            parent_id = self[nid].parent
            if parent_id != '0':
                self[parent_id].add_child(nid)  # parent's pointer to child

    def al_extension(self):
        pass
        # for node in self._nodes: if det: new node add child
        # for nid in range(1,self.node_count+1):
        #     if self[str(nid)].features['pos'].find('/DET+') > -1: # found Al+
        #         # shift nodes IDs for the nodes after
        #         for nid2 in range(self.node_count, nid, -1):
        #             self[str(nid2)] = self[str(nid2-1)]
        #
        #         # create new node for the Al+ and add it at the same location
        #         self.create_node(str(nid), 'Al+', 'PRT', str(nid+1), 'MOD',
        #                          {'WORD':'Al+', 'LEXEME':'', 'pos':'PRT/DT+/DET+', 'full_features':'[WORD:Al+,LEXEME:,PRT/DT+/DET+]', 'catibex': 'PRTDTR'})

    def location_map(self):
        # generate the locations for nodes by traversing the tree
        pass

    def write_tree_catib(self):
        id_list = list(self._nodes.viewkeys())  # TODO: use location_map function to update locations
        id_list.sort(key=int)
        for nid in id_list:
            print '\t'.join([self[nid].identifier, self[nid].tag, self[nid].pos, self[nid].parent, self[nid].relation])+'\t',
            if self[nid].features['pos'] == 'Nil':
                print 'Nil'
            else:
                for feature in feat_names:
                    print feature+':'+self[nid].features[feature],
                print

    def write_tree_catibex_gold(self):
        id_list = list(self._nodes.viewkeys())
        id_list.sort(key=int)
        for nid in id_list:
            print '\t'.join([self[nid].identifier, self[nid].tag, self[nid].features['catibex'],
                             self[nid].parent, self[nid].relation, self[nid].pos, self[nid].features['full_features']])
            # for feature in feat_names:
            #     print feature+':'+self[nid].features[feature],
            # print

    def write_tree_ud(self):
        # format = ['id', 'form', 'lemma', 'POS_UD', 'POS', 'features', 'head', 'relation_UD', 'DEPS', 'MISC']
        #                            ?        ?                                       ?          ?        ?
        id_list = list(self._nodes.viewkeys())
        id_list.sort(key=int)
        for nid in id_list:
            print '\t'.join([self[nid].identifier, self[nid].tag, '_', '_', self[nid].pos])+'\t',
            if self[nid].features['pos'] == 'Nil':
                print 'Nil',
            else:
                for feature in feat_names[0:-1]:
                    # print feature+'='+self[nid].features[feature]+'|',
                    sys.stdout.write(feature.capitalize()+'='+self[nid].features[feature].capitalize()+'|')
                print feat_names[-1].capitalize()+'='+self[nid].features[feat_names[-1]].capitalize()+'\t',
            print '\t'.join([self[nid].parent, self[nid].relation, '_', '_'])

# t = Tree()
# print t
# t.create_node('1','qAl','verb','0','---', {"cas":"n", "stt":"i"})
# t.create_node('2','qAl2','noun','1','sub', {"cas":"n", "stt":"i"})
# print t['1']
# print t['2']

# n = Node("Harry", "harry" )
# n.parent = "test"
# n.children = ["fdsa"]
# # n._parent = "test2"
# print n.parent
# print n._parent
# print n._children
