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
import os
import shutil

def create_xml_from_question_data(file, category, questions_data):
    """
    This is the public functions which uses internal ones
    :param file: file name (without extension, this will be added)
    :param category: category name
    :param questions_data: all info for the questions.
    :return: none, it just creates an xml file for Moodle.
    """
    elem = create_xml_elem_(category, questions_data)
    prettify_(elem)
    save_to_file_(elem, file + ".xml")

def prettify_(elem):
    """
    :param elem: Element previously generated with ElementTree
    :return: pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    reparsed_pretty = reparsed.toprettyxml(indent="  ", encoding="utf-8")
    return reparsed_pretty

def fix_html_tags_(file):
    # Opening the file to be fixed
    fin = open(file, "rt", encoding='UTF-8')
    # output file to write the result to
    fout = open("temp.xml", "wt", encoding='UTF-8')
    # for each line in the input file
    for line in fin:
        fout.write(line.replace('&lt;', '<').replace('&gt;', '>'))
    # close input and output files
    fin.close()
    fout.close()
    shutil.copyfile("temp.xml", file)
    os.remove("temp.xml")

def save_to_file_(elem, file_name="output_xml"):
    """
    :param elem: Element previously generated with ElementTree
    :param file_name: this is the file name of the gerenated file
    :return: a file with the prettified string obtained from the element elem
    """
    string = prettify_(elem)
    # file = open(file_name, "w")
    # file.write(string)
    # file.close()
    # with open(file_name, "w", encoding="utf-8") as outfile:
    #     outfile.write(string)
    with open(file_name, "wb") as outfile:
        outfile.write(prettify_(elem))
        outfile.close()
    fix_html_tags_(file_name)

def create_xml_elem_(category_name_str, question_data):
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
        question_text = SubElement(question, "questiontext", format='moodle_auto_format')
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
That other .py file should create th e lists for create_xml_elem function to be run
"""
#
# import numpy as np
#
# # Data for building the question
# no_test_questions = 10
# question_data = [["question_test_{}".format(i),
#                  "<p>DATOS DEL PROBLEMA. DÍA</p><p></p><p><b>Datos de las plantas</b></p>",
#                  "{}".format(100*np.random.random()),
#                  "{}".format(10*np.random.random())]
#                  for i in range(10)]
#
# create_xml_from_question_data("prueba_202125.xml", "test_category", question_data)