import pandas as pd

# Preenche os taxos vazios
def fillTaxos(db:pd.DataFrame, ntaxo:list):
    dict_name = {
        'phylum':'Phy',
        'subphylum':'SPh',
        'class':'Cls',
        'subclass':'SCl',
        'order':'Ord',
        'infraorder':'IOr',
        'suborder':'SOr',
        'family':'Fam',
        'genus':'Gen',
        'species':'sp'
    }
    for k,v in dict_name.items():
        if k in db.columns:
            db[k] = db[k].fillna(v)

    db.species = db.species.replace('sp.','sp')

    db['species'] = db['genus'] + ' ' + db['species']
    dict_name['species'] = 'Gen sp'

    for t in range(len(ntaxo)):
        for a in db.index[db[ntaxo[t]]==dict_name[ntaxo[t]]]:
            for b in range(t+1,len(ntaxo)):
                if db[ntaxo[b]][a] not in dict_name.values():
                    for c in range(t,b):
                        db.loc[a,ntaxo[c]]=db.loc[a,ntaxo[c]] + '-' + db[ntaxo[b]][a]
                    break

    return db

# Agrupamento para especie e type
def groupySpecies(db:pd.DataFrame,taxo:list):
    db3 = db[taxo[::-1]+['species','type_status','catalog_number']].groupby(
        taxo[::-1]+['species']
    ).count().reset_index()
    return db3

# Configura o dado de registro para a criação do grafo completo
def fixRecordData(db:pd.DataFrame,nosSpecies:pd.DataFrame):
    newbase=db.merge(nosSpecies,left_on=['species','family'], right_on=['nometx','nome'])
    newbase['nome']=newbase.family

    newbase=db.merge(nosSpecies,left_on=['species','family'], right_on=['nometx','nome'])
    newbase['nome']=newbase.family

    newbase['t']= newbase.type_status.notna()
    newbase = newbase.sort_values(['species','t'],ascending=False).reset_index(drop=True)
    newbase['image'] = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

    lista = [1]
    for a in range(1,len(newbase.species)):
        if newbase.species[a] == newbase.species[a-1]:
            lista.append(lista[-1]+1)
        else:
            lista.append(1)
    newbase['rank'] = lista

    return newbase