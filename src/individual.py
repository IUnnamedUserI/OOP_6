#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Выполнить индивидуальное задание лабораторной работы 4.5, использовав
классы данных, а также загрузку и сохранение данных в формат XML.
"""

import os
import argparse
import xml.etree.ElementTree as ET


class FileNode:
    """Класс для представления узла дерева (файла или папки)."""

    def __init__(self, name, is_dir):
        """Инициализация узла."""
        self.name = name
        self.is_dir = is_dir
        self.children = []


def build_tree(path, level, max_level, show_hidden):
    """
    Рекурсивно строит дерево каталогов.

    :param path: Путь к текущему каталогу.
    :param level: Текущий уровень вложенности.
    :param max_level: Максимальный уровень вложенности.
    :param show_hidden: Показывать ли скрытые файлы.
    :return: Узел дерева.
    """
    if level > max_level:
        return None

    name = os.path.basename(path)
    is_dir = os.path.isdir(path)
    node = FileNode(name, is_dir)

    if is_dir:
        for item in os.listdir(path):
            if not show_hidden and item.startswith('.'):
                continue
            child_path = os.path.join(path, item)
            child_node = build_tree(child_path, level + 1,
                                    max_level, show_hidden)
            if child_node:
                node.children.append(child_node)

    return node


def print_tree(node, level=0):
    """
    Выводит дерево каталогов на экран.

    :param node: Корневой узел дерева.
    :param level: Текущий уровень вложенности.
    """
    if not node:
        return

    indent = "  " * level
    print(f"{indent}/{node.name}" if node.is_dir else f"{indent}{node.name}")
    for child in node.children:
        print_tree(child, level + 1)


def save_to_xml(node, parent_element=None):
    """
    Сохраняет дерево каталогов в XML.

    :param node: Корневой узел дерева.
    :param parent_element: Родительский XML-элемент.
    :return: XML-элемент.
    """
    if parent_element is None:
        element = ET.Element("directory", {"name": node.name})
    else:
        element = ET.SubElement(
            parent_element,
            "directory" if node.is_dir else "file",
            {"name": node.name}
        )

    for child in node.children:
        save_to_xml(child, element)

    return element


def load_from_xml(element):
    """
    Загружает дерево каталогов из XML.

    :param element: XML-элемент.
    :return: Узел дерева.
    """
    name = element.attrib["name"]
    is_dir = element.tag == "directory"
    node = FileNode(name, is_dir)

    for child_element in element:
        child_node = load_from_xml(child_element)
        node.children.append(child_node)

    return node


def main():
    """Основная функция программы."""
    parser = argparse.ArgumentParser(
        description="Утилита для вывода дерева каталогов."
    )
    parser.add_argument("directory", nargs="?", default=".",
                        help="Путь к каталогу")
    parser.add_argument("-l", "--level", type=int, default=100,
                        help="Максимальная глубина отображения")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Показывать скрытые файлы")
    parser.add_argument("--save", type=str,
                        help="Сохранить дерево в XML файл")
    parser.add_argument("--load", type=str,
                        help="Загрузить дерево из XML файла")

    args = parser.parse_args()

    if args.load:
        tree_xml = ET.parse(args.load)
        root = load_from_xml(tree_xml.getroot())
        print("Дерево загружено из XML:")
        print_tree(root)
        return

    path = os.path.abspath(args.directory)
    if not os.path.exists(path):
        print("Ошибка: каталог не существует.")
        return

    if not os.path.isdir(path):
        print("Ошибка: указанный путь не является каталогом.")
        return

    root = build_tree(path, 0, args.level, args.all)
    print(f"Дерево каталогов для {path}:")
    print_tree(root)

    if args.save:
        root_xml = save_to_xml(root)
        tree_xml = ET.ElementTree(root_xml)
        tree_xml.write(args.save, encoding="utf-8", xml_declaration=True)
        print(f"Дерево сохранено в {args.save}")


if __name__ == "__main__":
    main()
