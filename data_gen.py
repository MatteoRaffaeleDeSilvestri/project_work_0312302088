from datetime import date, timedelta
from retry_requests import retry
import openmeteo_requests
import requests_cache
import pandas as pd
import random

def weather_data_gen():

	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = 'https://api.open-meteo.com/v1/forecast'
	params = {
		'latitude': 40.85,
		'longitude': 14.28,
		'hourly': ['temperature_2m', 'relative_humidity_2m', 'precipitation_probability', 'cloud_cover', 'wind_speed_10m'],
   		'forecast_days': 14
	}
	responses = openmeteo.weather_api(url, params=params)

	response = responses[0]

	hourly = response.Hourly()
	hourly_ground_temperature = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
	hourly_ground_wind_speed = hourly.Variables(4).ValuesAsNumpy()
	
	hourly_data = {'date': pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = 's', utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = 's', utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = 'left'
	)}
	hourly_data['temperature_on_ground'] = hourly_ground_temperature
	hourly_data['humidity'] = hourly_relative_humidity_2m
	hourly_data['precipitation_%'] = hourly_precipitation_probability
	hourly_data['cloud_cover'] = hourly_cloud_cover
	hourly_data['wind_speed_at_ground'] = hourly_ground_wind_speed
	
	hourly_dataframe = pd.DataFrame(data = hourly_data)
	
	return hourly_dataframe

def alq_cun(utile):

	if utile <= 50000: val = 0.3
	elif utile <= 10000: val = 0.4 
	else: val = 0.5

	return val

def random_interval(t):

	if t == 'cst':
		inter_cst = list(x for x in range(-2, 5))
		return random.choice(inter_cst)/100

	elif t == 'ric':
		inter_ric = list(x for x in range(-10, 25))
		return random.choice(inter_ric)/100
	
	elif t == 'inv': 
		invest = list(x for x in range(0, 30))
		return random.choice(invest)/100
	
	elif t == 'com':
		inter_com = list(x for x in range(0, 30))
		return random.choice(inter_com)/100
	
	return 0

def uscite(utile, cun_f, costi):

	c_res = list(x for x in range(0, 100))

	imposte = int(utile*cun_f)
	residuo = int(costi)-int(imposte)
	dett_costi = {'imposte':imposte,'terreni':0,'immobili':0,'macchinari':0,'beni':0}

	k_ls = list(dett_costi.keys())
	i = 1

	while i < len(k_ls):
		
		if i == len(k_ls)-1:
			dett_costi[k_ls[i]] = int(residuo)
			residuo = 0
		else: 
			incr_com = random.choice(c_res)/100
			dett_costi[k_ls[i]] = int(residuo*incr_com)
			residuo -= int(residuo*incr_com)
		i += 1

	return dett_costi

