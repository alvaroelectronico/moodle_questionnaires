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
    """Return a pretty-printed XML string for the Element.
    """
    #rough_string = ElementTree.tostring(elem, encoding='unicode')
    rough_string = ElementTree.tostring(elem, encoding='UTF-8') #Python2
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def save_to_file(elem, file_name="output_xml"):
    string = prettify(elem)
    file = open(file_name, "w")
    file.write(string)
    file.close()


def create_xml_elem(category_name_str, question_data):
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

# Data for building the question
category_name_str = "category name"
question_name_str = "pregunta prueba 1"
question_text_str = "Enunciado de la pregunta"
answer_str = "10"
tolerance_str = "1"

question_data = [[question_name_str, question_text_str, answer_str, tolerance_str]]

# Creating the ET elment to be prettified
quiz = create_xml_elem("tutorial AIMMS", question_data)

# Prettifying and saving the pretty string to an .xml file
save_to_file(quiz, "prueba_202122.xml")

print(prettify(quiz))
