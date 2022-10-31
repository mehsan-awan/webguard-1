
import folium
import ipinfo


# res=requests.get('https://ipinfo.io/') #getting requests from the url
# data=res.json() #converting the res file into json
# #print(data) # shows what this data will print
# location=data['loc'].split(',')
from . import views


class ip_based_map:
    def plot_map(self, ip_list):
        access_token = 'bbdd9f7a2a125a'
        handler = ipinfo.getHandler(access_token)
        fg = folium.FeatureGroup("my map")
        map = folium.Map()
        city_list =[]
        # ip_address = '210.56.11.84'
        for ip in ip_list:
            details = handler.getDetails(ip)
            loc = details.loc
            city = details.city + ", " + details.country
            city_list.append(city)
            print(loc)

            lat = loc.split(",")[0]
            log = loc.split(",")[1]

            fg.add_child(folium.Marker(location=[lat, log], popup=city))

            map = folium.Map(location=[51.249, -2.8610], zoom_start=2)

            map.add_child(fg)
        # if Funtions.GetEnvironmentType() == Funtions.Environment.Production.name:
        #     path = os.getcwd() + "/UI/app/home/templates/location.html"
        # else:
        #     path = os.getcwd() + "/app/home/templates/location.html"
        path = views.GetBasePath() + "templates/location.html"
        map.save(path)
        return city_list
        # the location format is loc[ latitude, longitude]. So we created 2 separated
        # variables to capture those values

        # folium is a base map framework which can create coordinates and show data related to the locations

        # featureGroup

        # fg = folium.FeatureGroup("my map")
        # fg.add_child(folium.GeoJson(data=(
        #     open('/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/app/home/Brazil-states.json', 'r',
        #          encoding='utf-8-sig').read())))
        #
        # fg.add_child(folium.Marker(location=[lat, log], popup=city))
        #
        # map = folium.Map(location=[lat, log], zoom_start=6)
        #
        # map.add_child(fg)
        # map.save("/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/app/home/templates/location.html")


if __name__ == '__main__':
    ip_map = ip_based_map()
    ip_map.plot_map(["151.101.2.216"])
