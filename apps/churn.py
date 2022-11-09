
from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

import app
#%%
# Definition of past trimester

#getting actual "today's" date
today = date.today()

#simulating to have an impact for the data that we have
#today = datetime.strptime('05-08-2021', '%d-%m-%Y').date()


churn_df = None

#%%

layout = html.Div([
    html.Button(id = 'button_invisible', n_clicks=0, style = dict(display='none') ),
    html.Div(id='debug_string', children=[]),
    
    html.H1('Churn', style={"textAlign": "center"}),
    
    html.Br(),
    dcc.Dropdown(id="slct_areas",
                 options = {1:'Administration & Management',
                            2:'Financial', 
                            3:'Information Technology',
                            4:'Human Resources', 
                            5:'Logistics',
                            6:'Commercial & Marketing', 
                            7:'Engineering & Research', 
                            8:'Production', 
                            9:'Quality',
                            10:'Maintenance'},
                 value = [1,2,3,4,5,6,7,8,9,10],
                 multi=True,
                 style={'width': "60%"}
                 ),
    html.Br(),
    dcc.DatePickerRange(id='date_picker',
        start_date=date(2020, 1, 15),
        end_date=today,
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=today,
        display_format='DD-MM-YYYY',
        #start_date_placeholder_text='MMM Do, YY'
        ),
    
    dcc.Dropdown(id="slct_time_dif",
                  options = {1:'Month',
                            3:'Trimester'},
                  value = 1,
                  multi=False,
                  style={'width': "40%"}
                  ),
    
    html.H2('Table Churn Data', style={"textAlign": "left"}),
    dash_table.DataTable( id='table_churn_data',
        data=[],
        columns=[{"name": 'Date', "id": 'dates', 'editable': False},
                 {"name": 'Churn Rate', "id": 'ChurnRate', 'editable': False},
                 {"name": 'Leave Rate', "id":  'LeaveRate', 'editable': False},
                 {"name": 'Involuntary Churn Rate', "id":  'Involuntary', 'editable': False},
                 {"name": 'Voluntary Churn Rate', "id":  'Voluntary', 'editable': False},
                 {"name": 'Other Churn Rate', "id":  'Other', 'editable': False},
                 {"name": 'Retirement Churn Rate', "id":  'Retirement', 'editable': False},
                ]
        ),
    dcc.Graph(id='churn_graph', 
              style = {'visibility':'hidden'},
              figure={"layout": {"title": "waiting for data..."}}),
    
    ])


#%%
conn = app.con

def get_churn(date_start, date_end, time_dif, areas_lst):
    if len(areas_lst)==1:
        area_tup = '({})'.format(areas_lst[0])
    else:
        area_tup = str(tuple(areas_lst))
    start_date = datetime.strptime(date_start, '%Y-%m-%d').date()
    ref_month=int(start_date.month)
    ref_year=int(start_date.year)
    
    past_date = start_date + relativedelta(months=-int(time_dif))
    past_year = int(past_date.year)
    if int(time_dif) == 1:
        first_date=datetime.strptime('01-12-'+str(past_year), '%d-%m-%Y').date()
    elif int(time_dif) ==3 : 
        if ref_month in [1,2,3]:
            first_date=datetime.strptime('01-10-'+str(past_year), '%d-%m-%Y').date()
        elif ref_month in [4,5,6]:
            first_date=datetime.strptime('01-01-'+str(ref_year), '%d-%m-%Y').date()
        elif ref_month in [7,8,9]:
            first_date=datetime.strptime('01-04-'+str(ref_year), '%d-%m-%Y').date()
        elif ref_month in [10,11,12]:
            first_date=datetime.strptime('01-07-'+str(ref_year), '%d-%m-%Y').date()

    # number of employees at beggining of trimester
    base_query = 'SELECT COUNT(ics."IdInternalCollaborator")  FROM "InternalCollaborator_Status" ics, "Contract" co WHERE (co."IdInternalCollaborator" = ics."IdInternalCollaborator") AND (co."IdArea" IN {}) AND (ics."StartDate" <{} {})   AND ( (ics."EndDate" IS Null) OR (ics."EndDate" >{} {}) )'
    
    date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
    new_date = first_date
    stri='start: '
    lst_dates = []
    lst_ChurnRate = []
    lst_LeaveRate = []
    lst_Involuntary = []
    lst_Voluntary = []
    lst_Other = []
    lst_Retirement = []
    while new_date < date_end:
        new_date_str1="'01-{}-{}'".format(new_date.month, new_date.year)

        stri += str(new_date)
        
        beggining_query = base_query.format(area_tup, '=', new_date_str1, '=', new_date_str1)
        N_beggining = pd.read_sql(beggining_query, conn)['count'].values[0]
        
        new_date = new_date + relativedelta(months=+int(time_dif))
        new_date_str2="'01-{}-{}'".format(new_date.month, new_date.year)

        # number of employees at end of trimester
        finish_query = base_query.format(area_tup, '',new_date_str2, '=', new_date_str2)
        N_finish = pd.read_sql(finish_query, conn)['count'].values[0]
        
        leave_query = 'SELECT COUNT(co."IdInternalCollaborator")  FROM "Contract" co  WHERE (co."IdArea" IN {})  AND (co."LeaveDate" >= {})  	AND (co."LeaveDate" < {})'.format(area_tup, new_date_str1, new_date_str2)
        N_leave = pd.read_sql(leave_query, conn)['count'].values[0]
        
        #claculate churn rate
        ChurnRate=round(((N_beggining-N_finish)/N_beggining)*100, 2)
        LeaveRate=round(((N_leave)/N_beggining)*100, 2)
        stri += ' N_beggining'+str(N_beggining)
        stri += ' N_finish'+str(N_finish)
        stri += ' ChurnRate'+str(ChurnRate)
        stri += ' LeaveRate'+str(LeaveRate)+',    '
        
        lst_dates.append(new_date + relativedelta(days=-1))
        lst_ChurnRate.append(ChurnRate)
        lst_LeaveRate.append(LeaveRate)
        
        churn_class_query = 'SELECT COUNT(ch."IdChurn"), ch."Description"   FROM "Contract" co, "LeaveMotive" lm, "Churn" ch  WHERE (co."IdLeaveMotive" = lm."IdLeaveMotive")  	AND (lm."IdChurn" = ch."IdChurn")  	AND (co."LeaveDate" >= {})  	AND ( co."LeaveDate" < {})  	AND (co."IdArea" IN {} )  GROUP BY (ch."IdChurn")  ORDER BY COUNT(ch."IdChurn") DESC'.format(new_date_str1, new_date_str2, area_tup)
        N_ChurnClass = pd.read_sql(churn_class_query, conn)
        N_ChurnClass.rename(columns={'count':'Number of employees', 'Description':'Churn Class'}, inplace=True)
        
        df_tab = pd.DataFrame(columns=['Churn Class'], data = {'Churn Class': ['Involuntary', 'Voluntary', 'Other', 'Retirement']})
        df_tab.set_index('Churn Class')
        
        N_ChurnClass['Percentage of employees'] = N_ChurnClass['Number of employees'].apply(lambda x: x/N_beggining *100 )
        
        df_tab = df_tab.join(N_ChurnClass.set_index('Churn Class'), on='Churn Class') #,  lsuffix='_left', rsuffix='_right')

        df_tab.fillna(0, inplace=True)
        df_tab = df_tab.round(2)
        df_tab = df_tab.drop(['Number of employees'], axis=1).set_index('Churn Class').T
        
        lst_Involuntary.append(df_tab['Involuntary'][0])
        lst_Voluntary.append(df_tab['Voluntary'][0])
        lst_Other.append(df_tab['Other'][0])
        lst_Retirement.append(df_tab['Retirement'][0])
        
    df=pd.DataFrame({'dates': lst_dates,
                    'ChurnRate': lst_ChurnRate,
                    'LeaveRate': lst_LeaveRate,
                    'Involuntary': lst_Involuntary,
                    'Voluntary': lst_Voluntary,
                    'Other': lst_Other,
                    'Retirement': lst_Retirement})
    #stri += '----               ----'+beggining_query
    return stri, df, df_tab
    

