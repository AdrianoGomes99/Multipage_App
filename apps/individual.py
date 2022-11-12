from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
#import pathlib
#from app import app, DATA, LST_IDS
import app
#from pycaret.classification import predict_model, load_model
#import numpy as np
#import json

DATA_GROUP = None
DATA_ID = None

#%%
layout = html.Div([
    html.Div(id='debug_text', children=[str(app.LST_DEFAULT_AREA)], style = dict(display='none') ),
    html.Hr(),
    html.Div(
        children=[
                html.H1('Individual Attrition Dashboards', style={"textAlign": "center"}),
                html.Button(id = 'test_button', n_clicks=0, style = dict(display='none') ),
                
                dcc.Dropdown(id="drop_areas",
                             options = app.AREAS,
                             value = [],
                             multi=True,
                             style={'width': "100%"}
                             ),
                dcc.Dropdown(id="drop_att",
                             options = ['Voluntary', 'Involuntary', 'No'],
                             value = 'Voluntary',
                             multi=True,
                             style={'width': "80%"}
                             ),
                ],
        className='flex flex-col items-center',
        ),
    
    html.Div(
        children=[
                html.H1('Select Employees', style={"textAlign": "left"}),
                
                dash_table.DataTable( id='datatable-interactivity',
                    data=[],
                    columns=[#{"name": 'idInternalCollaborator', "id": 'idInternalCollaborator', 'editable': False},
                             {"name": 'idContract', "id": 'idContract', 'editable': False},
                             {"name": 'Attrition', "id": 'Attrition', 'editable': False},
                             {"name": 'P(Non-attrition)', "id": 'ValueStay', 'editable': False},# , 'type':'numeric',  'format':'percentage'},
                             {"name": 'P(Voluntary attrition)', "id": 'ValueVoluntary', 'editable': False},# , 'type':'numeric',  'format':'percentage'},
                             {"name": 'P(Involuntary attrition)', "id": 'ValueInvoluntary', 'editable': False},# , 'type':'numeric',  'format':'percentage'},
            
                             {"name": 'Age', "id": 'Age', 'editable': False},
                             {"name": 'Years at Company', "id": 'Float_Year_at_Company', 'editable': False},
                             {"name": 'Sex', "id": 'Sex', 'editable': False},
                             {"name": 'Marital Status', "id": 'Marital_Status', 'editable': False},
                             {"name": 'Academic Qualifications', "id": 'Academic_Qualifications', 'editable': False},
                             {"name": 'Field of Study', "id": 'Study_Area', 'editable': False},
                             {"name": 'Area', "id": 'Area', 'editable': False},
                             {"name": 'Professional Qualifications', "id": 'Qualifications', 'editable': False},
                             {"name": 'Salary Rate', "id": 'Salary_Rate', 'editable': False},
                             {"name": 'Contract Type', "id": 'Contract_Type', 'editable': False},
                             ],
                    editable=False,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                    style_table={'overflowX': 'auto'},
                ),
                ],
        className='flex flex-col max-w-full',
        ),
    html.Div(
        children=[
                html.Hr(),
                dcc.Dropdown(id="drop_ids",
                             options=[], #app.LST_IDS,
                             multi=False,
                             style={'width': "40%"}
                            ),
                
                html.Div(
                    children=[
                            html.Div([
                                html.H2(children="Original Probabilities of Attrition", 
                                        style={"textAlign": "center"}),
                                dcc.Graph(id='individual_attrition_graph', 
                                          style = {'visibility':'hidden'},
                                          figure={"layout": {"title": "waiting for data..."}}),
                            ], className='flex flex-col w-1/3'),
                            
                            html.Div([
                                html.H2(children="Variables to change", style={"textAlign": "center"}),
                                html.H4(children="Area", style={"textAlign": "center"}),
                                dcc.Dropdown(id="drop_area", options=['Administration/Management',
                                    'Financial', 'IT', 'HR', 'Logistics', 'Commercial/Marketing',
                                    'Engineering_Research', 'Production', 'Quality', 'Maintenance'],
                                             value = '',
                                             multi = False),
                                html.H4(children="Type of Contract", style={"textAlign": "center"}),
                                dcc.Dropdown(id="drop_contract", options=['Fixed_Term',
                                    'Uncertain_Term', 'No_Term'],
                                             value = '',
                                             multi = False),
                                html.H4(children="Time interval", style={"textAlign": "center"}),
                                dcc.Dropdown(id="drop_time", options=['1 month','6 month', '1 year'],
                                             value = '1 month',
                                             multi = False),
                                html.Br(),
                                html.Button(id = 'estimate_button', n_clicks=0, children='Estimate Attrition',
                                            className='outline outline-offset-2 outline-[#E3E3E4] bg-[#E3E3E4]'),    
                            ], className='flex flex-col w-1/3'),
                            
                            html.Div([
                                html.H2(children="Probabilities of Attrition with applied changes",
                                        style={"textAlign": "center"}),
                                dcc.Graph(id='estimate_attrition_graph', 
                                          style = {'visibility':'hidden'}, 
                                          figure={"layout": {"title": "waiting for data..."}})
                                ], className='flex flex-col w-1/3'),
                            ],
                    className='flex flex-row',
                    ),
                ],
        className='flex flex-col w-full',
        ),
    
    
    # html.Div(id='original_df', children='{original_df empty}'),
    # html.Div(id='changed_df', children='{changed_df empty}'),
    
],
className='overflow-y-auto h-full w-full flex flex-col items-center',
)


