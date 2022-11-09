from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output
import plotly.express as px

import app 

DATA_CUT = None 
DATA_ATT = None

layout = html.Div([
    
    html.Div(id='debug_print', children=[str(app.DEFAULT_AREA)]),
    html.Hr(),
    
    html.H1('Group Attrition Dashboards', style={"textAlign": "center"}),

    html.Br(),
    dcc.Dropdown(id="slct_area",
                 options = app.AREAS,
                 value = app.DEFAULT_AREA,
                 multi=True,
                 style={'width': "60%"}
                 ),
   
    html.Br(),
    html.Div([
        html.Div([
            html.H2(children="Bar Plot", style={"textAlign": "center"}),
            dcc.Graph(id='bar_plot', figure=px.bar(
                data_frame=app.DATA.loc[app.DATA['Area'].isin([app.DEFAULT_AREA])],
                x='Area',
                color='Attrition',
                color_discrete_map={
                    'No': 'green', 'Voluntary': 'red', 'Involuntary': 'blue'},
                barmode="group") )
                #}, style = {'visibility':'hidden'})
        ], className='six columns'),
        
        html.Div([
            html.H2(children="Pie Char", style={"textAlign": "center"}),
            dcc.Graph(id='pie_plot', figure=px.pie(
                data_frame=app.DATA.loc[app.DATA['Area'].isin([app.DEFAULT_AREA])].Attrition.value_counts(normalize=True).rename_axis('attrition').reset_index(name='counts') ,
                values='counts', 
                color='attrition', 
                 color_discrete_map={
                     'Voluntary': 'red', 'Involuntary': 'blue', 'No': 'green'}
                ))
                #}, style = {'visibility':'hidden'})
            ], className='six columns'),
    ], className='row'),
   
    # html.Hr(),
    # dash_table.DataTable( id='datatable-interactivity',
    #     data=[],
    #     columns=[{"name": 'idInternalCollaborator', "id": 'idInternalCollaborator', 'editable': False},
    #              {"name": 'idContract', "id": 'idContract', 'editable': False},
    #              {"name": 'Attrition', "id": 'Attrition', 'editable': False},
    #              {"name": 'P(Non-attrition)', "id": 'ValueStay', 'editable': False},
    #              {"name": 'P(Voluntary attrition)', "id": 'ValueVoluntary', 'editable': False},
    #              {"name": 'P(Involuntary attrition)', "id": 'ValueInvoluntary', 'editable': False},

    #              {"name": 'Age', "id": 'Age', 'editable': False},
    #              {"name": 'Years at Company', "id": 'Float_Year_at_Company', 'editable': False},
    #              {"name": 'Sex', "id": 'Sex', 'editable': False},
    #              {"name": 'Marital Status', "id": 'Marital_Status', 'editable': False},
    #              {"name": 'Academic Qualifications', "id": 'Academic_Qualifications', 'editable': False},
    #              {"name": 'Field of Study', "id": 'Study_Area', 'editable': False},
    #              {"name": 'Area', "id": 'Area', 'editable': False},
    #              {"name": 'Professional Qualifications', "id": 'Qualifications', 'editable': False},
    #              {"name": 'Salary Rate', "id": 'Salary_Rate', 'editable': False},
    #              {"name": 'Contract Type', "id": 'Contract_Type', 'editable': False},
    #              ],
    #     editable=False,
    #     filter_action="native",
    #     sort_action="native",
    #     sort_mode="multi",
    #     column_selectable="single",
    #     row_selectable="multi",
    #     row_deletable=False,
    #     selected_columns=[],
    #     selected_rows=[],
    #     page_action="native",
    #     page_current= 0,
    #     page_size= 10,
    # ),
    
    # html.Div(id='choosen_id_msg', children=[str(global_var)]),
    #this data is teh result of the selection in the table
    # (will be sent for page "Individual attrition)
    #    dcc.Store(id='selected_rows_data', storage_type='local'),
    html.Div(id='choosen_att_msg', children='Please select Attrition category in pie chart'),
    
])



#%%

@app.APP.callback(
    [Output(component_id='bar_plot', component_property='figure'),
     Output(component_id='pie_plot', component_property='figure'),
     #Output(component_id='bar_plot', component_property='style'),
     #Output(component_id='debug_print', component_property='children'), 
    ],
    [Input(component_id='slct_area', component_property='value'),
     Input(component_id='pie_plot', component_property='clickData' )]      
)
def update_graph(slctd_value, click_data):   
    app.LST_DEFAULT_AREA = slctd_value
    global DATA_CUT
    if type(slctd_value)==str:
        DATA_CUT = app.DATA.loc[app.DATA['Area'].isin([slctd_value])]
    else:
        DATA_CUT = app.DATA.loc[app.DATA['Area'].isin(slctd_value)]
    fig1 = px.bar(
        data_frame=DATA_CUT,
        x='Area',
        color='Attrition',
        color_discrete_map={
            'No': 'green', 'Voluntary': 'red', 'Involuntary': 'blue'},
        barmode="group")
    vc = DATA_CUT.Attrition.value_counts(normalize=True).to_frame()
    vc['category'] = vc.index
    fig2= px.pie(data_frame=vc, 
                  values='Attrition', 
                  color='category', 
                  color_discrete_map={
                      'Voluntary': 'red', 'Involuntary': 'blue', 'No': 'green'})
    if click_data:
        slctd_att = click_data.get('points')[0].get('customdata')[0]
        if slctd_att == vc.category[0]:
            fig2.update_traces(pull=[0.2,0,0], selector=dict(type='pie'))
        elif slctd_att == vc.category[1]:
            fig2.update_traces(pull=[0,0.2,0], selector=dict(type='pie'))
        elif slctd_att == vc.category[2]:
            fig2.update_traces(pull=[0,0,0.2], selector=dict(type='pie'))
    #style_fig = {'visibility':'visible'}
    return fig1, fig2 #, ['new: {}'.format(str(app.LST_DEFAULT_AREA))]


@app.APP.callback(
    Output(component_id='choosen_att_msg', component_property='children'),
    Input(component_id='pie_plot', component_property='clickData' )
    )
def update_id_drop(click): 
    if click:
        slctd_att = click.get('points')[0].get('customdata')[0]
        app.DEFAULT_ATT = slctd_att
        return 'The selected Attrition category is: {}'.format(slctd_att)
    else:
        return no_update

#%%

# @app.APP.callback(
#     Output(component_id='datatable-interactivity', component_property='data'),
#     Input(component_id='pie_plot', component_property='clickData' )
#     )
# def update_id_drop(click): 
#     if click:
#         slctd_att = click.get('points')[0].get('customdata')[0]
#         app.DEFAULT_ATT = slctd_att
        
#         global DATA_ATT
#         DATA_ATT = DATA_CUT.loc[DATA_CUT['Attrition']==slctd_att]
#         #msg = 'you have selected the class of {} Attrition'.format(slctd_att)
        
#         #return msg, DATA_ATT.to_dict('records') 
#         return DATA_ATT.to_dict('records') 
#     else:
#         return no_update

# @app.APP.callback(
#     [
#       Output('selected_rows_data', 'data'),
#       Output('choosen_id_lst', 'children')],
#     Input('datatable-interactivity', "selected_rows")
#     )
# def update_select_ids(selected_rows):  
#     if selected_rows:
#         df = DATA_ATT.iloc[selected_rows] 
#         app.LST_IDS = df.idContract.tolist()
#         msg = 'The selected rows are:'
#         for r in app.LST_IDS: 
#             msg = msg+'\n'+str(r)
#             return app.LST_IDS, msg  
#     else:
#           return no_update, no_update
