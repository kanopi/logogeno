import os
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from io import StringIO
import cairosvg

# Configuration for platforms
CONFIG = {
    "Saplings": {
        "background_gradient_1": "#153e35",
        "background_gradient_2": "#153e35",
        "background_gradient_3": "#789a3d",
        "background_color": "#789a3d",
        "foreground_color": "#ffffff",
        "gradient_1": "0%",
        "gradient_2": "25%",
        "gradient_3": "100%",
        "svg_path": '''<svg baseProfile="full" height="400" width="400" xmlns="http://www.w3.org/2000/svg"><path d="M114.128 270.419s64-154.767 22.771-220.742c-46.08-73.702-89.498 95.186 7.405 75.248 67.307-13.865 62.391 22.171 42.775 41.187-17.578 17.041-33.696 20.968-36.143-53.956-4.357-133.155 172.903-44.708-.193 12.877" fill="none" stroke="#fff" stroke-linecap="round" stroke-miterlimit="10" stroke-width="15.743"/></svg>'''
    },
    "Arbor": {
        "background_gradient_1": "#789a3d",
        "background_gradient_2": "#789a3d",
        "background_gradient_3": "#153e35",
        "background_color": "#153e35",
        "foreground_color": "#ffffff",
        "gradient_1": "0%",
        "gradient_2": "35%",
        "gradient_3": "100%",
        "svg_path": '''<svg baseProfile="full" height="400" width="400" xmlns="http://www.w3.org/2000/svg"><path d="M228.617 112.38c3.12-6.17 3.96-13.238 2.079-19.593-2.195-7.439-8.165-13.255-15.147-15.548 1.283-10.929-2.992-23.042-11.77-32.105-7.851-8.095-20.021-18.696-33.444-23.184-22.473-7.51-51.172 2.323-66.777 22.871-4.901 6.456-7.253 13.98-8.763 19.809-2.779 10.743-2.138 19.55-.185 26.419-6.298.969-14.549 6.969-22.144 16.103-8.365 10.073-14.65 22.414-17.685 34.754-10.588 42.979 19.124 71.749 37.776 85.073 20.549 14.678 46.669 12.639 63.583 4.075-.028 3.648-.057 6.585-.071 9.049-.115 11.086-.143 14.064.713 34.727a6.415 6.415 0 0 0 6.398 6.156h.271c3.535-.142 6.284-3.134 6.142-6.669-.841-20.335-.813-23.256-.698-34.071.056-5.145.113-12.197.113-23.755a6.404 6.404 0 0 0-6.413-6.413c-3.207 0-5.856 2.352-6.341 5.431-1.239 1.568-6.983 5.828-17.457 8.136-8.236 1.81-24.24 3.305-38.787-7.082-35.425-25.309-37.378-52.896-32.775-71.578 6.127-24.852 24.396-40.57 29.34-41.254a6.2 6.2 0 0 0 3.149-1.396c2.95 4.519 5.815 6.912 6.113 7.14 2.736 2.209 6.712 1.781 8.95-.94 2.236-2.708 1.838-6.742-.84-9.007-.5-.427-12.184-10.574-6.742-31.691 1.198-4.675 3.036-10.618 6.556-15.262 12.225-16.104 35.282-24.226 52.481-18.469 10.973 3.663 21.447 12.868 28.315 19.951 8.592 8.864 9.72 19.808 7.111 26.22a6.407 6.407 0 0 0 6.669 8.793c4.132-.471 8.736 2.892 10.047 7.353 1.368 4.631-.327 10.375-4.219 14.321a6.43 6.43 0 0 0-1.639 6.156 6.43 6.43 0 0 0 4.489 4.532c7.152 1.981 15.674 7.353 15.66 21.718 0 9.12-1.639 25.949-12.483 36.351-8.82 8.45-21.717 11.258-37.663 8.265.171-.256.327-.513.471-.797 8.664-17.414 5.556-35.155-8.779-49.932-10.859-11.201-25.251-17.799-37.961-23.613a6.42 6.42 0 0 0-6.214.484 6.42 6.42 0 0 0-2.878 5.53 248 248 0 0 0 3.676 36.28c1.042 5.871 2.465 12.625 6.271 18.54 6.898 10.743 22.201 20.476 33.003 23.684 9.192 2.736 17.229 3.862 24.267 3.862 16.815 0 27.831-6.469 34.671-13.025 13.565-12.996 16.416-31.977 16.429-45.6.015-17.585-9.02-26.419-16.913-30.766z" fill="#fff"/></svg>'''
    }
}

def scaled_font_size(text, max_width=460, base_size=36):
    char_width = base_size * 0.6  # approx 60% of font size in px
    est_width = char_width * len(text)
    if est_width > max_width:
        scale = max_width / est_width
        return int(base_size * scale)
    return base_size

