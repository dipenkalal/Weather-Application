import urllib.request
import json

from django.http import HttpResponse
from django.shortcuts import render

# from weatherProject.main import models
# from weatherProject.main.models import WeatherModel
# import psycopg2

from main.models import CurrentWeatherStatus

from main.models import CurrentAirQualityStatus


def index(request):
    if request.method == 'POST':
        city = request.POST['city']

        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                        city + '&units=metric&appid=104d5ffac43c1420b0797087139f411c').read()
        list_of_data = json.loads(source)

        data = {
            "city_name": city,
            "dt_in_api": str(list_of_data['dt']),
            "country_code": str(list_of_data['sys']['country']),
            "coordinate_x": float(list_of_data['coord']['lon']),
            "coordinate_y": float(list_of_data['coord']['lat']),
            "temp": float(list_of_data['main']['temp']),
            "pressure": float(list_of_data['main']['pressure']),
            "humidity": float(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            'description': str(list_of_data['weather'][0]['description']),
            "icon": str(list_of_data['weather'][0]['icon']),
        }

        current_weather = CurrentWeatherStatus(country_code=data['country_code'], dt_in_api=data['dt_in_api'],
                                               coordinate_x=data['coordinate_x'],
                                               coordinate_y=data['coordinate_y'], temp=data['temp'],
                                               pressure=data['pressure'], humidity=data['humidity'], main=data['main'],
                                               description=data['description'], icon=data['icon'],
                                               city_name=city.upper())
        current_weather.save()
        responds_data = {"current_weather": current_weather}

    else:
        print("inside else")
        responds_data = {}

    return render(request, "main/index.html", responds_data)


def pollution_index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                        city + '&units=metric&appid=104d5ffac43c1420b0797087139f411c').read()
        list_of_data = json.loads(source)
        longitude_of_city = float(list_of_data['coord']['lon'])
        latitude_of_city = float(list_of_data['coord']['lat'])
        air_quality = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat=' +
                                             str(latitude_of_city) + '&lon=' + str(longitude_of_city) +
                                             '&appid=104d5ffac43c1420b0797087139f411c').read()
        print(air_quality)
        list_of_pollution_data = json.loads(air_quality)

        air_quality_dict = {
            "city_name": city,
            "aqi": str(list_of_pollution_data['list'][0]['main']['aqi']),
            "co": float(list_of_pollution_data['list'][0]['components']['co']),
            "no": float(list_of_pollution_data['list'][0]['components']['no']),
            "no2": float(list_of_pollution_data['list'][0]['components']['no2']),
            "o3": float(list_of_pollution_data['list'][0]['components']['o3']),
            "so2": float(list_of_pollution_data['list'][0]['components']['so2']),
            "pm2_5": float(list_of_pollution_data['list'][0]['components']['pm2_5']),
            "pm10": float(list_of_pollution_data['list'][0]['components']['pm10']),
            "nh3": float(list_of_pollution_data['list'][0]['components']['nh3']),
        }
        current_air_quality = CurrentAirQualityStatus(city_name=air_quality_dict['city_name'],
                                                      aqi=air_quality_dict['aqi'],
                                                      co=air_quality_dict['co'],
                                                      no=air_quality_dict['no'],
                                                      no2=air_quality_dict['no2'],
                                                      o3=air_quality_dict['o3'],
                                                      so2=air_quality_dict['so2'],
                                                      pm2_5=air_quality_dict['pm2_5'],
                                                      pm10=air_quality_dict['pm10'],
                                                      nh3=air_quality_dict['nh3'])
        current_air_quality.save()

        responds_data = {"current_air_quality": current_air_quality}
        print("end")

    else:
        print("inside else")
        responds_data = {}

    return render(request, "main/pollution_index.html", responds_data)


def chart(request):
    data_fetched = CurrentWeatherStatus.objects.all()
    print("data fetched", data_fetched.values())
    data_arr = []
    temp_arr = []

    index_1 = 0
    for i in reversed(data_fetched):
        data_arr.append(i.city_name)
        temp_arr.append(i.temp)
        index_1 + 1
        if index_1 > 5:
            break
    print("city array", data_arr)
    print(temp_arr)
    # chart_dict = {
    #     "time": data_arr,
    #     "temp": temp_arr
    # }
    # for i, j in data_arr, temp_arr:
    chart_array = [['city_name', 'temperature'], [data_arr[0], temp_arr[0]], [data_arr[1], temp_arr[1]],
                   [data_arr[2], temp_arr[2]], [data_arr[3], temp_arr[3]], [data_arr[4], temp_arr[4]], [data_arr[5],
                                                                                                        temp_arr[5]]]
    # iterate and push to a table in html
    return render(request, "main/chart.html", {'chart_array': json.dumps(chart_array)})


def pollution(request):
    data_fetched = CurrentAirQualityStatus.objects.all()
    data_arr = []
    temp_arr = []

    index_1 = 0
    for i in reversed(data_fetched):
        data_arr.append(i.city_name)
        temp_arr.append(i.o3)
        index_1 + 1
        if index_1 > 5:
            break
    print("city array", data_arr)
    print(temp_arr)
    # chart_dict = {
    #     "time": data_arr,
    #     "temp": temp_arr
    # }
    # for i, j in data_arr, temp_arr:
    pollution_array = [['city_name', 'ozone'], [data_arr[0], temp_arr[0]], [data_arr[1], temp_arr[1]],
                       [data_arr[2], temp_arr[2]], [data_arr[3], temp_arr[3]], [data_arr[4],
                                                                                temp_arr[4]],
                       [data_arr[5], temp_arr[5]]]
    # iterate and push to a table in html
    return render(request, "main/pollution.html", {'pollution_array': json.dumps(pollution_array)})


# api calls
def get_all_pollutants(request):
    if request.method == 'GET':
        data_fetched = CurrentAirQualityStatus.objects.all()
        context = {
            "object_list": data_fetched,
        }
        return render(request, "main/get_all_pollutants.html", context)


def get_by_id(request):
    if request.method == 'GET':
        id_to_fetch = request.GET['id']
        data_fetched = CurrentWeatherStatus.objects.filter(id=int(id_to_fetch))
        context = {
            "object_list": data_fetched,
        }
        return render(request, "main/get_all_elements.html", context)


def get_all_elements(request):
    if request.method == 'GET':
        data_fetched = CurrentWeatherStatus.objects.all()
        context = {
            "object_list": data_fetched,
        }
        return render(request, "main/get_all_elements.html", context)
