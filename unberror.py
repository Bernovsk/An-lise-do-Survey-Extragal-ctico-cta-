import gammalib
import ctools
import cscripts
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from astropy.io import fits
from astropy.table import Table
import itertools


test_bins= [('bin1', 0.2, 0.75),
	    ('bin2', 0.75, 5),
            ('bin3', 5, 50)]

def sim_test(RA, DEC, INOBS, outevents, logobs, emin, emax, outbkgmodel, outmodel, loglike, model, edisp = False):
    #ctobssim, ele simula os eventos em cima do range de energia fornecido através de um arquivo modelo, onde este contem
    #modelo espectral, prefactor, index e pivot energy, esse arquivo é o que deve ser modificado antes das simulações
    #passarem pela função de simulação.
    
    
    
    sim = ctools.ctobssim()
    sim['ra'] = RA
    sim['dec'] = DEC
    sim['inobs'] = INOBS # 
    sim['inmodel'] = model 
    sim['tmin'] = '2021-01-01T00:00'#
    sim['tmax'] = '2021-02-25T00:00'#
    sim['emin'] = emin
    sim['emax'] = emax
    sim['rad'] = 4.0#
    sim['maxrate'] = 1e7
    sim['edisp'] = edisp
    sim['outevents'] = outevents
    sim['logfile'] = logobs
    sim.logFileOpen()
    sim.execute()

    like =ctools.ctlike()
    like['inobs'] = outevents #
    like['outmodel'] = outmodel #
    like['inmodel'] = outbkgmodel #
    like['logfile'] = loglike
    like.logFileOpen()
    like.execute()
    
    return


