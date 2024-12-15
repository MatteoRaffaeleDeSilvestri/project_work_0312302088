from dash import Dash, dcc, html, Input, Output
from data_gen import weather_data_gen
from datetime import datetime
import plotly.express as px
import pandas as pd

def weather_graph():

    lable_dict = {'temperature_on_ground':'Temperatura (°C)',
                'humidity':'Umidità (%)',
                'precipitation_%':'Probabilità di precipitazioni (%)',
                'cloud_cover':'Nuvolosità (%)', 
                'wind_speed_at_ground':'Velocità del vento (km/h)'}
   
    df = weather_data_gen()
    
    fig = px.line(df,x='date',y=['temperature_on_ground','humidity','precipitation_%','cloud_cover','wind_speed_at_ground'],labels={'date':'Data','value':'Valore (°C - % - Km/h)'})
    
    fig.for_each_trace(lambda t: t.update(name = lable_dict[t.name],
                                      legendgroup = lable_dict[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, lable_dict[t.name])))
    
    fig.update_legends(title='Categoria')
    # fig.update_traces(visible='legendonly', selector=lambda t: not t.name in ['Temperatura (°C)'])
    
    fig.update_layout(paper_bgcolor='rgb(242, 242, 242)')

    return fig, f'Ultimo aggiornamento: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}'

def activity_graph():

    df_activity = pd.read_csv('assets/dataset_attività.csv') 

    df_activity_tiles = df_activity.loc[df_activity['Inizio']==df_activity['Inizio'].min()]
   
    preparazione_terreno = str(df_activity_tiles.where(df_activity_tiles['Attività']=='Preparazione terreno').count()['Attività'])
    coltivazione_trattamenti = str(df_activity_tiles.where(df_activity_tiles['Attività']=='Coltivazione e trattamenti').count()['Attività'])
    crescita = str(df_activity_tiles.where(df_activity_tiles['Attività']=='Crescita').count()['Attività'])
    raccolta = str(df_activity_tiles.where(df_activity_tiles['Attività']=='Raccolta').count()['Attività'])
    
    fig_activity = px.timeline(df_activity, x_start='Inizio', x_end='Fine', y='Appezzamento', color='Attività', labels={'Appezzamento':''})
   
    fig_activity.update_legends(title='Categoria')
    fig_activity.update_traces(visible='legendonly', selector=lambda t: not t.name in ['Preparazione terreno','Coltivazione e trattamenti','Crescita','Raccolta'])
    
    fig_activity.update_layout(paper_bgcolor='rgb(242, 242, 242)')

    return fig_activity, preparazione_terreno, coltivazione_trattamenti, crescita, raccolta

def balance_dropdown():

    df = pd.read_csv('assets/dataset_bilancio.csv')
    df_anno = df['anno'].sort_values(ascending=False)
    val = max(df_anno.unique())
    df_anno.loc[len(df_anno)] = 'Storico'

    return df_anno.unique(), val

def balance_graph():

    df = pd.read_csv('assets/dataset_bilancio.csv') 
    
    tot_costi = '€{:,}'.format(int(df['costi'].sum()))
    tot_ricavi = '€{:,}'.format(int(df['ricavi'].sum()))
    tot_utile = '€{:,}'.format(int(df['utile'].sum()))
    tot_liquidita = '€{:,}'.format(int(df['liquidita'].sum()))

    fig = px.line(df, x='anno-mese', y=['costi','ricavi'], labels={'anno-mese':'Mese','value':'Valore (€)'})
    
    leg_names = {'costi':'Costi','ricavi':'Ricavi','utile':'Utile','liquidita':'Liquidità'}
    fig.for_each_trace(lambda t: t.update(name = leg_names[t.name],
                                      legendgroup = leg_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, leg_names[t.name])))
    
    fig.add_bar(x=df['anno-mese'], y=df['utile'], name='Utile')
    fig.add_bar(x=df['anno-mese'], y=df['liquidita'], name='Liquidità')
    
    fig.update_legends(title='Categoria')
    fig.update_traces(visible='legendonly', selector=lambda t: not t.name in ['Costi','Ricavi'])
    
    fig.update_layout(paper_bgcolor='rgb(242, 242, 242)')

    return fig, tot_costi, tot_ricavi, tot_utile, tot_liquidita

