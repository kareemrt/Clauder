#!/usr/bin/env python3
"""
Skydash — Beautiful terminal weather dashboard powered by Open-Meteo.
No API key required. Works anywhere Python 3.8+ is installed.
"""

import sys
import argparse
from datetime import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from rich.align import Align
from rich.rule import Rule

console = Console()

# WMO Weather interpretation codes → (description, art_key)
WMO_CODES = {
    0:  ("Clear Sky",                "sunny"),
    1:  ("Mainly Clear",             "sunny"),
    2:  ("Partly Cloudy",            "partly_cloudy"),
    3:  ("Overcast",                 "cloudy"),
    45: ("Fog",                      "fog"),
    48: ("Icy Fog",                  "fog"),
    51: ("Light Drizzle",            "drizzle"),
    53: ("Drizzle",                  "drizzle"),
    55: ("Heavy Drizzle",            "drizzle"),
    61: ("Light Rain",               "rain"),
    63: ("Rain",                     "rain"),
    65: ("Heavy Rain",               "rain"),
    71: ("Light Snow",               "snow"),
    73: ("Snow",                     "snow"),
    75: ("Heavy Snow",               "snow"),
    77: ("Snow Grains",              "snow"),
    80: ("Rain Showers",             "showers"),
    81: ("Showers",                  "showers"),
    82: ("Heavy Showers",            "showers"),
    85: ("Snow Showers",             "snow"),
    86: ("Heavy Snow Showers",       "snow"),
    95: ("Thunderstorm",             "thunder"),
    96: ("Thunderstorm + Hail",      "thunder"),
    99: ("Thunderstorm + Heavy Hail","thunder"),
}

ASCII_ART = {
    "sunny": [
        "   [yellow]\\   /[/]   ",
        "    [yellow].--.[/]    ",
        "[yellow]― (    ) ―[/] ",
        "    [yellow]`--'[/]    ",
        "   [yellow]/   \\[/]   ",
    ],
    "night_clear": [
        "   [white]✦ · ✦[/]   ",
        "  [white]·[/]        ",
        "    [yellow]☾[/]      ",
        "  [white]·   ✦[/]    ",
        "   [white]✦ · ·[/]   ",
    ],
    "partly_cloudy": [
        "   [yellow]\\  /[/]    ",
        "[yellow]_ /[/][white]\"\".·.[/]   ",
        "  [yellow]\\_(  [/][white]).·[/] ",
        "   [white](___)[/]   ",
        "           ",
    ],
    "cloudy": [
        "           ",
        "  [white]   .--.[/]  ",
        " [white].-(    ).[/] ",
        "[white](__.__(__))[/]",
        "           ",
    ],
    "drizzle": [
        "           ",
        "  [white]  .--.[/]   ",
        " [white].-(    ).[/] ",
        "[white](__.__(__))[/]",
        " [cyan], , , ,[/]   ",
    ],
    "rain": [
        "           ",
        "  [white]  .--.[/]   ",
        " [white].-(    ).[/] ",
        "[white](__.__(__))[/]",
        " [blue]' ' ' '[/]   ",
    ],
    "showers": [
        "   [yellow]\\  /[/]   ",
        "[yellow]_ /[/][white]\"\".·.[/]   ",
        "  [yellow]\\_(  [/][white]).·[/] ",
        "   [white](___)[/]   ",
        "  [blue]' , ' ,[/]  ",
    ],
    "snow": [
        "           ",
        "  [white]  .--.[/]   ",
        " [white].-(    ).[/] ",
        "[white](__.__(__))[/]",
        " [cyan]❄  ❄  ❄[/]   ",
    ],
    "thunder": [
        "           ",
        "  [white]  .--.[/]   ",
        " [white].-(    ).[/] ",
        "[white](__.__(__))[/]",
        " [yellow]⚡  ⚡  ⚡[/]  ",
    ],
    "fog": [
        "           ",
        " [white]─ ─ ─ ─ ─[/]",
        "  [white]─ ─ ─ ─[/] ",
        " [white]─ ─ ─ ─ ─[/]",
        "           ",
    ],
}


def geocode(city: str) -> tuple:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        console.print(f"[bold red]✗ City not found:[/] {city}")
        sys.exit(1)
    res = data["results"][0]
    return res["latitude"], res["longitude"], res.get("name", city), res.get("country", "")


