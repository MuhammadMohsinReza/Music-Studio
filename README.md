# 🎵 Music Studio — Turn Sound into Light

**Music Studio** transforms the sounds around you into a vivid, fullscreen visual experience. Using your microphone, it listens to live audio and responds with flowing colors, pulsing shapes, shimmering patterns, and scenes that come alive with the rhythm.

From bold neon energy to calm moonlit reflections, choose a visual mood and let the sound shape the show. Whether you’re enjoying music, setting the atmosphere, or simply exploring the connection between sound and color, Music Studio turns your screen into a living canvas.

## ✨ A visual mood for every moment

Music Studio includes **11 themes**, each with its own palette, style, and animated scene:

- **DEFAULT** — A radiant, rotating spectrum that pulses with the audio.
- **SUNSET** — Warm, glowing colors flow through responsive audio bars.
- **NEON** — Bright geometric forms move in a vivid, electric atmosphere.
- **RETRO** — A nostalgic grid and pixel-inspired bars bring a classic digital feel.
- **CYBER** — A futuristic cityscape flickers with sound-reactive energy.
- **MATRIX** — Streams of digital symbols cascade in a deep green glow.
- **NAAT** — A serene arch, crescent, and delicate ornaments create a refined scene.
- **RACE** — A glowing horizon, racing track, and trophy capture the rush of motion.
- **LOVE** — Soft bokeh and floating hearts create a warm, romantic display.
- **JOY** — A bright sun and colorful landscape bring a cheerful, uplifting mood.
- **PEACE** — A tranquil moonlit scene and flowing waves offer a calm visual escape.

## 🌈 Live, audio-responsive animation

The visualizer continuously analyzes microphone input to estimate sound intensity and frequency energy. These measurements influence the animations, helping the display react to changes in the sound around you. Motion is smoothed between frames for a more fluid experience, while each theme interprets the audio in its own way.

## 🖥️ Designed for the big screen

Music Studio opens in fullscreen, giving the animation room to fill your display. The experience updates continuously for smooth, flowing motion, and you can close the visualizer at any time by pressing **Esc**.

## ⚙️ Choose your theme

Set the `LIGHT_MODE` value near the top of `Music Studio.py` to one of the available themes:

```python
LIGHT_MODE = "NEON"
```

For example, change `"NEON"` to `"PEACE"`, `"RETRO"`, or any other theme name listed in the file. The visualizer starts with the selected theme when you launch it.

You can also adjust the audio response and animation timing using the settings near the top of the file:

```python
AUDIO_SENSITIVITY = 8.0
AUDIO_NOISE_FLOOR = 0.003
FRAME_INTERVAL_MS = 16
```

## 🚀 Getting started

Install the required Python packages:

```bash
pip install numpy sounddevice
```

Then run the application:

```bash
python "Music Studio.py"
```

Make sure your microphone is connected and available to your system. If you have multiple audio input devices, select the desired input device using your system’s audio settings.

## 🧰 Built with

- **Python** for the application logic
- **Tkinter** for the fullscreen canvas and animated graphics
- **sounddevice** for live microphone input
- **NumPy** for audio signal and frequency analysis
- **Math** for smooth movement, shapes, and color effects

## 🎧 A note about audio

Music Studio visualizes **live microphone input**. It does not play, record, or edit audio. The result depends on the microphone and the sounds it can hear.

**Pick a theme, turn up the sound, and watch your world move to the beat.**
