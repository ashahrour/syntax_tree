from tree import Tree


def read_catib(in_file):

    trees_arr = []
    eof = False
    while not eof:
        line = 'init line'
        sent_arr = []  # array of tokens in one sentence

        # read one sentence at a time
        while not line == '\t\n':  # currently, empty lines have a tab in the beginning
            line = in_file.readline()
            if not line:  # reached EOF
                eof = True
                break
                # if len(sent_arr)>1:
                #     t = Tree()
                #     t.read_tree_catib(sent_arr[0:-1])
                # raise SystemExit
            sent_arr.append(line)

        t = Tree()
        t.read_tree_catib(sent_arr[0:-1])  # last element is an empty line
        trees_arr.append(t)

    return trees_arr


def read_catibex_gold(in_file):

    trees_arr = []
    eof = False
    while not eof:
        line = 'init line'
        sent_arr = []  # array of tokens in one sentence

        # read one sentence at a time
        while not line == '\n':  # empty lines separates sentences
            line = in_file.readline()
            if not line:  # reached EOF
                eof = True
                break

            sent_arr.append(line)

        t = Tree()
        t.read_tree_catibex_gold(sent_arr[0:-1])  # last element is an empty line
        trees_arr.append(t)

    return trees_arr


def al_ext(trees_arr):

    for tree in trees_arr:
        tree.al_extension()


def write_catib(trees_arr):

    for tree in trees_arr:
        tree.write_tree_catib()
        print  # '\t'

def write_catibex_gold(trees_arr):

    for tree in trees_arr:
        tree.write_tree_catibex_gold()
        print  # '\t'

def write_ud(trees_arr):

    for tree in trees_arr:
        tree.write_tree_ud()
        print  # '\t'


if __name__ == '__main__':
    input_file = open('ATB123_dev.catibex', 'r')
    t_arr = read_catibex_gold(input_file)
    # print t_arr[-1]
    al_ext(t_arr)
    write_catibex_gold(t_arr)
