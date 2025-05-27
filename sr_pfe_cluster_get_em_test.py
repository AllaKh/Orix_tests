#!/usr/bin/env python3
#######################################################################################
# file: sr_pfe_get_em.py
#
# Description:
# 1. In emulator mode update some pixels and save them into the dump and calibration files.
# 2. Get specific field of cluster/column and save it into csv file.
#OR:
# 3. Get vectors of column and cluster.
# 4. Parse vectors to csv tables and save them
# 5. Check for difference between the saved vector files and the calibration file (must be the same).
######################################################################################
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
import csv


class PFE_Bits(Structure):
    _fields_ = [("DFT_ANALOG_EN",c_uint64, 1),
        ("DFT_SELP",c_uint64, 2),
        ("CMPIP_SEL",c_uint64, 1),
        ("CMPIN_SEL",c_uint64, 1),
        ("TIA_FINE0",c_uint64, 4),
        ("TIA_COARSE1",c_uint64, 4),
        ("DFT_EN_TIA_SENVNB",c_uint64, 1),
        ("VREF_SEL",c_uint64, 3),
        ("AUX_EN",c_uint64, 1),
        ("PRA_DAC",c_uint64, 6),
        ("D2S_HGB",c_uint64, 1),
        ("D2S_DAC",c_uint64, 6),
        ("VN_SEL",c_uint64, 1),
        ("EN_PFE",c_uint64, 1),
        ("DFT_SELN",c_uint64, 2),
        ("DFT_ANALOG_SEL",c_uint64, 1),
        ("YODA_EN",c_uint64, 1),
        ("SP_RST",c_uint64, 1),
        ("DFT_RSNS",c_uint64, 1),
        ("DFT_SEL_TIA_SENVN",c_uint64, 1),
        ("DFT_TIA_EN_VP",c_uint64, 1),
        ("GM_DACA",c_uint64, 5),
        ("REF_ENH",c_uint64, 1),
        ("REF_ENL",c_uint64, 1),
        ("AMP_ATT",c_uint64, 5),
        ("BM_CTRL",c_uint64, 2),
        ("DFT_EN_PRA",c_uint64, 1),
        ("DFT_CLK_OUT",c_uint64, 1),
        ("GM_DAC",c_uint64, 6),
        ("AVN_EN",c_uint64, 1)]

