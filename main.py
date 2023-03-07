import os
import pygame as py
import requests
import io
py.init()
py.display.set_caption('yamaps')
screen = py.display.set_mode((800, 600))
x, y = screen.get_size()
last = ''
update_flag = True


def get_image(response):
    """converts requests response to surface"""
    img = io.BytesIO(response.content)
    return py.image.load(img)

def update2(name='map.png', ll=(37.530887, 55.703118), scale=1.0, l='map'):
    global update_flag
    if update_flag:
        screen.fill((255, 0, 255))
        if l == 'sat':
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(ll[0])},{float(ll[1])}&spn=0.002,0.002&l={l}'
        else:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(ll[0])},{float(ll[1])}&scale={scale}&spn=0.002,0.002&l={l}'
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return None
        map_file = name
        image = get_image(response)
        screen.blit(py.transform.scale(image, (x, y)), (0, 0))
        py.display.update()
        update_flag = False


def update(name='map.png', ll=(37.530887, 55.703118), scale=1.0, l='map'):
    global last
    if name + str(ll[0]) + str(ll[1]) + str(scale) + l != last:
        screen.fill((255, 0, 255))
        if l == 'sat':
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(ll[0])},{float(ll[1])}&spn=0.002,0.002&l={l}'
        else:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(ll[0])},{float(ll[1])}&scale={scale}&spn=0.002,0.002&l={l}'
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        map_file = name
        with open(map_file, 'wb') as file:
            file.write(response.content)
        image = py.image.load(map_file)
        screen.blit(py.transform.scale(image, (x, y)), (0, 0))
        py.display.update()
        os.remove(map_file)
    last = name + str(ll[0]) + str(ll[1]) + str(scale) + l


ll = [37.530887, 55.703118]
scale = 2.0
l = ['map', 'sat', 'skl', 'trf']
lCount = 0
past = ''
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()
        if event.type == py.KEYUP:
            update_flag = True
    keys = py.key.get_pressed()
    scale += 0.1 if keys[py.K_w] and (scale < 3.9) else 0
    scale -= 0.1 if keys[py.K_s] and (1.1 < scale) else 0
    if keys[py.K_m]:
        lCount = 0 if lCount == 3 else lCount+1
        py.time.delay(250)
    update2('map.png', ll, scale, l[lCount])
