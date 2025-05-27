#!/usr/bin/env python3
#######################################################################################
# file: sr_example.py
#
# Description:
#
######################################################################################
import csv
from deepdiff import DeepDiff
from pprint import pprint
try:
    from shiftreg import *
    from fpga import *
    from power_sequencer import *
    from connect  import *
except:
    from oryxsdk.shiftreg import *
    from oryxsdk.fpga import *
    from oryxsdk.power_sequencer import *
    from oryxsdk.connect import *
import time

NUM_OF_QUARTERS = 4
NUM_OF_CLUSTERS_IN_Q = 12
NUM_OF_COLUMNS_IN_CLUSTER = 8
NUM_OF_PIXELS_IN_COL = 32
NUM_OF_PLL_IN_Q = 6
TOTAL_NUM_OF_WORDS_IN_TX = 10
NUM_OF_WORDS_IN_TX_PER_LATCH = 5

def prepare_pfe_out():

    rownum = 0
    cluster_key = 0
    col_key = 0
    pix_key = 0
    Cluster_dict = {}
    colDict ={}
    pixDict = {}
    obj = PFE()
    st = 'obj.PFE_Bits.'

    while True:
        try:
            filename=input("Enter Exel filemane and path: ")
            file=open(filename, "r")
            reader = csv.reader(file)
        except FileNotFoundError:
            print("This file doesn't exists, please check its name and path and try again")
        else:
            break

    for row in reader:
        if rownum == 0:
            header = row
        elif rownum == 1:
            bitNumbers = row
        else:
            colnum = 0
            for col in row:
                if colnum == 0:
                    cluster_key = col
                elif colnum == 1:
                    col_key = col
                elif colnum == 2:
                    pix_key = col
                else:
                    name = header[colnum]
                    exe_str = "{}{}={}".format(st,name,int(col,16))
                    #exe_str = st + name + "={}".format(int(col,16))
                    exec(exe_str)
                pixDict[pix_key] = copy.deepcopy(obj)
                colnum = colnum+1
            pixDict[pix_key] = copy.deepcopy(obj)

            if pix_key=='31':
                colnum=0
                colDict[col_key] = copy.deepcopy(pixDict)
            if col_key=='7'and pix_key=='31' :
                Cluster_dict[cluster_key] = copy.deepcopy(colDict)

        rownum = rownum+1

    file.close()

    #print("cluster_key: ",cluster_key)
    return Cluster_dict


def printPfeBitfield(pix_in,pix_out):
    print('---- PFE ----')
    print("DFT_ANALOG_EN",hex(pix_in.PFE_Bits.DFT_ANALOG_EN),hex(pix_out.PFE_Bits.DFT_ANALOG_EN))
    print("DFT_SELP",hex(pix_in.PFE_Bits.DFT_SELP),hex(pix_out.PFE_Bits.DFT_SELP))
    print("CMPIP_SEL",hex(pix_in.PFE_Bits.CMPIP_SEL),hex(pix_out.PFE_Bits.CMPIP_SEL))
    print("CMPIN_SEL",hex(pix_in.PFE_Bits.CMPIN_SEL),hex(pix_out.PFE_Bits.CMPIN_SEL))
    print("TIA_FINE0",hex(pix_in.PFE_Bits.TIA_FINE0),hex(pix_out.PFE_Bits.TIA_FINE0))
    print("TIA_COARSE1",hex(pix_in.PFE_Bits.TIA_COARSE1),hex(pix_out.PFE_Bits.TIA_COARSE1))
    print("DFT_EN_TIA_SENVNB",hex(pix_in.PFE_Bits.DFT_EN_TIA_SENVNB),hex(pix_out.PFE_Bits.DFT_EN_TIA_SENVNB))
    print("VREF_SEL",hex(pix_in.PFE_Bits.VREF_SEL),hex(pix_out.PFE_Bits.VREF_SEL))
    print("AUX_EN",hex(pix_in.PFE_Bits.AUX_EN),hex(pix_out.PFE_Bits.AUX_EN))
    print("PRA_DAC",hex(pix_in.PFE_Bits.PRA_DAC),hex(pix_out.PFE_Bits.PRA_DAC))
    print("D2S_HGB",hex(pix_in.PFE_Bits.D2S_HGB),hex(pix_out.PFE_Bits.D2S_HGB))
    print("D2S_DAC",hex(pix_in.PFE_Bits.D2S_DAC),hex(pix_out.PFE_Bits.D2S_DAC))
    print("VN_SEL",hex(pix_in.PFE_Bits.VN_SEL),hex(pix_out.PFE_Bits.VN_SEL))
    print("EN_PFE",hex(pix_in.PFE_Bits.EN_PFE),hex(pix_out.PFE_Bits.EN_PFE))
    print("DFT_SELN",hex(pix_in.PFE_Bits.DFT_SELN),hex(pix_out.PFE_Bits.DFT_SELN))
    print("DFT_ANALOG_SE",hex(pix_in.PFE_Bits.DFT_ANALOG_SEL),hex(pix_out.PFE_Bits.DFT_ANALOG_SEL))
    print("YODA_EN",hex(pix_in.PFE_Bits.YODA_EN),hex(pix_out.PFE_Bits.YODA_EN))
    print("SP_RST",hex(pix_in.PFE_Bits.SP_RST),hex(pix_out.PFE_Bits.SP_RST))
    print("DFT_RSNS",hex(pix_in.PFE_Bits.DFT_RSNS),hex(pix_out.PFE_Bits.DFT_RSNS))
    print("DFT_SEL_TIA_SENVN",hex(pix_in.PFE_Bits.DFT_SEL_TIA_SENVN),hex(pix_out.PFE_Bits.DFT_SEL_TIA_SENVN))
    print("DFT_TIA_EN_VP",hex(pix_in.PFE_Bits.DFT_TIA_EN_VP),hex(pix_out.PFE_Bits.DFT_TIA_EN_VP))
    print("GM_DACA",hex(pix_in.PFE_Bits.GM_DACA),hex(pix_out.PFE_Bits.GM_DACA))
    print("REF_ENH",hex(pix_in.PFE_Bits.REF_ENH),hex(pix_out.PFE_Bits.REF_ENH))
    print("REF_ENL",hex(pix_in.PFE_Bits.REF_ENL),hex(pix_out.PFE_Bits.REF_ENL))
    print("AMP_ATT",hex(pix_in.PFE_Bits.AMP_ATT),hex(pix_out.PFE_Bits.AMP_ATT))
    print("BM_CTRL",hex(pix_in.PFE_Bits.BM_CTRL),hex(pix_out.PFE_Bits.BM_CTRL))
    print("DFT_EN_PRA",hex(pix_in.PFE_Bits.DFT_EN_PRA),hex(pix_out.PFE_Bits.DFT_EN_PRA))
    print("DFT_CLK_OUT",hex(pix_in.PFE_Bits.DFT_CLK_OUT),hex(pix_out.PFE_Bits.DFT_CLK_OUT))
    print("GM_DAC",hex(pix_in.PFE_Bits.GM_DAC),hex(pix_out.PFE_Bits.GM_DAC))
    print("AVN_EN",hex(pix_in.PFE_Bits.AVN_EN),hex(pix_out.PFE_Bits.AVN_EN))

