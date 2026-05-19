#region Imports
import tkinter as tk
from tkinter import filedialog, Listbox, Image

import requests

import json
#endregion

#region Weather App
#region ================== GEOCODING API ==================
class LocationEntry:
    def __init__(self, location):
        self.location = location
        self.latitude = None
        self.longitude = None
        self.city_name = None

    def fetch_location(self):
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": self.location,
            "count": 1
        }

        geo_data = requests.get(geo_url, params=geo_params).json()

        if "results" not in geo_data:
            return False

        result = geo_data["results"][0]

        self.latitude = result["latitude"]
        self.longitude = result["longitude"]
        self.city_name = result["name"]

        return True

def submitLocation():
    global currentWeather
    global currentLocation

    city = getLocationTextBox.get()

    location = LocationEntry(city)

    if location.fetch_location():
        currentLocation = location

        currentWeather = WeatherAPP(location)

        updateWeatherScreen()

        openWeatherScreen()

    else:
        openWeatherGetLocationFailed()


#endregion

#region ================== Weather API ==================
class WeatherAPP:
    def __init__(self, location):
        self.location = location
        self.latitude = location.latitude
        self.longitude = location.longitude

        self.weather_data = self.fetch_weather_data()

    def fetch_weather_data(self):
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": self.latitude,
            "longitude": self.longitude,

            "timezone": "auto",

            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "weather_code",
                "wind_speed_10m",
                "precipitation_probability"
            ],

            "hourly": [
                "temperature_2m"
            ],

            "forecast_hours": 5
        }
        return requests.get(weather_url, params=weather_params).json()

    def getWeather(self):
        weather_code = self.weather_data["current"]["weather_code"]

        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm"
        }

        return weather_codes.get(weather_code, "Unknown")

    def getCurrentTime(self):
        return self.weather_data["current"]["time"]

    def getCurrentTemp(self):
        return self.weather_data["current"]["temperature_2m"]

    def getHumidity(self):
        return self.weather_data["current"]["relative_humidity_2m"]

    def getWindSpeed(self):
        return self.weather_data["current"]["wind_speed_10m"]

    def getCurrentRainChance(self):
        return self.weather_data["current"]["precipitation_probability"]

    def getFutureTemp(self):
        times = self.weather_data["hourly"]["time"]
        temps = self.weather_data["hourly"]["temperature_2m"]

        futureTemps = []

        for i in range(1, 5):
            futureTemps.append({
                "time": times[i],
                "temp": temps[i]
            })

        return futureTemps

#endregion

#endregion

#region Text writer App
def saveTextFile():
            filePath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")]
            )

            if not filePath:
                return

            content = textEditor.get("1.0", tk.END)

            with open(filePath, "w") as file:
                file.write(content)

def openTextFile():
            filePath = filedialog.askopenfilename(
                filetypes=[("Text Files", "*.txt")]
            )

            if not filePath:
                return

            with open(filePath, "r") as file:
                content = file.read()

            textEditor.delete("1.0", tk.END)
            textEditor.insert("1.0", content)
#endregion

#region Settings
class SettingsEntry:
    def __init__(self):
        self.currentTheme = "Light"
        self.currentTempUnit = "C"
        self.currentSpeedUnit = "Km/h"
        self.currentTimeUnit = 12

    def to_dict(self):
        return {
            "currentTheme": self.currentTheme,
            "currentTempUnit": self.currentTempUnit,
            "currentSpeedUnit": self.currentSpeedUnit,
            "currentTimeUnit": self.currentTimeUnit
        }

