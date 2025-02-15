#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
from src.individual import FileNode, build_tree, print_tree, save_to_xml, load_from_xml


def test_build_tree():
    test_dir = "test_dir"
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, "file1.txt"), "w") as f:
        f.write("test")
    os.makedirs(os.path.join(test_dir, "subdir"), exist_ok=True)

    root = build_tree(test_dir, 0, 10, False)

    assert root.name == "test_dir"
    assert root.is_dir is True
    assert len(root.children) == 2
    assert root.children[0].name == "file1.txt"
    assert root.children[0].is_dir is False
    assert root.children[1].name == "subdir"
    assert root.children[1].is_dir is True

    os.remove(os.path.join(test_dir, "file1.txt"))
    os.rmdir(os.path.join(test_dir, "subdir"))
    os.rmdir(test_dir)


def test_save_and_load_xml():
    root = FileNode("test_dir", True)
    file_node = FileNode("file1.txt", False)
    subdir_node = FileNode("subdir", True)
    root.children.append(file_node)
    root.children.append(subdir_node)

    xml_file = "test.xml"
    root_xml = save_to_xml(root)
    tree_xml = ET.ElementTree(root_xml)
    tree_xml.write(xml_file, encoding="utf-8", xml_declaration=True)

    tree_xml = ET.parse(xml_file)
    loaded_root = load_from_xml(tree_xml.getroot())

    assert loaded_root.name == "test_dir"
    assert loaded_root.is_dir is True
    assert len(loaded_root.children) == 2
    assert loaded_root.children[0].name == "file1.txt"
    assert loaded_root.children[0].is_dir is False
    assert loaded_root.children[1].name == "subdir"
    assert loaded_root.children[1].is_dir is True

    os.remove(xml_file)


def test_print_tree(capsys):
    root = FileNode("test_dir", True)
    file_node = FileNode("file1.txt", False)
    subdir_node = FileNode("subdir", True)
    root.children.append(file_node)
    root.children.append(subdir_node)

    print_tree(root)

    captured = capsys.readouterr()
    expected_output = "/test_dir\n  file1.txt\n  /subdir\n"
    assert captured.out == expected_output


if __name__ == "__main__":
    test_build_tree()
    test_save_and_load_xml()
    test_print_tree()
