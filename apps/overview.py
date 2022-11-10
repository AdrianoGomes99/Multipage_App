
from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date, datetime
import pandas as pd

import app 

#%%
layout = html.Div([
    html.Button(id = 'invisible_button', n_clicks=0, style = dict(display='none') ),
    html.Div(id='debug_place', children=[]),
    
    html.H1('Overview', style={"textAlign": "center"}),
    
    html.H2('Company Churn Rate:', style={"textAlign": "left"}),
    html.H3(id='churn_rate', children='', style={"textAlign": "left"}),
    
    
    html.H2('Top 5 Leave Motives:', style={"textAlign": "left"}),
    html.H3(id='top_motives', children='', style={"textAlign": "left"}),
    dash_table.DataTable( id='top_motives',
        data=[],
        columns=[{"name": 'Number of employees', "id": 'Number of employees', 'editable': False},
                 {"name": 'Leave Motive', "id": 'Leave Motive', 'editable': False},
                ]
        ),
    
    html.H2('Number of Employess in Churn Class:', style={"textAlign": "left"}),
    dash_table.DataTable( id='n_employees_churn_class',
        data=[],
        columns=[{"name": 'Number of employees', "id": 'Number of employees', 'editable': False},
                 {"name": 'Churn Class', "id": 'Churn Class', 'editable': False},
                ]
        ),
    html.Div([
        html.H2(children="Churn Pie Plot", style={"textAlign": "center"}),
        dcc.Graph(id='churn_pie_plot', figure=px.pie() )
            #}, style = {'visibility':'hidden'})
    ]),
    
    
    html.H2('% of Employess in Churn Class By Area', style={"textAlign": "left"}),
    dash_table.DataTable( id='n_employees_churn_class_area',
        data=[],
        columns=[{"name": 'Churn Class', "id": 'Churn Class', 'editable': False},
                 {"name": 'Administration/Management', "id": 'Administration/Management', 'editable': False},
                 {"name": 'Financial', "id":  'Financial', 'editable': False},
                 {"name": 'Information Technologies', "id":  'InformationTechnologies', 'editable': False},
                 {"name": 'Human Resources', "id":  'HumanResources', 'editable': False},
                 {"name": 'Logistics', "id":  'Logistics', 'editable': False},
                 {"name": 'Commercial/Marketing', "id":  'Commercial/Marketing', 'editable': False}, 
                 {"name": 'Engineering & Research', "id":  'EngineeringandResearch', 'editable': False}, 
                 {"name": 'Production', "id":  'Production' , 'editable': False},
                 {"name": 'Quality', "id":  'Quality', 'editable': False},
                 {"name": 'Maintenance', "id":  'Maintenance', 'editable': False}
                ]
        ),
    html.Div([
        html.H2(children="Churn Bar Plot", style={"textAlign": "center"}),
        dcc.Graph(id='churn_bar_plot', figure=px.bar() )
            #}, style = {'visibility':'hidden'})
    ]),
    
    html.H2('Areas with highest Class Churn Rate', style={"textAlign": "left"}),
    dash_table.DataTable( id='area_highest_churn_class',
        data=[],
        columns=[{"name": 'Churn Class', "id": 'Churn Class', 'editable': False},
                 {"name": 'Area', "id": 'Area', 'editable': False},
                 {"name": 'Churn Rate (%)', "id":  'Churn Rate (%)', 'editable': False},
                ]
        ),
    ],
    className='overflow-y-auto h-full w-full flex flex-col items-center',
    )

conn = app.con

#%%
# Definition of past trimester

#getting actual "today's" date
# today = date.today()

#simulating to have an impact for the data that we have
today = datetime.strptime('05-08-2021', '%d-%m-%Y').date()


today_month=int(today.month)
if today_month in [1,2,3]:
    beggining_date=datetime.strptime('01-10-'+str(int(today.year)-1), '%d-%m-%Y').date()
    finish_date=datetime.strptime('01-01-'+str(int(today.year)), '%d-%m-%Y').date()
elif today_month in [4,5,6]:
    beggining_date=datetime.strptime('01-01-'+str(int(today.year)), '%d-%m-%Y').date()
    finish_date=datetime.strptime('01-04-'+str(int(today.year)), '%d-%m-%Y').date()
elif today_month in [7,8,9]:
    beggining_date=datetime.strptime('01-04-'+str(int(today.year)), '%d-%m-%Y').date()
    finish_date=datetime.strptime('01-07-'+str(int(today.year)), '%d-%m-%Y').date()
elif today_month in [10,11,12]:
    beggining_date=datetime.strptime('01-07-'+str(int(today.year)), '%d-%m-%Y').date()
    finish_date=datetime.strptime('01-10-'+str(int(today.year)), '%d-%m-%Y').date()