def fetch_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "weather_code", "wind_speed_10m", "wind_direction_10m",
            "surface_pressure", "uv_index", "precipitation",
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_sum", "wind_speed_10m_max", "uv_index_max",
            "sunrise", "sunset",
        ],
        "hourly": ["temperature_2m", "precipitation_probability"],
        "timezone": "auto",
        "forecast_days": 7,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def wind_direction(deg: float) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(deg / 45) % 8]


def sparkline(values: list, lo=None, hi=None) -> str:
    bars = "▁▂▃▄▅▆▇█"
    if lo is None:
        lo = min(values)
    if hi is None:
        hi = max(values)
    spread = hi - lo or 1
    return "".join(bars[int((v - lo) / spread * (len(bars) - 1))] for v in values)


def temp_color(t: float) -> str:
    if t <= 0:    return "bright_cyan"
    if t <= 10:   return "cyan"
    if t <= 20:   return "green"
    if t <= 28:   return "yellow"
    if t <= 35:   return "dark_orange"
    return "bold red"


def uv_label(uv: float) -> tuple:
    if uv <= 2:  return "Low",       "green"
    if uv <= 5:  return "Moderate",  "yellow"
    if uv <= 7:  return "High",      "dark_orange"
    if uv <= 10: return "Very High", "red"
    return "Extreme", "bold red"