def investimenti(investimento, appezzamenti):

	i_res = list(x for x in range(0, 100))

	dett_investimenti = {'invest_terreni':0,'invest_immobili':0,'invest_macchinari':0,'invest_beni':0}
	residuo = investimento
	
	k_ls = list(dett_investimenti.keys())
	i = 0

	while i < len(k_ls):
		
		if i == len(k_ls)-1:
			dett_investimenti[k_ls[i]] = int(residuo)
			residuo = 0
		else: 
			incr_com = random.choice(i_res)/100
			dett_investimenti[k_ls[i]] = int(residuo*incr_com)
			residuo -= int(residuo*incr_com)
		i += 1
	
	if dett_investimenti['invest_terreni'] >= int(investimento//2) and dett_investimenti['invest_terreni'] >= 30000: # Min valore di acquisto terreni: 30'000
		appezzamenti += 1

	return dett_investimenti, appezzamenti

def dataset_generator():

	anno = random.randint(2000, 2010)
	mese = random.randint(1, 12)

	incr_cst = random_interval('cst')
	incr_ric = random_interval('ric')
	incr_com = random_interval('com')

	# Definizione valori iniziali
	costi = random.randint(10000, 30000)
	ricavi = int(costi*(1+incr_ric))
	utile = int(ricavi)-int(costi)	
	liquidita = int(costi*alq_cun(utile)) # Liquidità iniziale pari al 30% dei costi

	# Entrate
	commercio = int(ricavi*(incr_com))
	produzione = int(ricavi)-int(commercio)

	# Uscite
	dett_costi = uscite(utile, alq_cun(utile), costi)

	# appezzamenti
	appezzamenti = 1

	# Investimenti
	investimento = 0
	dett_investimenti, appezzamenti = investimenti(investimento, appezzamenti)
	
	df_ls = list()

	while anno <= int(str(date.today())[:4]):
		while mese <= 12:
			
			df_ls.append([anno, mese, f'{anno}-{mese}', costi, ricavi, utile, liquidita, 
				 		investimento, dett_investimenti['invest_terreni'], dett_investimenti['invest_immobili'], dett_investimenti['invest_macchinari'], dett_investimenti['invest_beni'],
				 		produzione, commercio, dett_costi['imposte'], dett_costi['terreni'], dett_costi['immobili'], dett_costi['macchinari'],dett_costi['beni'],appezzamenti])

			incr_cst = random_interval('cst')
			incr_ric = random_interval('ric')
			incr_com = random_interval('com')
			
			costi = int(costi*(1+incr_cst))
			ricavi = int(costi*(1+incr_ric))
			utile = int(ricavi)-int(costi)

			# Compensazione utile negativo
			if utile < 0 and liquidita >= utile:
				liquidita += utile
			elif utile < 0 and liquidita < utile:
				costi -= utile 
				liquidita = 0

			# Definizione investimenti annuali
			dett_investimenti = {'invest_terreni':0,'invest_immobili':0,'invest_macchinari':0,'invest_beni':0}

			if liquidita > costi and mese == 12:
				invest_perc = random_interval('inv')
				costi += int(liquidita*invest_perc)
				liquidita -= int(liquidita*invest_perc)
				investimento = int(liquidita*invest_perc)
				dett_investimenti, appezzamenti = investimenti(investimento, appezzamenti)
			else: 
				investimento = 0
				liquidita += utile
			
			# Entrate
			commercio = int(ricavi*(incr_com))
			produzione = int(ricavi)-int(commercio)

			# Uscite
			dett_costi = uscite(utile, alq_cun(utile), costi)			

			# Stop
			if anno == int(str(date.today())[:4]) and mese == int(str(date.today())[5:7])-1: break
			mese += 1

		anno += 1
		mese = 1
	
	df = pd.DataFrame(df_ls, columns=['anno','mese','anno-mese','costi','ricavi','utile','liquidita',
									'investimento','invest_terreni','invest_immobili','invest_macchinari','invest_beni',
									'produzione','commercio','imposte','terreni','immobili','macchinari','beni',
									'appezzamenti'])

	# Definizione tabelle
	df_balance = df[['anno','mese','anno-mese','costi','ricavi','utile','liquidita']]
	df_balance.to_csv('assets/dataset_bilancio.csv',index=False)
	df_balance.to_excel('dataset.xlsx', sheet_name='dataset_bilancio')  

	df_investments = df[['anno','investimento','invest_terreni','invest_immobili','invest_macchinari','invest_beni']].query('investimento!=0')
	df_investments.to_csv('assets/dataset_investimenti.csv',index=False)

	df_productivity = df[['anno','mese','anno-mese','produzione']]
	df_productivity.to_csv('assets/dataset_produttività.csv',index=False)

	df_income_expenses = df[['anno','produzione','commercio','imposte','terreni','immobili','macchinari','beni']]
	df_income_expenses.to_csv('assets/dataset_entrate_uscite.csv',index=False)

	activity_type = ['Preparazione terreno','Coltivazione e trattamenti','Crescita','Raccolta']
	activity_ls = list()
	
	for i in range(appezzamenti):

		activity = random.choice(activity_type)
		split = random.choice([True, False])

		if split:
			next_activity = activity_type[(activity_type.index(activity)+1)%4]
			day_spilt = random.choice([x for x in range(1,14)])
			activity_ls.append({'Appezzamento':f'Appezzamento {i+1}','Inizio':f'{date.today()}','Fine':f'{date.today()+timedelta(day_spilt)}','Attività':activity})
			activity_ls.append({'Appezzamento':f'Appezzamento {i+1}','Inizio':f'{date.today()+timedelta(day_spilt)}','Fine':f'{date.today()+timedelta(13)}','Attività':next_activity})
		else:
			activity_ls.append({'Appezzamento':f'Appezzamento {i+1}','Inizio':f'{date.today()}','Fine':f'{date.today()+timedelta(13)}','Attività':random.choice(activity_type)})

	df_activity = pd.DataFrame(activity_ls)
	df_activity.to_csv('assets/dataset_attività.csv',index=False)

	return 0

if __name__ == '__main__':
    
	# weather_data_gen()
	dataset_generator()
