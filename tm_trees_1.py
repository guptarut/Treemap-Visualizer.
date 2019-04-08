"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees
    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: Optional[str]
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: Optional[str], subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self.data_size = 0

        self._expanded = False
        for subtree in self._subtrees:
            subtree._expanded = False
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if self._subtrees == []:
            self.data_size = data_size
        else:
            for subtree in self._subtrees:
                self.data_size += subtree.data_size

        for subtree in self._subtrees:
            subtree._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def _find_non_empty_subtree(self) -> TMTree:
        """Return the first subtree from the end of the self._subtrees which is
        not empty"""
        for subtree in self._subtrees[len(self._subtrees) - 2::-1]:
            if subtree.data_size != 0:
                return subtree
        return self._subtrees[0]

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendants using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        self.rect = rect
        width = rect[0]
        height = rect[1]
        if rect[2] > rect[3] and self.data_size != 0:
            width_sum = 0
            for subtree in self._subtrees:
                if subtree != self._subtrees[-1]:
                    sub_width = math.floor(
                        (subtree.data_size / self.data_size) * rect[2])
                    subtree.rect = (width, rect[1], sub_width, rect[3])
                    width += sub_width
                    width_sum += sub_width
                    subtree.update_rectangles(subtree.rect)
                elif self._subtrees[-1].data_size != 0:
                    sub_width = rect[2] - width_sum
                    subtree.rect = (width, rect[1], sub_width, rect[3])
                    width += sub_width
                    subtree.update_rectangles(subtree.rect)
                else:
                    previous_subtree = self._find_non_empty_subtree()
                    sub_width = rect[2] - width_sum
                    previous_sub_width = previous_subtree.rect[2]
                    previous_width = previous_subtree.rect[0]
                    previous_subtree.rect = (previous_width, rect[1],
                                             previous_sub_width + sub_width,
                                             rect[3])
                    width += previous_sub_width + sub_width
                    previous_subtree.update_rectangles(previous_subtree.rect)
                    self._subtrees[-1].rect = (width, rect[1], 0, rect[3])

        elif rect[2] <= rect[3] and self.data_size != 0:
            height_sum = 0
            for subtree in self._subtrees:
                if subtree != self._subtrees[-1]:
                    sub_height = math.floor(
                        (subtree.data_size / self.data_size) * rect[3])
                    subtree.rect = (rect[0], height, rect[2], sub_height)
                    height += sub_height
                    height_sum += sub_height
                    subtree.update_rectangles(subtree.rect)
                elif self._subtrees[-1].data_size != 0:
                    sub_height = rect[3] - height_sum
                    subtree.rect = (rect[0], height, rect[2], sub_height)
                    height += sub_height
                    subtree.update_rectangles(subtree.rect)
                else:
                    previous_subtree = self._find_non_empty_subtree()
                    sub_height = rect[3] - height_sum
                    previous_sub_height = previous_subtree.rect[3]
                    previous_height = previous_subtree.rect[1]
                    previous_subtree.rect = (rect[0], previous_height, rect[2],
                                             previous_sub_height + sub_height)
                    height += previous_sub_height + sub_height
                    previous_subtree.update_rectangles(previous_subtree.rect)
                    self._subtrees[-1].rect = (rect[0], height, rect[2], 0)
        else:
            return

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.data_size == 0:
            return []
        elif self._expanded is False:
            return [(self.rect, self._colour)]
        else:
            rect_lst = []
            for subtree in self._subtrees:
                rect_lst.extend(subtree.get_rectangles())
            return rect_lst

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        if self.is_empty() or self.data_size == 0:
            return None
        elif self._expanded is False:
            if (self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]) and \
                     (self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]):
                return self
            else:
                return None
        else:
            lst = []
            for subtree in self._subtrees:
                in_rectangle = (subtree.rect[0] <= pos[0] <=
                                (subtree.rect[0] + subtree.rect[2])) and \
                               (subtree.rect[1] <= pos[1] <= (subtree.rect[1] +
                                                              subtree.rect[3]))
                if in_rectangle:
                    lst.append(subtree)
            dist_lst = []
            for item in lst:
                dist_lst.append(math.sqrt(item.rect[0] * item.rect[0] +
                                          item.rect[1] * item.rect[1]))
            for i in range(len(dist_lst)):
                if dist_lst[i] == min(dist_lst):
                    return lst[i].get_tree_at_position(pos)
            return self

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self._subtrees == []:
            return self.data_size
        else:
            data_size = 0
            for subtree in self._subtrees:
                data_size += subtree.update_data_sizes()
            self.data_size = data_size
            return data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if (self._subtrees != []) or (destination._subtrees == []):
            pass
        else:
            removed_data_size = self.data_size
            destination._subtrees.append(self)
            self._parent_tree._subtrees.remove(self)
            self._parent_tree.data_size -= removed_data_size
            destination.data_size += removed_data_size
            destination._subtrees[-1]._parent_tree = destination

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._subtrees != []:
            pass
        else:
            if factor < 0:
                new_data_size = self.data_size - \
                                math.ceil(abs(factor) * self.data_size)
                if new_data_size >= 1:
                    self.data_size = new_data_size
                elif new_data_size < 1:
                    self.data_size = 1
            else:
                new_data_size = self.data_size + \
                                math.ceil(abs(factor) * self.data_size)
                if new_data_size >= 1:
                    self.data_size = new_data_size

    def expand(self) -> None:
        """Change the value of this displayed tree's and its parent tree's
        _expanded attribute to True.
        If the tree is a leaf, do nothing"""
        if self._subtrees == []:
            pass
        else:
            self._expanded = True
            if self._parent_tree is not None:
                self._parent_tree._expanded = True

    def expand_all(self) -> None:
        """Change the value of this displayed tree's, its <_parent_tree>'s and
        all of its <_subtrees>'s _expanded attribute to True.
        If the tree is a leaf, do nothing"""
        if self._subtrees == []:
            pass
        else:
            self._expanded = True
            if self._parent_tree is not None:
                self._parent_tree._expanded = True
            for subtree in self._subtrees:
                subtree.expand_all()

    def _collapse_subtrees(self) -> None:
        """Change the value of all the displayed tree's subtrees's _expanded
        attribute to False."""
        if self._subtrees == []:
            pass
        else:
            for subtree in self._subtrees:
                subtree._expanded = False
                subtree._collapse_subtrees()

    def collapse(self) -> None:
        """Change the value of this displayed tree's <_parent_tree>'s _expanded
        attribute to False.

        If the parent of this displayed tree is None because this is the root
        of the whole tree, nothing happens."""
        if self._parent_tree is None:
            pass
        else:
            self._parent_tree._expanded = False
            for subtree in self._parent_tree._subtrees:
                subtree._expanded = False
                subtree._collapse_subtrees()

    def collapse_all(self) -> None:
        """Change the value of all the displayed tree's ancestors's _expanded
        attribute and their subtree's _expanded attribute to False.

        If the parent of this displayed tree is None because this is the root
        of the whole tree, nothing happens."""
        if self._parent_tree is None:
            pass
        else:
            self._parent_tree._expanded = False
            self._parent_tree.collapse_all()
            for subtree in self._parent_tree._subtrees:
                subtree._expanded = False
                subtree._collapse_subtrees()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        if not os.path.isdir(path):
            TMTree.__init__(self, os.path.basename(path), [],
                            os.path.getsize(path))
        else:
            lst = []
            for filename in os.listdir(path):
                subitem = os.path.join(path, filename)
                lst.append(FileSystemTree(subitem))
            TMTree.__init__(self, os.path.basename(path), lst,
                            os.path.getsize(path))

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    a = FileSystemTree('C:\\Users\\DELL\\Desktop\\Uoft Docs\\CSC148S1\\csc148\\'
                       'assignments\\a2\\example-directory')
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
