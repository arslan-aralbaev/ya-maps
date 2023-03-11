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
scale, mapZoom = 2.0, 15
landArray = ['map', 'sat', 'skl', 'trf']
pmArray = list()
lCount = 0
past = ''
kToMoveMap = 0.002


def get_image(response):
    """converts requests response to surface"""
    img = io.BytesIO(response.content)
    return py.image.load(img)


def create_base_point(anypm, long, lat):
    if pmArray:
        pmArray.append('~' + str(long) + ',' + str(lat))
    else:
        pmArray.append('&' + anypm + '=' + str(long) + ',' + str(lat))
    print(pmArray, pmArray[-1])


def update(mode, name='map.png', longLat=(37.530887, 55.703118), mapScale=1.0, land='map', zoom=14):
    global update_flag, pmArray
    if update_flag:
        screen.fill((255, 0, 255))
        if mode == 'test':
            map_request = f'https://static-maps.yandex.ru/1.x/?l=map&z={zoom}&pt2'
        elif land == 'saat':
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}' \
                f'&z={zoom}&spn=0.002,0.002&l={land}'
        else:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}' \
                f'&z={zoom}&pn=0.002,0.002&l={land}' + ','.join(pmArray)
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
    if keys[py.K_UP] and ll[1] > 0:
        ll[1] += mapZoom * kToMoveMap
        py.time.delay(250)
    if keys[py.K_DOWN] and ll[1] < 180:
        ll[1] -= mapZoom * kToMoveMap
        py.time.delay(250)
    if keys[py.K_LEFT] and ll[0] > 0:
        ll[0] -= (0 + mapZoom) * kToMoveMap
        py.time.delay(250)
    if keys[py.K_RIGHT] and ll[0] < 360:
        ll[0] += mapZoom * kToMoveMap
        py.time.delay(250)
    if keys[py.K_w] and mapZoom < 23:
        mapZoom += 1
        py.time.delay(250)
    if keys[py.K_s] and mapZoom > 0:
        mapZoom -= 1
        py.time.delay(250)
    if keys[py.K_q]:
        exit()
    if keys[py.K_p] and len(pmArray) < 99:
        create_base_point('pt', ll[0], ll[1])
        print('key_down')
        py.time.delay(250)
    if keys[py.K_m]:
        lCount = 0 if lCount == 3 else lCount+1
        py.time.delay(250)
    update('work', 'map.png', ll, scale, landArray[lCount], mapZoom)
