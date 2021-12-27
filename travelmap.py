import folium
import pandas
import json

data = pandas.read_csv("geziler.txt")
sehir = list(data["SEHIR"])
isim = list(data["ISIM"])
ay = list(data["AY"])
yil = list(data["YIL"])
foto= list(data["FOTO"])
lattitude=list(data["LAT"])
longitude=list(data["LON"])

html = """
Yer:%s <br>
<a href="%s" target="_blank">foto</a> <br>
Ay: %s <br>
Yıl: %s <br>
"""
def colorproducer(yil):
    if yil==2020:
        return 'green'
    else:
        return 'pink'

map = folium.Map(location=[39.92, 32.86], zoom_start=5, tiles="cartodbpositron")
fgm=folium.FeatureGroup(name="Anılar")

for ism, a, yl, fot, lt, ln in zip(isim, ay, yil, foto, lattitude, longitude):
    iframe = folium.IFrame(html=html % (ism, fot, a, yl), width=200, height=100)
    fgm.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(colorproducer(yl))))


fgc=folium.FeatureGroup(name = "Gittiğimiz Şehirler")
fgc.add_child(folium.GeoJson(data=(open('cities.json','r', encoding='utf-8-sig').read()),
style_function=lambda x:{'fillColor':'blue' if sehir.__contains__(x['properties']['name']) else 'white'}))

map.add_child(fgc)
map.add_child(fgm)
map.add_child(folium.LayerControl())

map.save("Travelmap.html")
