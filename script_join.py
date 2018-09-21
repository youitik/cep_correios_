# coding: utf-8
#import bibliotecas
import pandas as pd
import numpy as np


# variaveis de entrada
#['BELO HORIZONTE','NITEROI','PORTO ALEGRE','RIO DE JANEIRO','SAO JOSE DOS CAMPOS','UBA']
# faltando BELO HORIZONTE RIO DE JANEIRO SAO JOSE DOS CAMPOS
arquivo_cidade = ['RIO DE JANEIRO','BELO HORIZONTE','NITEROI','PORTO ALEGRE','SAO JOSE DOS CAMPOS','UBA']


def layout_colunado_prazos(table_ordered_final,arquivo_cidade):
    
    # importa prazos
    df_prazos = pd.read_csv("arquivos_origens/ARQUIVO_PRAZOS.csv", sep = ';')
    df_prazos.columns = ['CEP_INICIAL', 'ORIGIN_ZIP_START','SERVICE','SERVICE_UID','PRAZO_CORREIOS','DELIVERY_TIME_START','DELIVERY_TIME_END','DELIVERY_TIME_SCALE']
    
    # trata prazos
    df_prazos['SERVICE_UID'] = np.where(df_prazos['SERVICE_UID']==51, 52, df_prazos['SERVICE_UID'])
    
    # cria pivot table com prazos
    table = pd.pivot_table(df_prazos, values=['DELIVERY_TIME_START','DELIVERY_TIME_END'], index=['CEP_INICIAL','ORIGIN_ZIP_START'],
                columns=['SERVICE_UID'], aggfunc=np.max)
    
    # tratamentos de index
    # remove multiindex
    table.columns = table.columns.map('{0[0]}_{0[1]}'.format)

    # reset index
    table = table.reset_index()

    # trata nomes de colunas
    table.columns = ['CEP_INICIAL','ORIGIN_ZIP_START','DELIVERY_TIME_START_52','DELIVERY_TIME_END_52','DELIVERY_TIME_START_1','DELIVERY_TIME_END_1']
    table_ordered = table[['ORIGIN_ZIP_START','CEP_INICIAL','DELIVERY_TIME_START_1','DELIVERY_TIME_END_1','DELIVERY_TIME_START_52','DELIVERY_TIME_END_52']]
    
    # merge dataframes - origim
    try:
        table_final_layout = pd.merge(table_ordered_final,table_ordered,on=['ORIGIN_ZIP_START','CEP_INICIAL'], how='left')
        print '------------------------'
        print 'join sucesso - colunado - prazos'
        print 'linhas: ' + str(len(table_final_layout))
        print 'qtd nulos: ' + str(table_final_layout['DELIVERY_TIME_START_1'].isnull().sum())
        print arquivo_cidade
        print '------------------------'

    except:
        print '------------------------'
        print 'nao conseguiu fazer o join - prazos '
        print arquivo_cidade
        print '------------------------'


    # ordenacao tabela final
    table_final_layout_ordered = table_final_layout[['UF_ORIGIN','UF_CITY_ORIGIN','TYPE_CITY_ORIGIN','ORIGIN_ZIP_START','ORIGIN_ZIP_END','UF_END','UF_CITY_END','TYPE_CITY_END','CEP_INICIAL','CEP_FINAL','SHIPPING_COST_1_300G','SHIPPING_COST_1_500G','SHIPPING_COST_1_1KG','SHIPPING_COST_1_2KG','SHIPPING_COST_1_3KG','SHIPPING_COST_1_4KG','SHIPPING_COST_1_5KG','SHIPPING_COST_1_6KG','SHIPPING_COST_1_7KG','SHIPPING_COST_1_8KG','SHIPPING_COST_1_9KG','SHIPPING_COST_1_10KG','SHIPPING_COST_52_500G','SHIPPING_COST_52_1KG','SHIPPING_COST_52_2KG','SHIPPING_COST_52_3KG','SHIPPING_COST_52_4KG','SHIPPING_COST_52_5KG','SHIPPING_COST_52_6KG','SHIPPING_COST_52_7KG','SHIPPING_COST_52_8KG','SHIPPING_COST_52_9KG','SHIPPING_COST_52_10KG','DELIVERY_TIME_START_1','DELIVERY_TIME_END_1','DELIVERY_TIME_START_52','DELIVERY_TIME_END_52']]

    # trata datas sem PAC
    table_final_layout_ordered['DELIVERY_TIME_START_52'] = np.where(table_final_layout_ordered['SHIPPING_COST_52_500G'].isnull(),'',table_final_layout_ordered['DELIVERY_TIME_START_52'])
    table_final_layout_ordered['DELIVERY_TIME_END_52'] = np.where(table_final_layout_ordered['SHIPPING_COST_52_500G'].isnull(),'',table_final_layout_ordered['DELIVERY_TIME_END_52'])

    
    #table_final_layout_ordered.to_csv('arquivos_gerados_colunados/TABELA_FRETE_FINAL_'+arquivo_cidade+'_COLUNADO.csv',index=False,sep=';')

    return table_final_layout_ordered


