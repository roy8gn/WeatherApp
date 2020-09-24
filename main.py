from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO


def display_icon(icon):


    url = 'http://openweathermap.org/img/wn/'+icon+'@2x.png'
    response = requests.get(url)

    size = int(lowerFrame.winfo_height() * 0.25)
    icon_image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0, 0, anchor='nw', image=icon_image)
    weather_icon.image = icon_image


def arrange_weather_text(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temperature = weather['main']['temp']
        feels_like = weather['main']['feels_like']
        humidity = weather['main']['humidity']

        weather_str = "City: {} \nDescription: {} \nTemperature: {}°C\nFeels like: {}°C\nHumidity: {}%".\
            format(name, desc, temperature, feels_like, humidity)

    except:
        weather_str = '''Couldn't find the city.'''
    return weather_str


def get_weather(input1):
    key = 'b60f96801f0d0804c2f021bccfa05a64'
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'appid': key, 'q': input1, 'units': 'metric'}
    response = requests.get(url, params=params)
    weather = response.json()

    label['text'] = arrange_weather_text(weather)
    try:
        icon = weather['weather'][0]['icon']
        display_icon(icon)
    except:
        weather_icon.delete("all")

HEIGHT = 400
WIDTH = 500
backgroundColor = "#004d80"
borderColor = '#ffffff'

root = Tk()
root.title("Weather")

canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

backgroundImage = PhotoImage(file='./images/weather.png')
background1 = Label(root, image=backgroundImage)
background1.place(relwidth=1, relheight=1)

frame = Frame(root, bg=borderColor, bd=2)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

text = Entry(frame, font=('Corbel', 14))
text.place(relwidth=0.65, relheight=1)

img = Image.open('./images/search_button.png')
img = img.resize((124, 41), Image.ANTIALIAS)
photoImg = ImageTk.PhotoImage(img)
button = Button(frame, image=photoImg, relief=RAISED,
                command=lambda: get_weather(text.get()))

button.place(relx=0.7, relwidth=0.3, relheight=1)

lowerFrame = Frame(root, bg=borderColor, bd=2)
lowerFrame.place(relx=0.5, rely=0.25, relheight=0.6, relwidth=0.75, anchor='n')

label = Label(lowerFrame, bg='#ccebff', anchor='nw', justify='left', font=('Corbel', 14))
label.place(relwidth=1, relheight=1)

weather_icon = Canvas(label, bg='#ccebff', bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

root.mainloop()
