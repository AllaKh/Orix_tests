#!/usr/bin/env python3
###############################################################################
#                              file: sr_basic_connect.py                      #
#                                                                             #
# 	author: Alla Khananashvili                                                #
# 	date: Apr-18-2019                                                         #
#                                                                             #
# 	version: 2.0                                                              #
# 	python version: 3.6	                                                      #
#                                                                             #
#   Description:                                                              #
#   Load test for most important functionaliry of ShiftRegister (SR)          #
#                                                                             #
#   1. In FPGA mode connect to Master FPGA via Ehernet.                       #
#                                                                             #
#   2. Run Power Sequence commands                                            #
#                                                                             #
#   3. Update some pixels in some columns of some clustes in one quoter       #
#       according to the specific field in pfe_registers.csv table            #
#       and save them into the calibration file.                              #
#                                                                             #
#   4. Update some BAs in some clustes in one quoter                          #
#       according to the specific field in ba_registers.csv table             #
#       and save them into the calibration file.                              #
#                                                                             #
#   5. Update some PLLs in some clustes in one quoter                         #
#       according to the specific field in pll_registers.csv table            #
#       and save them into the calibration file.                              #
#                                                                             #
#   6. Update some TXs in some clustes in one quoter                          #
#       according to the specific field in tx_registers.csv table             # 
#       and save them into the calibration file.                              #
#                                                                             #
#   7. Update dump files from SR via "Get" API                                #
#      and save them into the dump and calibration files:                     #
#       a. sr.cs_cluster_get_PFE updates all fields of specific cluster       #
#           in one quoter.                                                    #
#       b. sr.cs_column_get_PFE updates specific field in one column          #
#           of specific cluster in one quoter.                                #
#                                                                             #
#   8. Set all fields or specific field of cluster/column via "Set" API:      #
#       a. sr.cs_cluster_set_PFE sets all fields of specific cluster          #
#           in one quoter according to the vectors from specific dump file.   #
#       b. sr.cs_column_set_PFE sets with the same value the specific field   #
#           in one column of specific cluster in one quoter.                  #
#                                                                             #
#   9. Save all the updates into calibration file.                            #
#                                                                             #
#	10. Test API Stop Server.  							     			 	  #
#                                                                             #
###############################################################################

#region Imports
from oryxsdk import AD569X
from oryxsdk import si5341
######################################################
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

#Import Python libraries
import time
import csv

#Create table structure
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

#Write vector of pixels into the spesific column
def dump_vector_col_to_file():
    
    with open(r"C:\Orix_SDK\workDir\data\col_vector_dump.csv", 'w', newline='') as f:
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

#Write vector of pixels into the specific clustes
def dump_vector_cls_to_file():
    
    NUM_OF_QUARTERS              = 4
    NUM_OF_CLUSTERS_IN_Q         = 12
    NUM_OF_COLUMNS_IN_CLUSTER    = 8
    NUM_OF_PIXELS_IN_COL         = 32
    NUM_OF_PIXELS_IN_CLUSTER     = 256
    
    with open(r"C:\Orix_SDK\workDir\data\cluster_vector_dump.csv", 'w', newline='') as f:
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

#Create one PFE object from specific row in the dump file
def createPfeObjFromRow(row, header):
    pfe = PFE()

    index = 0
    for col in row:
        setattr(pfe.PFE_Bits,header[index], int(col,16))
        index +=1
        print("PFE", pfe)
    return pfe

#Create vector of PFE objects from the dump file
def get_vector_from_file():    

    # while True:
    #     try:
    #         pfe_vector_file = open(input("Enter dump filemane and path: ", "r"))
    #     except FileNotFoundError:
    #         print("This file doesn't exists, please check its name and path and try again")
    #     else:
    #         break

    pfe_vector_file = open(r"C:\Orix_SDK\workDir\data\real_column_vector_dump_fpga.csv", "r")    
    reader = csv.reader(pfe_vector_file)
    
    pfe_bitfield_names_list = ["DFT_ANALOG_EN","DFT_SELP","CMPIP_SEL","CMPIN_SEL","TIA_FINE0","TIA_C OARSE1","DFT_EN_TIA_SENVNB",
                             "VREF_SEL","AUX_EN","PRA_DAC","D2S_HGB","D2S_DAC","VN_SEL","EN_PFE","DFT_SELN",
                             "DFT_ANALOG_SEL","YODA_EN","SP_RST","DFT_RSNS","DFT_SEL_TIA_SENVN","DFT_TIA_EN_VP",
                             "GM_DACA","REF_ENH","REF_ENL","AMP_ATT","BM_CTRL","DFT_EN_PRA","DFT_CLK_OUT","GM_DAC",
                             "AVN_EN"]    
    local_pfe_list = []
    if pfe_bitfield_names_list:
        next(reader)
    for row in reader:
        local_pfe_list.append(createPfeObjFromRow(row[4:len(row)-1],pfe_bitfield_names_list))
        print("ROW", row)
    pfe_vector_file.close()
    
    return local_pfe_list