def gera_novo_formato(df, arquivo_cidade):
    
    # import de arquivos
    df_cidades = pd.read_csv("arquivos_origens/cidade_cep.csv", sep = ';')
    print 'generating nice layout for ' + arquivo_cidade + '...'
    
    # marca cep de origem e destino
    ORIGEM_S = df['ORIGIN_ZIP_START'][1]
    ORIGEM_E = df['ORIGIN_ZIP_END'][1]
   
    # cria pivot table com servico e peso como colunas
    table = pd.pivot_table(df, values=['SHIPPING_COST'], index=['CEP_INICIAL', 'CEP_FINAL'],
                columns=['SERVICE_UID','WEIGHT_START'], aggfunc=np.max)
    
    # tratamentos de index
    # remove multiindex
    table.columns = table.columns.map('{0[0]}_{0[1]}'.format)
    
    # reset index
    table = table.reset_index()
    
    # cria colunas de origem
    table['ORIGIN_ZIP_START'] = ORIGEM_S
    table['ORIGIN_ZIP_END'] = ORIGEM_E
    
    # trata nomes de colunas
    table.columns = ['CEP_INICIAL','CEP_FINAL','SHIPPING_COST_1_300G','SHIPPING_COST_1_500G','SHIPPING_COST_1_1KG','SHIPPING_COST_1_2KG','SHIPPING_COST_1_3KG','SHIPPING_COST_1_4KG','SHIPPING_COST_1_5KG','SHIPPING_COST_1_6KG','SHIPPING_COST_1_7KG','SHIPPING_COST_1_8KG','SHIPPING_COST_1_9KG','SHIPPING_COST_1_10KG','SHIPPING_COST_52_500G','SHIPPING_COST_52_1KG','SHIPPING_COST_52_2KG','SHIPPING_COST_52_3KG','SHIPPING_COST_52_4KG','SHIPPING_COST_52_5KG','SHIPPING_COST_52_6KG','SHIPPING_COST_52_7KG','SHIPPING_COST_52_8KG','SHIPPING_COST_52_9KG','SHIPPING_COST_52_10KG','ORIGIN_ZIP_START','ORIGIN_ZIP_END']
    table_ordered = table[['ORIGIN_ZIP_START','ORIGIN_ZIP_END','CEP_INICIAL','CEP_FINAL','SHIPPING_COST_1_300G','SHIPPING_COST_1_500G','SHIPPING_COST_1_1KG','SHIPPING_COST_1_2KG','SHIPPING_COST_1_3KG','SHIPPING_COST_1_4KG','SHIPPING_COST_1_5KG','SHIPPING_COST_1_6KG','SHIPPING_COST_1_7KG','SHIPPING_COST_1_8KG','SHIPPING_COST_1_9KG','SHIPPING_COST_1_10KG','SHIPPING_COST_52_500G','SHIPPING_COST_52_1KG','SHIPPING_COST_52_2KG','SHIPPING_COST_52_3KG','SHIPPING_COST_52_4KG','SHIPPING_COST_52_5KG','SHIPPING_COST_52_6KG','SHIPPING_COST_52_7KG','SHIPPING_COST_52_8KG','SHIPPING_COST_52_9KG','SHIPPING_COST_52_10KG']]

    # cria dataframes para merge origem destino localidades
    df_cidades_destino = df_cidades[['CEP_INICIAL','UF','UF_LOCALIDADE','TIPO']]
    df_cidades_destino.columns = ['CEP_INICIAL','UF_END','UF_CITY_END','TYPE_CITY_END']

    df_cidades_origem = df_cidades[['CEP_INICIAL','UF','UF_LOCALIDADE','TIPO']]
    df_cidades_origem.columns = ['ORIGIN_ZIP_START','UF_ORIGIN','UF_CITY_ORIGIN','TYPE_CITY_ORIGIN']

    
    # merge dataframes - destiny
    try:
        table_city = pd.merge(table_ordered,df_cidades_destino,on=['CEP_INICIAL'], how='left')
        print '------------------------'
        print 'join sucesso - colunado'
        print 'linhas: ' + str(len(table_city))
        print 'qtd nulos: ' + str(table_city['UF_END'].isnull().sum())
        print arquivo_cidade
        print '------------------------'

    except:
        print '------------------------'
        print 'nao conseguiu fazer o join'
        print arquivo_cidade
        print '------------------------'


    # merge dataframes - origim
    try:
        table_city_origin = pd.merge(table_city,df_cidades_origem,on=['ORIGIN_ZIP_START'], how='left')
        print '------------------------'
        print 'join sucesso - colunado'
        print 'linhas: ' + str(len(table_city_origin))
        print 'qtd nulos: ' + str(table_city_origin['UF_ORIGIN'].isnull().sum())
        print arquivo_cidade
        print '------------------------'

    except:
        print '------------------------'
        print 'nao conseguiu fazer o join'
        print arquivo_cidade
        print '------------------------'

        
    # ordenacao tabela final
    table_ordered_final = table_city_origin[['UF_ORIGIN','UF_CITY_ORIGIN','TYPE_CITY_ORIGIN','ORIGIN_ZIP_START','ORIGIN_ZIP_END','UF_END','UF_CITY_END','TYPE_CITY_END','CEP_INICIAL','CEP_FINAL','SHIPPING_COST_1_300G','SHIPPING_COST_1_500G','SHIPPING_COST_1_1KG','SHIPPING_COST_1_2KG','SHIPPING_COST_1_3KG','SHIPPING_COST_1_4KG','SHIPPING_COST_1_5KG','SHIPPING_COST_1_6KG','SHIPPING_COST_1_7KG','SHIPPING_COST_1_8KG','SHIPPING_COST_1_9KG','SHIPPING_COST_1_10KG','SHIPPING_COST_52_500G','SHIPPING_COST_52_1KG','SHIPPING_COST_52_2KG','SHIPPING_COST_52_3KG','SHIPPING_COST_52_4KG','SHIPPING_COST_52_5KG','SHIPPING_COST_52_6KG','SHIPPING_COST_52_7KG','SHIPPING_COST_52_8KG','SHIPPING_COST_52_9KG','SHIPPING_COST_52_10KG']]

    # inclui prazos
    df_final_export = layout_colunado_prazos(table_ordered_final,arquivo_cidade)
    
    df_final_export.to_csv('arquivos_gerados_colunados/TABELA_FRETE_FINAL_'+arquivo_cidade+'_COLUNADO.csv',index=False,sep=';')
    
    return table_ordered_final


