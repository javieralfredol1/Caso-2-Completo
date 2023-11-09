import dash
from dash import Dash,dcc,html,Input,Output
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

TA = pd.read_excel("Tasa Activa Excel.xlsx")
TA
IN = pd.read_excel("Inflación Excel.xlsx")
IN
CB = pd.read_excel("Crédito Excel.xlsx")
CB

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.title="Dashboard"

app.layout = html.Div([
    html.Div([
        # dropdown line TA
        html.Div([
            dcc.Graph(id="graph-line"),
            html.P("Año:"),
            dcc.Dropdown(id="namesTA",
                         options=[1996, 1997, 1998, 1999, 2000, 2001, 2002,
                                  2003, 2004, 2005, 2006, 2007, 2008, 2009,
                                  2010, 2011, 2012, 2013, 2014, 2015, 2016,
                                  2017, 2018, 2019, 2020, 2021, 2022
                                  ],
                         value=2022, clearable=False),
        ]),
        
        # dropdown bar IN
        html.Div([
            dcc.Graph(id="graph-bar"),
            html.P("Año:"),
            dcc.Dropdown(id="namesIN",
                         options=[1996, 1997, 1998, 1999, 2000, 2001, 2002,
                                  2003, 2004, 2005, 2006, 2007, 2008, 2009,
                                  2010, 2011, 2012, 2013, 2014, 2015, 2016,
                                  2017, 2018, 2019, 2020, 2021, 2022
                                  ],
                         value=2022, clearable=False),
        ]),
        
        # dropdown pie CB
        html.Div([
            dcc.Graph(id="pie-chart"),
            html.P("Año:"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{'label': str(year), 'value': year} for year in CB['AÑOS']],
                value=2022,
                clearable=False
            ),
        ]),
       
    #tabla
    html.Div(html.Div(id="table-container"),style={'marginBottom':'15px','marginTop':
                                                 "10px"}), 
        
    ])
])
  
@app.callback([Output("graph-line","figure"),
               Output("graph-bar","figure"),
               Output("pie-chart", "figure"),
               Output("table-container","children")],
              [Input("namesTA","value"),
               Input("namesIN","value"),
               Input("year-dropdown", "value")]
    
)

def generate_chart(namesTA,namesIN,selected_year):
    
    #graph line TA
    df1 = TA
    fig1 = px.line(df1, x="Año/Mes", y=namesTA, title=f"Tasas Activas para {namesTA}",markers=True)
    fig1.update_xaxes(title_text="Mes", title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje X
    fig1.update_yaxes(title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje Y
    fig1.update_xaxes(tickangle=55)
    fig1.update_layout(
    plot_bgcolor="black",  # Cambia el fondo de la gráfica
    paper_bgcolor="black",  # Cambia el fondo del área del gráfico
    font=dict(family="Arial", size=14, color="white"),  # Cambia la fuente y el tamaño del texto
    title_font=dict(size=18, color="white"))
    fig1.update_traces(marker_color="blue")
    fig1.update_traces(marker=dict(color="white"))  # Cambia el color de los marcadores
    fig1.update_traces(line=dict(width=3))  # Aumenta el ancho de las líneas
    fig1.update_traces(marker=dict(size=5, line=dict(width=2, color="white")))  # Cambia el tamaño y el borde de los marcadores
    
    #graph bar IN
    df2 = IN
    fig2 = px.bar(df2, x="Periodo", y=namesIN, title=f"Inflación para {namesIN}")
    fig2.update_xaxes(title_text="Mes", title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje X
    fig2.update_yaxes(title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje Y
    fig2.update_xaxes(tickangle=55)
    fig2.update_layout(
    plot_bgcolor="black",  # Cambia el fondo de la gráfica
    paper_bgcolor="black",  # Cambia el fondo del área del gráfico
    font=dict(family="Arial", size=14, color="white"),  # Cambia la fuente y el tamaño del texto
    title_font=dict(size=18, color="white"))
    fig2.update_traces(marker_line=dict(width=2, color="white"))
    fig2.update_traces(text=df2[namesIN], textposition="outside")
    fig2.update_yaxes(range=[0, df2[namesIN].max() + 1.5])  # Personalizar los límites del eje Y
    fig2.update_traces(marker_color="blue")
    
    #graph pie CB
    df3 = CB[CB['AÑOS'] == selected_year]
    labels = ["Sector Público", "Sector Privado"]
    values = [df3["Sector Público"].values[0], df3["Sector Privado"].values[0]]
    fig3 = px.pie(names=labels, values=values, title=f"Proporción de crédito para {selected_year}")

    # Personalizar el diseño del gráfico
    fig3.update_traces(textinfo="percent")  # No muestra los nombres en el pie
    fig3.update_traces(marker=dict(colors=['white', 'blue']))
    fig3.update_layout(
        plot_bgcolor="black",  # Cambia el fondo del gráfico
        paper_bgcolor="black",  # Cambia el fondo del área del gráfico
        font=dict(family="Arial", size=14, color="white"),  # Cambia la fuente y el tamaño del texto
        title_font=dict(size=18, color="white")
    )
    
    return(fig1,fig2,fig3,
          dash_table.DataTable(columns=[{"namesTA":i,"id":i} for i in TA],
                               data=TA.to_dict("records"),
                               export_format="csv",#para guardar como csv
                               fill_width=True,
                               style_header={'backgroundColor':'black',
                                            'color':'white'})
          )
           

    
if __name__ == '__main__':
    app.run_server(debug=False,host="0.0.0.0",port=10000)
