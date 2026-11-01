import tkinter as tk
import sounddevice as sd
import numpy as np
import math

# --- CHOOSE YOUR VISUALIZER THEME ---
# Options: "DEFAULT", "SUNSET", "NEON", "RETRO", "CYBER", "MATRIX",
# "NAAT", "RACE", "LOVE", "JOY", "PEACE"
LIGHT_MODE = "DEFAULT"
AUDIO_SENSITIVITY = 8.0
AUDIO_NOISE_FLOOR = 0.003
FRAME_INTERVAL_MS = 16

THEME_PALETTES = {
    "DEFAULT": ("#17133B", "#5636A8", "#D14FFF", "#42DDF5"),
    "NAAT": ("#071D25", "#164653", "#B6A16B", "#F0E4BE"),
    "RACE": ("#101B36", "#E23B32", "#F6A623", "#E9F1FF"),
    "LOVE": ("#32172E", "#9C426F", "#E995B5", "#FFE2E9"),
    "JOY": ("#174C68", "#F4A340", "#FFE16B", "#FFF4C7"),
    "PEACE": ("#123B4A", "#3B8C83", "#92BCA0", "#DDE9C8"),
    "SUNSET": ("#6F2100", "#D94D08", "#FF9E1B", "#FFE26B"),
    "NEON": ("#34104E", "#FF2D95", "#25E6FF", "#F5F3FF"),
    "RETRO": ("#141331", "#FF4B6E", "#35E0A1", "#FFE66D"),
    "CYBER": ("#120B2D", "#772BCE", "#FC357A", "#48E5FF"),
    "MATRIX": ("#03140B", "#075525", "#12A64A", "#9CFFB1"),
}


class UltimatePerfectVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini A-718 Ultimate Entertainment Visualizer")

        # Absolute borderless full-screen layout
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#010101")

        self.width = int(self.root.winfo_screenwidth())
        self.height = int(self.root.winfo_screenheight())
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        # Balanced central core radius
        self.base_radius = min(self.width, self.height) // 4

        self.canvas = tk.Canvas(self.root, bg="#010101", highlightthickness=0, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)

        # Escape key to close window instantly
        self.root.bind("<Escape>", lambda e: self.close())

        # Mathematical engine tracking channels
        self.audio_volume = 0
        self.rotation_angle = 0
        self.wave_phase = 0
        self.fft_data = np.zeros(64)
        self.smooth_volume = 0
        self.frame_count = 0

        # Launch live microphonic collection loop
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=44100, blocksize=512)
        self.stream.start()

        self.animate()

    def audio_callback(self, indata, frames, time, status):
        signal = indata[:, 0].astype(np.float32, copy=False)
        if len(signal) > 0:
            centered = signal - np.mean(signal)
            rms = float(np.sqrt(np.mean(centered ** 2)))
            self.audio_volume = min(
                1.0, max(0.0, (rms - AUDIO_NOISE_FLOOR) * AUDIO_SENSITIVITY)
            )

            window = np.hanning(len(centered))
            spectrum = np.abs(np.fft.rfft(centered * window)[:64])
            spectrum *= 2.0 / max(1.0, window.sum())
            self.fft_data = np.clip(spectrum * AUDIO_SENSITIVITY * 2.5, 0.0, 1.0)

    def get_theme_color(self, index, total_points, intensity):
        ratio = index / total_points
        if LIGHT_MODE == "DEFAULT":
            channels = [
                max(0, min(255, int(
                    128 + 127 * math.sin(2 * math.pi * ratio + self.rotation_angle + offset)
                )))
                for offset in (0, 2, 4)
            ]
            return f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"

        palette = THEME_PALETTES.get(LIGHT_MODE, ("#FFFFFF",))
        position = (ratio % 1) * len(palette)
        palette_index = int(position)
        blend = position - palette_index
        first = palette[palette_index]
        second = palette[(palette_index + 1) % len(palette)]
        channels = [
            max(0, min(255, int(
                int(first[i:i + 2], 16) * (1 - blend)
                + int(second[i:i + 2], 16) * blend
                + min(20, int(intensity * 30))
            )))
            for i in (1, 3, 5)
        ]
        return f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"

    def draw_theme_scene(self):
        palette = THEME_PALETTES.get(LIGHT_MODE, ("#FFFFFF",) * 4)
        dark, mid, accent, light = palette
        cx, cy = self.center_x, self.center_y
        pulse = min(1.0, self.smooth_volume)
        beat = math.sin(self.wave_phase)
        size_scale = min(self.width, self.height)

        if LIGHT_MODE == "NAAT":
            self.canvas.configure(bg="#071D25")
            # A quiet illuminated arch, crescent, and restrained geometric ornament.
            arch_width = min(self.width * 0.48, self.height * 0.8)
            arch_height = min(self.height * 0.82, self.width * 0.7)
            left, right = cx - arch_width / 2, cx + arch_width / 2
            bottom, top = cy + arch_height / 2, cy - arch_height / 2
            for inset, color, width in ((0, mid, 2), (18, dark, 2)):
                points = [(left + inset, bottom), (left + inset, top + arch_width * 0.28)]
                for step in range(25):
                    angle = math.pi - step * math.pi / 24
                    points.append((
                        cx + (arch_width / 2 - inset) * math.cos(angle),
                        top + arch_width * 0.28 - (arch_width / 2 - inset) * math.sin(angle)
                    ))
                points.append((right - inset, bottom))
                self.canvas.create_line(points, fill=color, width=width, smooth=True)
            self.canvas.create_line(left, bottom, right, bottom, fill=dark, width=2)
            for side in (-1, 1):
                x = cx + side * arch_width * 0.36
                for y in range(int(top + 50), int(bottom), 42):
                    self.canvas.create_polygon(
                        x, y - 9, x + 9 * side, y, x, y + 9,
                        x - 9 * side, y, fill="", outline=dark
                    )
            moon_x, moon_y = cx, top + arch_width * 0.18
            moon_size = max(18, int(min(self.width, self.height) * 0.035 + pulse * 5))
            for halo in (1.7, 2.4):
                halo_size = moon_size * (halo + pulse * 0.35)
                self.canvas.create_oval(
                    moon_x - halo_size, moon_y - halo_size,
                    moon_x + halo_size, moon_y + halo_size,
                    outline=mid, width=1
                )
            self.canvas.create_oval(moon_x - moon_size, moon_y - moon_size,
                                    moon_x + moon_size, moon_y + moon_size,
                                    fill=light, outline="")
            self.canvas.create_oval(moon_x - moon_size * 0.15, moon_y - moon_size * 1.15,
                                    moon_x + moon_size * 1.3, moon_y + moon_size * 0.3,
                                    fill="#071D25", outline="")
            for i in range(8):
                angle = i * math.pi / 4
                sx = cx + math.cos(angle) * arch_width * 0.41
                sy = moon_y + math.sin(angle) * arch_width * 0.27
                size = 1.5 + pulse * (2 + max(0, math.sin(self.wave_phase * 0.35 + i)) * 2)
                self.canvas.create_oval(sx - size, sy - size, sx + size, sy + size,
                                        fill=accent, outline="")
            self.canvas.create_text(cx, bottom + 32, text="NAAT",
                                    fill=light, font=("Segoe UI", 15))

        elif LIGHT_MODE == "RACE":
            self.canvas.configure(bg="#101B36")
            horizon = int(self.height * 0.35)
            sun_size = 34 + pulse * 34
            self.canvas.create_oval(cx - sun_size, horizon - sun_size,
                                    cx + sun_size, horizon + sun_size,
                                    fill=accent, outline="")
            self.canvas.create_polygon(0, horizon, self.width, horizon,
                                       self.width, self.height, 0, self.height,
                                       fill=dark, outline="")
            for side in (-1, 1):
                self.canvas.create_line(cx, horizon, cx + side * self.width, self.height,
                                        fill=light, width=3)
                self.canvas.create_line(cx, horizon, cx + side * self.width * 0.53, self.height,
                                        fill=mid, width=2)
            road_cycle = (self.wave_phase * (0.25 + pulse * 2.0)) % 1
            for i in range(7):
                position = ((i / 7) + road_cycle) % 1
                y = horizon + int((self.height - horizon) * position ** 2)
                self.canvas.create_line(cx - self.width * 0.48, y, cx + self.width * 0.48, y,
                                        fill=dark if i % 2 else mid,
                                        width=max(1, int(1 + position * 4)))
            # Finish-line checkerboard, trophy, and moving speed accents unify racing and contest.
            flag_y = horizon + 24
            square = max(8, min(22, self.width // 90))
            for row in range(2):
                for col in range(12):
                    if (row + col) % 2 == 0:
                        x = cx - 6 * square + col * square
                        self.canvas.create_rectangle(x, flag_y + row * square,
                                                     x + square, flag_y + (row + 1) * square,
                                                     fill=light, outline="")
            trophy_y = int(self.height * 0.76)
            tw = min(55, self.width // 20)
            self.canvas.create_polygon(cx - tw, trophy_y, cx + tw, trophy_y,
                                       cx + tw * 0.7, trophy_y + tw,
                                       cx - tw * 0.7, trophy_y + tw,
                                       fill=accent, outline="")
            self.canvas.create_rectangle(cx - 7, trophy_y + tw, cx + 7, trophy_y + tw + 25,
                                         fill=accent, outline="")
            self.canvas.create_line(cx - 24, trophy_y + tw + 26,
                                    cx + 24, trophy_y + tw + 26, fill=accent, width=6)
            for i in range(8):
                speed = 5 + pulse * 95
                x = (i * 197 + int(self.wave_phase * speed)) % self.width
                y = horizon + 12 + i * 7
                streak = 30 + i * 5 + int(pulse * 65)
                self.canvas.create_line(x, y, x + streak, y,
                                        fill=light if i % 2 else accent,
                                        width=2 + int(pulse * 2))
            self.canvas.create_text(cx, 30, text="RACE",
                                    fill=light, font=("Segoe UI", 15, "bold"))

        elif LIGHT_MODE == "LOVE":
            self.canvas.configure(bg="#32172E")
            # Soft bokeh and drifting hearts rather than a spinning audio wheel.
            drift = self.wave_phase * (0.15 + pulse * 0.85)
            for i in range(24):
                x = (i * 173 + int(math.sin(drift * 0.22 + i) * (8 + pulse * 28))) % self.width
                y = (i * 97 + int(drift * (2 + i % 4))) % self.height
                size = 3 + i % 8 + pulse * 5
                self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                        fill=dark if i % 2 else mid, outline="")
            for i in range(9):
                x = cx + math.sin(self.wave_phase * 0.3 + i * 1.7) * self.width * 0.32
                y = cy + math.cos(self.wave_phase * 0.22 + i * 2.1) * self.height * 0.32
                size = 13 + (i % 3) * 5
                self.draw_heart(x, y, size, accent if i % 2 else light)
            heart_size = size_scale * (0.065 + pulse * 0.17)
            for halo in (1.45, 1.8):
                halo_size = heart_size * halo
                self.canvas.create_oval(
                    cx - halo_size, cy - halo_size, cx + halo_size, cy + halo_size,
                    outline=mid if halo < 1.6 else dark, width=2
                )
            self.draw_heart(cx, cy, heart_size,
                            light)
            self.canvas.create_text(cx, int(self.height * 0.82), text="LOVE",
                                    fill=light, font=("Segoe UI", 18, "bold"))

        elif LIGHT_MODE == "JOY":
            self.canvas.configure(bg="#174C68")
            sun_x, sun_y = cx, int(self.height * 0.38)
            sun_r = size_scale * (0.09 + pulse * 0.065)
            for i in range(16):
                angle = i * math.pi / 8 + self.wave_phase * 0.025
                self.canvas.create_line(
                    sun_x + math.cos(angle) * sun_r * 1.12,
                    sun_y + math.sin(angle) * sun_r * 1.12,
                    sun_x + math.cos(angle) * sun_r * (1.25 + pulse * 0.2),
                    sun_y + math.sin(angle) * sun_r * (1.25 + pulse * 0.2),
                    fill=accent, width=4, capstyle="round"
                )
            self.canvas.create_oval(sun_x - sun_r, sun_y - sun_r,
                                    sun_x + sun_r, sun_y + sun_r, fill=light, outline="")
            self.canvas.create_polygon(
                0, self.height * 0.72, self.width * 0.27, self.height * 0.51,
                self.width * 0.52, self.height * 0.74, self.width * 0.75,
                self.height * 0.55, self.width, self.height * 0.72,
                self.width, self.height, 0, self.height, fill=mid, outline=""
            )
            self.canvas.create_polygon(
                0, self.height * 0.84, self.width * 0.36, self.height * 0.68,
                self.width * 0.68, self.height * 0.87, self.width,
                self.height * 0.7, self.width, self.height, 0, self.height,
                fill=dark, outline=""
            )
            for i in range(18):
                x = (i * 131 + int(self.wave_phase * (9 + i % 5))) % self.width
                y = int(self.height * (0.2 + (i * 37 % 55) / 100))
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                        fill=accent if i % 2 else light, outline="")
            self.canvas.create_text(cx, int(self.height * 0.91), text="JOY",
                                    fill=light, font=("Segoe UI", 17, "bold"))

        elif LIGHT_MODE == "PEACE":
            self.canvas.configure(bg="#123B4A")
            horizon = int(self.height * 0.56)
            moon_r = size_scale * (0.05 + pulse * 0.045)
            self.canvas.create_oval(cx - moon_r, horizon - moon_r * 2.5,
                                    cx + moon_r, horizon - moon_r * 0.5,
                                    fill=light, outline="")
            self.canvas.create_polygon(0, horizon + 35, self.width * 0.25, horizon - 65,
                                       self.width * 0.5, horizon + 30,
                                       self.width * 0.76, horizon - 35,
                                       self.width, horizon + 20, self.width, self.height,
                                       0, self.height, fill=mid, outline="")
            for i in range(7):
                y = horizon + 52 + i * 25
                offset = math.sin(self.wave_phase * 0.18 + i) * pulse * (8 + i * 2)
                points = []
                for x in range(0, self.width + 1, 40):
                    wave_height = 1 + pulse * (8 + i * 1.5)
                    points.append((
                        x,
                        y + math.sin(x * 0.008 + self.wave_phase * 0.2 + i) * wave_height + offset
                    ))
                self.canvas.create_line(points, fill=dark if i % 2 else accent,
                                        width=1 + int(pulse * 2), smooth=True)
            for radius in (0.18, 0.26, 0.34):
                r = size_scale * (radius + pulse * 0.075)
                self.canvas.create_oval(cx - r, horizon - r, cx + r, horizon + r,
                                        outline=dark if pulse < 0.35 else accent, width=1 + int(pulse * 2))
            self.canvas.create_text(cx, int(self.height * 0.9), text="PEACE",
                                    fill=light, font=("Segoe UI", 16))

        elif LIGHT_MODE == "DEFAULT":
            self.canvas.configure(bg="#080817")
            for i in range(96):
                angle = i * 2 * math.pi / 96 + self.rotation_angle
                length = 12 + pulse * 75 + self.fft_data[i % len(self.fft_data)] * 235
                self.canvas.create_line(
                    cx + 125 * math.cos(angle), cy + 125 * math.sin(angle),
                    cx + (125 + length) * math.cos(angle),
                    cy + (125 + length) * math.sin(angle),
                    fill=self.get_theme_color(i, 96, pulse), width=2 + int(pulse * 4), capstyle="round"
                )
            core = 22 + pulse * 30
            self.canvas.create_oval(cx - core, cy - core, cx + core, cy + core,
                                    fill=palette[1], outline=light, width=2)

        elif LIGHT_MODE == "SUNSET":
            self.canvas.configure(bg="#260D05")
            count = 48
            spacing = self.width / count
            for i in range(count):
                value = self.fft_data[i % len(self.fft_data)]
                height = 3 + value * self.height * 0.55 + pulse * self.height * 0.07
                x = i * spacing
                self.canvas.create_rectangle(
                    x + 2, self.height - height, x + spacing - 2, self.height,
                    fill=self.get_theme_color(i, count, pulse), outline=""
                )
            for radius in (0.18, 0.27, 0.36):
                r = size_scale * (radius + pulse * 0.035)
                self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                                       start=195, extent=150, style="arc",
                                       outline=accent, width=3)

        elif LIGHT_MODE == "NEON":
            self.canvas.configure(bg="#10091D")
            for ring in range(1, 7):
                radius = size_scale * (
                    0.055 * ring + (0.01 + pulse * 0.045) * beat
                )
                points = []
                for i in range(7):
                    angle = i * 2 * math.pi / 6 + self.rotation_angle * 0.3
                    points.extend((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
                self.canvas.create_polygon(points, outline=palette[ring % 4],
                                           fill="", width=3)
            self.canvas.create_oval(cx - 25, cy - 25, cx + 25, cy + 25,
                                    outline=light, width=3)

        elif LIGHT_MODE == "RETRO":
            self.canvas.configure(bg="#141331")
            spacing = max(30, self.width // 32)
            offset = int(self.wave_phase * (2 + pulse * 24)) % spacing
            for x in range(-spacing + offset, self.width, spacing):
                self.canvas.create_line(x, 0, x, self.height, fill=dark)
            for y in range(-spacing + offset, self.height, spacing):
                self.canvas.create_line(0, y, self.width, y, fill=dark)
            block = max(8, spacing // 2)
            for i in range(32):
                value = self.fft_data[i % len(self.fft_data)]
                rows = 1 + int(value * 14 + pulse * 5)
                for row in range(rows):
                    x = i * spacing
                    y = self.height - (row + 1) * block
                    self.canvas.create_rectangle(
                        x + 2, y + 2, x + block - 2, y + block - 2,
                        fill=palette[(i + row) % 4], outline=""
                    )

        elif LIGHT_MODE == "CYBER":
            self.canvas.configure(bg="#10091D")
            ground = int(self.height * 0.78)
            self.canvas.create_line(0, ground, self.width, ground, fill=accent, width=2)
            for i in range(18):
                x = i * self.width / 18
                building_w = self.width / 21
                building_h = self.height * (0.12 + (i * 29 % 40) / 100) * (1 + pulse * 0.12)
                self.canvas.create_rectangle(x, ground - building_h, x + building_w, ground,
                                             fill=dark, outline=mid, width=2)
                for row in range(3):
                    self.canvas.create_line(
                        x + 5, ground - building_h + 18 + row * 22,
                        x + building_w - 5, ground - building_h + 18 + row * 22,
                        fill=palette[(i + row) % 4], width=2
                    )
            self.canvas.create_line(0, ground + 30, self.width, ground + 30,
                                    fill=mid, width=2)
            for i in range(32):
                x = i * self.width / 32
                height = self.fft_data[i % len(self.fft_data)] * 220 + pulse * 65
                self.canvas.create_line(x, ground + 30, x, ground + 30 - height,
                                        fill=accent, width=2)

        elif LIGHT_MODE == "MATRIX":
            self.canvas.configure(bg="#03140B")
            columns = min(48, max(1, self.width // 32))
            for column in range(columns):
                x = int((column + 0.5) * self.width / columns)
                stream_length = 5 + (column * 3 % 7)
                speed = 1 + pulse * 12
                head = int(self.wave_phase * speed * (10 + column % 7) + column * 31) % (self.height + stream_length * 22)
                for row in range(stream_length):
                    y = head - row * 22
                    if 0 <= y < self.height:
                        color = light if row == 0 else palette[2] if row < 3 else palette[1]
                        self.canvas.create_text(x, y, text=str((column + row + int(self.wave_phase)) % 2),
                                                fill=color, font=("Consolas", 13))

        self.canvas.create_text(
            cx, 25, text=LIGHT_MODE.replace("_", " "),
            fill=light, font=("Segoe UI", 13, "bold")
        )

    def draw_heart(self, x, y, size, color):
        points = (
            x, y + size,
            x - size * 1.25, y - size * 0.1,
            x - size, y - size * 0.8,
            x - size * 0.35, y - size * 0.9,
            x, y - size * 0.35,
            x + size * 0.35, y - size * 0.9,
            x + size, y - size * 0.8,
            x + size * 1.25, y - size * 0.1,
        )
        self.canvas.create_polygon(points, fill=color, outline="", smooth=True)

    def animate(self):
        self.canvas.delete("all")

        target = self.audio_volume
        smoothing = 0.38 if target > self.smooth_volume else 0.12
        self.smooth_volume += (target - self.smooth_volume) * smoothing
        self.rotation_angle += 0.001 + (self.smooth_volume * 0.07)
        self.wave_phase += 0.001 + (self.smooth_volume * 0.2)
        self.frame_count += 1
        self.draw_theme_scene()
        self.root.after(FRAME_INTERVAL_MS, self.animate)

    def close(self):
        self.stream.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimatePerfectVisualizer(root)
    root.mainloop()
