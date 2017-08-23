# !/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Jukka
#
# Created:     02/04/2014
# Copyright:   (c) Jukka 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------

"""
Base file for projects
"""

# import time
# from bs4 import BeautifulSoup
# import os
import sys  # , re
#from urllib2 import urlopen


try:
    import win32clipboard as wc
    import win32con

    def copy_to_clipboard(msg):
        """ Copy to clipboard

        :param msg:
        :return:
        """
        if sys.platform == 'win32':
            wc.OpenClipboard()  # pylint: disable=no-member
            wc.EmptyClipboard()  # pylint: disable=no-member
            #wc.SetClipboardData(win32con.CF_TEXT, msg)
            wc.SetClipboardText(msg, wc.CF_UNICODETEXT)# pylint: disable=no-member

            wc.CloseClipboard()  # pylint: disable=no-member


    def paste_from_clipboard():
        """ Paste from clipboard

        :return:
        """
        wc.OpenClipboard()  # pylint: disable=no-member
        msg = wc.GetClipboardData(win32con.CF_TEXT)  # pylint: disable=no-member
        wc.CloseClipboard()  # pylint: disable=no-member
        return msg

except:
    import subprocess

    def paste_from_clipboard():
     p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
     retcode = p.wait()
     data = p.stdout.read()
     return data

    def copy_to_clipboard(data):
     p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
     p.stdin.write(data)
     p.stdin.close()
     retcode = p.wait()


try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError



def get_urli(urli):
    """ load a reseource from url

    :param urli:
    :return:
    """
    uresource = urlopen(urli)
    return uresource.read()


def tallennatiedosto(tiednimi, sisalto):
    """ Save a File

    :param tiednimi:
    :param sisalto:
    :return:
    """
    fil = open(tiednimi, 'w')
    fil.write(sisalto)
    fil.close()


def lataa_tied(tiednimi):
    """ Load a file
    :param tiednimi:
    :return:
    """
    readfil = open(tiednimi, 'r')
    html_doc = readfil.read()
    readfil.close()
    return html_doc


def listojen_erot(list1, list2):
    """ set operation: get the differences of two lists

    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) - set(list2))


def listojen_leikkaus(list1, list2):
    """ intersection of two lists as sets

    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) & set(list2))


def filter_dups(lista):
    """ filter duplicates from a list
    returns unique members in origial order

    :param lista:
    :return:
    """
    list_uniq = []
    for list_item in lista:
        if list_item not in list_uniq:
            list_uniq.append(list_item)
    return list_uniq


def histogram(list_arr):
    """ Create a histogram

    :param list_arr:
    :return:
    """
    hashi = dict()
    for limtem in list_arr:
        if limtem not in hashi:
            hashi[limtem] = 1
        else:
            hashi[limtem] += 1
    return hashi


def order_histo(histo):
    """ Convert histogram hash to list and sort it
    :param histo:
    :return:
    """
    histoar = [[histo[key1], key1] for key1 in histo.keys()]
    histoar.sort()
    return histoar


def ordered_histo(list_arr):
    """
    create ordered histogram list
    :param list_arr:
    :return:
    """
    return order_histo(histogram(list_arr))
