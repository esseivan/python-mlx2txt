#! /usr/bin/env python

import argparse
import re
import xml.etree.ElementTree as ET
import zipfile
import os
import sys


nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def process_args():
    parser = argparse.ArgumentParser(description='A pure python-based utility '
                                                 'to extract text and images '
                                                 'from mlx files.')
    parser.add_argument("mlx", help="path of the mlx file")

    args = parser.parse_args()

    if not os.path.exists(args.mlx):
        print('File {} does not exist.'.format(args.mlx))
        sys.exit(1)

    return args


def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml. For
    example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
    Source: https://github.com/python-openxml/python-docx/
    """
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return '{{{}}}{}'.format(uri, tagroot)


def xml2text(xml):
    """
    A string representing the textual content of this run, with content
    child elements like ``<w:tab/>`` translated to their Python
    equivalent.
    Adapted from: https://github.com/python-openxml/python-docx/
    """
    text = u''
    root = ET.fromstring(xml)
    for child in root.iter():
        if child.tag == qn('w:t'):
            t_text = child.text
            text += t_text if t_text is not None else ''
        elif child.tag == qn('w:tab'):
            text += '\t'
        elif child.tag in (qn('w:br'), qn('w:cr')):
            text += '\n'
        elif child.tag == qn("w:p"):
            text += '\n\n'
    return text


def process(mlx):
    text = u''

    # unzip the mlx in memory
    zipf = zipfile.ZipFile(mlx)

    # get main text
    doc_xml = 'matlab/document.xml'
    text += xml2text(zipf.read(doc_xml))


    zipf.close()
    return text.strip()


if __name__ == '__main__':
    args = process_args()
    text = process(args.mlx)
    sys.stdout.buffer.write(text.encode("UTF8"))
