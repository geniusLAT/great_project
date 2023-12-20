#!/usr/bin/python 
#pip install osmnx
print("map - ok")

import requests



def get_data(cmd):
    URL='https://maps.mail.ru/osm/tools/overpass/api/interpreter?data='+cmd
    data = requests.get(URL)
    return (data.text)
#node[shop][name="Дикси"](55.7263,37.6503,55.7816,37.7864);out;
cmd='node[building](55.7263,37.6503,55.7816,37.7864);out;'

cmd='''[out:json][timeout:25];
(               // radius, lat, lon
node["building"](around:700.0, 56.843396, 60.650773);
way["building"](around:700.0, 56.843396, 60.650773);
relation["building"](around:700.0, 56.843396, 60.650773);
);
out body;
>;
out skel qt;'''

def get_places(lat,lon,radius):
    t=str(radius)+', '+str(lat)+', '+str(lon)

    cmd='''[out:json][timeout:25];
(               // radius, lat, lon
node["building"](around:'''+t+''');
way["building"](around:'''+t+''');
relation["building"](around:'''+t+''');
);
out body;
>;
out skel qt;'''

    #print(cmd)
    data=  get_data(cmd)
    #print(data)

    return data

#w=get_data(cmd)
#print(w)


def parse_tag(tag):
    result=''
    try:
        housenumber = tag.split('housenumber":')[1]
        housenumber=housenumber.split('\n')[0]
        housenumber= housenumber.replace(',','').replace('"','')
        #print(housenumber)
        result=' '+housenumber
    except:
        pass
    try:
        street = tag.split('street":')[1]
        street=street.split('\n')[0]
        street= street.replace(',','').replace('"','')
        #print(street)
        result=street+result
    except:
        pass
    try:
        name = tag.split('name":')[1]
        name=name.split('\n')[0]
        name= name.replace(',','').replace('"','')
        #print(name)
        result=name+", "+result
    except:
        pass
    print(result)
    return result


def get_nameful_array(lat,lon):
    w = get_places( lat, lon,1000)

    tags_array= w.split('"tags": {')

    tags=[]
    for tag in tags_array:
        parts=tag.split('}')
        tags.append(parts[0])


    importants=[]
    for tag in tags:
        if ('housenumber'  in tag) and ('street'  in tag)and ('name'  in tag):
            importants.append(tag)
            
    

    for tag in importants:
        print(tag)
        print('-------------------------------')

    result =''
    for tag in importants:
        result +=parse_tag(tag)+'\n'
    return result
    lines=w.split('\n')




    for line in lines:
        if 'name' in line:
            #print(line)
            w=w.replace(line,line+'✅')

#print(w)

#file= open('map.txt','w')
#file.write(w)

#for letter in w:
#    try:
#        file.write(letter)
#    except:
#        pass
            

#w = get_nameful_array( 56.843396, 60.650773)