# ⛅ Skydash

> A beautiful, zero-configuration terminal weather dashboard — no API key, no sign-up, just weather.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║       ⛅  SKYDASH    Tokyo, Japan    Tuesday, 16 June 2026  •  11:08        ║
╚══════════════════════════════════════════════════════════════════════════════╝
╭── Conditions ──╮  ╭────── Current Weather ──────╮
│     \  /       │  │   Partly Cloudy             │
│  _ /"".·.      │  │                             │
│    \_(  ).·    │  │   21.6°C  feels like 23.3°C │
│     (___)      │  │                             │
│                │  │   Humidity   75%            │
╰────────────────╯  │   Wind       5.1 km/h S     │
                    │   Pressure   1014 hPa       │
                    │   UV Index   0 (Low)        │
                    │                             │
                    │   🌅 04:24  🌇 18:58        │
                    ╰─────────────────────────────╯
╭──────────────────────────── Hourly Forecast ─────────────────────────────────╮
│  Temp  (24 h)   16°  ▁▁▁▁▁▁▁▂▄▅▆▆▇▇██▇▇▆▅▄▄▄▃  27°                         │
│  Rain  prob      0%  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁  100%                        │
│                    00:00  06:00  12:00  18:00  23:00                         │
╰──────────────────────────────────────────────────────────────────────────────╯
                             7-Day Forecast
╭────────────┬──────────────────────┬─────────┬─────────┬──────────┬──────────╮
│ Day        │ Condition            │    High │     Low │     Rain │ Wind max │
├────────────┼──────────────────────┼─────────┼─────────┼──────────┼──────────┤
│ Today      │ Overcast             │  26.9°C │  15.7°C │   0.0 mm │  7 km/h  │
│ Wed 17 Jun │ Overcast             │  26.0°C │  18.4°C │   0.0 mm │  8 km/h  │
│ Thu 18 Jun │ Light Rain           │  25.1°C │  19.1°C │   7.6 mm │  6 km/h  │
│ Fri 19 Jun │ Light Rain           │  28.8°C │  19.4°C │   3.6 mm │ 12 km/h  │
│ Sat 20 Jun │ Showers              │  26.2°C │  21.3°C │  18.3 mm │ 12 km/h  │
│ Sun 21 Jun │ Thunderstorm         │  26.9°C │  19.3°C │  47.7 mm │ 26 km/h  │
│ Mon 22 Jun │ Light Drizzle        │  24.1°C │  16.3°C │   0.6 mm │ 25 km/h  │
╰────────────┴──────────────────────┴─────────┴─────────┴──────────┴──────────╯

  Data: Open-Meteo (open-meteo.com) · Free · No API key required
```

---

## Features

- **Zero configuration** — no API key, no account, no `.env` file
- **Live data** from [Open-Meteo](https://open-meteo.com), updated hourly
- **ASCII art weather icons** — 9 condition types including night mode
- **Sparkline charts** — 24-hour temperature curve and rain probability
- **7-day forecast table** — highs/lows, precipitation, wind, UV index
- **Sunrise & sunset times** — pulled from the forecast API
- **Color-coded temperatures** — blue → cyan → green → yellow → orange → red
- **UV risk labels** — Low / Moderate / High / Very High / Extreme
- **WMO code support** — all 23 standard weather condition codes mapped

---

## Weather Conditions & Icons

| Icon                    | Condition        |
|-------------------------|------------------|
| `\  /` `.--` `(  )` `/  \` | ☀️ Clear / Mainly Clear |
| `\  /` `"".·.` `(  ).·`    | ⛅ Partly Cloudy |
| `.--. .-(   ). (__.____)` | ☁️ Overcast / Cloudy |
| Same + `, , , ,`         | 🌦 Drizzle       |
| Same + `' ' ' '`         | 🌧 Rain          |
| Same + `❄ ❄ ❄`           | ❄️ Snow          |
| Same + `⚡ ⚡ ⚡`          | ⛈ Thunderstorm  |
| `─ ─ ─ ─ ─` (fog lines)  | 🌫 Fog           |
| `✦ ☾ ✦` (night glyphs)  | 🌙 Clear Night   |

---

## Project Structure

```
Clauder/
├── skydash.py          # Main application (single file, ~220 lines)
├── requirements.txt    # Python dependencies (rich, requests)
└── README.md           # You are here
```

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/kareemrt/Clauder.git
cd Clauder
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run it**
```bash
python skydash.py London
python skydash.py "New York"
python skydash.py Tokyo
python skydash.py Sydney
```

---

## Usage

```
usage: skydash [-h] [--version] [city]

Skydash — Beautiful terminal weather dashboard

positional arguments:
  city        City name (default: London)

options:
  -h, --help  show this help message and exit
  --version   show version and exit
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                      skydash.py                         │
│                                                         │
│  1. Parse args → city name                              │
│  2. geocode()  → lat/lon via Open-Meteo Geocoding API   │
│  3. fetch_weather() → current + hourly + daily data     │
│  4. render()   → Rich panels, sparklines, table         │
│                                                         │
│  APIs used (both free, no auth):                        │
│  ├── geocoding-api.open-meteo.com/v1/search             │
│  └── api.open-meteo.com/v1/forecast                     │
└─────────────────────────────────────────────────────────┘
```

### Data flow

```
City name  ──►  Geocoding API  ──►  lat, lon, display name
                                           │
                                           ▼
                               Open-Meteo Forecast API
                                           │
                      ┌────────────────────┼─────────────────────┐
                      ▼                    ▼                     ▼
                 current{}            daily{}[7]           hourly{}[168]
                 temp, UV,           hi/lo, rain,         temp, rain prob
                 wind, etc.          wind, UV              per hour
                      │
                      ▼
               WMO code → ASCII art icon + condition label
```

---

## Requirements

| Package    | Version   | Purpose                     |
|------------|-----------|-----------------------------|
| `rich`     | ≥ 13.0.0  | Terminal colors, panels, tables |
| `requests` | ≥ 2.28.0  | HTTP calls to Open-Meteo    |
| Python     | ≥ 3.8     | f-strings, type hints       |

---

## Acknowledgements

- Weather data: [Open-Meteo](https://open-meteo.com) — open-source weather API, free forever
- Terminal rendering: [Rich](https://github.com/Textualize/rich) by Will McGugan
- ASCII weather art inspired by [wego](https://github.com/schachmat/wego) and [wttr.in](https://wttr.in)

---

*Built autonomously by [Claude Code](https://claude.ai/code) · No API key required · Works anywhere Python 3.8+ runs*