def join_prazos_check(arquivo_cidade):
    
    #import tabelas
    df_final = pd.read_csv("arquivos_origens/TABELA_FRETE_CHECK_"+arquivo_cidade+".csv",sep = ';')
    df_prazos = pd.read_csv("arquivos_origens/ARQUIVO_PRAZOS.csv", sep = ';')

    # renomeia colunas prazo
    df_prazos.columns = ['CEP_INICIAL', 'ORIGIN_ZIP_START','SERVICE','SERVICE_UID','PRAZO_CORREIOS','DELIVERY_TIME_START','DELIVERY_TIME_END','DELIVERY_TIME_SCALE']
    
      
    # altera tipos das colunas para fazer merge
    df_final['ORIGIN_ZIP_START'] = df_final['ORIGIN_ZIP_START'].astype('int64')
    df_prazos['ORIGIN_ZIP_START'] = df_prazos['ORIGIN_ZIP_START'].astype('int64')

    df_final['CEP_INICIAL'] = df_final['CEP_INICIAL'].astype('int64')
    df_prazos['CEP_INICIAL'] = df_prazos['CEP_INICIAL'].astype('int64')

    df_final['SERVICE_UID'] = df_final['SERVICE_UID'].astype('int64')
    df_prazos['SERVICE_UID'] = df_prazos['SERVICE_UID'].astype('int64')
    
    
    # fixes #########################################################################################
    
    # onde service_uid = 51 entao 52
    df_final['SERVICE_UID'] = np.where(df_final['SERVICE_UID']==51, 52, df_final['SERVICE_UID'])
    df_prazos['SERVICE_UID'] = np.where(df_prazos['SERVICE_UID']==51, 52, df_prazos['SERVICE_UID'])

    # origem uba = 36500000
    df_prazos['ORIGIN_ZIP_START'] = np.where(df_prazos['ORIGIN_ZIP_START']==36500001, 36500000, df_prazos['ORIGIN_ZIP_START'])

    # weigth start nao arredondado
    df_final['WEIGHT_START'] = np.where(df_final['WEIGHT_START']==3.0010000000000003, 3.001, df_final['WEIGHT_START'])

    # fim fixes #########################################################################################
    
    # merge dataframes
    try:
        df_final_com_prazos = pd.merge(df_final,df_prazos,on=['ORIGIN_ZIP_START','CEP_INICIAL','SERVICE_UID'], how='left')
        print '------------------------'
        print 'join sucesso - check'
        print 'linhas: ' + str(len(df_final_com_prazos))
        print 'qtd nulos: ' + str(df_final_com_prazos['DELIVERY_TIME_START'].isnull().sum())
        print arquivo_cidade
        print '------------------------'
    
    except:
        print '------------------------'
        print 'nao conseguiu fazer o join'
        print arquivo_cidade
        print '------------------------'
        
    #export dataframe
    df_final_com_prazos.to_csv('arquivos_gerados_check/TABELA_FRETE_CHECK_'+arquivo_cidade+'_COM_PRAZOS.csv',index=False,sep=';')
    
    return df_final_com_prazos
    

