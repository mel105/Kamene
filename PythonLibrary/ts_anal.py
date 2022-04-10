#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 12:36:04 2022

@author: mel
"""

import time
import pandas as pd
from src.config import config
from src.process_csv import process_csv
from jinja2 import Environment, FileSystemLoader
from src.support import check_folder


def get_version_table():
    """
    Funkcia, ktora sluzi k tomu, ze vrati tabuklu verzii. To znamena, ze obsahuje metainfo, napr:
        autor, zmena, posledna uprava atp.

    Returns
    -------
    None.

    """

    # data, ktore by sa mali nejak editovat. Sluzi mi to hlavne pre nacvicenie vyrobi html reportu.
    edit_data = {
        "Verzia": ["0.0.1", "0.0.2"],
        "Autor": ["mel", "mel"],
        "Dátum": ["2022-03-07", "2022-04-10"],
        "Zmena": [
            "Založenie súboru",
            "Dokončenie prvej verzie reportu. Obsahuje dve úrovne.",
        ],
    }

    df_vt = pd.DataFrame(edit_data)

    return df_vt


def print_level2_report(cvsObj, input_file_name, input_file_add):
    """
    funkcia vytvori sub stranku urovne 2 na ktorej vyprinti vysledkty pre kazdu casovu radu
    samostatne
    """
    env = Environment(loader=FileSystemLoader("html_sablony"))
    temp_level2 = env.get_template("report_level2.html")

    # adresar, kam budeme html level2 reporty ukladat
    level2_folder_path = "Report" + "/" + input_file_name

    # kontrola, ze ci takato adresa existuje, ak nie, tak ju vytvor
    check_folder(level2_folder_path)

    data_level2 = {
        "fig_xyz": cvsObj.get_fig_record().to_html(),
        "fig_dec_x": cvsObj.get_fig_decomposition()[0].to_html(),
        "fig_dec_y": cvsObj.get_fig_decomposition()[1].to_html(),
        "fig_dec_z": cvsObj.get_fig_decomposition()[2].to_html(),
        "fig_out": cvsObj.get_outliers().to_html(),
        "stat": cvsObj.get_stats(),
    }

    # Naplnenie sablony pozadovanymi udajmi
    html = temp_level2.render(data_level2)

    # kontrola, ze ci takato adresa existuje, ak nie, tak ju vytvor
    check_folder(level2_folder_path)

    level2_file = level2_folder_path + "/" + "index.html"
    with open(level2_file, "w", encoding="utf8") as f:
        f.write(html)

    return level2_file


# MAIN funkcia: Moderuje spracvoanie csv tabulky a generovanie reportu
def generuj_report():

    #                                                         PRIPRAVA DAT PRE TVORBU HTML REPORTU
    # Tabulka verzie dokumentu
    version_table = get_version_table()

    # Nacitaj konfigurak
    configObj = config()

    # loop skrz pocet spracovanych suborov
    # for iFile in configObj.get_inp_file_name():
    idx = 0
    list_of_file_names = []
    list_of_links = []

    while idx < len(configObj.get_inp_file_name()):

        print(idx, configObj.get_inp_file_name()[idx])

        # Spracovanie CSV tabulky a vycet zaujimavych informacii
        csvObj = process_csv(configObj, idx)

        # Vyber obrazka
        fig_xyz = csvObj.get_fig_record()

        actual_input = (
            configObj.get_inp_local_path()
            + "/"
            + configObj.get_inp_file_name()[idx]
            + ".csv"
        )

        # vytvor html stranku pre data, cize Level 2 (suhrna tabulka so vsetkymi subormi je Level 1)
        level2 = print_level2_report(
            csvObj, configObj.get_inp_file_name()[idx], actual_input,
        )

        # zber dat
        list_of_file_names.append(configObj.get_inp_file_name()[idx])
        list_of_links.append(f"<a href={level2}>Link</a>")

        idx += 1

    info_summary = {"Súbor": list_of_file_names, "Link": list_of_links}

    info_table = pd.DataFrame(info_summary)

    #                                                                           TVORBA HTML REPORTU
    # Sablony
    env = Environment(loader=FileSystemLoader("html_sablony"))

    # Nacitanie sablony pre generovanie uvodnej stranky
    temp_uvod = env.get_template("report_main.html")

    # data, ktore sa zobrazia na hlavne/uvodnej stranke
    data_uvod = {
        "version_table": version_table,
        "docu_gen_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "info_table": info_table,
    }

    # Naplnenie sablony pozadovanymi udajmi
    html = temp_uvod.render(data_uvod)
    with open("py_ts_report.html", "w") as f:
        f.write(html)


# spustenie reportu
if __name__ == "__main__":
    generuj_report()
