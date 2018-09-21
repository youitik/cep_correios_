
# import biliotecas
from datetime import datetime
import numpy as np
import pandas as pd
import correios.py
import correios as cr


# Import Tabelas
df = pd.read_csv('C:\Users\daniel.kabata\Desktop\TABELA_FRETE_RJ\cidade_cep.csv',delimiter=";")

# Lista de CEPS de todas cidades destino
df["CEP INICIAL"] = df["CEP INICIAL"].astype(str)
CEPS = df["CEP INICIAL"].tolist()

#Define origens
#CEP_ORIGIM_LIST = ['90000001','20000001','30000001','24000001','12200001','36500001','69932000']
CEP_ORIGIM_LIST = ['36500001','69932000'] #origens Pedro

# Define variaveis (TODAS)
CEPS_LIST = CEPS
ListCEPSDictPAC = []
L_CEPS = []
L_PRAZOS = []
dfFinal = pd.DataFrame()


# Define variaveis (sample)
#CEPS_LIST = ['69900001','69932000','57000001','57840000','69260000']
#ListCEPSDictPAC = []
#CEP_ORIGIM = '90000002'
#L_CEPS = []
#L_PRAZOS = []
#dfFinal = pd.DataFrame()



def calculaPrazoSedex(CEPS_LIST,ListCEPSDictPAC,CEP_O,L_CEPS,L_PRAZOS,dfFinal):
    tstart = datetime.now()
    for CEP in CEPS_LIST:
        CEPDict = {
              "empresa": '11035269',
              "senha": '9339936',
              "cod": Correios().SEDEX, 
              "GOCEP": CEP, #Destino
              "HERECEP": CEP_O, #Origem
              "peso": "1",
              "formato": "1", 
              "comprimento": "25",
              "altura": "25",
              "largura": "25",
              "diametro": "1"
        }
        test = cr.Correios().frete(**CEPDict)
        ListCEPSDictPAC.append(CEP + ";" + test['PrazoEntrega'])
        L_CEPS.append(CEP)
        L_PRAZOS.append(test['PrazoEntrega'])

        # Cria DF Final
        dfFinal = pd.DataFrame()
        L_PRAZOS_INT = map(int, L_PRAZOS)

        # Coloca campos e exporta
        dfFinal["CEP_DESTINO"] = L_CEPS
        dfFinal["CEP_ORIGEM"] = CEP_O
        dfFinal["TIPO"] = 'SEDEX'
        dfFinal["TIPO_COD"] = 1
        dfFinal["PRAZO_CORREIOS"] = L_PRAZOS_INT
        dfFinal["DELIVERY_TIME_START"] = dfFinal["PRAZO_CORREIOS"] + 2
        dfFinal["DELIVERY_TIME_END"] = dfFinal["PRAZO_CORREIOS"] + 4
        dfFinal["DELIVERY_TIME_SCALE"] = 'DAYS'
        dfFinal.to_csv('df_'+CEP_O+'_sedex.csv', sep=";", index=False)


    tend = datetime.now()

    print '------------------------'    
    print CEP_O
    print 'SEDEX'
    print tstart
    print tend
    print tend - tstart
    print '------------------------'


def calculaPrazoPAC(CEPS_LIST,ListCEPSDictPAC,CEP_O,L_CEPS,L_PRAZOS,dfFinal):
    tstart = datetime.now()
    for CEP in CEPS_LIST:
        CEPDict = {
              "empresa": '11035269',
              "senha": '9339936',
              "cod": Correios().PAC, 
              "GOCEP": CEP, #Destino
              "HERECEP": CEP_O, #Origem
              "peso": "1",
              "formato": "1", 
              "comprimento": "25",
              "altura": "25",
              "largura": "25",
              "diametro": "1"
        }
        test = cr.Correios().frete(**CEPDict)
        ListCEPSDictPAC.append(CEP + ";" + test['PrazoEntrega'])
        L_CEPS.append(CEP)
        L_PRAZOS.append(test['PrazoEntrega'])

        # Cria DF Final
        dfFinal = pd.DataFrame()
        L_PRAZOS_INT = map(int, L_PRAZOS)

        # Coloca campos e exporta
        dfFinal["CEP_DESTINO"] = L_CEPS
        dfFinal["CEP_ORIGEM"] = CEP_O
        dfFinal["TIPO"] = 'PAC'
        dfFinal["TIPO_COD"] = 51
        dfFinal["PRAZO_CORREIOS"] = L_PRAZOS_INT
        dfFinal["DELIVERY_TIME_START"] = dfFinal["PRAZO_CORREIOS"] + 2
        dfFinal["DELIVERY_TIME_END"] = dfFinal["PRAZO_CORREIOS"] + 4
        dfFinal["DELIVERY_TIME_SCALE"] = 'DAYS'
        dfFinal.to_csv('df_'+CEP_O+'_pac.csv', sep=";", index=False)


    tend = datetime.now()

    print '------------------------'    
    print CEP_O
    print 'SEDEX'
    print tstart
    print tend
    print tend - tstart
    print '------------------------'



# main
for CEP_O in CEP_ORIGIM_LIST:
    
    #limpa
    ListCEPSDictPAC = []
    L_CEPS = []
    L_PRAZOS = []
    dfFinal = pd.DataFrame()
    
    # Calcula SEDEX
    calculaPrazoSedex(CEPS_LIST,ListCEPSDictPAC,CEP_O,L_CEPS,L_PRAZOS,dfFinal)

    
    #limpa
    ListCEPSDictPAC = []
    L_CEPS = []
    L_PRAZOS = []
    dfFinal = pd.DataFrame()

    # Calcula PAC
    calculaPrazoPAC(CEPS_LIST,ListCEPSDictPAC,CEP_O,L_CEPS,L_PRAZOS,dfFinal)   


