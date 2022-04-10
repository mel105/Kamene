#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:36:58 2022

@author: mel
"""
# import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import date, timedelta
import re
import numpy as np
import datetime as dt

from pathlib2 import Path
from math import pi


class process_csv:
    """
    Trieda ma za ulohu prevziat nastavenie z html reportu, spracovat csv subor a poskytnut vysledky
    pre potrebu spracovania samotneho html reportu
    """

    def __init__(self, conf, file_idx):
        """
        Konstruktor

        Parameters
        ----------
        conf : TYPE config object
            DESCRIPTION. nastavenie konfiguracneho suboru
        file_idx : TYPE int
            DESCRIPTION. poukazuje na index spracovaneho suboru, ktory je validny pre konfiguracny
            subor. to znamena, ze ak fileIdx = 0, potom spracujem prvy subor nastaveny v config.json

        Returns
        -------
        None.

        """

        # prevezme data: tykaju sa vstupu
        self._inp_file = conf.get_inp_file_name()[file_idx]
        self._inp_local_path = conf.get_inp_local_path()

        # prevezme data tykajuce sa vystupu
        self._out_file = conf.get_out_file_name()
        self._out_local_path = conf.get_out_local_path()

        # nastavenie cesty k suboru
        # self._inp_file_path = Path(self._inp_local_path, self._inp_file + ".csv")
        self._inp_file_path = Path(self._inp_local_path, self._inp_file + ".txt")

        # nacitanie csv suboru
        self._read_csv_file()

        # redukovanie hodnot o priemernu hodnotu. Pozor, pracujem len s xyz
        self._subtract_mean()

        # vyroba median year rady. Pozor, validne len pre data s dennou frekvenciou
        self._median_year()

        # doplnenie chybajucich hodnot. Ak sa v rade nachadza chybajuce datum, jeho hodnota bude
        # nahradena hodnotou z medianoveho roku
        self._fill_missings()

        # vykresli zakladny priebeh rady
        self._plot_situation()

        # dekompozicia casovej rady
        self._ts_decomposition()

        # odhad odlahlych hodnot s pouzitim metody iqr
        self._outliers()

        # nejake popisne statistiky
        self._stats()

        #

        # pre kazdy track zakladne info + analyza. Vysledkom zrejme bude viac vnorenych dict
        # kontajnerov
        # self._analyse_record()

    # GET FUNKCIE
    def get_stats(self):
        """
        Metoda vrati tabulky s popisnymi statistikami. Jedna tabulka sa bude tykat orig dat a druha
        casovej rady residui

        Returns
        -------
        None.

        """

        return self._stat_table

    def get_outliers(self):
        """
        Metoda vrati fig objekt triedy graph_objects a zobrazuje priebeh odlahlych hodnot na
        na redukovanych radach

        Returns
        -------
        None.

        """

        return self._fig_out

    def get_fig_decomposition(self):
        """
        metoda vrati fig objekt tykajuci sa priebehu dekompozicie ts

        Returns
        -------
        None.

        """
        return self._fig_dc_X, self._fig_dc_Y, self._fig_dc_Z

    def get_fig_record(self):
        """
        Metoda vrati obejkt fig, ktory obsahuje data k zobrazeniu

        Returns
        -------
        None.

        """
        return self._fig_xyz

    # PRIVATE METODY

    def _stats(self):
        """
        Metoda, ktora pre zvoleny vektor odhadne popisne statistiky. Vysledkom je kontajner, ktory
        obsahuje celu radu informacii

        Returns
        -------
        None.

        """

        list_of_params = ["X", "Y", "Z"]

        # orig.
        or_array = np.zeros((8, len(list_of_params)))

        for i_params in range(len(list_of_params)):

            actual_param = list_of_params[i_params]

            or_array[0, i_params] = int(len(self._df[actual_param]))
            or_array[1, i_params] = np.percentile(self._df[actual_param], 0)
            or_array[2, i_params] = np.percentile(self._df[actual_param], 5)
            or_array[3, i_params] = np.percentile(self._df[actual_param], 50)
            or_array[4, i_params] = np.percentile(self._df[actual_param], 95)
            or_array[5, i_params] = np.percentile(self._df[actual_param], 100)
            or_array[6, i_params] = self._df[actual_param].mean()
            or_array[7, i_params] = self._df[actual_param].std()

        df_stat_imodul = pd.DataFrame(or_array, columns=list_of_params)
        df_stat_imodul.insert(
            0, "Statistiky", ["N", "Min", "P05", "Median", "P95", "Max", "Mean", "Sdev"]
        )

        self._stat_table = df_stat_imodul

    def _outliers(self):
        """
        Metoda zobrazi box plot a vysledkom je vyzobrazit situaciu, ze ci subory obsahuju odlahle
        merania.

        Returns
        -------
        None.

        """

        x_data = ["X", "Y", "Z"]

        y_data = [
            self._add_dec_x.resid,
            self._add_dec_y.resid,
            self._add_dec_z.resid,
        ]

        colors = [
            "rgba(93, 164, 214, 0.5)",
            "rgba(255, 144, 14, 0.5)",
            "rgba(44, 160, 101, 0.5)",
        ]

        fig = go.Figure()

        for xd, yd, cls in zip(x_data, y_data, colors):
            fig.add_trace(
                go.Box(
                    y=yd,
                    name=xd,
                    boxpoints="suspectedoutliers",
                    marker=dict(
                        color="rgb(8,81,156)",
                        outliercolor="rgba(219, 64, 82, 0.6)",
                        line=dict(
                            outliercolor="rgba(219, 64, 82, 0.6)", outlierwidth=2
                        ),
                    ),
                    line_color="rgb(8,81,156)",
                    jitter=0.5,
                    pointpos=-1.8,
                    whiskerwidth=0.2,
                    fillcolor=cls,
                    marker_size=3,
                    line_width=2,
                )
            )

        fig.update_layout(
            title="Odhad odľahlých pozorovaní v radach s mesačnou frekvenciou",
            autosize=False,
            width=1500,
            height=1500,
            yaxis=dict(
                autorange=True,
                showgrid=True,
                zeroline=True,
                dtick=250,
                gridcolor="rgb(255, 255, 255)",
                gridwidth=1,
                zerolinecolor="rgb(255, 255, 255)",
                zerolinewidth=2,
            ),
            margin=dict(l=40, r=30, b=80, t=100,),
            paper_bgcolor="rgb(243, 243, 243)",
            plot_bgcolor="rgb(243, 243, 243)",
            showlegend=False,
        )

        # fig.update_traces(orientation="h")

        self._fig_out = fig

    def _fill_missings(self):
        """
        Metoda doplni chybajuce data. Povodne som chcel pomocou median year. Ale ukazuje sa, ze
        kvoli trendu je to nezmysel. Preto chybajuca hodnota bude interpolovana linearnou
        interpolaciou dvoma susednymi hodnotami.
        """
        # copy df. dfadv bude obsahovat chybajuce data
        self._dfadv = self._df

        # Fill the missing dates and relative attribute with 0
        r = pd.date_range(start=self._df.Date.min(), end=self._df.Date.max())

        """
        self._dfadv = (
            self._dfadv.set_index("Date")
            .reindex(r)
            .fillna(method="ffill")  # !!
            .rename_axis("Date")
            .reset_index()
            .dropna()
        )
        """

        self._dfadv = (
            self._dfadv.set_index("Date").reindex(r).fillna(method="ffill")  # !!
        )

        # Set period/frequency using set_index() dates
        # self._dfadv["Date"] = pd.to_datetime(self._dfadv["Date"])

        # TODO: Tu by sa oplatilo sa zamysliet nad periodami v rade a do konfiguraku periodu
        # tu je nastavena na dennu frekvenciu
        # self._dfadv = self._dfadv.set_index("Date").asfreq("86400S").dropna()
        # self._dfadv = self._dfadv.set_index("Date").asfreq("D").dropna()
        # self._dfadv = self._dfadv.("Date").asfreq("D").dropna()

        print("")

    def _median_year(self):
        """
        Metoda odhadne tzv. medianovy casovu radu. Nou by som chcel vyplnit chybajuce data.
        Kontrola je, ze by mala mat 365 hodnot, pretoze momentalne je validna len pre data
        s dennou frekvenciou. Ak by vacsia frekvencia, nbutne prerobit. Ak sa nepodari
        vyrobit data, ktoreho rozmer by mal byt predpokladanych 365 dni, potom chybajuce dni
        budu aproximovane napr. medianom celej rady.

        Returns
        -------
        None.

        """
        d = self._df["Date"].dt.day
        r = self._df.groupby(d).median()

        if len(r) != 31:
            # TODO: tu nutne zistit chybajuce dni a doplnit medianom stavajuceho r
            print(" ")
        else:
            pass

        self._median_year = r

    def _subtract_mean(self):
        """
        Metoda odcita priemerne hodnoty. Pozor, pracujem len s xyz. Potom nutne prerobit

        Returns
        -------
        None.

        """

        # budem sa venovat len suradniciam xyz (podla potreby potom doplnim na ostatne params).
        # Suradnice X, Y, a Z redukujem na nulu, t.j. od hodnot odcitam priemer
        self._df.X = self._df.X - self._df.X.mean()
        self._df.Y = self._df.Y - self._df.Y.mean()
        self._df.Z = self._df.Z - self._df.Z.mean()

    def _read_csv_file(self):
        """
        Funkcia nacita data zo suboru, ktory je definovany ako input

        Returns
        -------
        None.

        """

        # self._df = pd.read_csv(self._inp_file_path, sep=",")
        self._df = pd.read_csv(
            self._inp_file_path, sep=" ", names=["Date", "X", "Y", "Z", "NAN"]
        )

        # yyyydoy convert yyyy-mm-dd
        nDate = []
        for iDate in self._df.Date:
            old_format_date = str(iDate)
            new_format_date = dt.datetime.strptime(old_format_date, "%Y%j0").strftime(
                "%Y-%m-%d"
            )
            nDate.append({"Date": new_format_date})

        nDf = pd.DataFrame(nDate)

        self._df.Date = nDf

        # skonvertujem Date zo str do datatime
        self._df.Date = pd.to_datetime(self._df.Date)

        print(" ")

    def _ts_decomposition(self, comb="XYZ"):
        """
        Metoda ma za ulohu rozlosit blok casovych rad (zatial len XYZ). Vysledkom su dekompozicie
        casovych radov

        Parameters
        ----------
        comb : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        if comb == "XYZ":
            self._add_dec_x = seasonal_decompose(
                self._dfadv["X"].asfreq("D"),
                model="additive",
                extrapolate_trend="freq",
            )
            self._add_dec_y = seasonal_decompose(
                self._dfadv["Y"].asfreq("D"), model="additive", extrapolate_trend="freq"
            )
            self._add_dec_z = seasonal_decompose(
                self._dfadv["Z"].asfreq("D"), model="additive", extrapolate_trend="freq"
            )

            self._fig_dc_X = self._plot_ts_decompose(
                self._add_dec_x, "Rozklad X-vej súradnice"
            )
            self._fig_dc_Y = self._plot_ts_decompose(
                self._add_dec_y, "Rozklad Y-vej súradnice"
            )
            self._fig_dc_Z = self._plot_ts_decompose(
                self._add_dec_z, "Rozklad Z-vej súradnice"
            )

        else:
            pass

    def _plot_ts_decompose(self, result, mTitle):

        return (
            make_subplots(
                rows=4,
                cols=1,
                subplot_titles=["Observed", "Trend", "Seasonal", "Residuals"],
            )
            .add_trace(
                go.Scatter(x=result.seasonal.index, y=result.observed, mode="lines"),
                row=1,
                col=1,
            )
            .add_trace(
                go.Scatter(x=result.trend.index, y=result.trend, mode="lines"),
                row=2,
                col=1,
            )
            .add_trace(
                go.Scatter(x=result.seasonal.index, y=result.seasonal, mode="lines"),
                row=3,
                col=1,
            )
            .add_trace(
                go.Scatter(x=result.resid.index, y=result.resid, mode="lines"),
                row=4,
                col=1,
            )
            .update_layout(
                height=900,
                title=mTitle,
                # title="Aditívne rozloženie vybraných časových radov",
                margin=dict(t=100),
                title_x=0.5,
                showlegend=False,
            )
        )

    def _plot_situation(self, comb="XYZ"):
        """
        Metoda by mala vykreslit zakladny priebeh casovej rady a zvolenych stlpcov

        Parameters
        ----------
        comb : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        fig = make_subplots(rows=3, cols=1, x_title=("Time"))

        if comb == "XYZ":
            df = self._df[["Date", "X", "Y", "Z"]].copy()

            fig.add_trace(
                go.Scatter(x=self._df["Date"], y=df["X"], name="X"), row=1, col=1
            )

            fig.add_trace(
                go.Scatter(x=self._df["Date"], y=df["Y"], name="Y"), row=2, col=1
            )

            fig.add_trace(
                go.Scatter(x=self._df["Date"], y=df["Z"], name="Z"), row=3, col=1
            )
        else:
            pass

        fig.update_layout(
            height=600,
            width=1000,
            title_text="Graf zobrazuje priebeh pravouhlých súradnic X, Y, Z",
            font=dict(family="Courier New, monospace", size=18),
            yaxis1_title="X",
            yaxis2_title="Y",
            yaxis3_title="Z",
        )

        # fig['layout']['yaxis']['title']='X'
        # fig['layout']['yaxis2']['title']='Y'
        # fig['layout']['yaxis3']['title']='Z'

        self._fig_xyz = fig