def investments_dropdown():

    df = pd.read_csv('assets/dataset_investimenti.csv')
    df_anno = df['anno'].sort_values(ascending=False)
    val = max(df_anno.unique())
    df_anno.loc[len(df_anno)] = 'Storico'

    return df_anno.unique(), val

def investments_graph():

    df = pd.read_csv('assets/dataset_investimenti.csv') 

    tot_investimenti = '€{:,}'.format(int(df['investimento'].sum()))
    
    fig = px.histogram(df, x='anno', y=['invest_terreni','invest_immobili','invest_macchinari','invest_beni'],barmode='group',labels={'anno':'Anno','sum_of_value':'Valore (€)'})

    leg_names = {'invest_terreni':'Terreni','invest_immobili':'Immobili','invest_macchinari':'Macchinari','invest_beni':'Beni'}
    fig.for_each_trace(lambda t: t.update(name = leg_names[t.name],
                                      legendgroup = leg_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, leg_names[t.name])))
    
    fig.update_legends(title='Categoria')
    fig.update_layout(paper_bgcolor='rgb(242, 242, 242)',yaxis_title='Valore (€)')

    return fig, tot_investimenti

def productivity_dropdown():

    df = pd.read_csv('assets/dataset_produttività.csv')
    df_anno = df['anno'].sort_values(ascending=False)
    val = max(df_anno.unique())
    df_anno.loc[len(df_anno)] = 'Storico'

    return df_anno.unique(), val

def productivity_graph():

    df = pd.read_csv('assets/dataset_produttività.csv') 

    tot_productivity = '€{:,}'.format(int(df['produzione'].sum()))
    
    fig_productivity = px.line(df, x='anno-mese', y=['produzione'], labels={'anno-mese':'Mese','value':'Produttività (€)'})

    leg_names = {'produzione':'Produttività'}
    fig_productivity.for_each_trace(lambda t: t.update(name = leg_names[t.name],
                                      legendgroup = leg_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, leg_names[t.name])))
    
    fig_productivity.update_legends(title='Categoria')   
    fig_productivity.update_layout(paper_bgcolor='rgb(242, 242, 242)')
    
    return fig_productivity, tot_productivity

def income_expenses_dropdown():

    df = pd.read_csv('assets/dataset_entrate_uscite.csv')
    df_anno = df['anno'].sort_values(ascending=False)
    val = max(df_anno.unique())
    df_anno.loc[len(df_anno)] = 'Storico'

    return df_anno.unique(), val

def income_expenses_graph():

    df = pd.read_csv('assets/dataset_entrate_uscite.csv') 

    df_income = df[['produzione','commercio']].sum()
    df_expenses = df[['imposte','terreni','immobili','macchinari','beni']].sum()

    fig_income = px.pie(df_income,values=df_income,names=['Produzione','Commercio'],hole=0.4)
    fig_expenses = px.pie(df_expenses,values=df_expenses,names=['Imposte','Terreni','Immobili','Macchinari','Beni'],hole=0.4)

    fig_income.update_legends(title='Categoria')
    fig_expenses.update_legends(title='Categoria')
    fig_income.update_layout(paper_bgcolor='rgb(242, 242, 242)')
    fig_expenses.update_layout(paper_bgcolor='rgb(242, 242, 242)')
   
    return fig_income, fig_expenses

# Logo azienda
logo_path = 'assets/logo.png'

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

# Creazione app
app = Dash(__name__)

