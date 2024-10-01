import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
import time

API_KEY = "70ffff213f1cb224a667c4fd333f63f2"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

CSV_FILE = "weather_data.csv"

def fetch_weather_data(city):
    try:
        url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            print(f"Error: {data['message']}")
            return None

        weather = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        }
        return weather
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

def save_data_to_csv(data):
    df = pd.DataFrame([data])
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, mode='w', header=True, index=False)
    print("Weather data saved to CSV.")

def load_data_from_csv():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        print(f"No data found. CSV file {CSV_FILE} doesn't exist.")
        return None

def plot_weather_trend(df, parameter):
    if parameter not in df.columns:
        print(f"Invalid parameter: {parameter}")
        return

    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="time", y=parameter, data=df)
    plt.title(f"{parameter.capitalize()} Trend Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Weather Data Analysis Tool")
    parser.add_argument("--city", type=str, help="City name to fetch weather data", required=True)
    parser.add_argument("--plot", type=str, help="Weather parameter to plot", choices=["temperature", "humidity", "pressure", "wind_speed"])
    args = parser.parse_args()

    weather_data = fetch_weather_data(args.city)
    if weather_data:
        save_data_to_csv(weather_data)

    df = load_data_from_csv()
    if df is not None and args.plot:
        plot_weather_trend(df, args.plot)

if __name__ == "__main__":
    main()
