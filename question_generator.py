#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib.metadata import files
from unicodedata import category
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment

from jinja2.nodes import Sub
from sympy.printing.pretty.stringpict import prettyForm
from torch.utils.collect_env import check_release_file


def prettify(elem):
    """
    :param elem: Element previously generated with ElementTree
    :return: pretty-printed XML string for the Element.
    """
    #rough_string = ElementTree.tostring(elem, encoding='unicode')
    rough_string = ElementTree.tostring(elem, encoding='utf-8') #Python2
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def save_to_file(elem, file_name="output_xml"):
    """
    :param elem: Element previously generated with ElementTree
    :param file_name: this is the file name of the gerenated file
    :return: a file with the prettified string obtained from the element elem
    """
    string = prettify(elem)
    file = open(file_name, "w")
    file.write(string)
    file.close()


def create_xml_elem(category_name_str, question_data):
    """
    This function creates an Element with information for serveral Moodle questions corresponding to a give
    category
    :param category_name_str: the name of the category in Moodle the questions belong to.
    :param question_data: this a list of lists, where each list is has four elements:
        question_data[0] is the question name which will be used to store it in Moodle
        question_data[1] text is the question text itself
        question_data[2] is the correct value for the question
        question_data[3] is the tolerance for the correct value
    :return: Element type (of ElementTree).
    """
    quiz = Element("quiz")

    # Question comment
    comment = Comment('Generated from Python ')
    quiz.append(comment)

    # Category information
    question = SubElement(quiz, "question", type="category")
    category = SubElement(question, "category")
    category_text = SubElement(category, "text")
    category_text.text = category_name_str
    info = SubElement(question, "info", format="html")
    info_text = SubElement(info, "text")
    info_text.text = ""


    for question_name_str, question_text_str, answer_str, tolerance_str in question_data:

        # Type of question is numerical
        question = SubElement(quiz, "question", type="numerical")

        # Question name: the name that will be seen in Moodle
        question_name = SubElement(question, "name")
        question_name_text = SubElement(question_name, "text")
        question_name_text.text = question_name_str

        # Question text: what the student has to reply to
        question_text = SubElement(question, "questiontext", format='html')
        question_text_text = SubElement(question_text, "text")
        question_text_text.text = question_text_str

        # Correct value of the answer
        answer = SubElement(question, "answer", fraction="100", format="moodle_auto_format")
        answer_text = SubElement(answer, "text")
        answer_text.text = answer_str

        # Tolerance value
        tolerance_text = SubElement(answer, "tolerance")
        tolerance_text.text = tolerance_str

    return quiz

"""
What follows is code to check that the previous functions work fine.
When using this module from another .py file, importing the functions would be enough.
That other .py file should create the lists for create_xml_elem function to be run
"""

import numpy as np

# Data for building the question
no_test_questions = 10
question_data = [["question_test_{}".format(i),
                 "text_{}".format(i),
                 "{}".format(100*np.random.random()),
                 "{}".format(10*np.random.random())]
                 for i in range(10)]

# Creating the ET elment to be prettified
quiz = create_xml_elem("test_category", question_data)
# Prettifying and saving the pretty string to an .xml file
save_to_file(quiz, "prueba_202122.xml")