class SettingsTracker:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.load()

    def add_entry(self, entry):
        self.entries.append(entry)
        self.save()

    def save(self):
        with open(self.filename, "w") as file:
            json.dump([e.to_dict() for e in self.entries], file, indent=4)

    def load(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.entries = [SettingsEntry(**d) for d in data]
        except FileNotFoundError:
            self.entries = []
#endregion

#region GUI
#region ================== WINDOW ==================
root = tk.Tk()
root.title("Test")
root.geometry("1000x650")
root.configure(bg="black")

HEIGHT = 650
WIDTH = 1000

BAR_HEIGHT = 60
BAR_WIDTH = 600

#endregion

#region ================== THEME ==================
APP_BG = "white"
APP_FG = "#333"
ACCENT = "#333"
SOFT_BG = "#f2f2f2"
LINE_BG = "#eaeaea"
#endregion

#region ================== TASKBAR ==================
taskbar = tk.Frame(root, bg="gray")

# Inner frame for padding
inner_frame = tk.Frame(taskbar, bg="gray")
inner_frame.pack(fill="both", expand=True, padx=10, pady=10)
#endregion

# region ================== APP SCREENS ==================
def center_screen(frame):
    hide_all_screens()
    frame.place(x=0, y=0, relwidth=1, relheight=1)
    taskbar.lift()

def openWeatherGetLocation():
    center_screen(weatherGetLocation)

def openWeatherScreen():
    center_screen(weatherScreen)

def openWeatherGetLocationFailed():
    center_screen(weatherGetLocationFailed)

def opentextWriterScreen():
    center_screen(textWriterScreen)

def openSettingsScreen():
    center_screen(settingsScreen)

def hide_all_screens():
    weatherGetLocation.place_forget()
    weatherGetLocationFailed.place_forget()
    weatherScreen.place_forget()
    musicScreen.place_forget()
    textWriterScreen.place_forget()
    settingsScreen.place_forget()

def updateWeatherScreen():
    weatherScreenLocationName.config(
        text=currentLocation.city_name
    )

    weatherScreenCurrTemp.config(
        text=f"{currentWeather.getCurrentTemp()}°C"
    )

    weatherScreenWeather.config(
        text=f"{currentWeather.getWeather()}"
    )

    weatherScreenHumidity.config(
        text=f"Humidity: \n{currentWeather.getHumidity()}%"
    )

    weatherScreenRainChance.config(
        text=f"Rain Chance: \n{currentWeather.getCurrentRainChance()}%"
    )

    weatherScreenWindSpeed.config(
        text=f"Wind Speed: \n{currentWeather.getWindSpeed()} km/h"
    )
    futureTemps = currentWeather.getFutureTemp()

    cards = [card1, card2, card3, card4]

    for i, cardObj in enumerate(cards):
        cardObj.timeLabel.config(
            text=futureTemps[i]["time"][11:16]
        )

        cardObj.tempLabel.config(
            text=f"{futureTemps[i]['temp']}°C"
        )

    cardNow.timeLabel.config(text="Now")

    cardNow.tempLabel.config(
        text=f"{currentWeather.getCurrentTemp()}°C"
    )
#endregion

#region ================== Weather App ==================
weatherGetLocation = tk.Frame(root, bg="white", width=WIDTH, height=HEIGHT)

#region ================== Get Location Widgets ==================
getLocationCenterFrame = tk.Frame(
    weatherGetLocation,
    bg="white"
)

getLocationTextLabel = tk.Label(getLocationCenterFrame, text="Enter a location", bg="white", fg="#333", font=("Arial", 20))

getLocationTextBox = tk.Entry(
    getLocationCenterFrame,
    font=("Arial", 20),
    bg="white",
    fg="#333",
    width=25
)
getLocationTextBtn = tk.Button(
    getLocationCenterFrame,
    font=("Arial", 20),
    bg="#333",
    fg="white",
    text="Go",
    padx=10,
    bd=0,
    command=submitLocation
)


getLocationCenterFrame.place(relx=0.5, rely=0.5, anchor="center")
getLocationTextLabel.pack(side="top", anchor="center")
getLocationTextBox.pack(side="left", padx=10)
getLocationTextBtn.pack(side="left", ipady=3)
#endregion

weatherScreen = tk.Frame(root, bg="white", width=WIDTH, height=HEIGHT)

#region ================== Weather Screen Widgets ==================
#region Icons
humidityIcon = tk.PhotoImage(
    file="Icons/Weather/humidity_percentage.png"
).subsample(2, 2)

rainIcon = tk.PhotoImage(
    file="Icons/Weather/rain_chance.png"
).subsample(2, 2)

windIcon = tk.PhotoImage(
    file="Icons/Weather/wind_speed.png"
).subsample(2, 2)
#endregion

#region top left
weatherScreenTopLeftFrame = tk.Frame(
    weatherScreen,
    bg="white",
)

weatherScreenCurrTemp = tk.Label(
    weatherScreenTopLeftFrame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#333"
)

weatherScreenWeather = tk.Label(
    weatherScreenTopLeftFrame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#333"
)

weatherScreenTopLeftFrame.place(
    relx=0.01,
    rely=0.01,
    anchor="nw"
)
weatherScreenCurrTemp.pack(side="top", anchor="w")
weatherScreenWeather.pack(side="top", anchor="w")
#endregion

#region top right
weatherScreenTopRightFrame = tk.Frame(
    weatherScreen,
    bg="white",
)

# ================== HUMIDITY ==================
humidityFrame = tk.Frame(
    weatherScreenTopRightFrame,
    bg="white"
)

humidityIconLabel = tk.Label(
    humidityFrame,
    image=humidityIcon,
    bg="white"
)

weatherScreenHumidity = tk.Label(
    humidityFrame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#333",
    justify="left"
)

humidityIconLabel.pack(side="left", padx=(0, 5))
weatherScreenHumidity.pack(side="left")

# ================== RAIN ==================
rainFrame = tk.Frame(
    weatherScreenTopRightFrame,
    bg="white"
)

rainIconLabel = tk.Label(
    rainFrame,
    image=rainIcon,
    bg="white"
)

weatherScreenRainChance = tk.Label(
    rainFrame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#333",
    justify="left"
)

rainIconLabel.pack(side="left", padx=(0, 5))
weatherScreenRainChance.pack(side="left")

# ================== WIND ==================
windFrame = tk.Frame(
    weatherScreenTopRightFrame,
    bg="white"
)

windIconLabel = tk.Label(
    windFrame,
    image=windIcon,
    bg="white"
)

weatherScreenWindSpeed = tk.Label(
    windFrame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#333",
    justify="left"
)

windIconLabel.pack(side="left", padx=(0, 5))
weatherScreenWindSpeed.pack(side="left")

# ================== POSITION ==================
weatherScreenTopRightFrame.place(
    relx=0.99,
    rely=0.01,
    anchor="ne"
)

humidityFrame.pack(anchor="e", pady=2)
rainFrame.pack(anchor="e", pady=2)
windFrame.pack(anchor="e", pady=2)

#endregion

#region top middle
weatherScreenTopMiddleFrame = tk.Frame(
    weatherScreen,
    bg="white",
)

weatherScreenLocationName = tk.Button(
    weatherScreenTopMiddleFrame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#333",
    command=openWeatherGetLocation
)

weatherScreenTopMiddleFrame.place(
    relx=0.5,
    rely=0.02,
    anchor="center"
)
weatherScreenLocationName.pack(side="top", anchor="n")
#endregion

#region bottom middle
class card:
    def __init__(self, time, temp, color):
        self.time = time
        self.temp = temp
        self.color = color

        self.timeLabel = None
        self.tempLabel = None

    def getCard(self):
        self.frame = tk.Frame(
            weatherScreenBottomMiddleFrame,
            bg=self.color,
            width=120,
            height=160
        )

        self.frame.pack_propagate(False)

        self.timeLabel = tk.Label(
            self.frame,
            text=self.time,
            font=("Arial", 12, "bold"),
            bg=self.color,
            fg="#333"
        )

        self.tempLabel = tk.Label(
            self.frame,
            text=self.temp,
            font=("Arial", 22),
            bg=self.color,
            fg="#333"
        )

        self.timeLabel.pack(pady=(35, 10))
        self.tempLabel.pack()

        return self.frame

#region frame
weatherScreenBottomMiddleFrame = tk.Frame(
    weatherScreen,
    bg="black",
    width=700,
    height=180
)
weatherScreenBottomMiddleFrame.pack_propagate(False)

cardNow = card("", "", "white")
card1 = card("", "", "grey")
card2 = card("", "", "white")
card3 = card("", "", "grey")
card4 = card("", "", "white")

weatherScreenBottomMiddleFrame.place(
    relx=0.5,
    rely=0.72,
    anchor="center"
)
hourTable = [cardNow, card1, card2, card3, card4]
for i, card in enumerate(hourTable):
    cardWidget = card.getCard()

    cardWidget.grid(
        row=0,
        column=i,
        padx=1,
        pady=1,
        sticky="nsew"
    )

    weatherScreenBottomMiddleFrame.grid_columnconfigure(i, weight=1)

#endregion

#endregion

weatherGetLocationFailed = tk.Frame(root, bg="white", width=WIDTH, height=HEIGHT)

#region ================== Get Location Failed Widgets ==================
locationFailedCenterFrame = tk.Frame(
    weatherGetLocationFailed,
    bg="white"
)

locationFailedTextLabel = tk.Label(
    locationFailedCenterFrame,
    text="Location not found",
    bg="white",
    fg="#333",
    font=("Arial", 20)
)


locationFailedConfirmBtn = tk.Button(
    locationFailedCenterFrame,
    font=("Arial", 20),
    bg="#333",
    fg="white",
    text="Ok",
    padx=10,
    bd=0,
    command=openWeatherGetLocation
)

locationFailedCenterFrame.place(relx=0.5, rely=0.5, anchor="center")

locationFailedTextLabel.pack(pady=10)
locationFailedConfirmBtn.pack()
#endregion

#endregion


musicScreen = tk.Frame(root, bg="green", width=WIDTH, height=HEIGHT)
textWriterScreen = tk.Frame(root, bg="red", width=WIDTH, height=HEIGHT)
settingsScreen = tk.Frame(root, bg="yellow", width=WIDTH, height=HEIGHT)

# endregion

#region ================== Text Writer App ==================
# ================== UI FRAME ==================

textWriterScreen = tk.Frame(root, bg=APP_BG, width=WIDTH, height=HEIGHT)

# Editor panel container (matches weather card style)
editorContainer = tk.Frame(
    textWriterScreen,
    bg="#e6e6e6",
    highlightbackground="#cfcfcf",
    highlightthickness=2,
    bd=0
)
editorContainer.place(relx=0.5, rely=0.45, anchor="center", width=900, height=520)

# ================== LINE NUMBERS ==================

lineNumbers = tk.Text(
    editorContainer,
    width=4,
    font=("Consolas", 14),
    bg="#e6e6e6",
    fg="#555",
    padx=6,
    takefocus=0,
    state="disabled",
    bd=0
)
lineNumbers.pack(side="left", fill="y")

# ================== TEXT EDITOR ==================

textEditor = tk.Text(
    editorContainer,
    font=("Consolas", 16),
    wrap="none",
    undo=True,
    bg="white",
    fg="#222",
    insertbackground="#333",
    bd=0,
    padx=10,
    pady=10
)
textEditor.pack(side="right", fill="both", expand=True)

# highlight style (Weather-like soft gray)
textEditor.tag_configure("current_line", background="#f3f3f3")

# ================== BUTTON BAR ==================

buttonBar = tk.Frame(textWriterScreen, bg="white")
buttonBar.place(relx=0.5, rely=0.89, anchor="center")

openBtn = tk.Button(
    buttonBar,
    text="Open",
    bg="#333",
    fg="white",
    bd=0,
    padx=15,
    pady=5,
    command=openTextFile
)

saveBtn = tk.Button(
    buttonBar,
    text="Save",
    bg="#333",
    fg="white",
    bd=0,
    padx=15,
    pady=5,
    command=saveTextFile
)

openBtn.pack(side="left", padx=10)
saveBtn.pack(side="left", padx=10)

# ================== EVENTS ==================
textEditor.config(yscrollcommand=lambda *args: None)
#endregion

#region ================== Settings ==================

settingsScreen = tk.Frame(root, bg=APP_BG, width=WIDTH, height=HEIGHT)

# ================== LEFT SIDEBAR ==================

settingsSidebar = tk.Frame(
    settingsScreen,
    bg="#e6e6e6",
    width=220,
    height=HEIGHT
)
settingsSidebar.pack(side="left", fill="y")
settingsSidebar.pack_propagate(False)

settingsTitle = tk.Label(
    settingsSidebar,
    text="Settings",
    font=("Arial", 22, "bold"),
    bg="#e6e6e6",
    fg="#333"
)
settingsTitle.pack(pady=(30, 20))

# ================== CONTENT AREA ==================

settingsContent = tk.Frame(
    settingsScreen,
    bg="white"
)
settingsContent.pack(side="right", fill="both", expand=True)

# ================== SCREENS ==================

themeScreen = tk.Frame(settingsContent, bg="white")
unitsScreen = tk.Frame(settingsContent, bg="white")
readMeScreen = tk.Frame(settingsContent, bg="white")
creditsScreen = tk.Frame(settingsContent, bg="white")

allSettingScreens = [
    themeScreen,
    unitsScreen,
    readMeScreen,
    creditsScreen
]

def openSettingPage(frame):
    for screen in allSettingScreens:
        screen.place_forget()

    frame.place(relwidth=1, relheight=1)

# ================== SIDEBAR BUTTONS ==================

themeBtn = tk.Button(
    settingsSidebar,
    text="Theme",
    font=("Arial", 16),
    bg="#333",
    fg="white",
    bd=0,
    pady=10,
    command=lambda: openSettingPage(themeScreen)
)

unitsBtn = tk.Button(
    settingsSidebar,
    text="Units",
    font=("Arial", 16),
    bg="#333",
    fg="white",
    bd=0,
    pady=10,
    command=lambda: openSettingPage(unitsScreen)
)

readMeBtn = tk.Button(
    settingsSidebar,
    text="Read Me",
    font=("Arial", 16),
    bg="#333",
    fg="white",
    bd=0,
    pady=10,
    command=lambda: openSettingPage(readMeScreen)
)

creditsBtn = tk.Button(
    settingsSidebar,
    text="Credits",
    font=("Arial", 16),
    bg="#333",
    fg="white",
    bd=0,
    pady=10,
    command=lambda: openSettingPage(creditsScreen)
)

sidebarButtons = [
    themeBtn,
    unitsBtn,
    readMeBtn,
    creditsBtn
]

# ================== THEME SCREEN ==================

themeTitle = tk.Label(
    themeScreen,
    text="Themes",
    font=("Arial", 26, "bold"),
    bg="white",
    fg="#333"
)
themeTitle.pack(pady=20)

themeContainer = tk.Frame(
    themeScreen,
    bg="white"
)
themeContainer.pack(pady=20)

def setTheme(theme):
    global APP_BG
    global APP_FG

    if theme == "Light":
        APP_BG = "white"
        APP_FG = "#333"

        root.configure(bg="white")

    elif theme == "Dark":
        APP_BG = "#1e1e1e"
        APP_FG = "white"

        root.configure(bg="#1e1e1e")

lightThemeCard = tk.Frame(
    themeContainer,
    bg="#f5f5f5",
    width=180,
    height=220,
    highlightbackground="#ccc",
    highlightthickness=2
)

darkThemeCard = tk.Frame(
    themeContainer,
    bg="#222",
    width=180,
    height=220,
    highlightbackground="#444",
    highlightthickness=2
)

lightThemeCard.pack(side="left", padx=25)
darkThemeCard.pack(side="left", padx=25)

lightThemeCard.pack_propagate(False)
darkThemeCard.pack_propagate(False)

lightThemeLabel = tk.Label(
    lightThemeCard,
    text="Light",
    font=("Arial", 18, "bold"),
    bg="#f5f5f5",
    fg="#333"
)
lightThemeLabel.pack(pady=20)

darkThemeLabel = tk.Label(
    darkThemeCard,
    text="Dark",
    font=("Arial", 18, "bold"),
    bg="#222",
    fg="white"
)
darkThemeLabel.pack(pady=20)

lightThemeBtn = tk.Button(
    lightThemeCard,
    text="Apply",
    font=("Arial", 14),
    bg="#333",
    fg="white",
    bd=0,
    padx=15,
    pady=5,
    command=lambda: setTheme("Light")
)
lightThemeBtn.pack(side="bottom", pady=20)

darkThemeBtn = tk.Button(
    darkThemeCard,
    text="Apply",
    font=("Arial", 14),
    bg="white",
    fg="#333",
    bd=0,
    padx=15,
    pady=5,
    command=lambda: setTheme("Dark")
)
darkThemeBtn.pack(side="bottom", pady=20)

# ================== UNITS SCREEN ==================

unitsTitle = tk.Label(
    unitsScreen,
    text="Units",
    font=("Arial", 26, "bold"),
    bg="white",
    fg="#333"
)
unitsTitle.pack(pady=20)

unitsContainer = tk.Frame(
    unitsScreen,
    bg="white"
)
unitsContainer.pack(pady=20)

# TEMP UNIT

tempLabel = tk.Label(
    unitsContainer,
    text="Temperature Unit",
    font=("Arial", 16),
    bg="white",
    fg="#333"
)
tempLabel.grid(row=0, column=0, padx=20, pady=20, sticky="w")

tempVar = tk.StringVar(value="C")

tempCBtn = tk.Radiobutton(
    unitsContainer,
    text="Celsius",
    variable=tempVar,
    value="C",
    bg="white",
    font=("Arial", 14)
)
tempFBtn = tk.Radiobutton(
    unitsContainer,
    text="Fahrenheit",
    variable=tempVar,
    value="F",
    bg="white",
    font=("Arial", 14)
)

tempCBtn.grid(row=0, column=1, padx=10)
tempFBtn.grid(row=0, column=2, padx=10)

# SPEED UNIT

speedLabel = tk.Label(
    unitsContainer,
    text="Speed Unit",
    font=("Arial", 16),
    bg="white",
    fg="#333"
)
speedLabel.grid(row=1, column=0, padx=20, pady=20, sticky="w")

speedVar = tk.StringVar(value="Km/h")

speedKmBtn = tk.Radiobutton(
    unitsContainer,
    text="Km/h",
    variable=speedVar,
    value="Km/h",
    bg="white",
    font=("Arial", 14)
)

speedMphBtn = tk.Radiobutton(
    unitsContainer,
    text="MPH",
    variable=speedVar,
    value="MPH",
    bg="white",
    font=("Arial", 14)
)

speedKmBtn.grid(row=1, column=1, padx=10)
speedMphBtn.grid(row=1, column=2, padx=10)

# TIME UNIT

timeLabel = tk.Label(
    unitsContainer,
    text="Time Format",
    font=("Arial", 16),
    bg="white",
    fg="#333"
)
timeLabel.grid(row=2, column=0, padx=20, pady=20, sticky="w")

timeVar = tk.IntVar(value=12)

time12Btn = tk.Radiobutton(
    unitsContainer,
    text="12 Hour",
    variable=timeVar,
    value=12,
    bg="white",
    font=("Arial", 14)
)

time24Btn = tk.Radiobutton(
    unitsContainer,
    text="24 Hour",
    variable=timeVar,
    value=24,
    bg="white",
    font=("Arial", 14)
)

time12Btn.grid(row=2, column=1, padx=10)
time24Btn.grid(row=2, column=2, padx=10)

# ================== README SCREEN ==================

readMeTitle = tk.Label(
    readMeScreen,
    text="Read Me",
    font=("Arial", 26, "bold"),
    bg="white",
    fg="#333"
)
readMeTitle.pack(pady=20)

readMeText = tk.Label(
    readMeScreen,
    text=
    "This application includes:\n\n"
    "- Weather App\n"
    "- Text Writer\n"
    "- Settings System\n\n"
    "Use the sidebar to navigate through settings.",
    font=("Arial", 14),
    bg="white",
    fg="#444",
    justify="left"
)
readMeText.pack(padx=40, anchor="nw")

# ================== CREDITS SCREEN ==================

creditsTitle = tk.Label(
    creditsScreen,
    text="Credits",
    font=("Arial", 26, "bold"),
    bg="white",
    fg="#333"
)
creditsTitle.pack(pady=20)

creditsText = tk.Label(
    creditsScreen,
    text=
    "Made by Zack\n\n"
    "Weather API:\nOpen-Meteo\n\n"
    "GUI Library:\nTkinter",
    font=("Arial", 14),
    bg="white",
    fg="#444",
    justify="left"
)
creditsText.pack(padx=40, anchor="nw")

# ================== DEFAULT PAGE ==================

openSettingPage(themeScreen)

#endregion

#region ================== BUTTONS ==================
weatherBtn = tk.Button(inner_frame, text="Weather", command=openWeatherGetLocation)
textBtn = tk.Button(inner_frame, text="textWriter", command=opentextWriterScreen)
settingsBtn = tk.Button(inner_frame, text="Settings", command=openSettingsScreen)

buttons = [weatherBtn, textBtn, settingsBtn]

# Place buttons evenly
for i, btn in enumerate(buttons):
    btn.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
    inner_frame.grid_columnconfigure(i, weight=1)

# THIS centers vertically
inner_frame.grid_rowconfigure(0, weight=1)


#endregion

#region ================== TOGGLE BUTTON ==================
taskBarOpenIcon = tk.PhotoImage(
    file="Icons/General/taskBarOpenIcon.png"
).subsample(4, 4)

taskBarCloseIcon = tk.PhotoImage(
    file="Icons/General/taskBarCloseIcon.png"
).subsample(4, 4)

toggle_btn = tk.Button(
    root,
    image=taskBarOpenIcon,
    bg="#222",
    bd=0,
    width=80,
    height=20,
    compound="center"
)
toggle_btn.place(relx=0.5, y=HEIGHT, anchor="s")
#endregion

#region ================== HOVER SCALE ==================
def add_dock_hover_button(button, base_size=10, max_size=16):
    current_size = base_size
    target_size = base_size
    animating = False

    def animate():
        nonlocal current_size, animating

        if current_size < target_size:
            current_size += 1
        elif current_size > target_size:
            current_size -= 1

        button.config(font=("Arial", current_size))

        if current_size != target_size:
            button.after(10, animate)
        else:
            animating = False

    def on_enter(e):
        nonlocal target_size, animating
        target_size = max_size
        if not animating:
            animating = True
            animate()

    def on_leave(e):
        nonlocal target_size, animating
        target_size = base_size
        if not animating:
            animating = True
            animate()

    button.config(font=("Arial", base_size), bg="#444", fg="white", bd=0)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
def add_dock_hover_frame(frame, base_size=10, max_size=16):
    current_size = base_size
    target_size = base_size
    animating = False

    def animate():
        nonlocal current_size, animating

        if current_size < target_size:
            current_size += 2
        elif current_size > target_size:
            current_size -= 2

        size = 120 + (current_size - base_size) * 5

        frame.config(width=size, height=size + 40)

        if current_size != target_size:
            frame.after(10, animate)
        else:
            animating = False

    def on_enter(e):
        nonlocal target_size, animating
        target_size = max_size
        if not animating:
            animating = True
            animate()

    def on_leave(e):
        nonlocal target_size, animating
        target_size = base_size
        if not animating:
            animating = True
            animate()

    frame.config(bg="#444", bd=0)
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)

