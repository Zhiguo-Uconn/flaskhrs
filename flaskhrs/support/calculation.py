from . import df
import pandas as pd
import numpy as np
import os


class HRS:

    def __init__(self, patient, mr):
        self.field_name = []  # list
        self.value = []  # list
        self.display = []  # list
        self.hr = []  # list
        self.add(patient, 'race')
        self.add(patient, 'education')
        self.add(patient, 'marital')
        self.add(patient, 'gestation_hist')
        self.add(patient, 'family_hist')
        self.add(mr, 'alcohol')
        self.add(mr, 'physical')
        self.add(mr, 'fastGlucose')
        self.add(mr, 'a1c')
        self.add(mr, 'bmi')
        self.add(mr, 'hei')
        self.add(mr, 'hdl')
        self.add(mr, 'ldl')
        self.add(mr, 'tag')
        self.add(mr, 'total_cho')
        self.add(mr, 'systolic')
        self.add(mr, 'diastolic')
        self.add(mr, 'cvd')
        self.add(mr, 'stroke')
        self.add(mr, 'kidney')

        self.hle = round(get_hle(self.hr, patient), 1)

    def add(self, inst, key):
        f = inst._meta.get_field(key)
        self.field_name.append(f.verbose_name)
        self.value.append(f.value_from_object(inst))
        if hasattr(inst, 'get_%s_display' % key):
            self.display.append(getattr(inst, 'get_%s_display' % key)())
            self.hr.append(df.get_hr(key)[self.value[-1]])
        elif f.get_internal_type() == 'BooleanField':
            self.display.append('Yes' if f.value_from_object(inst) else 'No')
            self.hr.append(1)
        else:
            self.display.append(f.value_from_object(inst))
            self.hr.append(1)


def get_hle(hr, patient):
    adj = np.prod(hr)
    age = patient.age
    gender = patient.gender
    mortality = getMortality()[age:]
    i_df = getIncidenceRate()
    q = mortality['H_Male'].to_numpy()
    # d = mortality['D_Male'].to_numpy()
    i = i_df.iloc[0:(q.size), age + 1].to_numpy()
    q_adj = 1 - np.power(1 - q, adj)
    i_adj = 1 - np.power(1 - i, adj)
    hle_h = cal_hle(q, i)

    hle_adj = cal_hle(q_adj, i_adj)
    print(adj)
    print(hle_h)
    return hle_adj


def cal_hle(q, i):
    p_hh = (1 - i) * (1 - q)
    p1 = np.delete(p_hh, p_hh.size - 1).cumprod()
    x = 1 - np.delete(p_hh, 0)
    hle = sum(x * p1 * np.arange(1, p_hh.size))
    return hle


def getMortality():
    file_folder = os.path.join(os.path.dirname(__file__), 'supports')
    file_name = 'Mortality.csv'
    file_path = os.path.join(file_folder, file_name)
    df = pd.read_csv(file_path)
    return df


def getIncidenceRate():
    file_folder = os.path.join(os.path.dirname(__file__), 'supports')
    file_name = 'incidenceRate.csv'
    file_path = os.path.join(file_folder, file_name)
    df = pd.read_csv(file_path)
    return df
