import pygame as py
import requests
import io
from pygame import MOUSEWHEEL

py.init()
py.display.set_caption('Яндекс.Карты')
x, y = 800, 600
screen = py.display.set_mode((x, y))
update_flag = True
ll = [37.617698, 55.755864]
scale, mapZoom, lCount, kToMoveMap = 2.0, 10, 0, 0.002
landArray, ptArray = ['map', 'sat', 'skl', 'trf'], list()
app_mode = 'st'
apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
vision_panel_count = 0


def get_geo(place, postal_code_bullin):
    global ll
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={place}&format=json'
    response = requests.get(geocoder_request)
    if response:
        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_postalcode = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]\
                if postal_code_bullin else '000000'
            ll = [float(toponym_coodrinates.split(' ')[0]), float(toponym_coodrinates.split(' ')[1])]
            full_info = toponym_address, toponym_postalcode, toponym_coodrinates
            return full_info
        except Exception as ex:
            print('!!error!!!', geocoder_request, ex)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def get_image(response):
    """converts requests response to surface"""
    img = io.BytesIO(response.content)
    return py.image.load(img)


def create_base_point(anypm, long, lat):
    if ptArray:
        ptArray.append('~' + str(long) + ',' + str(lat))
    else:
        ptArray.append('&' + anypm + '=' + str(long) + ',' + str(lat))
    print(ptArray, ptArray[-1])


def update(mode, longLat=(37.530887, 55.703118), mapScale=1.0, land='map', zoom=14):
    global update_flag, ptArray
    if update_flag:
        screen.fill((255, 0, 255))
        if mode == 'test':
            map_request = f'https://static-maps.yandex.ru/1.x/?l=map&z={zoom}&pt2'
        else:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}' \
                f'&z={zoom}&pn=0.002,0.002&l={land}' + ','.join(ptArray)
        print(map_request)
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            screen.fill((255, 0, 0))
        if response:
            image = get_image(response)
            screen.blit(py.transform.scale(image, (x, y)), (0, 0))
        py.display.update()
        update_flag = False


class PanelView:
    def __init__(self):
        self.x = x
        self.y = y + y // 6
        self.y_move = y

    def view(self):
        if vision_panel_count % 2 != 0 and self.y_move < self.y:
            self.y_move += 1
        if vision_panel_count % 2 == 0 and self.y_move > y:
            self.y_move -= 1
        py.display.set_mode((x, self.y_move))


panel = PanelView()
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()
        if event.type == py.KEYUP:
            update_flag = True
        if event.type == MOUSEWHEEL:
            mapZoom += event.y if event.y == 1 and mapZoom <= 22 else 0
            mapZoom += event.y if event.y == -1 and 2 <= mapZoom else 0
            py.time.delay(250)
            update_flag = True
        if event.type == py.KEYDOWN:
            py.time.delay(250)
    keys = py.key.get_pressed()
    scale += 0.1 if keys[py.K_PAGEUP] and (scale < 3.9) else 0
    scale -= 0.1 if keys[py.K_PAGEDOWN] and (1.1 < scale) else 0
    if keys[py.K_UP] and ll[1] > 0:
        ll[1] += mapZoom * kToMoveMap
    if keys[py.K_DOWN] and ll[1] < 180:
        ll[1] -= mapZoom * kToMoveMap
    if keys[py.K_LEFT] and ll[0] > 0:
        ll[0] -= (0 + mapZoom) * kToMoveMap
    if keys[py.K_RIGHT] and ll[0] < 360:
        ll[0] += mapZoom * kToMoveMap
    if keys[py.K_w] and mapZoom < 23:
        mapZoom += 1
    if keys[py.K_s] and mapZoom > 0:
        mapZoom -= 1
    if keys[py.K_q]:
        exit()
    if keys[py.K_p] and len(ptArray) < 99:
        create_base_point('pt', ll[0], ll[1])
    if keys[py.K_m]:
        lCount = 0 if lCount == 3 else lCount + 1
    if keys[py.K_f]:
        get_geo(input('~'), False)
    if keys[py.K_d]:
        vision_panel_count += 1
    print(vision_panel_count)
    panel.view()
    update('work', ll, scale, landArray[lCount], mapZoom)
