import pandas as pd
import numpy as np
from pprint import pprint as pp
from sklearn.preprocessing import Imputer 

df = pd.read_csv('Hack2018_ES.csv')

## Columns Rename:
df = df.rename(columns = lambda x: x.lower()) 

## Checking Null value:
_null = df.isnull().sum()

## Handle Null value :
from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp = imp.fit(df.iloc[:,4:5].values)
df['patient_age'] = imp.transform(df.iloc[:,4:5].values)
df['patient_age'] = df['patient_age'].astype(int)

## Checking Duplicate Values:
_duplicates = df.duplicated()

## Drop duplicate value
df = df.drop_duplicates()
df = df[df.patient_age != -5]
## List of unique value:
_age = df.patient_age.unique() 
_Visit_Status = df.visit_status.unique()
_Is_Patient_Minor = df.is_patient_minor.unique()

## Date to date_time:
df['dateTime'] = pd.to_datetime(df['date'])
# pp(len(df['dateTime'].dt.dayofweek.unique()))

## Time to analysis:
import matplotlib.pyplot as plt
import calendar
plt.style.use('ggplot')

## Q. Patient age Wise Count :
_patient_age_wise = df.groupby(df['patient_age'] != -5).size()
_patient_age_wise.plot(kind = 'bar', alpha =1, figsize = (20,7))
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Patient age density')
# plt.show()

## Q. Day wise Visits:
_day_wise = df.groupby(df['dateTime'].dt.dayofweek).count().date
_day_wise.index = [calendar.day_name[x] for x in range(0,7)]
_day_wise.plot(kind = 'bar')
plt.xlabel('Day')
plt.ylabel('Count')
plt.title('Visits per day')
# plt.show()

## Q. Month wise Visits:
_month_wise = df.groupby(df['dateTime'].dt.month).count().date
_month_wise.plot(kind = 'bar',alpha = 1, figsize = (12,7))
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('Visits Per Month')
plt.xticks(np.arange(0,12), [calendar.month_name[x] for x in range(1,13)])
# plt.show()

## Year wise Vists:
_year_wise = df.groupby(df['dateTime'].dt.year).count().date
_year_wise.plot(kind='bar', alpha = 1, figsize = (12,7))
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Visits Per Year')
# plt.show()

## Under age patients(UAP) and Over age patients(OAP):
_minor_injuries = df.groupby(df['is_patient_minor']).size()
my_xticks = ['UAP','OAP']
_minor_injuries.plot(kind = 'bar',color = ['red', 'green'], alpha=1)
plt.xticks(np.arange(0,2), my_xticks)
plt.xlabel('Type of Patients')
plt.ylabel('Count')
plt.title('Analysis age value count')
# plt.show()

## Per hour UAP(under age patient) and OAP(Over age patient) visits:
_hourwise_UAP_injuries = df[df['is_patient_minor'] != 2].groupby(df['dateTime'].dt.hour).sum().is_patient_minor

_hourwise_OAP_injuries = df[df['is_patient_minor'] != 1].groupby(df['dateTime'].dt.hour).sum().is_patient_minor

rate = pd.DataFrame({'UAP': _hourwise_UAP_injuries, 'OAP': _hourwise_OAP_injuries})
rate.plot(kind = 'bar', color = ['red', 'green'], alpha = 1, figsize = (20,7))
plt.xlabel('Hour')
plt.ylabel('Count')
plt.title('Per hour UAP(under age patient) and OAP(Over age patient) visits')
# plt.show()

## Coordinates analysis:
df.latitude = df.latitude.apply(lambda x: x.replace(',','.'))
df.longitude = df.longitude.apply(lambda x: x.replace(',',"."))

pp(df.latitude.head())
# Display Home Visits:
import folium
from folium import plugins
from folium.plugins import FastMarkerCluster

folium_map = folium.Map(location = [41.38879, 2.15899], zoom_start = 12 )
FastMarkerCluster(data=list(zip(df['latitude'].values, df['longitude'].values))).add_to(folium_map)
folium.LayerControl().add_to(folium_map)
for lat, lng, label in zip(df.latitude, df.longitude, df.is_patient_minor.astype(str)):
    if label != '0':
        folium.CircleMarker(
            [lat,lng],
            radius = 3,
            color = 'red',
            fill = True,
            popup = label,
            fill_colored = "#007849",
            fill_opacity = 0.6
        ).add_to(folium_map)
# folium_map.save('index2.html')