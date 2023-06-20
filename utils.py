import pandas as pd
# from twilio.rest import Client
# from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
from config import API_KEY_WAPI, SENDGRID_API_KEY
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date


def request_wapi(api_key, query):

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key=' + \
        api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try:
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response


def get_forecast(response, i):

    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[
        0]
    hora = int(response['forecast']['forecastday'][0]
               ['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return fecha, hora, condicion, tempe, rain, prob_rain


def create_df(data):

    cols = ['Fecha', 'Hora', 'Condicion',
            'Temperatura', 'Lluvia', 'Prob_lluvia']
    df = pd.DataFrame(data, columns=cols)
    df = df.sort_values(by='Hora', ascending=True)

    # df_rain = df[(df['Lluvia'] == 0) & (df['Hora'] > 6) & (df['Hora'] < 22)]
    # df_rain = df_rain[['Hora', 'Condicion']]
    # df_rain.set_index('Hora', inplace=True)

    df_no_rain = df.query('Lluvia == 0 and 6 < Hora < 22  ')
    df_no_rain = df_no_rain[['Hora', 'Condicion']]
    df_no_rain.set_index('Hora', inplace=True)

    return df_no_rain


def send_mail(SENDGRID_API_KEY, input_date, df_no_rain, query):

    # Configuración del remitente y destinatario
    sender_email = 'fbkett.pruebas@gmail.com'
    recipient_email = 'faviobarberiskettler@gmail.com'

    # Crea el objeto del correo electrónico
    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject='EL CLIMA DE HOY WACHO',
        plain_text_content='\nHola! \n\n\n El pronostico del tiempo hoy  ' + input_date + ' en  ' + query + ' es : \n\n\n ' + str(df_no_rain))

    try:
        # Configura la API key de SendGrid
        sendgrid_api_key = SENDGRID_API_KEY
        sg = SendGridAPIClient(api_key=sendgrid_api_key)

        # Envía el correo electrónico
        response = sg.send(message)
        print('El correo se ha enviado correctamente.')
    except Exception as e:
        print('Ocurrió un error al enviar el correo:', str(e))

    return response
