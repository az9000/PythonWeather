'''
Created on Jan 2, 2018

@author: Fawzi
'''
from weather import WeatherData

def main():
    '''
        testing
    '''
    zipcode = input("Enter zip code: ")
    weather_data = WeatherData(zipcode)
    weather_data.get_weather_data()
    weather_data.display()


if __name__ == '__main__':
    main()