def join_prazos_final(arquivo_cidade):
    
    #import tabelas
    df_final = pd.read_csv("arquivos_origens/TABELA_FRETE_FINAL_"+arquivo_cidade+".csv",sep = ';')
    df_prazos = pd.read_csv("arquivos_origens/ARQUIVO_PRAZOS.csv", sep = ';')

    # renomeia colunas prazo
    df_prazos.columns = ['CEP_INICIAL', 'ORIGIN_ZIP_START','SERVICE','SERVICE_UID','PRAZO_CORREIOS','DELIVERY_TIME_START','DELIVERY_TIME_END','DELIVERY_TIME_SCALE']
    
      
    # altera tipos das colunas para fazer merge
    df_final['ORIGIN_ZIP_START'] = df_final['ORIGIN_ZIP_START'].astype('int64')
    df_prazos['ORIGIN_ZIP_START'] = df_prazos['ORIGIN_ZIP_START'].astype('int64')

    df_final['CEP_INICIAL'] = df_final['CEP_INICIAL'].astype('int64')
    df_prazos['CEP_INICIAL'] = df_prazos['CEP_INICIAL'].astype('int64')

    df_final['SERVICE_UID'] = df_final['SERVICE_UID'].astype('int64')
    df_prazos['SERVICE_UID'] = df_prazos['SERVICE_UID'].astype('int64')
    
    
    # fixes #########################################################################################
    
    # onde service_uid = 52 entao 51
    df_final['SERVICE_UID'] = np.where(df_final['SERVICE_UID']==51, 52, df_final['SERVICE_UID'])
    df_prazos['SERVICE_UID'] = np.where(df_prazos['SERVICE_UID']==51, 52, df_prazos['SERVICE_UID'])

    # origem uba = 36500000
    df_prazos['ORIGIN_ZIP_START'] = np.where(df_prazos['ORIGIN_ZIP_START']==36500001, 36500000, df_prazos['ORIGIN_ZIP_START'])

    # weigth start nao arredondado
    df_final['WEIGHT_START'] = np.where(df_final['WEIGHT_START']==3.0010000000000003, 3.001, df_final['WEIGHT_START'])


    # fim fixes #########################################################################################
    
    # merge dataframes
    try:
        df_final_com_prazos = pd.merge(df_final,df_prazos,on=['ORIGIN_ZIP_START','CEP_INICIAL','SERVICE_UID'], how='left')
        print '------------------------'
        print 'join sucesso - final'
        print 'linhas: ' + str(len(df_final_com_prazos))
        print 'qtd nulos: ' + str(df_final_com_prazos['DELIVERY_TIME_START'].isnull().sum())
        print arquivo_cidade
        print '------------------------'
    
    except:
        print '------------------------'
        print 'nao conseguiu fazer o join'
        print arquivo_cidade
        print '------------------------'
        
    #export dataframe
    df_final_com_prazos.to_csv('arquivos_gerados/TABELA_FRETE_FINAL_'+arquivo_cidade+'_COM_PRAZOS.csv',index=False,sep=';')
    return df_final_com_prazos


