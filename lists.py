
from flask import Flask, request, jsonify, render_template
import spacy
import random
import gspread
sa = gspread.service_account()
sh = sa.open("team32")
wks = sh.worksheet("team_data")
data_list = wks.row_values(1)
print(data_list)
income = int(data_list[3])
cap = float(data_list[2])
dur = float(data_list[0])


if income>0 and income<=700000:
    Pertax = 0
elif income>700000 and income<=900000:
    Pertax = 10
elif income>900000 and income<=1200000:
    Pertax = 15
elif income>1200000 and income<=1500000:
    Pertax = 20
elif income>1500000:
    Pertax = 30

print(Pertax)

def func_T1(cap, ror, dur):

    fin = cap * (1 + (ror/100))**dur
    pro = fin - cap
    if dur < 1:
        rer = pro * 0.85
        rarer = ((((cap + rer)/cap)**(1/dur)) - 1) * 100
    elif dur > 1:
        rer = (pro - 100000) * 0.9 + 100000
        rarer = ((((cap + rer)/cap)**(1/dur)) - 1) * 100
    return rarer

def func_T2(ror, cap, dur, Pertax):
    fin = cap * (1 + (ror / 100))**dur
    pro = fin - cap
    rer = pro * (1 - Pertax / 100)
    rarer = (((cap + rer) / cap)**(1 / dur) - 1) * 100
    return rarer

def func_T3(cap, ror, dur):
    cap1 = cap
    n = 0
    while n < dur:
        pro = ((cap1 * ror) / 100)
        rer = (pro - 40000) * 0.9 + 40000
        cap1 = cap1 + rer
        n = n + 1
    rarer = (((cap1 / cap) ** (1 / dur)) - 1) * 100
    return rarer

def func_T4(ror, cap, dur, Pertax, rarer):
    if dur < 3:
        fin = cap * (1 + (ror/100))**dur
        pro = fin - cap
        rer = pro * (1 - Pertax/100)
        rarer = ((((cap + rer)/cap)**(1/dur)) - 1) * 100
    elif dur > 3:
        fin = cap * (1 + (ror/100))**dur
        pro = fin - cap
        rer = pro * 0.8
        rarer = ((((cap + rer)/cap)**(1/dur)) - 1) * 100
    return rarer

def func_T5(cap, ror, dur, Pertax):
    fin = cap * (1 + (ror / 100)) ** dur
    pro = fin - cap
    if dur < 1:
        rer = pro * (1 - Pertax / 100)
        rarer = (((cap + rer / cap) ** (1 / dur)) - 1) * 100
    elif dur >= 1:
        rer = pro * 0.9
        rarer = (((cap + rer / cap) ** (1 / dur)) - 1) * 100
    return rarer

def func_T6(cap, ror, dur, Pertax):
    fin = cap * (1 + (ror / 100))**dur
    pro = fin - cap
    Rer = fin * (1 - Pertax / 100) - cap
    rarer = (((cap + Rer) / cap)**(1 / dur) - 1) * 100
    return rarer

def func_T7(cap,ror,dur,rarer):

    fin = cap * (1 + (ror/100))**dur
    pro = fin - cap
    ror = rarer
    return rarer

def func_T8(cap, ror, dur):

    fin = cap * (1 + (ror / 100))**dur
    pro = fin - cap
    if dur < 5:
        rer = (pro - 50000) * 0.9 + 50000
        rarer = ((((cap + rer )/ cap) ** (1 / dur)) - 1) * 100
    elif dur >= 5:
        rer = pro
        rarer = ((((cap + rer) / cap) ** (1 / dur)) - 1) * 100
    return rarer

def func_T9(cap, ror, dur, Pertax):


    fin = cap * (1 + (ror / 100)) ** dur
    pro = fin - cap
    interest = ((cap * 2.5 * dur) / 100) * (1 - Pertax / 100)

    if dur < 5:
        rer = pro * 0.8 + interest
        rarer = ((((cap + rer) / cap) ** (1 / dur)) - 1) * 100
    elif dur > 5:
        rer = pro + interest
        rarer = ((((cap + rer) / cap) ** (1 / dur)) - 1) * 100

    return rarer

def func_T10(cap, dur, ror, Pertax):
    cap1 = cap
    n = 0
    while n < dur:
        pro = (cap1 * ror) / 100
        rer = (pro - 10000) * (1 - Pertax / 100) + 10000
        cap1 = cap1 + rer
        n = n + 1

    rarer = (((cap1 / cap) ** (1 / dur)) - 1) * 100
    return rarer

def func_T11(cap, ror, dur, Pertax):
  
    if dur < 1:
        rer = (cap * (1 + ror / 100) ** dur - cap) * 0.9
    elif dur > 1 and dur < 7:
        rer = (cap * (1 + ror / 100) ** dur - cap) * (1 - Pertax / 100)
    elif dur == 7:
        rer = cap * (1 + ror / 100) ** dur - cap
    elif dur > 7:
        rer = cap * (1 + ror / 100) ** dur - cap

    rarer = ((((cap + rer )/ cap) ** (1 / dur)) - 1) * 100
    return rarer









list1 = ["recurring deposits","low","0.5,10","5","partially liquid","t3"]

list2 = ["fixed deposits","very low","0.25,10","5","partially liquid","t3"]

list3 = ["saving accounts","very low","any","2.5","liquid","t10"]

list4= ["national saving certificates","very low","5","7","illiquid","t2"]

list5= ["sukanya samridhi yojana ","very low","21","7.6","illiquid","t7"]

