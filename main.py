import os
# from twilio.rest import Client
# from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
from config import API_KEY_WAPI, SENDGRID_API_KEY
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime
from utils import request_wapi, get_forecast, create_df, get_date, send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


query = 'Corrientes'
api_key = API_KEY_WAPI

input_date = get_date()
response = request_wapi(api_key, query)

datos = []

for i in tqdm(range(24), colour='green'):

    datos.append(get_forecast(response, i))


df_no_rain = create_df(datos)

# Send Message
message = send_mail(
    SENDGRID_API_KEY, input_date, df_no_rain, query)


print('Correo envidado con exito ')