def render(city: str, country: str, data: dict, units: str = "metric"):
    cur   = data["current"]
    daily = data["daily"]
    hourly= data["hourly"]

    wmo = cur["weather_code"]
    desc, art_key = WMO_CODES.get(wmo, ("Unknown", "sunny"))

    hour = datetime.now().hour
    if (hour < 6 or hour >= 20) and art_key == "sunny":
        art_key = "night_clear"

    temp        = cur["temperature_2m"]
    feels_like  = cur["apparent_temperature"]
    humidity    = cur["relative_humidity_2m"]
    wind_spd    = cur["wind_speed_10m"]
    wind_dir    = wind_direction(cur["wind_direction_10m"])
    pressure    = cur["surface_pressure"]
    uv          = cur.get("uv_index", 0) or 0
    precip      = cur.get("precipitation", 0) or 0

    tc = temp_color(temp)
    uv_text, uv_color = uv_label(uv)

    # ── Header ───────────────────────────────────────────────────────────────
    now_str = datetime.now().strftime("%A, %d %B %Y  •  %H:%M")
    header = Text(justify="center")
    header.append("⛅  SKYDASH", style="bold cyan")
    header.append(f"    {city}, {country}", style="bold white")
    header.append(f"    {now_str}", style="dim white")
    console.print()
    console.print(Panel(Align.center(header), style="cyan", box=box.DOUBLE_EDGE, padding=(0, 2)))

    # ── ASCII art panel ───────────────────────────────────────────────────────
    art_lines = ASCII_ART.get(art_key, ASCII_ART["sunny"])
    art_text  = Text.from_markup("\n".join(art_lines))

    # ── Current conditions panel ──────────────────────────────────────────────
    info = Text()
    info.append(f"  {desc}\n\n", style="bold white")
    info.append(f"  {temp}°C", style=f"bold {tc}")
    info.append(f"  feels like {feels_like}°C\n", style="dim")
    info.append(f"\n")
    info.append("  Humidity   ", style="dim"); info.append(f"{humidity}%\n",         style="cyan")
    info.append("  Wind       ", style="dim"); info.append(f"{wind_spd} km/h {wind_dir}\n", style="green")
    info.append("  Pressure   ", style="dim"); info.append(f"{pressure:.0f} hPa\n",  style="white")
    info.append("  UV Index   ", style="dim"); info.append(f"{uv} ", style=uv_color); info.append(f"({uv_text})\n", style=f"dim {uv_color}")
    if precip > 0:
        info.append("  Precip     ", style="dim"); info.append(f"{precip} mm\n", style="blue")

    # Sunrise / sunset
    sunrise = data["daily"]["sunrise"][0].split("T")[1] if data["daily"].get("sunrise") else "—"
    sunset  = data["daily"]["sunset"][0].split("T")[1]  if data["daily"].get("sunset")  else "—"
    info.append(f"\n  🌅 {sunrise}  ", style="yellow"); info.append(f"🌇 {sunset}", style="dark_orange")

    art_panel  = Panel(Align.center(art_text, vertical="middle"),
                       title="[bold cyan]Conditions[/]", width=18)
    info_panel = Panel(info, title="[bold cyan]Current Weather[/]")
    console.print(Columns([art_panel, info_panel]))

    # ── Hourly sparkline (next 24 h) ──────────────────────────────────────────
    temps_24  = hourly["temperature_2m"][:24]
    rain_24   = hourly["precipitation_probability"][:24]
    spark_t   = sparkline(temps_24)
    spark_r   = sparkline(rain_24, 0, 100)

    hourly_txt = Text()
    hourly_txt.append("  Temp  (24 h)   ", style="dim")
    hourly_txt.append(f"{min(temps_24):.0f}°  ", style="cyan")
    hourly_txt.append(spark_t, style=tc)
    hourly_txt.append(f"  {max(temps_24):.0f}°\n", style="red")

    hourly_txt.append("  Rain  prob      ", style="dim")
    hourly_txt.append("0%  ",   style="dim")
    hourly_txt.append(spark_r, style="blue")
    hourly_txt.append("  100%\n", style="blue")

    hourly_txt.append("                  ", style="dim")
    for h in [0, 6, 12, 18, 23]:
        hourly_txt.append(f"  {h:02d}:00", style="dim")

    console.print(Panel(hourly_txt, title="[bold cyan]Hourly Forecast[/]", box=box.ROUNDED))

    # ── 7-day table ───────────────────────────────────────────────────────────
    tbl = Table(title="7-Day Forecast", box=box.ROUNDED, show_header=True,
                header_style="bold cyan", border_style="cyan", title_style="bold cyan",
                expand=True)
    tbl.add_column("Day",       style="bold white",  no_wrap=True, min_width=10)
    tbl.add_column("Condition",                      no_wrap=True, min_width=20)
    tbl.add_column("High",      justify="right",     no_wrap=True, min_width=7)
    tbl.add_column("Low",       justify="right",     no_wrap=True, min_width=7)
    tbl.add_column("Rain",      justify="right",     no_wrap=True, min_width=8)
    tbl.add_column("Wind max",  justify="right",     no_wrap=True, min_width=9)
    tbl.add_column("UV",        justify="right",     no_wrap=True, min_width=14)

    for i in range(7):
        dt      = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        day_lbl = "Today" if i == 0 else dt.strftime("%a %d %b")
        code    = daily["weather_code"][i]
        d_desc, _ = WMO_CODES.get(code, ("Unknown", "sunny"))
        hi  = daily["temperature_2m_max"][i]
        lo  = daily["temperature_2m_min"][i]
        rn  = daily["precipitation_sum"][i] or 0
        wnd = daily["wind_speed_10m_max"][i]
        uv_d= daily["uv_index_max"][i] or 0
        uv_lbl, uv_clr = uv_label(uv_d)

        row_style = "on grey11" if i % 2 == 0 else ""
        tbl.add_row(
            day_lbl,
            d_desc,
            Text(f"{hi:.1f}°C", style=f"bold {temp_color(hi)}"),
            Text(f"{lo:.1f}°C", style=temp_color(lo)),
            Text(f"{rn:.1f} mm", style="blue" if rn > 1 else "dim"),
            f"{wnd:.0f} km/h",
            Text(f"{uv_d:.1f} — {uv_lbl}", style=uv_clr),
            style=row_style,
        )

    console.print(tbl)

    # ── Footer ────────────────────────────────────────────────────────────────
    console.print()
    console.print(Rule(style="dim"))
    console.print("[dim]  Data: Open-Meteo (open-meteo.com) · Free · No API key required  "
                  "· github.com/kareemrt/Clauder[/]")
    console.print()


def main():
    parser = argparse.ArgumentParser(
        prog="skydash",
        description="Skydash — Beautiful terminal weather dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python skydash.py London
  python skydash.py "New York"
  python skydash.py Tokyo
  python skydash.py Sydney
        """,
    )
    parser.add_argument("city", nargs="?", default="London",
                        help="City name (default: London)")
    parser.add_argument("--version", action="version", version="Skydash 1.0.0")
    args = parser.parse_args()

    with console.status(f"[cyan]Fetching weather for [bold]{args.city}[/]…", spinner="dots"):
        lat, lon, city_name, country = geocode(args.city)
        weather = fetch_weather(lat, lon)

    render(city_name, country, weather)


if __name__ == "__main__":
    main()
