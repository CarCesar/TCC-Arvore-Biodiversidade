import pandas as pd
import numpy as np

### criar nos
def createNodes(base, ntaxo=['species', 'genus', 'family', 'order', 'class', 'phylum']):
    nos=pd.DataFrame(columns=['nome','x','y','taxo','total_lotes','total_tipos'])
    
    listaNomes = base[ntaxo[0]].unique()
    groupBase = base.groupby([ntaxo[0]]).sum()
    for a in range(len(listaNomes)):
        nos.loc[ntaxo[0]+listaNomes[a]] = [listaNomes[a],6,a+2,ntaxo[0],groupBase.loc[listaNomes[a],'catalog_number'],
                                                                        groupBase.loc[listaNomes[a],'type_status']]

    for ind in range(1,len(ntaxo)):
        listaNomes = base[ntaxo[ind]].unique()
        groupBase = base.groupby([ntaxo[ind]]).sum()
        for nome in listaNomes:
            db1=base[base[ntaxo[ind]]==nome].reset_index()
            y = np.ceil(nos.loc[ntaxo[0]+db1[ntaxo[0]].unique()]['y'].median())
            nos.loc[ntaxo[ind]+nome] = [nome, 6-ind, y, ntaxo[ind], groupBase.loc[nome,'catalog_number'],
                                                                    groupBase.loc[nome,'type_status']]
    
    return nos

### criar arestas
def createEdges(nos, base, ntaxo=['species', 'genus', 'family', 'order', 'class', 'phylum']):
    arestas=pd.DataFrame(columns=['nome1','x1','y1','taxo1',
                              'nome2','x2','y2','taxo2',
                              'count'])
    for linha in base.index:
        for t in range(1,len(ntaxo)):
            t1=ntaxo[t-1]
            t2=ntaxo[t]
            tax1 = t1+base.loc[linha,:][t1]
            tax2 = t2+base.loc[linha,:][t2]
            tax = tax1+tax2
            if tax in arestas.index:
                arestas.loc[tax,'count']=arestas.loc[tax,'count']+1
            else:
                taxo1 = nos.loc[tax1,:]
                taxo2 = nos.loc[tax2,:]
                arestas.loc[tax] = [taxo1.nome,taxo1.x,taxo1.y,taxo1.taxo,
                                    taxo2.nome,taxo2.x,taxo2.y,taxo2.taxo,1]
    
    return arestas

### criar nos G2
def createNodesG2(base, ntaxo=['species', 'genus', 'family']):
    nos=pd.DataFrame(columns=['nometx','x','y','taxo','nome','total_lotes','total_tipos'])

    for txPai in base[ntaxo[-1]].unique():
        baseFil = base[base[ntaxo[-1]]==txPai].sort_values(ntaxo[::-1]).reset_index(drop=True)

        listaNomes = baseFil[ntaxo[0]].unique()
        groupBase = baseFil.groupby([ntaxo[0]]).sum()
        for a in range(len(listaNomes)):
            nos.loc[ntaxo[0]+listaNomes[a]+txPai] = [listaNomes[a],6,a,ntaxo[0],txPai,groupBase.loc[listaNomes[a],'catalog_number'],
                                                                                      groupBase.loc[listaNomes[a],'type_status']]
        for ind in range(1,len(ntaxo)):
            listaNomes = baseFil[ntaxo[ind]].unique()
            groupBase = baseFil.groupby([ntaxo[ind]]).sum()
            for nome in listaNomes:
                db1=baseFil[baseFil[ntaxo[ind]]==nome].reset_index()
                y = np.ceil(nos.loc[ntaxo[0]+db1[ntaxo[0]].unique()+txPai]['y'].median())
                nos.loc[ntaxo[ind]+nome+txPai] = [nome,6-ind,y,ntaxo[ind],txPai,
                                                           groupBase.loc[nome,'catalog_number'],
                                                           groupBase.loc[nome,'type_status']]
    
    return nos

### criar arestas
def createEdgesG2(nos, base, ntaxo=['species', 'genus', 'family']):
    arestas=pd.DataFrame(columns=['nome1','x1','y1','taxo1',
                                  'nome2','x2','y2','taxo2',
                                  'count','nome'])
    for txPai in base[ntaxo[-1]].unique():
        baseFil = base[base[ntaxo[-1]]==txPai]
        for linha in baseFil.index:
            for t in range(1,len(ntaxo)):
                t1=ntaxo[t-1]
                t2=ntaxo[t]
                tax1 = t1+baseFil.loc[linha,:][t1]+txPai
                tax2 = t2+baseFil.loc[linha,:][t2]+txPai
                tax = tax1+tax2+txPai
                if tax in arestas.index:
                    arestas.loc[tax,'count']=arestas.loc[tax,'count']+1
                else:
                    taxo1 = nos.loc[tax1,:]
                    taxo2 = nos.loc[tax2,:]
                    arestas.loc[tax] = [taxo1.nome,taxo1.x,taxo1.y,taxo1.taxo,
                                        taxo2.nome,taxo2.x,taxo2.y,taxo2.taxo,1,txPai]
    
    return arestas