####################
# main
####################  
if __name__ == "__main__":

    for i in range(100000000):
        print("attempt :",i)
        #Connect(emulation=True)
        Connect(param='--fpga_ip_zynq 10.99.0.172')
        sr = Sr()           # for non-default host IP/path-to-csv-files "Sr(host = <ip>, path=<path>)"

        fpga = Fpga(MASTER) # Fpga(SLAVE) for slave 
        pwrseq = PowerSeq()
        #Connect(param ='--modules-log FtdiProtocol:1')
        
        #region Init DAC Objects
        #Init DAC Objects
        dac_vbias_q0_q1 = AD569X(0, 0xC, 1, 2499)     #DAC Channel A
        dac_vbias_q2_q3 = AD569X(0, 0xC, 2, 2499)     #DAC Channel B
        dac_VDDA_ldo    = AD569X(0, 0xC, 4,  100)     #DAC Channel C
        dac_VEEA_ldo    = AD569X(0, 0xC, 8, 2499)     #DAC Channel D
    #endregion
        #region Set DAC Initial Values
        #Set VANA LDO DAC Channel to 0v
        dac_VDDA_ldo.SetVoltage(2500)
    #endregion
    
    #region Init Clock Synthesizer
        #Init SI5341 Object
        clock_synth = si5341.SI5341(0,0x75)
        #Load Clock Configuration From File
        CurrentDir = os.path.dirname(os.path.abspath(__file__))
        Clock_Config_File = "data\\Si5341-RevD-ALL_Q_LVCMOS-Registers.txt"
        clock_synth.LoadFile(os.path.join(CurrentDir, Clock_Config_File))
        
        ###################
        # Creating objects
        # Test Phase - Init    
        ###################
        
        print("Basic connect passed")
        time.sleep(3) 
        #host='127.0.0.1'
        print("PWR_SEQ Status Reg = ", hex(fpga.readReg32(PWR_SEQ_STATUS_REGISTER)))
        fpga.writeReg32(PWR_SEQ_CLR_STATUS_REGISTER, 1)
        print("PWR_SEQ Status Reg (after clear)= ", hex(fpga.readReg32(PWR_SEQ_STATUS_REGISTER)))        

    #Set parameters
        QSTR="0"
        CLSSTR="0:2,11,8:10,3,5:7,4"
        COLSTR="0:5,6:7"
        PIXSTR="2:6,25:30,10:15,8,0,20:23,1,7,9,16:19,24,31"
        PLLSTR="1:3,4:5,0"    
        NAME_PFE='DEFAULT_LOW' 
        NAME_TX='DEFAULT_PAT2'
        NAME_BA='MY_BA_1'
        NAME_PLL='PLL_DEF'
        TY=PLL_EVEN
        CF=r'C:\Orix_SDK\workDir\data\pfe_calib_values_fpga.csv'
        FISTR1='GM_DAC'
        FISTR="ALL"
        VEC=get_vector_from_file()
        VEC1=[3]*32        

    #Run APIs 
        sr.loadPFE(Q=QSTR,CLS=CLSSTR,COL=COLSTR,PIX=PIXSTR,V=NAME_PFE)
        sr.loadBA(Q=QSTR,CLS=CLSSTR,V=NAME_BA)
        sr.loadPLL(Q=QSTR,PLL=PLLSTR,V=NAME_PLL,TYPE=TY)
        sr.loadTX(Q=QSTR,CLS=CLSSTR,V=NAME_TX)  
        sr.cs_cluster_set_PFE(Q=QSTR,CLS='4',FIELD=FISTR,V=VEC)
        sr.cs_column_set_PFE(Q=QSTR,CLS='3',COL='5',FIELD=FISTR1,V=VEC1)
        q_list_cls=sr.cs_cluster_get_PFE(Q=QSTR,CLS='3',FIELD=FISTR)
        q_list_col=sr.cs_column_get_PFE(Q=QSTR,CLS='4',COL='3',FIELD=FISTR)     
        # q_list_cls=sr.cs_cluster_get_PFE(Q=QSTR,CLS='3',FIELD=FISTR1)
        # q_list_col=sr.cs_column_get_PFE(Q=QSTR,CLS='4',COL='3',FIELD=FISTR1)              
        sr.save_calibPFE(filename=CF)
 
        if FISTR == "ALL":
            dump_vector_col_to_file()
            dump_vector_cls_to_file()

        else:        
            with open('cluster_get_PFE.csv', 'w') as outFile:
                outFile.write(str(FISTR)+"\n")
                for line in q_list_cls[int(QSTR)]:
                    outFile.write(hex(line)+"\n")
                    print(hex(line))
    
            with open('columnr_get_PFE.csv', 'w') as outFile1:
                outFile1.write(str(FISTR)+"\n")
                for line1 in q_list_col[int(QSTR)]:
                    outFile1.write(hex(line1)+"\n")
                    print(hex(line1))

        if i<99999999:
            print("Stopping")
            sr.rpcClient.call("stop_server")
            print("Stop")
            time.sleep(2)       
        else:
            time.sleep(3)
