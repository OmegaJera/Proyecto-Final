import board
import busio
import displayio
import terminalio
import random
import time
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

import pwmio
import digitalio
from adafruit_ov7670 import (OV7670, OV7670_SIZE_DIV16, OV7670_COLOR_YUV)


# Configuración de los pines del carrito
m11 = digitalio.DigitalInOut(board.GP16)
m11.direction = digitalio.Direction.OUTPUT
m12 = digitalio.DigitalInOut(board.GP17)
m12.direction = digitalio.Direction.OUTPUT
m21 = digitalio.DigitalInOut(board.GP10)
m21.direction = digitalio.Direction.OUTPUT
m22 = digitalio.DigitalInOut(board.GP11)
m22.direction = digitalio.Direction.OUTPUT

# Configuración de la cámara
cam_bus = busio.I2C(board.GP19, board.GP18)
cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,  # Cambiado de GP0 a GP10
        board.GP1,  # Cambiado de GP1 a GP11
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP9,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP8,
    shutdown=board.GP15,
    reset=board.GP14,
)

cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = False

# Configuración de PWM para controlar la velocidad del carrito
pwm = pwmio.PWMOut(board.GP22, frequency=100, duty_cycle=0)


# Liberar recursos del display (Optional)
displayio.release_displays()

SCL, SDA = board.GP21, board.GP20
# Configure the I2C pins for communication with the OLED display
i2c = busio.I2C(SCL, SDA)

# Configurar el bus de display y la dirección de la pantalla OLED (0x3C es común)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Configurar el display SSD1306 con dimensiones 128x64
WIDTH = 128
HEIGHT = 64
display = SSD1306(display_bus, width=WIDTH, height=HEIGHT)

def imprimir1(text,x,y):
    
    # Crear el grupo de display
    splash = displayio.Group()
    display.root_group = splash 

    # Crear el fondo y color del rectángulo
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Negro

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Crear un texto
    text = text
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y)
    splash.append(text_area)

def imprimir2(text,x,y):
    
    # Crear el grupo de display
    splash = displayio.Group()
    display.root_group = splash 

    # Crear el fondo y color del rectángulo
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Negro

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    text = text
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y-10)
    splash.append(text_area)
    
def imprimir(text,text_2,x,y):
    
    # Crear el grupo de display
    splash = displayio.Group()
    display.root_group = splash 

    # Crear el fondo y color del rectángulo
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Negro

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Crear un texto
    text = text
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y)
    splash.append(text_area)
    
    text = text_2
    text_area_2 = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y-10)
    splash.append(text_area_2)
def imprimir3(text,text_2,text_3,x,y):
    
    # Crear el grupo de display
    splash = displayio.Group()
    display.root_group = splash 

    # Crear el fondo y color del rectángulo
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Negro

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Crear un texto
    text = text
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y)
    splash.append(text_area)
    
    text = text_2
    text_area_2 = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y+10)
    splash.append(text_area_2)
    
    text = text_3
    text_area_3 = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y+20)
    splash.append(text_area_3)
# Función para detener el carrito
def detener_carrito():
    m11.value = False
    m12.value = False
    m21.value = False
    m22.value = False

# Función para mover el carrito hacia adelante
def mover_adelante():
    m11.value = True
    m12.value = False
    m21.value = True
    m22.value = False

# Función para mover el carrito hacia atrás
def mover_atras():
    m11.value = False
    m12.value = True
    m21.value = False
    m22.value = True

# Función para girar el carrito a la izquierda
def girar_izquierda():
    m11.value = True
    m12.value = False
    m21.value = False
    m22.value = False

# Función para girar el carrito a la derecha
def girar_derecha():
    m11.value = False
    m12.value = False
    m21.value = True
    m22.value = False

# Búfer para capturar imágenes de la cámara
buf = bytearray(2 * cam.width * cam.height)



while True:
    
    cam.capture(buf)
    matrix = []
    for j in range(cam.height):
        row = []
        for i in range(cam.width):
            
            if ((buf[2 * (cam.width * j + i)]*10//255)<5):
                intensity="0"
            else:
                intensity="-"
            #intensity = "0" if buf[2 * (cam.width * j + i)] * 10 // 255 < 5 else "-"
            row.append(intensity)
            print(intensity, end=' ')
#            print(buf[2 * (cam.width * j + i)]*10)
            
            
        matrix.append(row)
        print()
    print()
    aplanado = [elemento for fila in matrix for elemento in fila]
   # print(aplanado)
    #print(cam.height,cam.width)

    # Procesar la última línea de la imagen para determinar la dirección
    ulinea = matrix[-1][:]
    suma = 0
    contador = 0
    for i in range(len(ulinea)):
        if ulinea[i] == "0":
            suma += i
            contador += 1

    promedio = suma / contador if contador != 0 else 0
    diferencia = (20 - promedio) * (100 / 20) if promedio != 0 else 100
    diferencia = (diferencia / 2) + 50


    print(f'Diferencia: {diferencia}')
    
    if diferencia > 60:
        girar_derecha()
        speed_1=random.randint(20,120)
        ruedader=0
        imprimir("Rueda derecha:"+str(ruedader),"Rueda izq:"+str(speed_1),25,30)
        
    elif diferencia < 40:
        girar_izquierda()
        speed_2=random.randint(20,120)
        ruedaizq=0
        imprimir("Rueda derecha:"+str(speed_2),"Rueda izq:"+str(ruedaizq),25,30)
    else:
        mover_adelante()
        speed_2=random.randint(20,120)
        imprimir("Rueda derecha:"+str(speed_2),"Rueda izq:"+str(speed_2),25,30)

    

 

        
    time.sleep(0.01)