beggining_date="'01-{}-{}'".format(beggining_date.month, beggining_date.year)
finish_date="'01-{}-{}'".format(finish_date.month, finish_date.year)

#%%
# number of employees at beggining of trimester
base_query = 'SELECT COUNT(ics."IdInternalCollaborator")  FROM "InternalCollaborator_Status" ics  WHERE (ics."StartDate" <{} {})   AND ( (ics."EndDate" IS Null) OR (ics."EndDate" >{} {}) )'
beggining_query = base_query.format('=', beggining_date, '=', beggining_date)
N_beggining = pd.read_sql(beggining_query, conn)['count'].values[0]

# number of employees at end of trimester
finish_query = base_query.format('',finish_date, '=', finish_date)
N_finish = pd.read_sql(finish_query, conn)['count'].values[0]

#claculate churn rate
ChurnRate=str(round(((N_beggining-N_finish)/N_beggining)*100, 2))+'%'

#%%
# top 5 motives of leave in trimester
top_motives_query = 'SELECT COUNT(lm."IdLeaveMotive"), lm."Description"  FROM "Contract" co, "LeaveMotive" lm  WHERE (co."IdLeaveMotive" = lm."IdLeaveMotive") AND (co."LeaveDate" >= {}) AND ( co."LeaveDate" < {})  GROUP BY (lm."IdLeaveMotive")  ORDER BY COUNT(lm."IdLeaveMotive") DESC' #  LIMIT 5'
top_motives_query_dates = top_motives_query.format(beggining_date, finish_date)
df_motives = pd.read_sql(top_motives_query_dates, conn)
df_motives.rename(columns={'count':'Number of employees', 'Description':'Leave Motive'}, inplace=True)

#%%
# number of employees in each churn class
churn_class_query = 'SELECT COUNT(ch."IdChurn"), ch."Description"  FROM "Contract" co, "LeaveMotive" lm, "Churn" ch  WHERE (co."IdLeaveMotive" = lm."IdLeaveMotive") AND (lm."IdChurn" = ch."IdChurn") AND (co."LeaveDate" >= {}) AND ( co."LeaveDate" <= {})  GROUP BY (ch."IdChurn")  ORDER BY COUNT(ch."IdChurn") DESC'
churn_class_query_dates = churn_class_query.format(beggining_date, finish_date)
df_classes = pd.read_sql(churn_class_query_dates, conn)
df_classes.rename(columns={'count':'Number of employees', 'Description':'Churn Class'}, inplace=True)

#%%
def clean_df(df_area_classes):
    df = pd.DataFrame(columns=['Number of employees', 'Churn Class'])
    j=0
    for i in ["Involuntary", "Voluntary", "Other", "Retirement"]:
        if i not in df_area_classes['Churn Class']:
            new_row = {'Number of employees':0, 'Churn Class':i}
        else:
            n= df_area_classes.at[j, 'Number of employees']
            new_row = {'Number of employees':n, 'Churn Class':i}
        j+=1
        #append row to the dataframe
        df = df.append(new_row, ignore_index=True)
    return df

# areas with highest class churn rate
df_tab = pd.DataFrame(columns=['Churn Class'], data = {'Churn Class': ['Involuntary', 'Voluntary', 'Other', 'Retirement']})
df_tab.set_index('Churn Class')