#%%
@app.APP.callback(
    [Output(component_id='debug_string', component_property='children'),
     Output(component_id='table_churn_data', component_property='data'),
     Output(component_id='churn_graph', component_property='figure'),
     Output(component_id='churn_graph', component_property='style'),
     ],
    [Input(component_id='button_invisible', component_property='n_clicks'),
     Input(component_id='slct_areas', component_property='value'),
     Input(component_id='date_picker', component_property='start_date'),
     Input(component_id='date_picker', component_property='end_date'),
     Input(component_id='slct_time_dif', component_property='value'),
     ]
    )
def update_debug(n_clicks, areas_lst, start_date, end_date, time_dif):
    if type(areas_lst)!=list:
        areas_lst=[areas_lst]
    stri, df, df_tab = get_churn(start_date, end_date, time_dif, areas_lst)
    # stri = 'start: '
    # date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
    # date_end = datetime.strptime(end_date, '%Y-%m-%d').date()
    # new_date = date_start
    # while new_date <= date_end:
    #     stri += str(new_date)+', '
    #     new_date = new_date + relativedelta(months=+int(time_dif))
     
    global churn_df
    
    churn_df=df
    
    # fig = px.line(df, x='dates', 
    #               y=['ChurnRate', 'LeaveRate',
    #                  'Involuntary', 'Voluntary', 'Other', 'Retirement'])
    
    fig = px.bar(df, x='dates', 
                  y=['Involuntary', 'Voluntary', 'Other', 'Retirement'],
                  color_discrete_map={
                      'Voluntary': 'red', 'Involuntary': 'blue', 'Other':'yellow', 'Retirement':'pink'},
                  barmode='stack')
    
    if int(time_dif)==1:
       x_axis='Month'
    elif int(time_dif)==3:
       x_axis='Trimester'
        
    fig.update_layout(
        title="Churn Rate Time Series",
        xaxis_title=x_axis,
        yaxis_title="Churn Rate (%)",
        legend_title="Churn Class",
        font=dict(
            family="Arial",
            size=18,
            color="RebeccaPurple")
        )
    if int(time_dif)==1:
       fig.update_xaxes(
           dtick="M1",
           tickformat="%b\n%Y",
           ticklabelmode="period")
    elif int(time_dif)==3:
       fig.update_xaxes(
           dtick="M3",
           tickformat="%b\n%Y",
           ticklabelmode="period")
    
    
    style_fig = {'visibility':'visible'}
    
    return [str(df_tab)], df.to_dict('records'), fig, style_fig
