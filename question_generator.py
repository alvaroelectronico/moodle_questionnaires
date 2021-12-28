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
    rough_string = ElementTree.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    reparsed_pretty = reparsed.toprettyxml(indent="  ", encoding="utf-8")
    return reparsed_pretty


def fix_html_tags_(file):
    # Opening the file to be fixed
    fin = open(file, "rt", encoding="UTF-8")
    # output file to write the result to
    fout = open("temp.xml", "wt", encoding="UTF-8")
    # for each line in the input file
    for line in fin:
        fout.write(line.replace("&lt;", "<").replace("&gt;", ">"))
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
        question_data[0] is the type of question
        question_data[1] is the question name which will be used to store it in Moodle
        question_data[2] text is the question text itself
        question_data[3] is the correct value for the question (only for numeric type questions)
        question_data[4] is the tolerance for the correct value (only for numeric type questions)
    :return: Element type (of ElementTree).
    """
    quiz = Element("quiz")

    # Question comment
    comment = Comment("Generated from Python ")
    quiz.append(comment)

    # Category information
    question = SubElement(quiz, "question", type="category")
    category = SubElement(question, "category")
    category_text = SubElement(category, "text")
    category_text.text = category_name_str
    info = SubElement(question, "info", format="html")
    info_text = SubElement(info, "text")
    info_text.text = ""

    for data in question_data:

        # Type of question is numerical
        question = SubElement(quiz, "question", type=data[0])

        # Question name: the name that will be seen in Moodle
        question_name = SubElement(question, "name")
        question_name_text = SubElement(question_name, "text")
        question_name_text.text = data[1]

        # Question text: what the student has to reply to
        question_text = SubElement(
            question, "questiontext", format="moodle_auto_format"
        )
        question_text_text = SubElement(question_text, "text")
        question_text_text.text = data[2]

        if data[0] == 'numerical':
            # Correct value of the answer
            answer = SubElement(
                question, "answer", fraction="100", format="moodle_auto_format"
            )
            answer_text = SubElement(answer, "text")
            answer_text.text = data[3]

            # Tolerance value
            tolerance_text = SubElement(answer, "tolerance")
            tolerance_text.text = data[4]

    return quiz


"""
What follows is code to check that the previous functions work fine.
When using this module from another .py file, importing the functions would be enough.
That other .py file should create the lists for create_xml_from_question_data which will be 
passed on to create_xml_elem function to be run
"""

import numpy as np

# Data for building the question
no_test_questions_numeric = 1
question_data = [["numerical",
                  "question_numeric_{}".format(i),
                 "<![CDATA[<p>DATOS DEL PROBLEMA. DÍA</p><p></p><p><b>Datos de las plantas</b></p>]]>",
                 "{}".format(100*np.random.random()),
                 "{}".format(10*np.random.random())]
                 for i in range(no_test_questions_numeric)]
no_test_questions_cloze = 1
for i in range(no_test_questions_cloze):
    question_data.append(["cloze",
                            "question_cloze_{}".format(i),
                     "<![CDATA[<p>DÍA</p><p></p><p><b>Datos de las plantas</b></p><p></p><p>Pregunta 1: {1:NUMERICAL:=12000} euros.</p>]]>"])

create_xml_from_question_data("prueba_202128", "Pruebas Python", question_data)

