import pandas as pd
import altair as alt
alt.data_transformers.enable('default', max_rows=None)

def pictureTaxoTree(nodesFamily,edgesFamily,nodesSpecies,edgesSpecies,newbase,title):
    # Configurações de Eixo muito usadas
    axisDefault = alt.Axis(labels=False, ticks=False, domain=False)
    axisDefaultX = alt.Axis(labels=False, ticks=False, domain=False, grid=True, gridOpacity=0.3)
    axisGrid = alt.Axis(domain=False, ticks=True, tickOpacity=0.3, tickWidth=1,tickSize=10,tickColor='#555555',
                                        labels= False, title= '', grid=True, gridOpacity=0.3, orient='top',gridColor='#555555')

    # Selecionar Família
    selectFamily=alt.selection_single(fields= ['nome'],empty='none')

    # Nomes dos grupos taxonômicos e linha de fundo
    t = alt.Chart(
        data = nodesFamily.groupby(['taxo','x']).count().reset_index(),
        width = 500,         height = 700
    ).mark_text(
        align = 'right',     baseline = 'top',
        font = 'monospace',  fontSize = 10, 
        color ='#555555',    y = -15, 
        dx = -5,             opacity = 0.5
    ).encode(
        text='taxo',
        x=alt.X('x:O', axis = axisGrid)
    )

    tS = alt.Chart(
        data = nodesSpecies.groupby(['taxo','x']).count().reset_index(), 
        width = 500,         height = 700
    ).mark_text(
        align = 'right',     baseline = 'top',
        font = 'monospace',  fontSize = 10, 
        color = '#555555',   y = -15, 
        dx = -5,             opacity = 0.5
    ).encode(
        text = 'taxo',
        x = alt.X('x:O', axis = axisGrid)
    )

    # Bases
    baseNodesFamily = alt.Chart(data=nodesFamily, width=500,height=700)
    baseNodesSpecies = alt.Chart(data=nodesSpecies, width=500,height=700)

    # Nomeclaturas dos taxos
    ## Parte I
    n0 = baseNodesFamily.encode(
        text = 'nome',
        x = alt.X('x:O', axis = axisDefault),
        y = alt.Y('y:O', axis = axisDefault),
        tooltip = ['nome','taxo','total_lotes', 'total_tipos']
    )

    n = n0.mark_text(
        align = 'left',    baseline = 'bottom',   font = 'monospace', 
        fontSize = 9,      color = '#000000',     dx=3
    ).transform_filter(alt.datum.taxo!='family')

    n1 = n0.mark_text(
        align = 'left',    baseline = 'middle',   font = 'monospace',
        fontSize = 9,      color = '#000000',     dx = 3
    ).transform_filter(alt.datum.taxo=='family')

    ## Parte II
    nS0 = baseNodesSpecies.encode(
        text = 'nometx',
        x = alt.X('x:O', axis = axisDefault),
        y = alt.Y('y:O', axis = axisDefault),
        tooltip = ['nome','taxo','total_lotes', 'total_tipos']
    ).transform_filter(selectFamily)

    nS = nS0.mark_text(
        align = 'left',   baseline = 'bottom',   font = 'monospace',
        fontSize = 9,     color = '#000000',     dx=3
    ).transform_filter(alt.datum.taxo!='species')

    nS1 = nS0.mark_text(
        align = 'left',   baseline = 'middle',   font = 'monospace', 
        fontSize = 9,     color = '#000000',     dx=3
    ).transform_filter(alt.datum.taxo=='species')

    # Nós
    p = baseNodesFamily.mark_circle(opacity = 1,color = 'blue').encode(
        x = alt.X('x:O', axis = axisDefault,title=None),
        y = alt.Y('y:O', axis = axisDefault,title=None),
        tooltip = ['nome','taxo','total_lotes', 'total_tipos']    
    ).transform_filter(alt.datum.taxo!='family')

    p1 = baseNodesFamily.mark_circle(opacity = 1,color = 'blue').encode(
        x = alt.X('x:O', axis = axisDefault,title=None),
        y = alt.Y('y:O', axis = axisDefault,title=None),
        tooltip = ['nome','taxo','total_lotes', 'total_tipos'],
        size = alt.condition(selectFamily, alt.value(120), alt.value(20))
    ).transform_filter(alt.datum.taxo=='family').add_selection(selectFamily)

    pS = baseNodesSpecies.mark_circle(opacity = 1,color = 'blue').encode(
        x = alt.X('x:O', axis=axisDefault,title=None),
        y = alt.Y('y:O', axis=axisDefault,title=None),
        tooltip = [alt.Tooltip('nometx:N', title='nome'),'taxo','total_lotes', 'total_tipos']
        ).transform_filter(selectFamily)

    # Arestas
    r  = alt.Chart(data=edgesFamily,width=500,height=700
    ).mark_rule(color='grey').encode(x='x1:O',y='y1:O',x2='x2:O',y2='y2:O')

    rS = alt.Chart(data=edgesSpecies,width=500,height=700
    ).mark_rule(color='grey').encode(x='x1:O',y='y1:O',x2='x2:O',y2='y2:O'
    ).transform_filter(selectFamily)

    # Registros
    eBase = alt.Chart(newbase,height=700, width=500).mark_circle().transform_filter(selectFamily)
    eAxis = alt.Axis(grid=True,gridOpacity=0.3,domain=False,ticks=False, labels = False)
    eX = alt.X("rank:O", title=None, axis=eAxis)
    eY = alt.Y('y:O',    title=None, axis = eAxis,)
    eColor = alt.condition(alt.datum.t, alt.value('red'), alt.value('blue'))
    eTooltip = ['catalog_number', 'year_cataloged', 'year_collected',
            'class', 'order', 'family', 'genus', 'species', 
            'type_status', 'qualifier', 'rank']

    eS= eBase.encode(
        x = eX, y = eY, color = eColor, tooltip= alt.Tooltip(eTooltip)
    ).transform_filter(alt.datum.t==False)

    eS1= eBase.encode(
            x=eX, y=eY, color=eColor, tooltip= alt.Tooltip(['image']+eTooltip)
    ).transform_filter(alt.datum.t)

    chart_title = alt.TitleParams(
       title,
        subtitle=["Visualização Hierárquica de Coleções Científicas de Biodiversidade"],
    )

    return alt.hconcat((t+r+p+p1+n+n1), (tS+rS+pS+nS+nS1), (eS+eS1), spacing=0).properties(title=chart_title
                                                                ).configure_title(align='center',anchor='middle', fontSize=20, subtitleFontSize=11
                                                                ).configure_view(strokeWidth=0)