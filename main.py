import os
import pygame as py
import requests
import io
py.init()
py.display.set_caption('yamaps')
screen = py.display.set_mode((800, 600))
x, y = screen.get_size()
update_flag = True
last = ''
ll = [32.530887, 55.703118]
scale, mapZoom = 2.0, 14
landArray = ['map', 'sat', 'skl', 'trf']
lCount = 0
past = ''


def get_image(response):
    """converts requests response to surface"""
    img = io.BytesIO(response.content)
    return py.image.load(img)


def update(name='map.png', longLat=(37.530887, 55.703118), mapScale=1.0, land='map', zoom=14):
    global update_flag
    if update_flag:
        screen.fill((255, 0, 255))
        if land == 'sat':
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}&z={zoom}&spn=0.002,0.002&l={land}'
        else:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}&z={zoom}&pn=0.002,0.002&l={land}'
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


while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()
        if event.type == py.KEYUP:
            update_flag = True
            py.time.delay(250)
    keys = py.key.get_pressed()
    scale += 0.1 if keys[py.K_PAGEUP] and (scale < 3.9) else 0
    scale -= 0.1 if keys[py.K_PAGEDOWN] and (1.1 < scale) else 0
    if keys[py.K_w] and mapZoom < 23:
        mapZoom += 1
        py.time.delay(250)
    elif keys[py.K_s] and mapZoom > 0:
        mapZoom -= 1
        py.time.delay(250)
    elif keys[py.K_m]:
        lCount = 0 if lCount == 3 else lCount+1
        py.time.delay(250)
    update('map.png', ll, scale, landArray[lCount], mapZoom)