def join_prazos_colunado(arquivo_cidade, df_final):
    
    #import tabelas
    df_final = df_final
    df_prazos = pd.read_csv("arquivos_origens/ARQUIVO_PRAZOS.csv", sep = ';')

    # renomeia colunas prazo
    df_prazos.columns = ['CEP_INICIAL', 'ORIGIN_ZIP_START','SERVICE','SERVICE_UID','PRAZO_CORREIOS','DELIVERY_TIME_START','DELIVERY_TIME_END','DELIVERY_TIME_SCALE']
    
      
    # altera tipos das colunas para fazer merge
    df_final['ORIGIN_ZIP_START'] = df_final['ORIGIN_ZIP_START'].astype('int64')
    df_prazos['ORIGIN_ZIP_START'] = df_prazos['ORIGIN_ZIP_START'].astype('int64')

    df_final['CEP_INICIAL'] = df_final['CEP_INICIAL'].astype('int64')
    df_prazos['CEP_INICIAL'] = df_prazos['CEP_INICIAL'].astype('int64')

        
    # fixes #########################################################################################
    
    # onde service_uid = 52 entao 51
    df_prazos['SERVICE_UID'] = np.where(df_prazos['SERVICE_UID']==51, 52, df_prazos['SERVICE_UID'])

    # origem uba = 36500000
    df_prazos['ORIGIN_ZIP_START'] = np.where(df_prazos['ORIGIN_ZIP_START']==36500001, 36500000, df_prazos['ORIGIN_ZIP_START'])

    # weigth start nao arredondado
    df_final['WEIGHT_START'] = np.where(df_final['WEIGHT_START']==3.0010000000000003, 3.001, df_final['WEIGHT_START'])


    # fim fixes #########################################################################################
    
    # merge dataframes
    try:
        df_final_com_prazos = pd.merge(df_final,df_prazos,on=['ORIGIN_ZIP_START','CEP_INICIAL','SERVICE_UID'], how='left')
        print '------------------------'
        print 'join sucesso - final'
        print 'linhas: ' + str(len(df_final_com_prazos))
        print 'qtd nulos: ' + str(df_final_com_prazos['DELIVERY_TIME_START'].isnull().sum())
        print arquivo_cidade
        print '------------------------'
    
    except:
        print '------------------------'
        print 'nao conseguiu fazer o join'
        print arquivo_cidade
        print '------------------------'
        
    #export dataframe
    df_final_com_prazos.to_csv('arquivos_gerados/TABELA_FRETE_FINAL_'+arquivo_cidade+'_COM_PRAZOS.csv',index=False,sep=';')
    return df_final_com_prazos


    

# main()
# join prazos
for arquivo in arquivo_cidade:
    df = join_prazos_final(arquivo)
    df2 = join_prazos_check(arquivo)
    gera_novo_formato(df, arquivo)
