from django.db import models


class CurrentWeatherStatus(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    dt_in_api = models.CharField(max_length=15)
    city_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=20)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    temp = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    main = models.CharField(max_length=80)
    description = models.CharField(max_length=80)
    icon = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "current_weather_status"


class CurrentAirQualityStatus(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    city_name = models.CharField(max_length=30)
    aqi = models.FloatField()
    co = models.FloatField()
    no = models.FloatField()
    no2 = models.FloatField()
    o3 = models.FloatField()
    so2 = models.FloatField()
    pm2_5 = models.FloatField()
    pm10 = models.FloatField()
    nh3 = models.FloatField()

    class Meta:
        db_table = "current_airquality_status"