def create_svg(repo_name, platform, output_path):
    # Get CONFIG.
    config = CONFIG[platform]

    svg = ET.Element('svg', {
        'xmlns': "http://www.w3.org/2000/svg",
        'width': '512',
        'height': '512',
        'viewBox': '0 0 512 512'
    })

    defs = ET.SubElement(svg, 'defs')
    # Create the gradient.
    gradient = ET.SubElement(defs, 'linearGradient', {
        'id': 'bgGradient',
        'x1': '0%', 'y1': '0%',
        'x2': '100%', 'y2': '100%'
    })
    ET.SubElement(gradient, 'stop', {
        'offset': f'{config["gradient_1"]}',
        'style': f'stop-color:{config["background_gradient_1"]};stop-opacity:1'
    })
    ET.SubElement(gradient, 'stop', {
        'offset': f'{config["gradient_2"]}',
        'style': f'stop-color:{config["background_gradient_2"]};stop-opacity:1'
    })
    ET.SubElement(gradient, 'stop', {
        'offset': f'{config["gradient_3"]}',
        'style': f'stop-color:{config["background_gradient_3"]};stop-opacity:1'
    })
    ET.SubElement(gradient, 'stop', {
        'offset': '100%',
        'style': f'stop-color:{config["background_color"]};stop-opacity:1'
    })
    # Create the background.
    ET.SubElement(svg, 'rect', {
        'x': '0', 'y': '0',
        'width': '512', 'height': '512',
        'rx': '50', 'ry': '50',
        'fill': 'url(#bgGradient)'
    })

    # ⬇️ LOGO FIX STARTS HERE

    # Scale 300px artwork up to 400px → scale factor = 1.333
    scale = 400 / 300
    # Re-center for new scaled size
    scaled_size = 300 * scale  # = 400
    x_offset = (512 - scaled_size) / 2  # = 56
    y_offset = 20

    logo_group = ET.SubElement(svg, 'g', {
        'transform': f'translate({x_offset},{y_offset}) scale({scale})'
    })

    # Parse inner SVG and extract child elements
    logo_svg = ET.parse(StringIO(config["svg_path"])).getroot()
    for child in logo_svg:
        logo_group.append(child)

    style = ET.SubElement(svg, 'style', {'type': 'text/css'})
    style.text = """
      <![CDATA[
        @font-face {
          font-family: 'Playfair Display';
          font-style: normal;
          font-weight: bold;
          src: url(data:font/woff2;base64,d09GMgABAAAAAJXEABIAAAABUEAAAJVUAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGoJfG4G8ZhyMBD9IVkFSjGwGYD9TVEFUgQ4AhSwvYBEICoHzJIHBKQuEfgAwgaJcATYCJAOJYAQgBYoGB41zW44zcQN1w6RUp/LbLazS8MPOn8xmJiLQHbQkD/KXC7gx1MPGCYCM...UhWJ3mq6ZAHJXAFZzlyBxSnjO6l/Mv3VT+qpZt/XC7ebdJ2TsXCLJQbB2U3+bmActkEVbodsx18YKyyHA0diArblLEs5K8hewbLNGENClglLZkbcePLWAfsZj/ockbksdeeOpZdoxWxB4sSb0RSLENwPIW8tuvoxS+QmY0B9Oz+Tr3QvM8heXiFRYUhTu3mnZd/aKwMA) format('woff2');
        }
      ]]>
    """

    # Add text below the logo
    logo_height = 400
    logo_top = 20
    text_padding = 20
    text_y = logo_top + logo_height + text_padding  # = 440

    # Get variable from scaled_font_size.
    platform_font_size = scaled_font_size(platform)
    # Print the Platform name.
    ET.SubElement(svg, 'text', {
        'x': '50%',
        'y': str(text_y),
        'text-anchor': 'middle',
        'font-size': str(platform_font_size),
        'font-family': 'Playfair Display',
        'font-weight': 'bold',
        'fill': config["foreground_color"]
    }).text = platform

    if repo_name:
        # Get variable from scaled_font_size.
        repo_font_size = scaled_font_size(repo_name)
        # Print the Repo name.
        ET.SubElement(svg, 'text', {
            'x': '50%',
            'y': str(text_y + platform_font_size + 8),  # 8px vertical spacing
            'text-anchor': 'middle',
            'font-size': str(repo_font_size),
            'font-family': 'Playfair Display',
            'font-weight': 'bold',
            'fill': config["foreground_color"]
        }).text = repo_name

    ET.ElementTree(svg).write(output_path)

def convert_svg_to_png(svg_path, png_path):
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=512, output_height=512)

def generate_logo(repo_name, platform):
    if platform not in CONFIG:
        raise ValueError(f"Unknown platform '{platform}'. Valid options: {list(CONFIG.keys())}")

    output_dir = Path("generated_logos")
    output_dir.mkdir(exist_ok=True)

    svg_path = output_dir / f"{platform}-{repo_name}.svg"
    png_path = output_dir / f"{platform}-{repo_name}.png"

    create_svg(repo_name, platform, svg_path)
    convert_svg_to_png(svg_path, png_path)

    print(f"✅ SVG saved to: {svg_path}")
    print(f"✅ PNG saved to: {png_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a repository logo in SVG and PNG formats.")
    parser.add_argument(
        "--repo-name",
        help="The name of the repository. Optional — can be omitted.",
        default=None
    )
    parser.add_argument("--platform", required=True, choices=["Saplings", "Arbor"], help="The branding platform (Saplings or Arbor).")
    args = parser.parse_args()

    generate_logo(args.repo_name, args.platform)