def root_tree(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    value = []
    scale = []
    for spectrum in root.findall(".//*[@name='Src001']/spectrum/parameter"):
        value.append(float(spectrum.get('value')))
        scale.append(float(spectrum.get('scale')))
        #print(spectrum.get('value'))
    final_value = np.asarray(value)*np.asarray(scale)
    return final_value #[x*y for x in value for y in scale]


def prefactor_mod1(filename, x):
    tree = ET.parse(filename)
    root = tree.getroot()    
    prf = root.find(".//*[@name='Src001']/spectrum/parameter[@name='Prefactor']")
    prf.attrib["value"]= str(float(prf.attrib["value"]) + x) #"value"
    #print(prf.attrib["value"])
    tree.write(filename,encoding="UTF-8", xml_declaration=True)
    return (float(prf.attrib["value"]))
def ts_get(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for source in root.findall(".//*[@name='Src001']"):
        ts = source.get('ts')
        #print(float(ts))
    return float(ts)

def test_ts(RA, DEC, INOBS,outevents, logobs, emin, emax, outbkgmodel, outmodel, loglike, filename, edisp = False):
    sim_test(RA, DEC, INOBS,outevents, logobs, emin, emax, outbkgmodel, outmodel, loglike, filename, edisp = False)
    ts = ts_get(outmodel)
    pr = prefactor_mod1(filename, + 0.2)
    
    
    return (pr, ts)

#print("-----------BIN 01 - 01-----------")# REG ra 246, dec 38

#prefactorbin1_reg1 = []
#tsvaluebin1_reg1 = []
#for x in range(160):
#    print("Run", x+1)
#    prf, ts = test_ts(246, 38, 'inobs1.xml','errortesteventlist.xml', 'errortestsim.log', 0.2, 0.75, 'errortestbkgmodel.xml', 'errortest1like1.xml', 'errortest1like1.log', 'simsource1_1.xml')
#    print( "prf=", prf, "ts=", ts)
#    prefactorbin1_reg1.append(prf)
#    tsvaluebin1_reg1.append(ts)
#    print("__________________________________")

#plt.figure()	
#plt.plot(prefactorbin1_reg1, tsvaluebin1_reg1, "k-o")
#plt.grid()
#plt.title('bin1')
#plt.xlabel('prefactor')
#plt.ylabel('tsvalue')
#plt.grid(True) 
#plt.savefig("ts_pref_bin1_re1.png")

print("-----------BIN 01 - 02-----------")#REG ra 195.6, dec 1.5

prefactorbin1_regl2 = []
tsvaluebin1_regl2 = []
for y in range(160):
    print("Run", y+1)
    prf, ts = test_ts(195.6, 1.5, 'inobs2.xml','errortest2eventlist.xml', 'errortest2sim.log', 0.2, 0.75, 'errortestbkgm2.xml', 'errortest1like2.xml', 'errortest1like2.log', 'simsource1_2.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin1_regl2.append(prf)
    tsvaluebin1_regl2.append(ts)
    print("_________________________________")


plt.figure()	
plt.plot(prefactorbin1_regl2, tsvaluebin1_regl2, "r-o") 
plt.grid()
plt.title('bin1_2')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin1_regl2.png")

#print("-----------BIN 01 - 03-----------")#REG ra 181.7, dec -35.6

#prefactorbin1_reg3 = []
#tsvaluebin1_reg3 = []
#for z in range(160):
#    print("Run", z+1)
#    prf, ts = test_ts(181.7, -35.6, 'inobs3.xml', 'errortest3eventlist.xml', 'errortest3sim.log', 0.2, 0.75, 'errortestbkgm3.xml', 'errortest1like3.xml', 'errortest1like3.log', 'simsource1_3.xml')
#    print( "prf=", prf, "ts=", ts)
#    prefactorbin1_reg3.append(prf)
#    tsvaluebin1_reg3.append(ts)
#    print("________________________________")


#plt.figure()	
#plt.plot(prefactorbin1_reg3, tsvaluebin1_reg3, "g-o")
#plt.grid()
#plt.title('bin1_3')
#plt.xlabel('prefactor')
#plt.ylabel('tsvalue')
#plt.grid(True) 
#plt.savefig("ts_pref_bin1_re3.png")


with open("prf_tsbin1reg2_2.txt", "w") as f:
#    f.write("Região 1\n Prefactor \n ")
#    f.write(" ".join(str(a) for a in prefactorbin1_reg1) + "\n ts \n")
#    f.write(" ".join(str(a) for a in tsvaluebin1_reg1) + "\n")	
    f.write("Região 2_2\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin1_regl2) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin1_regl2) + "\n")
#    f.write("Região 3\n Prefactor \n ")
#    f.write(" ".join(str(a) for a in prefactorbin1_reg3) + "\n ts \n")
#    f.write(" ".join(str(a) for a in tsvaluebin1_reg3) + "\n")

print("-----------BIN 02 - 01 -----------")

prefactorbin2_reg1 = []
tsvaluebin2_reg1 = []
for x in range(160):
    print("Run", x+1)
    prf, ts = test_ts(246, 38, 'inobs1.xml', 'errortesteventlist.xml', 'errortestsim.log', 0.75, 5, 'errortestbkgmodel.xml', 'errortest2like1.xml', 'errortest2like1.log', 'simsource2_1.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin2_reg1.append(prf)
    tsvaluebin2_reg1.append(ts)
    print("__________________________________")

plt.figure()	
plt.plot(prefactorbin2_reg1, tsvaluebin2_reg1, "k-o")
plt.grid()
plt.title('bin2_1')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin2_re1.png")

print("-----------BIN 02 - 02 -----------")

prefactorbin2_reg2 = []
tsvaluebin2_reg2 = []
for y in range(160):
    print("Run", y+1)
    prf, ts = test_ts(195.6, 1.5, 'inobs2.xml', 'errortest2eventlist.xml', 'errortest2sim.log', 0.75, 5, 'errortestbkgm2.xml', 'errortest2like2.xml', 'errortest2like2.log', 'simsource2_2.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin2_reg2.append(prf)
    tsvaluebin2_reg2.append(ts)
    print("_________________________________")


plt.figure()	
plt.plot(prefactorbin2_reg2, tsvaluebin2_reg2, "r-o")
plt.grid()
plt.title('bin2_2')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin2_re2.png")

print("-----------BIN 02 - 03-----------")

prefactorbin2_reg3 = []
tsvaluebin2_reg3 = []
for z in range(160):
    print("Run", z+1)
    prf, ts = test_ts(181.7, -35.6, 'inobs3.xml', 'errortest3eventlist.xml', 'errortest3sim.log', 0.75, 5, 'errortestbkgm3.xml', 'errortest2like3.xml', 'errortest2like3.log', 'simsource2_3.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin2_reg3.append(prf)
    tsvaluebin2_reg3.append(ts)
    print("________________________________")


plt.figure()	
plt.plot(prefactorbin2_reg3, tsvaluebin2_reg3, "g-o")
plt.grid()
plt.title('bin2_3')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin2_re3.png")

with open("prf_tsbin2.txt", "w") as f:
    f.write("Região 1\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin2_reg1) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin2_reg1) + "\n")	
    f.write("Região 2\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin2_reg2) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin2_reg2) + "\n")
    f.write("Região 3\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin2_reg3) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin2_reg3) + "\n")


print("-----------BIN 03 - 01-----------")
prefactorbin3_reg1 = []
tsvaluebin3_reg1 = []
for x in range(160):
    print("Run", x+1)
    prf, ts = test_ts(246, 38, 'inobs1.xml', 'errortesteventlist.xml', 'errortestsim.log', 5, 50, 'errortestbkgmodel.xml', 'errortest3like1.xml', 'errortest3like1.log', 'simsource3_1.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin3_reg1.append(prf)
    tsvaluebin3_reg1.append(ts)
    print("__________________________________")

plt.figure()	
plt.plot(prefactorbin3_reg1, tsvaluebin3_reg1, "k-o")
plt.grid()
plt.title('bin3_1')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin3_re1.png")

print("-----------BIN 03 - 02-----------")

prefactorbin3_reg2 = []
tsvaluebin3_reg2 = []
for y in range(160):
    print("Run", y+1)
    prf, ts = test_ts(195.6, 1.5, 'inobs2.xml','errortest2eventlist.xml', 'errortest2sim.log', 5, 50, 'errortestbkgm2.xml', 'errortest3like2.xml', 'errortest3like2.log', 'simsource3_2.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin3_reg2.append(prf)
    tsvaluebin3_reg2.append(ts)
    print("_________________________________")


plt.figure()	
plt.plot(prefactorbin3_reg2, tsvaluebin3_reg2, "r-o")
plt.grid()
plt.title('bin3_2')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin3_re2.png")

print("-----------BIN 03 - 03 -----------") 

prefactorbin3_reg3 = []
tsvaluebin3_reg3 = []
for z in range(160):
    print("Run", z+1)
    prf, ts = test_ts(181.7, -35.6, 'inobs3.xml', 'errortest3eventlist.xml', 'errortest3sim.log', 5, 50, 'errortestbkgm3.xml', 'errortest3like3.xml', 'errortest3like3.log', 'simsource3_3.xml')
    print( "prf=", prf, "ts=", ts)
    prefactorbin3_reg3.append(prf)
    tsvaluebin3_reg3.append(ts)
    print("________________________________")


plt.figure()	
plt.plot(prefactorbin3_reg3, tsvaluebin3_reg3, "g-o")
plt.grid()
plt.title('bin3_3')
plt.xlabel('prefactor')
plt.ylabel('tsvalue')
plt.grid(True) 
plt.savefig("ts_pref_bin3_re3.png")


with open("prf_tsbin3.txt", "w") as f:
    f.write("Região 1\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin3_reg1) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin3_reg1) + "\n")	
    f.write("Região 2\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin3_reg2) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin3_reg2) + "\n")
    f.write("Região 3\n Prefactor \n ")
    f.write(" ".join(str(a) for a in prefactorbin3_reg3) + "\n ts \n")
    f.write(" ".join(str(a) for a in tsvaluebin3_reg3) + "\n")