#%%
# @app.callback(
#     Output(component_id='base_data', component_property='data'),
#     Input(component_id='selected_id_data', component_property='data') 
#     )
# def clean_data(index_data):
#     df = pd.read_json(index_data, orient='records')
#     return df.to_json(orient = 'records') 

# @app.callback(
#     Output(component_id='drop_ids', component_property='options'),
#     Input('base_data', 'data')
#     )
# def update_drop(data):
#     dff = pd.read_json(data, orient='records')
#     ids_dropdown = dff.idContract.to_list()
#     return ids_dropdown

@app.APP.callback(
    [#Output(component_id='drop_ids', component_property='options'),
     Output(component_id='drop_areas', component_property='value'),
     Output(component_id='drop_att', component_property='value')],
    Input(component_id='test_button', component_property='n_clicks') 
    )
def update_drop_test(n_clicks):
    return app.LST_DEFAULT_AREA, app.DEFAULT_ATT
#%%

@app.APP.callback(
    Output(component_id='datatable-interactivity', component_property='data'),
    [Input(component_id='drop_areas', component_property='value'),
     Input(component_id='drop_att', component_property='value')]
    )
def update_id_drop(slctd_areas, slctd_att): 
    if slctd_att:
        
        global DATA_GROUP
        
        if type(slctd_areas)==str:
            DATA_GROUP = app.DATA.loc[(app.DATA['Attrition']==slctd_att) 
                                      & (app.DATA['Area']==slctd_areas) ]
        else:
            DATA_GROUP = app.DATA.loc[(app.DATA['Attrition']==slctd_att) 
                                      & (app.DATA['Area'].isin(slctd_areas)) ]
            
        DATA_GROUP.loc[:, 'ValueStay'] =DATA_GROUP['ValueStay'].astype(float).map('{:.2%}'.format)
        DATA_GROUP.loc[:, 'ValueVoluntary'] =DATA_GROUP['ValueVoluntary'].astype(float).map('{:.2%}'.format)
        DATA_GROUP.loc[:, 'ValueInvoluntary'] =DATA_GROUP['ValueInvoluntary'].astype(float).map('{:.2%}'.format)
        
        return DATA_GROUP.to_dict('records')
    else:
        return no_update
    
@app.APP.callback(
    Output('drop_ids', 'options'),
    Input('datatable-interactivity', "selected_rows")
    )
def update_select_ids(selected_rows):  
    if selected_rows:
        df = DATA_GROUP.iloc[selected_rows] 
        lst_ids = df.idContract.tolist()
        return lst_ids
    else:
          return no_update
      
#%%

def prob_plot(df):
    ind = int(df.index[0])
    p_no  = round(df.to_dict().get('ValueStay').get(ind)*100, 4)
    p_vol = round(df.to_dict().get('ValueVoluntary').get(ind)*100, 4)
    p_inv = round(df.to_dict().get('ValueInvoluntary').get(ind)*100, 4) 
        
    df_temp = pd.DataFrame(data =
                            {'Attrition_Cat': ['No', 'Voluntary', 'Involuntary'], 
                            'Probability': [p_no, p_vol, p_inv]})
    fig = px.pie(
        data_frame=df_temp,
        values='Probability',
        names='Attrition_Cat',
        color='Attrition_Cat',
        color_discrete_map={
            'No': 'green', 'Voluntary': 'red', 'Involuntary': 'blue'},
        #hole=.5
        )
    fig.update_traces(textinfo='value')
    return fig, ind

