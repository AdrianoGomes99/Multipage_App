from dash import dcc, html
from dash.dependencies import Input, Output

# Connect to main app.py file
#from app import APP, SERVER
import app
# Connect to your app pages
from apps import group, individual, overview, churn

#link reference : https://medium.com/analytics-vidhya/beautiful-dashboards-with-dash-and-tailwindcss-bf0f8d5c67e

app.APP.layout = html.Div(
    children=[
        html.Header(
            children=[
                html.H1(children="Augmanity Dashboard Application", className=" py-3 text-5xl font-bold text-gray-800"), 
                ],
            className="flex h-20 w-full flex-none items-center border-b border-border-gray bg-blue-primary", #"w-full mx-14 px-16 shadow-lg bg-white -mt-14 px-6 container my-3 ",
            ),
        
        dcc.Location(id='url', refresh=False),
#------------------------------------------------------------------------------

        html.Div(
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Link('Overview', href='/apps/overview'),
                                html.Br(),
                                html.Span("Overview", className="text-lg font-bold ml-4"),
                            ],
                            className=" shadow-xl py-4 px-14 text-5xl bg-[#76c893] text-white  font-bold text-gray-800",
                        ),
                        html.Div(
                            children=[
                                dcc.Link('Churn', href='/apps/churn'),
                                html.Br(),
                                html.Span("Churn", className="text-lg font-bold ml-4"),
                            ],
                            className=" shadow-xl py-4 px-24 text-5xl bg-[#1d3557] text-white  font-bold text-gray-800",
                        ),
                        html.Div(
                            children=[
                                dcc.Link('Group Attrition', href='/apps/group'),
                                html.Br(),
                                html.Span("Group Attrition", className="inline-flex items-center text-lg font-bold ml-4"),
                            ],
                            className=" shadow-xl py-4 px-24 text-5xl bg-[#646ffa] text-white  font-bold text-gray-800",
                        ),
                        html.Div(
                            children=[
                                dcc.Link('Individual Attrition', href='/apps/individual'),
                                html.Br(),
                                html.Span("Individual Attrition", className="text-lg font-bold ml-4"),
                            ],
                            className="w-full shadow-xl py-4 px-24 text-5xl bg-[#ef553b] text-white  font-bold text-gray-800",
                        ),
                    ],
                    className="my-4 w-full grid grid-flow-rows grid-cols-1 lg:grid-cols-4 gap-y-4 lg:gap-[60px]",
                ),
                className="flex max-w-full justify-between items-center ",
            ),
        html.Div(id='page-content',
                 children=[],
                 className="flex flex-row"),
#------------------------------------------------------------------------------
        
        # html.Div(
        #     children=[
        #         dcc.Location(id='url', refresh=False),
        #         html.Div(
        #             children=[
        #                 html.Div(
        #                     children=[
        #                         dcc.Link('Overview', href='/apps/overview') 
        #                         ], 
        #                     className="flex flex-row"),
        #                 html.Div(
        #                     children=[
        #                         dcc.Link('Churn', href='/apps/churn') 
        #                         ], 
        #                     className="flex flex-row"),
        #                 html.Div(
        #                     children=[
        #                         dcc.Link('Group Attrition', href='/apps/group') 
        #                         ], 
        #                     className="flex flex-row"),
        #                 html.Div(
        #                     children=[
        #                         dcc.Link('Individual Attrition', href='/apps/individual') 
        #                         ],
        #                     className="flex flex-row"),
        #                 ], 
        #             className="flex flex-row-reverse")
        #         ,
        #         html.Div(id='page-content', 
        #                  children=[],
        #                  className="flex flex-row-reverse"), #"two-thirds column"),
        #     ],
        #     className="inline-flex items-center"
        #     ),
        
        html.Footer(
            children=[
                html.H1(
                    children=[
                        " ............ Footer ............ ",
                        ], 
                    className=" py-3 text-5xl font-bold text-gray-800 bg-contain bg-center"), 
                ],
            className="flex flex-row" #"w-full mx-14 px-16 shadow-lg bg-contain bg-center -mt-14 px-6 container my-3 ",
            ),
        
        ],
        className="flex h-screen w-screen flex-col overflow-hidden scroll-smooth antialiased", #"bg-[#ebeaee] container mx-auto px-14 py-4",
    )





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
