import base64
import io

##https://community.plotly.com/t/how-to-add-your-dash-app-to-flask/51870/2

from dash import Dash, html, dcc, dash_table, Input, Output, callback, State
import flask
import webview
import threading
import pandas as pd
import os
import signal

### FLASK ###
flaskServer = flask.Flask(__name__)

##The flask server is itself blank
@flaskServer.route('/')
def CWAAPP():
    return

#Link a dash server object the Flask server object
dashFrontend = Dash(server=flaskServer, routes_pathname_prefix='/CWAAPP/')

#Start the Dash Server
def startDash():
    dashFrontend.run_server()

#Script to set a thread event to true which can be read by the Dash Thread
def closeApp():
    appClosed.set()

### DASH APPLICATION LAYOUT ###
dashFrontend.layout = html.Div([
    #Checks for the window being closed, does not display
    dcc.Interval(id='closeAppChecker',interval=1*100, n_intervals=0),
    html.Div(id='emptyForIntervalOutput'),

    #Application body
    html.Div(['test']),
    dcc.Upload(id='uploadSpreadsheet', children=html.Div([html.A('Upload')])),
    html.Div(id='dataTable')
])

#Callback at a set interval to check if the user has closed the window. Terminate the thread if true.
@callback(Output('emptyForIntervalOutput','children'),
          Input('closeAppChecker', 'n_intervals'))
def closeAppChecker(n):
    if appClosed.is_set() == True:
        #https://stackoverflow.com/questions/77257094/how-to-stop-flask-application-propperly-without-ctrl-c-after-10-seconds
        os.kill(os.getpid(), signal.SIGTERM)

#https://dash.plotly.com/dash-core-components/upload
@callback(Output('dataTable', 'children'),
          Input('uploadSpreadsheet', 'contents'),
          State('uploadSpreadsheet', 'filename'))
def refreshdataTable(contents, filename):
    contents_type, contents = contents.split(',')
    decoded = base64.b64decode(contents)

    dfUploadedData = pd.read_excel(io.BytesIO(decoded))

    return dash_table.DataTable(
        dfUploadedData.to_dict('records'), [{'name':i,'id':i} for i
                                            in dfUploadedData.columns]
    )


### MAIN/ WEBVIEW ###
if __name__ == '__main__':

    #https://docs.python.org/3/library/threading.html
    Thread = threading.Thread(target=startDash)
    Thread.start()

    #https: // pywebview.flowrl.com / examples / events.html
    main = webview.create_window('CWAAPP', 'http://127.0.0.1:8050/CWAAPP/')
    main.events.closing += closeApp
    # https://superfastpython.com/thread-event-object-in-python/
    appClosed = threading.Event()
    webview.start()