for area_id in range(1, 11):
    area_name_query = 'SELECT ar."Name"  FROM "Area" ar  WHERE ar."IdArea" = {}'.format(area_id)
    area_name =  pd.read_sql(area_name_query, conn)['Name'].values[0].replace(' ', '')
    
    area_query = 'SELECT COUNT(ics."IdInternalCollaborator")  FROM "InternalCollaborator" ic, "Contract" co, "Area" ar, "InternalCollaborator_Status" ics  WHERE (co."IdInternalCollaborator" = ic."IdInternalCollaborator")  AND (ics."IdInternalCollaborator" = ic."IdInternalCollaborator")  AND (co."IdArea" = ar."IdArea")  AND (co."IdArea" = {})  AND (ics."StartDate" <{} {})  AND ( (ics."EndDate" IS Null)  OR (ics."EndDate" >{} {}) )'
    ## number of employees at beggining in the Area
    beggining_area_query = area_query.format(area_id, '=', beggining_date, '=', beggining_date)
    N_area_beggining = pd.read_sql(beggining_area_query, conn)['count'].values[0]
    
    ## number of employees at end in the Area
    finish_area_query = area_query.format(area_id, '',finish_date, '=', finish_date)
    N_area_finish = pd.read_sql(finish_area_query, conn)['count'].values[0]
    
    ### churn rate in area
    ChurnRate_Area=str(round(((N_area_beggining-N_area_finish)/N_area_beggining)*100, 2))+'%'

    ## number of employees in each churn class in the Area
    area_churn_class_query ='SELECT COUNT(ch."IdChurn"), ch."Description"  FROM "Contract" co, "LeaveMotive" lm, "Churn" ch  WHERE (co."IdLeaveMotive" = lm."IdLeaveMotive")  AND (lm."IdChurn" = ch."IdChurn")  AND (co."LeaveDate" >= {})  AND ( co."LeaveDate" < {})  AND (co."IdArea" = {})  GROUP BY (ch."IdChurn")  ORDER BY COUNT(ch."IdChurn") DESC'
    area_churn_class_query_dates = area_churn_class_query.format(beggining_date, finish_date, area_id)
    df_area_classes = pd.read_sql(area_churn_class_query_dates, conn)
    df_area_classes.rename(columns={'count':'Number of employees', 'Description':'Churn Class'}, inplace=True)
    df_area_classes[area_name] = df_area_classes['Number of employees'].apply(lambda x: x/N_area_beggining *100 )
    #df_area_classes.set_index('Churn Class')
    #df_area_classes = clean_df(df_area_classes)
    #df_tab = pd.concat([df_tab, df_area_classes], axis=1)
    df_tab = df_tab.join(df_area_classes.set_index('Churn Class'), on='Churn Class',  lsuffix='_left', rsuffix='_right')

df_tab.fillna(0, inplace=True)
df_tab = df_tab.round(2)

df_idmax = df_tab.drop(['Churn Class', 'Number of employees_right', 'Number of employees_left'], axis=1).T.idxmax(axis=0)
df_max = df_tab.drop(['Churn Class', 'Number of employees_right', 'Number of employees_left'], axis=1).T.max(axis=0)
df_area_max = df_idmax.to_frame().merge(df_max.to_frame(), left_index=True, right_index=True)
df_area_max.set_axis(df_tab['Churn Class'], inplace=True)
df_area_max.rename(columns={'0_x':'Area', '0_y':'Churn Rate (%)'}, inplace=True)
df_area_max['Churn Class'] = df_area_max.index

#%%
@app.APP.callback(
    [Output(component_id='debug_place', component_property='children'),
     Output(component_id='churn_rate', component_property='children'),
     Output(component_id='top_motives', component_property='data'),
     Output(component_id='n_employees_churn_class', component_property='data'),
     Output(component_id='n_employees_churn_class_area', component_property='data'),
     Output(component_id='area_highest_churn_class', component_property='data'),
     Output(component_id='churn_bar_plot', component_property='figure'),
     Output(component_id='churn_pie_plot', component_property='figure'),
     ],
    Input(component_id='invisible_button', component_property='n_clicks') 
    )
def update_debug(n_clicks):
    df = df_tab.drop(['Number of employees_right', 'Number of employees_left'], axis=1).set_index('Churn Class').T
    fig = px.bar(
        data_frame=df.to_dict('records'),
        x=[ 'Administration/Management', 'Financial', 'InformationTechnologies', 'HumanResources', 'Logistics', 'Commercial/Marketing', 'EngineeringandResearch', 'Production', 'Quality', 'Maintenance'],
        y=['Involuntary', 'Voluntary', 'Other', 'Retirement'],
        labels={
            "x": "Area",
            "value": "Churn Rate (%)",
            "variable": "Churn Class"
            },
        #color='Churn Class',
        color_discrete_map={
            'Voluntary': 'red', 'Involuntary': 'blue', 'Other':'yellow', 'Retirement':'pink'},
        barmode="stack")
        #barmode="group")
    
    fig2= px.pie(data_frame=df_classes.to_dict('records'), 
                  values='Number of employees', 
                  color='Churn Class', 
                  color_discrete_map={
                      'Voluntary': 'red', 'Involuntary': 'blue', 'Other':'yellow', 'Retirement':'pink'})
    fig2.update(layout_showlegend=True)
    #to present numbewrs instead of percentage in the pie chart
    fig2.update_traces(textinfo='value')
    
    return [str(df_classes.columns)], ChurnRate, df_motives.to_dict('records'), df_classes.to_dict('records'), df_tab.to_dict('records'), df_area_max.to_dict('records'), fig, fig2
    #return ['today: {},       start date: {},       end date: {}          '.format(str(today),str(beggining_date),str(finish_date)), 'N_beggining : {}       N_finish : {}'.format(N_beggining, N_finish)], ChurnRate, df_motives.to_dict('records')
