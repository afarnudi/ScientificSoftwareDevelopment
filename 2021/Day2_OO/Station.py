#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 10:14:37 2021

@author: ali
"""
import pandas as pd


class Train:
    _index = 1

    def __init__(self, destination, capacity_in_tons):
        self.destination = destination
        self.capacity_in_Kg = capacity_in_tons * 1000.0
        self.index = Train._index
        Train._index += 1

    def __init__(self, dest_cap_list):
        self.destination = dest_cap_list[0]
        self.capacity_in_Kg = dest_cap_list[1] * 1000.0
        self.index = Train._index
        Train._index += 1

    def get_destination(self):
        return self.destination

    def get_capacity(self):
        return self.capacity_in_Kg

    def get_index(self):
        return self.index

    def load_parcels(self, parcels_df):
        self.parcels_df = parcels_df

    def get_report(self):
        report = """
Train: {:03}
Destination:   {}
Capacity (kg): {}
Load (kg):     {:.3f}
Num of Parcels {}
Parcels:\n""".format(
            self.index,
            self.destination,
            self.capacity_in_Kg,
            self.parcels_df["parcel_weight_kg"].sum(),
            self.parcels_df.shape[0],
        )
        for des, wei in self.parcels_df.loc[:].values:
            report += " {:.4}  {:.4}\n".format(des, wei)
        return report


class Store_House:
    import pandas as pd

    def __init__(self, path_to_parcels):
        # self.parcelList = list(map(Parcel,pd.read_csv(pathToParcels, sep=" ").loc[:].values) )
        self.parcel_list = pd.read_csv(path_to_parcels, sep=" ")

    def get_parcels_with_net_weight(self, destination, net_weight):
        df = self.parcel_list[self.parcel_list["parcel_destination"] == destination]
        filterd = df["parcel_weight_kg"].cumsum() > net_weight
        parcel_count = filterd[filterd is False].count()
        delivery = df[:parcel_count].copy()
        self.parcel_list = self.parcel_list.drop(df[:parcel_count].index)
        return delivery

def get_list_of_train_objects(path, seporater):
    TrainsDF = pd.read_csv("trains.txt", sep=" ")
    return list(map(Train, TrainsDF.loc[:].values))


def station():
    store_house = Store_House("parcels.txt")
    trains = get_list_of_train_objects("trains.txt", " ")

    trains = trains[:5]

    for train in trains:
        parcel_list = store_house.get_parcels_with_net_weight(
            train.get_destination(), train.get_capacity()
        )
        train.load_parcels(parcel_list)
        with open("train{:03}.txt".format(train.get_index()), "w") as fw:
            fw.write(train.get_report())


if __name__ == "__main__":
    station()