# Definizione corpo dashboard
app.layout = html.Div([

    # SIDEBAR
    html.Div([html.Img(src=logo_path,style={'display':'block','margin-left':'auto','margin-right':'auto'}),
        html.H4(['RAGIONE SOCIALE'],style={'margin':'10px'}),
        html.Div(['Agritalia.srl'],style={'margin':'10px'}),
        html.H4(['PARTITA IVA'],style={'margin':'10px'}),
        html.Div(['00312302088'],style={'margin':'10px'}), 
        html.H4(['CODICE FISCALE'],style={'margin':'10px'}),
        html.Div(['FYHZPW40B05B319A'],style={'margin':'10px'}),  
        html.H4(['SEDE'],style={'margin':'10px'}),
        html.Div(['Centro Direzionale Isola F2 - 80143 Napoli (NA) - Italia'],style={'margin':'10px'}),
        html.H4(['TELEFONO'],style={'margin':'10px'}),
        html.Div(['(+39) 123 45 67 890'],style={'margin':'10px'}),
        html.H4(['PEC'],style={'margin':'10px'}),
        html.Div(['agritalia@pec.it'],style={'margin':'10px'}),   
        ],style={'width':'50%','height':'max-content','text-align':'left','border':'solid 1px black','border-radius':'30px','padding':'10px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'}
    ),

    # CORPO
    html.Div([

        # ATTIVITÀ
        html.H1(['ATTIVITÀ'],style={'margin-left':'20px'}),
        html.Div([
            html.H2('METEO'),
            html.Div(['''Principali indicatori meteorologici per i prossimi 14 giorni. Gli indicatori riportati sono stati selezionati per la loro rilevanza nel settore agricolo. 
                      Inoltre, la scelta di operare su un periodo di 14 giorni permette di massimmizzare il rapporto tra l'ampiezza dell'arco temporale ed affidabilità delle previsioni.'''],style={'margin-bottom':'20px'}),
            dcc.Graph(id='weather_chart',figure=weather_graph()[0]),
            dcc.Textarea(id='weather_text',value=weather_graph()[1],readOnly=True,draggable=False,style={'border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'16px','height':'25px','width':'380px','resize':'none'}),
            html.Br(),
            html.Button('Aggiorna',id='weather_btn'),
            html.Div('Powered by Open-Meteo.',style={'font-style':'italic','text-align':'right'})
            ],style={'border':'solid 1px black','border-radius':'30px','padding':'20px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'}),
            html.Div([
                html.H2('PIANO DEI LAVORI'),
                html.Div(['''Stato di avanzamento delle attività suddivise per appezzamento di terreno. Oltre allo stato attuale delle colture, 
                          suddivise in base allo stato di avanzamento dei lavori (preparazione, coltivazione, crescita e raccolta), 
                          sono presentate anche le scadenze previste per i prossimi 14 giorni.\nAvere un piano dei lavori basato sullo stesso 
                          lasso temporale dei dati meteorilogici permette di programmare al meglio le attività nel breve periodo.'''],style={'margin-bottom':'20px'}),
                html.Br(),
                html.Div([
                    dcc.Textarea(value='COLTURE IN\nPREPARAZIONE',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'50px','resize':'none'}),
                    dcc.Textarea(value='COLTURE IN\nCOLTIVAZIONE',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'50px','resize':'none'}),
                    dcc.Textarea(value='COLTURE IN\nCRESCITA',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'50px','resize':'none'}),
                    dcc.Textarea(value='COLTURE IN\nRACCOLTA',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'50px','resize':'none'})
                ],style={'display':'flex'}),
                html.Div([
                    dcc.Textarea(id='plan_t1',value=activity_graph()[1],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                    dcc.Textarea(id='plan_t2',value=activity_graph()[2],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                    dcc.Textarea(id='plan_t3',value=activity_graph()[3],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                    dcc.Textarea(id='plan_t4',value=activity_graph()[4],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'})
                ], style={'display':'flex'}),
            dcc.Graph(id='activity_chart',figure=activity_graph()[0])
            ],style={'border':'solid 1px black','border-radius':'30px','padding':'20px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'}),
        html.Br(),

        # ANDAMENTO
        html.H1(['ANDAMENTO'],style={'margin-left':'20px'}),       
        html.Div([
            html.H2('BILANCIO'),
            html.Div(['''Andamento economico dell'azienda rappresentato tramite gli indicatori di costi, ricavi utile e liquidità per periodo di esercizio (di default viene visualizzato il periodo di esercizio corrente). 
                      È possibile filtrare i dati per anno di esercizio o avere una visione d'insieme dell'andamento degli indici selezionando l'opzione "Storico" dal menù Periodo. 
                      I dati riportati sono rappresentati sia in forma numerica (con riferimento al periodo selezionato), che andamentale.'''],style={'margin-bottom':'20px'}),
            html.Div(['Periodo'],style={'margin-bottom':'0px'}),
            dcc.Dropdown(id='balance_dropdown',options=balance_dropdown()[0],value=balance_dropdown()[1],clearable=False,style={'width':'30%'}),
            html.Br(),
            html.Div([
                dcc.Textarea(value='TOTALE COSTI',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'}),
                dcc.Textarea(value='TOTALE RICAVI',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'}),
                dcc.Textarea(value='TOTALE UTILE',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'}),
                dcc.Textarea(value='TOTALE LIQUIDITÀ',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'})
            ],style={'display':'flex'}),
            html.Div([
                dcc.Textarea(id='blnc_t1',value=balance_graph()[1],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                dcc.Textarea(id='blnc_t2',value=balance_graph()[2],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                dcc.Textarea(id='blnc_t3',value=balance_graph()[3],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                dcc.Textarea(id='blnc_t4',value=balance_graph()[4],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'})
            ], style={'display':'flex'}),
            dcc.Graph(id='balance_chart',figure=balance_graph()[0])
        ],style={'border':'solid 1px black','border-radius':'30px','padding':'20px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'}),
        
        html.Div([
            html.H2('INVESTIMENTI'),
            html.Div(['''Investimenti effettuati all'interno dell'azienda suddivisi per tipologia e per periodo di esercizio (di default viene visualizzato il periodo di esercizio corrente). 
                      Gli investimenti sono effettuati di anno in anno reinvestendo fino al 30% della liquidità accumulata nel corso dell'attività, qualora sia sufficiente. 
                      È possibile filtrare i dati per anno di esercizio o avere una visione d'insieme dell'andamento degli indici selezionando l'opzione "Storico" dal menù Periodo. 
                      I dati riportati sono rappresentati sia in forma numerica (con riferimento al periodo selezionato), che andamentale.'''],style={'margin-bottom':'20px'}),
            html.Div(['Periodo'],style={'margin-bottom':'0px'}),
            dcc.Dropdown(id='investments_dropdown',options=investments_dropdown()[0],value=investments_dropdown()[1],clearable=False,style={'width':'30%'}),
            html.Div([
                dcc.Textarea(value='TOTALE INVESTIMENTI',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'})
                ],style={'text-align':'center'}),
            html.Div([
                dcc.Textarea(id='invest',value=investments_graph()[1],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                ],style={'text-align':'center'}),
            dcc.Graph(id='investments_chart', figure=investments_graph()[0]),
        ],style={'border':'solid 1px black','border-radius':'30px','padding':'20px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'}),

        html.Div([
            html.H2('PRODUTTIVITÀ'),
            html.Div(['''Indice della capacità produttiva dell'azienda per periodo di esercizio (di default viene visualizzato il periodo di esercizio corrente). 
                      Per produttività si intende la ricchezza generata dalla sola attività di produzione e vendita di articoli di propria produzione, senza tenere conto 
                      della ricchezza generata dall'attività di compravendita di proditti di terzi (permesso dalla legge fino ad un limite massimo del 30% del fatturato).
                      È possibile filtrare i dati per anno di esercizio o avere una visione d'insieme dell'andamento degli indici selezionando l'opzione "Storico" dal menù Periodo. 
                      I dati riportati sono rappresentati sia in forma numerica (con riferimento al periodo selezionato), che andamentale.'''],style={'margin-bottom':'20px'}),
            html.Div(['Periodo'],style={'margin-bottom':'0px'}),
            dcc.Dropdown(id='productivity_dropdown',options=productivity_dropdown()[0],value=productivity_dropdown()[1],clearable=False,style={'width':'30%'}),
            html.Div([
                dcc.Textarea(value='TOTALE PRODUTTIVITÀ',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'})
                ],style={'text-align':'center'}),
            html.Div([
                dcc.Textarea(id='product',value=productivity_graph()[1],readOnly=True,draggable=False,style={'margin':'auto','border':'solid 1px #d9d9d9','border-radius':'10px','padding':'10px','background':'#ffffff','font-family':'Verdana','font-size':'25px','text-align':'center','height':'30px','width':'230px','resize':'none'}),
                ],style={'text-align':'center'}),
            dcc.Graph(id='productivity_chart', figure=productivity_graph()[0]),
            ],style={'border':'solid 1px black','border-radius':'30px','padding':'20px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'}),

        html.Div([
            html.H2('ENTRATE & USCITE'),
            html.Div(['''Ripartizione di entrate ed uscite dell'azienda per periodo di esercizio (di default viene visualizzato il periodo di esercizio corrente). 
                      È possibile filtrare i dati per anno di esercizio o avere una visione d'insieme dell'andamento degli indici selezionando l'opzione "Storico" dal menù Periodo. 
                      I dati riportati sono rappresentati sia in forma numerica (con riferimento al periodo selezionato), che andamentale.'''],style={'margin-bottom':'20px'}),
            html.Div(['Periodo'],style={'margin-bottom':'0px'}),
            dcc.Dropdown(id='income_expenses_dropdown',options=income_expenses_dropdown()[0],value=income_expenses_dropdown()[1],clearable=False,style={'width':'30%'}),
            html.Br(),
            html.Div([
                dcc.Textarea(value='ENTRATE',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'}),
                dcc.Textarea(value='USCITE',readOnly=True,draggable=False,style={'margin':'auto','border':'none','background':'#f2f2f2','font-family':'Verdana','font-size':'20px','text-align':'center','height':'25px','resize':'none'}),
            ], style={'display':'flex'}),
            html.Div([
                dcc.Graph(id='income_chart',figure=income_expenses_graph()[0]),
                dcc.Graph(id='expenses_chart',figure=income_expenses_graph()[1])
            ],style={'display':'flex'})          
        ],style={'border':'solid 1px black','border-radius':'30px','padding':'20px','box-shadow':'7px 7px #bfbfbf','background':'#f2f2f2','margin':'10px'})

    ])
],style={'display':'flex'})

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

@app.callback( 
    [Output('weather_chart','figure'),
    Output('weather_text','value')],
    Input('weather_btn','n_clicks')
)

def weather_btn(click):
    fig, text = weather_graph()
    return fig, text    

@app.callback( 
    [Output('balance_chart','figure'),
    Output('blnc_t1','value'),
    Output('blnc_t2','value'),
    Output('blnc_t3','value'),
    Output('blnc_t4','value')],
    Input('balance_dropdown','value')
)

def balance_graph(interval):

    df = pd.read_csv('assets/dataset_bilancio.csv')

    if interval != 'Storico': df = df.where(df['anno']==interval)

    tot_costi = '€{:,}'.format(int(df['costi'].sum()))
    tot_ricavi = '€{:,}'.format(int(df['ricavi'].sum()))
    tot_utile = '€{:,}'.format(int(df['utile'].sum()))
    tot_liquidita = '€{:,}'.format(int(df['liquidita'].sum()))

    fig = px.line(df, x='anno-mese', y=['costi','ricavi'], labels={'anno-mese':'Mese','value':'Valore (€)'})
    
    leg_names = {'costi':'Costi','ricavi':'Ricavi','utile':'Utile','liquidita':'Liquidità'}
    fig.for_each_trace(lambda t: t.update(name = leg_names[t.name],
                                      legendgroup = leg_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, leg_names[t.name])))
    
    fig.add_bar(x=df['anno-mese'], y=df['utile'], name='Utile')
    fig.add_bar(x=df['anno-mese'], y=df['liquidita'], name='Liquidità')
    
    fig.update_legends(title='Categoria')
    fig.update_traces(visible='legendonly', selector=lambda t: not t.name in ['Costi','Ricavi'])
    
    fig.update_layout(paper_bgcolor='rgb(242, 242, 242)')

    return fig, tot_costi, tot_ricavi, tot_utile, tot_liquidita

@app.callback( 
    [Output('investments_chart','figure'),
    Output('invest','value')],
    Input('investments_dropdown','value')
)

def investments_graph(interval):

    df = pd.read_csv('assets/dataset_investimenti.csv')

    if interval != 'Storico': df = df.where(df['anno']==interval)

    tot_investimenti = '€{:,}'.format(int(df['investimento'].sum()))
    
    fig = px.histogram(df, x='anno', y=['invest_terreni','invest_immobili','invest_macchinari','invest_beni'],barmode='group',labels={'anno':'Anno'})

    leg_names = {'invest_terreni':'Terreni','invest_immobili':'Immobili','invest_macchinari':'Macchinari','invest_beni':'Beni'}
    fig.for_each_trace(lambda t: t.update(name = leg_names[t.name],
                                      legendgroup = leg_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, leg_names[t.name])))
    
    fig.update_legends(title='Categoria')    
    fig.update_layout(paper_bgcolor='rgb(242, 242, 242)',yaxis_title='Valore (€)')

    return fig, tot_investimenti

@app.callback( 
    [Output('productivity_chart','figure'),
    Output('product','value')],
    Input('productivity_dropdown','value')
)

def productivity_graph(interval):

    df = pd.read_csv('assets/dataset_produttività.csv') 

    if interval != 'Storico': df = df.where(df['anno']==interval)

    tot_productivity = '€{:,}'.format(int(df['produzione'].sum()))
    
    fig_productivity = px.line(df, x='anno-mese', y=['produzione'], labels={'anno-mese':'Mese','value':'Produttività (€)'})
    
    leg_names = {'produzione':'Produttività'}
    fig_productivity.for_each_trace(lambda t: t.update(name = leg_names[t.name],
                                      legendgroup = leg_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, leg_names[t.name])))
    
    fig_productivity.update_legends(title='Categoria')   
    fig_productivity.update_layout(paper_bgcolor='rgb(242, 242, 242)')
    
    return fig_productivity, tot_productivity

@app.callback( 
    [Output('income_chart','figure'),
    Output('expenses_chart','figure')],
    Input('income_expenses_dropdown','value')
)

def income_expenses_graph(interval):

    df = pd.read_csv('assets/dataset_entrate_uscite.csv')

    if interval != 'Storico': df = df.where(df['anno']==interval)

    df_income = df[['produzione','commercio']].sum()
    df_expenses = df[['imposte','terreni','immobili','macchinari','beni']].sum()

    fig_income = px.pie(df_income,values=df_income,names=['Produzione','Commercio'],hole=0.4)
    fig_expenses = px.pie(df_expenses,values=df_expenses,names=['Imposte','Terreni','Immobili','Macchinari','Beni'],hole=0.4)

    fig_income.update_legends(title='Categoria')
    fig_expenses.update_legends(title='Categoria')
    fig_income.update_layout(paper_bgcolor='rgb(242, 242, 242)')
    fig_expenses.update_layout(paper_bgcolor='rgb(242, 242, 242)')

    return fig_income, fig_expenses

if __name__ == "__main__":
    
    app.run_server(debug=True)
