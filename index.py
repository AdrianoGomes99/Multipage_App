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
                html.Div(
                    children=[
                        html.P('Augmanity', className='float-left'),
                        html.P(
                            children=[
                                html.Div('User Name'),
                                html.Div('Profile Pic'),
                                ],
                            className='float-right'),
                        ],
                    className='flow-root',
                    ),
                html.H1(children="Churn & Attrition Dashboards", 
                        className="place-self-center py-3 text-5xl font-bold text-white"),
                ],
            className="flex h-30 w-full flex-col border-b border-[#707070] bg-[#364857]", #"w-full mx-14 px-16 shadow-lg bg-white -mt-14 px-6 container my-3 ",
            ),
        
        dcc.Location(id='url', refresh=False),
#------------------------------------------------------------------------------
        html.Div(
            children=[
        
                html.Div(
                    children=[
                        html.Ul(
                            children=[
                                html.Div(
                                    children=[
                                        dcc.Link('Overview', href='/apps/overview'),
                                        ],
                                    className="flex items-center space-x-4 rounded-2xl py-2 px-3 mx-auto w-4/5",
                                    ),
                                html.Div(
                                    children=[
                                        dcc.Link('Churn', href='/apps/churn'),
                                        ],
                                    className="flex items-center space-x-4 rounded-2xl py-2 px-3 mx-auto w-4/5",
                                    ),
                                html.Div(
                                    children=[
                                        dcc.Link('Group Attrition', href='/apps/group'),
                                        ],
                                    className="flex items-center space-x-4 rounded-2xl py-2 px-3 mx-auto w-4/5",
                                    ),
                                html.Div(
                                    children=[
                                        dcc.Link('Individual Attrition', href='/apps/individual'),
                                        ],
                                    className="flex items-center space-x-4 rounded-2xl py-2 px-3 mx-auto w-4/5",
                                    ),
                                ],
                            className="h-full flex-col space-y-10 overflow-y-auto scroll-smooth bg-[#E3E3E4] py-4 flex justify-evenly w-24 items-center"
                            ),
                        ],
                    className="relative w-auto",
                    ),
                
                html.Div(id='page-content',
                         children=[],
                         className="overflow-y-auto h-full w-full flex flex-col items-center "),
                ],
            className="h-full w-full overflow-hidden bg-[#898989]/[8%] flex "),
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
                # html.H1(
                #     children=[
                #         " ............ Footer ............ ",
                #         ], 
                #     className=" py-3 text-5xl font-bold text-gray-800 bg-contain bg-center"), 
                html.P('', className='float-left'),
                html.P('Copyright Augmanity 2022', className='float-right'),
                ],
            className="flow-root" #"w-full mx-14 px-16 shadow-lg bg-contain bg-center -mt-14 px-6 container my-3 ",
            ),
        
        ],
        className="flex h-screen w-screen flex-col overflow-hidden scroll-smooth antialiased", 
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
