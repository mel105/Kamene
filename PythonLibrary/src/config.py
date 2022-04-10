#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 07:35:29 2022

@author: mel
"""


import json


class config:
    """
    Trieda ma za ciel spracovat konfiguracny subor
    """

    def __init__(self):
        """
        Konstruktor

        Returns
        -------
        None.

        """

        self._load_config()

    # get funkcie
    def get_inp_file_name(self):
        """
        Funkcia vrati nazov pozadovaneho vstupneho suboru

        Returns
        -------
        TYPE string
            DESCRIPTION. Nazov pozadovaneho suboru

        """
        return self._inp_file_name

    def get_inp_local_path(self):
        """
        Funkcia vrati lokalnu cast cesty k csv datam

        Returns
        -------
        TYPE string
            DESCRIPTION. Lokalna cast cesty k csv data,
        """
        return self._inp_local_path

    def get_out_file_name(self):
        """
         Funkcia vrati nazov pozadovaneho vystupneho suboru

         Returns
         -------
         TYPE string
             DESCRIPTION. Nazov pozadovaneho vystupneho suboru

         """
        return self._out_file_name

    def get_out_local_path(self):
        """
         Funkcia vrati lokalnu cast cesty pre ulozenie vystupu

         Returns
         -------
         TYPE string
             DESCRIPTION. Lokalna cast cesty pre ulozenie vystupu,
         """
        return self._out_local_path

    # protected funkcie

    def _load_config(self):
        """
        funkcia nacita konfiguracny subor.

        Returns
        -------
        None.

        """
        with open("config.json") as j:
            cf = json.load(j)

        # obecne nastavenie, napr. cesta/y k datam
        self._inp_file_name = cf["set_inp"]["inp_file_name"]
        self._inp_local_path = cf["set_inp"]["inp_local_path"]

        # nastavenie adresara, kam ulozim vystup
        self._out_file_name = cf["set_out"]["out_file_name"]
        self._out_local_path = cf["set_out"]["out_local_path"]
