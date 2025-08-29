# 🌱 Logogeno

**Logogeno** is a Python script for generating branded SVG and PNG logos for
projects across multiple platforms (like *Saplings* and *Arbor*). It supports
dynamic text placement, scalable layout, custom gradients, and embedded font
styling using system-installed Playfair Display.

---

## ✨ Features

* Generates 512×512 logos with:

  * Branded background gradients
  * Platform-specific SVG icon
  * Stylized platform and repo names (with smart font scaling)
* Outputs both `.svg` and `.png`
* Uses **Playfair Display Bold** from your system's installed fonts

---

## 👷️ Prerequisites

### 1. Python

Ensure you have **Python 3.8+** installed.
Check with:

```bash
python3 --version
```

### 2. Install Python Dependencies

Install the required Python packages:

```bash
pip install cairosvg
```

> **Note:** `cairosvg` also requires system-level libraries, including Cairo,
Pango, and GDK-PixBuf. On macOS:
>
> ```bash
> brew install cairo pango gdk-pixbuf
> ```

### 3. System Font: Playfair Display

You must have **Playfair Display Bold** installed on your system.
Download it from [Google Fonts](https://fonts.google.com/specimen/Playfair+Display)
and install it manually before running the script.

---

## 📅 Usage

```bash
python logogeno.py --platform Saplings --repo-name "Content types"
python logogeno.py --platform Arbor --repo-name "Theme"
```

This generates:

* `generated_logos/Saplings-content-types.svg`
* `generated_logos/Saplings-content-types.png`
* `generated_logos/Arbor-theme.svg`
* `generated_logos/Arbor-theme.png`

### Platform-only logo

You can also just create a platform logo.

```bash
python logogeno.py --platform Arbor
```

This omits the repository name.

### Excluding platform name

Use the `--no-platform-name` flag to generate logos without the platform name:

```bash
python logogeno.py --platform Saplings --repo-name "My Project" --no-platform-name
```

This generates a logo showing only "My Project" without "Saplings" below the icon.

---

## ➕ Adding New Platforms

To add a new branded platform:

1. Open the `CONFIG` dictionary at the top of the script.
2. Add a new entry following this format:

```python
"MyPlatform": {
    "background_gradient_1": "#hex1",
    "background_gradient_2": "#hex2",
    "background_gradient_3": "#hex3",
    "background_color": "#hexFallback",
    "foreground_color": "#hexText",
    "gradient_1": "0%",
    "gradient_2": "30%",
    "gradient_3": "100%",
    "svg_path": '''<svg>...your platform icon here...</svg>'''
}
```

> **SVG Icon Notes:**
>
> * Must be embedded as a string inside triple quotes (`'''`)
> * Must use a **400×400 coordinate space**
> * Use `fill` or `stroke` with `foreground_color` to colorize

---

## 🎨 Customization

* Font: Uses **Playfair Display Bold**, which must be installed on your system
* Font size auto-scales for long names
* SVG background uses a **4-stop gradient** for custom ramping control

---

## 📂 Output Directory

All generated logos are saved in:

```
generated_logos/
  ├— Saplings-example.svg
  └— Saplings-example.png
```

---

## ✅ Example

```bash
python logogeno.py --platform Arbor --repo-name "VeryLongRepositoryNameThatWillBeScaled"
```

## 🧩 Contributing

Feel free to open issues or submit pull requests to improve the script.
Contributions are welcome and encouraged!

## 💼 Sponsorship

Development of Logogeno is proudly sponsored by
[Kanopi Studios](https://kanopi.com), a digital agency focused on thoughtful
website design and development.

---

## 📄 License

This script is available under the GNU General Public License v3.0. See the
LICENSE file for details.