# Apply hover effect to ALL buttons
allButtons = [
    weatherBtn,
    textBtn,
    settingsBtn,

    getLocationTextBtn,
    locationFailedConfirmBtn,
    weatherScreenLocationName
]

for btn in allButtons:
    add_dock_hover_button(btn)


for btn in sidebarButtons:
    btn.pack(fill="x", padx=15, pady=8)
    add_dock_hover_button(btn, 16, 18)
#endregion

#region ================== ANIMATION ==================
current_y = HEIGHT

STEP_FACTOR = 0.25
MIN_STEP = 1
DELAY = 5

def animate_to(target_y):
    global current_y

    def step():
        global current_y

        distance = target_y - current_y
        move = int(distance * STEP_FACTOR)

        if abs(move) < MIN_STEP:
            move = MIN_STEP if distance > 0 else -MIN_STEP

        current_y += move

        if abs(target_y - current_y) < 2:
            current_y = target_y

        root.update_idletasks()
        btn_height = toggle_btn.winfo_height()

        # Center taskbar horizontally
        x_pos = (root.winfo_width() - BAR_WIDTH) // 2

        taskbar.place(x=x_pos, y=current_y, width=BAR_WIDTH, height=BAR_HEIGHT)

        # Button position
        if current_y >= HEIGHT:
            toggle_btn.place_configure(y=HEIGHT, anchor="s")
        else:
            toggle_btn.place_configure(y=current_y - btn_height, anchor="n")

        if current_y != target_y:
            root.after(DELAY, step)

    step()

def toggle_taskbar():
    if current_y >= HEIGHT:
        animate_to(HEIGHT - BAR_HEIGHT)
        toggle_btn.config(image=taskBarCloseIcon)
    else:
        animate_to(HEIGHT)
        toggle_btn.config(image=taskBarOpenIcon)

toggle_btn.config(command=toggle_taskbar)
#endregion
#endregion

#region Main
def main():
    settingsTracker = SettingsTracker(r"settingsavefolder//settings_log.json")
    openWeatherGetLocation()
    root.mainloop()

if __name__ == "__main__":
    main()

#endregion