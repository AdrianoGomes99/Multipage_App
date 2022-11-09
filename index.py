from dash import dcc, html
from dash.dependencies import Input, Output

# Connect to main app.py file
#from app import APP, SERVER
import app
# Connect to your app pages
from apps import group, individual, overview, churn


app.APP.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        # html.Div(id='msg', children=['Paste the string that represents the JSON file of employee data!']),
        # dcc.Input(id="input_text", type='text', placeholder=''),
        # html.Button(id = 'my_button', n_clicks=0, children='Load Data'),
        # dcc.Store(id='stored_data'),
        # html.Div(id='loaded_msg', children=''),
        # html.Br(),
        # dcc.Store(id='index_selected_data'),
        # html.Div(id='slcted_id_data_msg', children=''),
        # html.Br(),
        html.Div([dcc.Link('Overview', href='/apps/overview') ], className="button"),
        html.Div([dcc.Link('Churn', href='/apps/churn') ], className="button"),
        html.Div([dcc.Link('Group Attrition', href='/apps/group') ], className="row"),
        html.Div([dcc.Link('Individual Attrition', href='/apps/individual') ], className="link"),
    ], className="one-tenth column"), #"one-third column"),
    html.Div(id='page-content', children=[], className="nine-tenths column"), #"two-thirds column"),
], className="column")



#%%

# @app.callback(
#     [Output('stored_data', 'data'),
#      Output('loaded_msg', 'children')],
#     [Input('input_text', 'value'),
#      Input('my_button', 'n_clicks')]
#     )
# def clean_data(value, n_clicks):
#      df = create_df(value)
#      return df.to_json(orient = 'records') , 'Data loaded successfully!'
 
#%%

@app.APP.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
    )
def display_page(pathname):
    if pathname == '/apps/overview':
        return overview.layout
    if pathname == '/apps/churn':
        return churn.layout
    elif pathname == '/apps/group':
        return group.layout
    elif pathname == '/apps/individual':
        return individual.layout
    else:
        #return overview.layout 
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.APP.run_server(debug=True)
