from dash import Dash,html,dash_table
import pandas as pd

df = pd.read_csv("cleaned.csv")

app = Dash()

app.layout = [html.Div(children = "Immunohistochemistry Data"),
              dash_table.DataTable(data = df.to_dict("records"),page_size = 20)]

if __name__ == '__main__':
    app.run(debug=True)