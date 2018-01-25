'''
Created on Jan 4, 2018

@author: Fawzi
'''
import json
import sys
import httplib2

class InvalidZipCode(RuntimeError):
    '''
    Generate A custom Error message
    '''
    def __init__(self, arg):
        super().__init__(self)
        self.strerror = arg
        self.args = {arg}

class WeatherData():
    '''
    Retrieve weather information from forecast.weather.gov
    by providing location latitude and longitude
    based on zip code entry
    '''
    def __init__(self, _zip):
        try:
            self._zip = _zip
            with open('data/zipcode.json') as file:
                self.__zip_data = file.read()
                if self.__zip_data is not None:                
                    self._property = {}
                    self._json_data = {}
                    self._latitude = 'NA'
                    self._longitude = 'NA'
                    self._url_to_get = None
                    for obj in json.loads(self.__zip_data):
                        if obj['zip'] == self._zip:
                            self._latitude = obj['latitude']
                            self._longitude = obj['longitude']
                            break
                    if self._longitude != 'NA' and self._latitude != 'NA':
                        url_str1 = "http://forecast.weather.gov/MapClick.php?"
                        url_str2 = "lat={0}&lon={1}&lg=english&FcstType=json"
                        url_str_formatted = url_str2.format(self._latitude, self._longitude)
                        self._url_to_get = url_str1 + url_str_formatted
                    else:
                        raise InvalidZipCode("Invalid Zipcode: " + _zip)
        except InvalidZipCode as error_code:
            print("Error: " + error_code.strerror)

    def get_zip(self):
        '''
        get current zip code
        '''
        return self._zip
    def set_zip(self, _zip):
        '''
        set current zip code
        '''
        self._zip = _zip
    def get_latitude(self):
        '''
        get current latitude
        '''
        return self._latitude
    def get_longitude(self):
        '''
        get current longitude
        '''
        return self._longitude
    def get_weather_data(self):
        '''
        get current weather data
        '''
        try:
            if self._url_to_get is not None:
                http_lib_2 = httplib2.Http(".cache")
            hdrs = {'cache-control':'no-cache'}
            (resp_headers, content) = http_lib_2.request(self._url_to_get, "GET", headers=hdrs)
            if resp_headers['status'] == '200':
                text = content.decode('utf-8')
                self._json_data = json.loads(text)
                start_period_name = self._json_data['time']['startPeriodName']
                self.set_property("start_period_name", start_period_name)
                self.set_property("temperature", self._json_data['data']['temperature'])
                self.set_property("weather", self._json_data['data']['weather'])
                self.set_property("icon_link", self._json_data['data']['iconLink'])
                self.set_property("text", self._json_data['data']['text'])
                self.set_property("id", self._json_data['currentobservation']['id'])
                self.set_property("elev", self._json_data['currentobservation']['elev'])
                self.set_property("Temp", self._json_data['currentobservation']['Temp'])
                self.set_property("Date", self._json_data['currentobservation']['Date'])
                self.set_property("name", self._json_data['currentobservation']['name'])
                self.set_property("Dewp", self._json_data['currentobservation']['Dewp'])
                self.set_property("Relh", self._json_data['currentobservation']['Relh'])
                self.set_property("Winds", self._json_data['currentobservation']['Winds'])
                self.set_property("Windd", self._json_data['currentobservation']['Windd'])
                self.set_property("Gust", self._json_data['currentobservation']['Gust'])
                self.set_property("Weather", self._json_data['currentobservation']['Weather'])
                weather_image = self._json_data['currentobservation']['Weatherimage']
                self.set_property("Weatherimage", weather_image)
                visibility = self._json_data['currentobservation']['Visibility']
                self.set_property("Visibility", visibility)
                self.set_property("Altimeter", self._json_data['currentobservation']['Altimeter'])
                self.set_property("SLP", self._json_data['currentobservation']['SLP'])
                self.set_property("timezone", self._json_data['currentobservation']['timezone'])
                self.set_property("state", self._json_data['currentobservation']['state'])
                self.set_property("WindChill", self._json_data['currentobservation']['WindChill'])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    def set_property(self, key, value):
        '''
        set properties
        '''
        self._property[key] = value

    def get_property(self, key):
        '''
        get property based on key
        '''
        return self._property.get(key)

    def display(self):
        '''
        print data
        '''
        _name_ = self.get_property("name")
        _state_ = self.get_property("state")
        _date_ = self.get_property("Date")
        print("Weather information for {},{} at {}".format(_name_, _state_, _date_))
        print("Humidity: {}%".format(self.get_property("Relh")))
        print("Wind Speed: {} MPH".format(self.get_property("Winds")))
        print("Visibility: {} mi".format(self.get_property("Visibility")))
        if self.get_property("Altimeter") == 'NA':
            print("Barometer: {} in".format(self.get_property("SLP")))
        else:
            _slp_ = self.get_property("SLP")
            _altimeter_ = self.get_property("Altimeter")
            print("Barometer: {} in ({} mb)".format(_slp_, _altimeter_))
        print("Dewpoint: {}F".format(self.get_property("Dewp")))
        print()
        start_period_name = self.get_property("start_period_name")
        index = 0
        for period in start_period_name:
            temperature = self.get_property("temperature")
            weather = self.get_property("weather")
            icon_link = self.get_property("icon_link")
            text = self.get_property("text")
            print("\t{}".format(period))
            print("\t******************************")
            print("\t\tTemperature: {}F".format(temperature[index]))
            print("\t\tConditions: {}".format(weather[index]))
            print("\t\tImage: {}".format(icon_link[index]))
            print("\t\tDescription: {}".format(text[index]))
            print()
            index += 1

    def get_json(self):
        '''
        return json data
        '''
        return self._json_data
def main():

    '''
        testing
    '''
    zipcode = '90210'
    weather_data = WeatherData(zipcode)
    weather_data.get_weather_data()
    weather_data.display()

if __name__ == '__main__':
    main()
