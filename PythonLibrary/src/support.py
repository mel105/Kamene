#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:24:05 2022

@author: mel
"""

import os


def check_folder(folder_path):
    """
    Funkcia by mala skontrolovat existenciu adresara. Ak adresar neexistuje, tak ho vyrobi.

    Parameters:
        folder_path: TYPE string
                    DESCRIPTION. jedna sa cestu, kde by mal existovat prislusny adresar. Ak tam
                    neexistuje, tak ho vyrobi.
    Returns
    -------
    None.

    """

    check_folder_existance = os.path.isdir(folder_path)

    if not check_folder_existance:

        os.makedirs(folder_path)
    else:
        pass