def dump_vector_col_to_file():

    with open(r"C:\Orix_SDK\workDir\data\col_vector_dump_em.csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #write first row with column name - even if it exists

        writer.writerow(["quarter_number","cluster_number","column_number","pixel_number","DFT_ANALOG_EN",
                             "DFT_SELP","CMPIP_SEL","CMPIN_SEL","TIA_FINE0","TIA_COARSE1","DFT_EN_TIA_SENVNB",
                             "VREF_SEL","AUX_EN","PRA_DAC","D2S_HGB","D2S_DAC","VN_SEL","EN_PFE","DFT_SELN",
                             "DFT_ANALOG_SEL","YODA_EN","SP_RST","DFT_RSNS","DFT_SEL_TIA_SENVN","DFT_TIA_EN_VP",
                             "GM_DACA","REF_ENH","REF_ENL","AMP_ATT","BM_CTRL","DFT_EN_PRA","DFT_CLK_OUT","GM_DAC",
                             "AVN_EN"])
        row = ["DFT_ANALOG_EN","DFT_SELP","CMPIP_SEL","CMPIN_SEL","TIA_FINE0","TIA_COARSE1","DFT_EN_TIA_SENVNB",
                             "VREF_SEL","AUX_EN","PRA_DAC","D2S_HGB","D2S_DAC","VN_SEL","EN_PFE","DFT_SELN",
                             "DFT_ANALOG_SEL","YODA_EN","SP_RST","DFT_RSNS","DFT_SEL_TIA_SENVN","DFT_TIA_EN_VP",
                             "GM_DACA","REF_ENH","REF_ENL","AMP_ATT","BM_CTRL","DFT_EN_PRA","DFT_CLK_OUT","GM_DAC",
                             "AVN_EN"]
        q = int(QSTR)
        cls = int(CLSSTR)
        col = int(COLSTR)
        pix = 0
        for obj in q_list_col[q]:
            l1 = [q,cls,col,pix]
            pfe_val_list=[]
            for a in row:
                pfe_val_list.append(hex(getattr(obj.PFE_Bits,a)))
            l2 = pfe_val_list
            print("1",l1)
            print("2",l2)
            l1 = l1+l2
            writer.writerow(l1)
            pix +=1

def dump_vector_cls_to_file():

#    rownum = 0
    NUM_OF_QUARTERS              = 4
    NUM_OF_CLUSTERS_IN_Q         = 12
    NUM_OF_COLUMNS_IN_CLUSTER    = 8
    NUM_OF_PIXELS_IN_COL         = 32
    NUM_OF_PIXELS_IN_CLUSTER     = 256

    with open(r"C:\Orix_SDK\workDir\data\cluster_vector_dump_em.csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #write first row with column name - even if it exists

        writer.writerow(["quarter_number","cluster_number","column_number","pixel_number","DFT_ANALOG_EN",
                             "DFT_SELP","CMPIP_SEL","CMPIN_SEL","TIA_FINE0","TIA_COARSE1","DFT_EN_TIA_SENVNB",
                             "VREF_SEL","AUX_EN","PRA_DAC","D2S_HGB","D2S_DAC","VN_SEL","EN_PFE","DFT_SELN",
                             "DFT_ANALOG_SEL","YODA_EN","SP_RST","DFT_RSNS","DFT_SEL_TIA_SENVN","DFT_TIA_EN_VP",
                             "GM_DACA","REF_ENH","REF_ENL","AMP_ATT","BM_CTRL","DFT_EN_PRA","DFT_CLK_OUT","GM_DAC",
                             "AVN_EN"])
        row = ["DFT_ANALOG_EN","DFT_SELP","CMPIP_SEL","CMPIN_SEL","TIA_FINE0","TIA_COARSE1","DFT_EN_TIA_SENVNB",
                             "VREF_SEL","AUX_EN","PRA_DAC","D2S_HGB","D2S_DAC","VN_SEL","EN_PFE","DFT_SELN",
                             "DFT_ANALOG_SEL","YODA_EN","SP_RST","DFT_RSNS","DFT_SEL_TIA_SENVN","DFT_TIA_EN_VP",
                             "GM_DACA","REF_ENH","REF_ENL","AMP_ATT","BM_CTRL","DFT_EN_PRA","DFT_CLK_OUT","GM_DAC",
                             "AVN_EN"]
        q = int(QSTR)
        cls = int(CLSSTR)
        col = 0
        pix = 0
        for obj in q_list_cls[q]:
            l1 = [q,cls,col,pix]
            pfe_val_list=[]
            for a in row:
                pfe_val_list.append(hex(getattr(obj.PFE_Bits,a)))
            l2 = pfe_val_list
            print("1",l1)
            print("2",l2)
            l1 = l1+l2
            writer.writerow(l1)
            pix +=1
            if pix==NUM_OF_PIXELS_IN_COL:
                pix = 0
                col +=1
#                if col == NUM_OF_COLUMNS_IN_CLUSTER:
#                    col = 0
#                    cls +=1
#                    if cls == NUM_OF_CLUSTERS_IN_Q:
#                        cls = 0
#                        q += 1

####################
# main
####################
if __name__ == "__main__":

    Connect(emulation=True)


    ###################
    # Creating objects
    # Test Phase - Init
    ###################
    sr = Sr(pfe_calib_file=r'C:\Orix_SDK\workDir\data\pfe_calib_values_em.csv')           # for non-default host IP/path-to-csv-files "Sr(host = <ip>, path=<path>)"

    QSTR="0"
    CLSSTR="4"
    COLSTR="3"
    PIXSTR="0:31"
    NAME='DEFAULT_LOW'
    CF=r'C:\Orix_SDK\workDir\data\pfe_calib_values_em.csv'
    #CF=r"C:\Orix_SDK\workDir\data\alla.csv"
    #VEC=r"C:\Orix_SDK\workDir\cluster_get_PFE.csv"
    #FISTR='GM_DAC'
    #VEC=[3]*256
    FISTR="ALL"

    sr.loadPFE(Q=QSTR,CLS=CLSSTR,COL=COLSTR,PIX=PIXSTR,V=NAME)
    #sr.cs_column_set_PFE(Q=QSTR,CLS='3',COL='5',FIELD="ALL",V=VEC)
    q_list_cls=sr.cs_cluster_get_PFE(Q=QSTR,CLS=CLSSTR,FIELD=FISTR)
    q_list_col=sr.cs_column_get_PFE(Q=QSTR,CLS=CLSSTR,COL=COLSTR,FIELD=FISTR)
    sr.save_calibPFE(filename=CF)
    #pfe_obj = sr.get_sr_dict_obj("PFE",NAME)

    if FISTR=="ALL":
        dump_vector_col_to_file()
        dump_vector_cls_to_file()

    else:
        with open('cluster_get_PFE_em.csv', 'w') as outFile:
            outFile.write(str(FISTR)+"\n")
            for line in q_list_cls[int(QSTR)]:
                outFile.write(hex(line)+"\n")
                print(hex(line))
        outFile.close()
        with open('columnr_get_PFE_em.csv', 'w') as outFile1:
            outFile1.write(str(FISTR)+"\n")
            for line1 in q_list_col[int(QSTR)]:
                outFile1.write(hex(line1)+"\n")
                print(hex(line1))
        outFile1.close()

    sr.rpcClient.call("stop_server")