def rangeexpand(txt):
    lst = []
    for r in txt.split(','):
        if ':' in r[1:]:
            r0, r1 = r[1:].split(':', 1)

            #Note: "eval" below is allowing the use of variable instead of static number
            #? add range check in lst ?
            lst += range(int( eval(r[0] + r0)), int(eval(r1)) + 1)
        else:
            lst.append(int(eval(r)))

    if len(lst) != len(set(lst)):
        print("duplicate indexes - BAD command ", txt)
        return []
    return lst


####################
# main
####################
if __name__ == "__main__":

    Connect(emulation=True)


    ###################
    # Creating objects
    # Test Phase - Init
    ###################
    sr = Sr(path=r'C:\Orix_SDK\workDir', pfe_calib_file=r"C:\Orix_SDK\workDir\data\pfe_calib_values_em.csv")           # for non-default host IP/path-to-csv-files "Sr(host = <ip>, path=<path>)"

    fpga = Fpga(MASTER) # Fpga(SLAVE) for slave

    #Set parameters
    QSTR="0"
    CLSSTR="0:2,11"
    COLSTR="0:5,7"
    PIXSTR="2:6,18"
    NAME='DEFAULT_LOW'

    #Call API
    sr.loadPFE(Q=QSTR,CLS=CLSSTR,COL=COLSTR,PIX=PIXSTR,V=NAME)

    #
    # Test Phase - perpare output dictionaries
    #
    Cluster_dict = {}
    col = {}
    pix = {}
    Cluster_dict = prepare_pfe_out()

    #
    # Test Phase - perform tests and set pass/fail
    #
    #print(cluster_dict)
    pfe_obj_in = sr.PfeDict[NAME]
    print(pfe_obj_in)

    clusters=(rangeexpand(CLSSTR))
    print(clusters)
    columns=(rangeexpand(COLSTR))
    print(columns)
    pixels=(rangeexpand(PIXSTR))
    print(pixels)

    for cl in clusters:
        for col in columns:
            if len(pixels) == len(range(0,NUM_OF_PIXELS_IN_COL)):
                pfe_obj_out = Cluster_dict[cl,col]
                print(pfe_obj_out)
            else:
                for pix in pixels:
                    print("cl,col,pix: ",cl,col,pix)
                    pfe_obj_out = Cluster_dict[str(cl)][str(col)][str(pix)]
                    print(pfe_obj_out)
                    if pfe_obj_in.val_64bits == pfe_obj_out.val_64bits:
                        print(pfe_obj_out,"true")
                        #pix_in = pfe_obj_in
                        #pix_out = pfe_obj_out
                        #printPfeBitfield(pix_in,pix_out)
                    else:
                        print("False")
                        pprint(DeepDiff(pfe_obj_in.val_64bits, pfe_obj_out.val_64bits), indent = 2)
                        pix_in = pfe_obj_in
                        pix_out = pfe_obj_out
                        printPfeBitfield(pix_in,pix_out)

    #pfe_obj_out = Cluster_dict[CLSSTR][COLSTR][PIXSTR]

    sr.rpcClient.call("stop_server")