@app.APP.callback( [
    Output('individual_attrition_graph', 'figure'),
    Output('drop_area', 'value'),
    Output('drop_contract', 'value'),
    Output('individual_attrition_graph', 'style'),
    ],
    [Input('drop_ids', 'value'),
     Input('drop_contract', 'options'),]
)
def update_individual_graph(slctd_id, opt_contract ):
    if slctd_id:
        global DATA_ID
        DATA_ID = app.DATA.loc[app.DATA['idContract']==slctd_id]
        
        fig, ind = prob_plot(DATA_ID)
        fig.update_layout( {"title": "Employee (with contract id: {}) probabilities of attrition".format(slctd_id)})
        
        area_value = DATA_ID.to_dict().get('Area').get(ind)
        contract_value = DATA_ID.to_dict().get('Contract_Type').get(ind)
        
        style_fig = {'visibility':'visible'}

        return fig, area_value, contract_value, style_fig
    else:
        return no_update, no_update, no_update, no_update

#%%

import pathlib    
from pycaret.classification import predict_model, load_model
import numpy as np

# get relative data folder
PATH = pathlib.Path(__file__).parent
MODEL_PATH = PATH.joinpath("../static").resolve()
# ML model for attrition prediction (xgboost in joblib format)
MODEL = load_model(MODEL_PATH.joinpath("tuned_xgboost_pycaret"))

#function to estimate attrition with changes in data
def attrition_estimation(df):
    
    df_pred = predict_model(estimator = MODEL, data= df)
    df_pred['Attrition'] = df_pred['Label']
    df_pred['Attrition'] = np.where(df_pred['Label']=='Employee', 'Voluntary', df_pred['Attrition'])
    df_pred['Attrition'] = np.where(df_pred['Label']=='Company', 'Involuntary', df_pred['Attrition'])
    df_pred['Attrition'] = np.where(df_pred['Label']=='No', 'No', df_pred['Attrition'])
    
    df_results = predict_model(estimator = MODEL, data= df, raw_score = True)
    df_results['Attrition'] = df_pred['Attrition']
    df_results.rename(columns = {'Score_No':'ValueStay', 
                                 'Score_Employee':'ValueVoluntary', 
                                 'Score_Company':'ValueInvoluntary'},
                      inplace=True)
    
    date_today = pd.to_datetime("today").strftime("%d-%m-%Y")
    df_results['DateComputed'] = date_today

    return df_results

@app.APP.callback([Output('estimate_attrition_graph', 'style'),
    Output('estimate_attrition_graph', 'figure'),
    Output('estimate_button', 'n_clicks'),
    #Output(component_id='original_df', component_property='children'),
    #Output(component_id='changed_df', component_property='children'),
    ],
    [Input('drop_area', 'value'),
     Input('drop_contract', 'value'),
     Input('drop_time', 'value'),
     Input('estimate_button', 'n_clicks')]
    )
def update_estimate_attrition(area_value, contract_value, time_value, n_clicks):
    if n_clicks>0:
        global DATA_ID
        df = DATA_ID.copy()
        ind = int(df.index[0])
        df.loc[ind, 'Area'] = area_value
        df.loc[ind, 'Contract_Type'] = contract_value
        
        if time_value == '1 month':
            df.loc[ind, 'Float_Year_at_Company'] += 0.08
        elif time_value == '6 month':
            df.loc[ind, 'Float_Year_at_Company'] += 0.5
        elif time_value == '1 year':
            df.loc[ind, 'Age'] += 1
            df.loc[ind, 'Float_Year_at_Company'] += 1
        df = df.loc[ind,['idInternalCollaborator', 'idContract', 'Sex', 
                         'Marital_Status', 'Academic_Qualifications', 'Study_Area',
                         'Nationality', 'Age', 'Duration', 
                         'Number_Dependents', 'Number_holders', 'Number_Disabled_Dependents',
                         'Area', 'Qualifications', 'Contract_Type', 'Schedule',
                         'Day_off', 'Float_Year_at_Company', 'Salary_Rate',
                         'Morning_Schedule', 'Afternoon_Schedule', 
                         'Night_Schedule', 'Weekend_Schedule']]
        
        df_est = attrition_estimation(df.to_frame().T)
        
        fig, ind = prob_plot(df_est)
        
        style_fig = {'visibility':'visible'}
        
        n_clicks = 0
        
        return style_fig, fig, n_clicks#, [str(DATA_ID.to_dict(orient='records'))], [str(df_est.to_dict(orient='records'))]
    else:
        return no_update, no_update , no_update, #no_update, no_update
        