list6=["provident fund","low","any","8.15","illiquid","t8"]

list7=["money market funds","very low","any","6.5","liquid","t4"]

list8=["corporate bond fund","low","any","8.5","liquid","t4"]

list9=["government bond fund","very low","any","7.5","liquid","t4"]

list10=["mixed bond fund","medium","any","10","liquid","t4"]

list11=["high yield bond funds","high","any","12","liquid","t4"]

list12=["bluechip equity funds","low","any","9","liquid","t1"]

list13=["large cap equity fund","low","any","11","liquid","t1"]

list14=["small cap equity fund","high","any","15","liquid","t1"]

list15=["mid-cap equity fund","medium","any","13","liquid","t1"]

list16=["equity oriented hybrid funds","medium","any","11.5","liquid","t1"]

list17=["debt oriented hybrid funds","medium","any","9.5","liquid","t4"]

list18=["nifty 50 index funds","low","any","9.5","liquid","t1"]

list19=["sensex index fund","low","any","12","liquid","t1"]

list20=["nifty next 50 index funds","medium","any","12.5","liquid","t1"]

list21=["nasdaq composite index funds","low","any","8","liquid","t1"]

list22=["s&p 500 index fund","low","any","7.5","liquid","t1"]

list23=["tier 1 nps account","low","any","10","illiquid","t7"]

list24=["tier 2 nps account","low","any","10","liquid","t6"]

list25=["government saving bond","very low","1,40","7.5","partially liquid","t11"]

list26=["investment grade corporate bonds","low","1,30","8.5","illiquid","t5"]

list27=["high yield bonds","high","1,30","13","illiquid","t4"]

list28=["debentures","low","10,30","8.5","illiquid","t5"]

list29=["invits","medium","any","9.5","liquid","t1"]

list30=["reits","medium","any","9.5","liquid","t1"]

listslist = [list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, list11, list12, list13, list14, list15, list16, list17, list18, list19, list20, list21, list22, list23, list24, list25, list26, list27, list28, list29, list30]



relevant_list = []

for i in listslist:
    if i[2] == "any":
        rorrange_start = 0
        rorrange_end = 100
        if rorrange_start <= float(data_list[0]) <= rorrange_end and i[4] == data_list[1]:
            relevant_list.append(i)
 
    elif i[2] != "any":
        rorrange = i[2].split(",")
        if len(rorrange) == 1:  # Check if rorrange has only one value
            rorrange_start = float(rorrange[0])
            if float(data_list[0]) == rorrange_start and i[4] == data_list[1]:
               relevant_list.append(i)
        else:
            rorrange_start = float(rorrange[0])
            rorrange_end = float(rorrange[1])
            if rorrange_start <= float(data_list[0]) <= rorrange_end and i[4] == data_list[1]:
                relevant_list.append(i)
    else:
        print("currently there are no schemes recommended...but we are continually expanding our database. please come back at a later time and we might be able to accomodate your interests.")




for i in relevant_list:
    if i[-1] == 't1':
        ror = float(i[3])
        rarer = func_T1(cap, ror, dur)
        i.append(rarer)
    elif i[-1] == 't2':
        ror = float(i[3])
        rarer = func_T2(cap, ror, dur,Pertax)
        i.append(rarer)
    elif i[-1] == 't3':
        ror = float(i[3])
        rarer = func_T3(cap, ror, dur)
        i.append(rarer)
    elif i[-1] == 't4':
        ror = float(i[3])
        rarer = func_T4(ror,cap,dur,Pertax,rarer)
        i.append(rarer)

    elif i[-1] == 't5':
        ror = float(i[3])
        rarer = func_T5(cap,ror,dur,Pertax)
        i.append(rarer)

    elif i[-1] == 't6':
        ror = float(i[3])
        rarer = func_T6(cap,ror,dur,Pertax)
        i.append(rarer)

    elif i[-1] == 't7':
        ror = float(i[3])
        rarer = func_T7(cap,ror,dur,rarer)
        i.append(rarer)
    elif i[-1] == 't8':
        ror = float(i[3])
        rarer = func_T8(cap,ror,dur)
        i.append(rarer)
    elif i[-1] == 't9':
        ror = float(i[3])
        rarer = func_T9(cap,ror,dur,Pertax)
        i.append(rarer)
    elif i[-1] == 't10':
        ror = float(i[3])
        rarer = func_T10(cap,dur,ror,Pertax)
        i.append( rarer)
    elif i[-1] == 't11':
        ror = float(i[3])
        rarer = func_T11(cap,ror,dur,Pertax)
        i.append(rarer)


# Sort the lists based on their last element in descending order



for i in relevant_list:
    if i[1] == "very low":
        risk = 100
    elif i[1] == "low":
        risk = 75
    elif i[1] == "medium":
        risk = 50
    elif i[1] == "high":
        risk = 25


for i in relevant_list:
    rarerrisk = (i[-1] + risk)/2
    i.append(format(rarerrisk, '.3f'))    

relevant_sorted_list = sorted(relevant_list, key=lambda x: float(x[-1]) , reverse=True)

relevant_sorted_schemes = []

for i in relevant_sorted_list:

    relevant_sorted_schemes.append(i[0])
    relevant_sorted_schemes.append(i[1])
    relevant_sorted_schemes.append(format(i[6],".3f"))


final_sliced_lists = [relevant_sorted_schemes[i:i+3] for i in range(0, len(relevant_sorted_schemes), 3)]

print(final_sliced_lists)
print("Final sliced list: " + str(final_sliced_lists))





