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
    },
    "Shrubs": {
        "background_gradient_1": "#ff7d55",
        "background_gradient_2": "#ff7d55",
        "background_gradient_3": "#789a3d",
        "background_color": "#789a3d",
        "foreground_color": "#ffffff",
        "gradient_1": "0%",
        "gradient_2": "35%",
        "gradient_3": "100%",
        "svg_path": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="300" height="300"><path d="M88.406 244.533c-2.535 -0.443 -5.09 -0.825 -7.646 -1.127 -19.093 -2.354 -113.697 -24.506 -62.955 -92.169 36.216 -48.287 85.288 27.001 84.503 28.168s-54.323 -74.464 -16.096 -114.703C114.643 34.763 219.829 51.161 203.25 112.989c-12.414 46.276 -22.474 68.407 -22.474 68.407s28.168 -76.455 72.431 -78.467c59.153 -2.696 61.144 122.208 -10.06 138.827 -60.359 14.084 -135.648 6.096 -154.742 2.776" fill="none" stroke="#ffffff" stroke-linecap="round" stroke-linejoin="round" stroke-width="6.036"/></svg>'''
    },
    "Drupal AI": {
        "background_gradient_1": "#0678be",
        "background_gradient_2": "#0678be",
        "background_gradient_3": "#08447a",
        "background_color": "#08447a",
        "foreground_color": "#ffffff",
        "gradient_1": "0%",
        "gradient_2": "35%",
        "gradient_3": "100%",
        "svg_path": '''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><path fill="#FFFFFF" d="M66.237 153.4c.9 4.062 1.773 7.971 2.606 11.888.271 1.274-.218 2.085-1.48 2.665-4.355 2.005-8.776 3.659-13.662 3.77-.637.014-1.494.552-1.853 1.105-2.99 4.617-7.054 8.036-11.729 10.895-4.693-2.934-8.847-6.359-11.821-11.084-.307-.488-1.126-.91-1.717-.922-5.097-.102-9.725-1.799-14.16-4.104-.53-.277-1.042-1.243-1.006-1.857.282-4.847 1.054-9.609 3.433-13.934.56-1.02.488-1.767-.042-2.748-2.312-4.28-3.053-8.974-3.446-13.75-.087-1.052.227-1.663 1.258-2.169 4.504-2.209 9.15-3.799 14.22-3.994.522-.02 1.21-.481 1.502-.94 2.693-4.224 6.33-7.47 10.494-10.138.606-.388 1.853-.453 2.439-.086 4.251 2.661 7.932 5.952 10.664 10.235.31.486 1.108.904 1.697.93 5 .216 9.608 1.778 13.984 4.054.62.323 1.21 1.42 1.189 2.139-.128 4.39-.823 8.74-2.865 12.646-1.051 2.01-1.004 3.553.295 5.399m-1.642 9.914c-.543-4.156-1.527-8.139-4.032-11.636-2.2-3.072-7.928-4.723-11.304-2.365.931 5.013-1.112 8.57-5.443 10.934.942 4.35 4.333 7.202 8.593 7.391 3.992.177 7.68-.962 11.262-2.525.443-.194.639-.955.924-1.799M52.42 133.259c-4.468.358-7.273 2.815-8.582 6.995-.182.58.125 1.543.546 2.038.904 1.06 2.031 1.93 3.208 3.006 4.845-2.015 9.68-1.466 14.301 1.793 1.68-3.235 2.44-6.59 2.709-10.061.03-.395-.544-1.116-.956-1.22-3.607-.914-7.24-1.722-11.226-2.551m-33.523 14.76c2.8 4.357 7.287 5.833 11.573 3.944l1.423-5.374c-4.21-3.339-6.083-7.768-5.568-13.316-3.656.222-6.937 1.24-10.067 2.755-.347.169-.664 1.014-.551 1.424.946 3.458 1.996 6.887 3.19 10.568m11.432-13.597c-.236 3.843 1.27 6.804 4.152 8.937 3.324-2.112 5.934-4.465 7.164-8.055.265-.773.96-1.478 1.616-2.023 1.506-1.25 3.11-2.383 5.037-3.837-2.41-2.237-4.77-4.487-7.219-6.638-.348-.306-1.316-.392-1.67-.133-4.047 2.967-7.704 6.277-9.08 11.75m-7.12 32.824c1.738.115 3.483.393 5.21.31 3.982-.188 7.225-3.212 7.999-7.25-.859-.618-1.972-1.069-2.533-1.895-1.345-1.977-2.868-2.271-5.188-1.825-3.744.719-7.26-.432-10.748-3.07-.807 3.494-1.508 6.616-2.256 9.726-.276 1.152.135 1.725 1.25 2.048 1.991.577 3.952 1.255 6.267 1.956m13.856.435-5.046 3.772 8.13 7.846 8.4-8.162c-4.208-1.728-6.781-4.443-8.288-8.038-1.043 1.501-2.033 2.926-3.196 4.582m-2.147-15.137c.661 2.446 2.207 3.97 4.748 4.237 2.296.241 4.021-.838 5.132-2.804 1.259-2.226.612-4.269-.858-6.134-1.074-1.362-2.21-2.675-3.234-3.907-4.128 2.716-5.881 5.33-5.788 8.608Z"/><path fill="#FFFFFF" d="M110.724 160.363c-2.891 4.947-7.211 7.36-12.665 7.571-4.967.193-9.948.041-15.072.041V133.71c1.686 0 3.406-.018 5.126.004 3.495.043 7.022-.174 10.478.219 8.492.963 13.726 6.636 14.391 15.196.304 3.903-.332 7.626-2.258 11.235m-21.49-2.696v4.438c2.51 0 4.8.095 7.08-.018 5.725-.286 9.022-2.958 9.85-8.177.31-1.952.296-4.029.01-5.987-.66-4.508-3.566-7.495-8.05-8.029-2.891-.344-5.857-.064-8.89-.064v17.837ZM192.702 163.2c-4.306 6.061-9.77 6.771-17.662 2.277v13.212h-5.908v-36.4h5.674l.143 2.141c2.475-.874 4.94-2.326 7.507-2.54 7.466-.626 13.157 5.913 12.41 14.144-.216 2.391-1.363 4.698-2.164 7.166m-15.404-1.918c1.737 1.474 3.717 2.098 5.974 1.638 4.496-.917 6.875-5.809 5.298-10.86-.855-2.736-3.222-4.648-6.027-4.867-2.977-.232-5.672 1.238-6.844 3.95-1.537 3.553-1.224 6.922 1.6 10.139ZM251.952 160.232h-3.025c-3.439 0-3.439 0-4.678 3.33-1.686 4.525-1.686 4.524-6.474 4.48-.465-.004-.931 0-1.648 0 1.722-4.46 3.363-8.742 5.028-13.014 2.506-6.427 5.093-12.824 7.5-19.288.592-1.59 1.324-2.14 3.02-2.07 3.794.153 3.796.057 5.149 3.563 3.786 9.81 7.575 19.621 11.36 29.433.14.364.25.74.463 1.375-2.028 0-3.884.078-5.726-.055-.463-.034-1.057-.666-1.28-1.162-.712-1.588-1.42-3.205-1.859-4.881-.39-1.494-1.193-1.83-2.586-1.737-1.674.11-3.361.026-5.244.026m-2.419-10.642-1.85 4.986h9.211l-4.548-12.863a920.643 920.643 0 0 0-2.813 7.877ZM207.583 147.329c-1.78.892-3.4 1.757-5.002 2.611l-3.356-3.469c3.531-4.362 10.679-6.2 16.052-3.851 2.894 1.265 4.61 3.577 4.676 6.726.13 6.165.038 12.334.038 18.599h-5.578l-.158-2.132c-.56.33-1.05.588-1.508.893-2.81 1.866-5.848 2.284-9.031 1.273-3.424-1.088-5.446-3.944-5.407-7.4.04-3.623 1.887-6.279 5.515-7.238 2.24-.592 4.62-.676 6.945-.902 1.114-.109 2.247-.019 3.33-.019.54-3.87-2.074-5.868-6.516-5.091m6.755 11.516v-1.75c-2.485 0-4.827-.193-7.12.057-2.136.232-3.334 1.949-3.084 3.746.239 1.711 1.699 2.945 3.85 2.63 1.775-.26 3.55-.992 5.134-1.862.66-.362.828-1.623 1.22-2.82Z"/><path fill="#FFFFFF" d="M159.863 142.19h2.32v25.727h-5.789v-3.391c-2.473 2.465-4.994 4-8.298 3.945-4.74-.08-8.26-2.73-8.749-7.439-.45-4.328-.294-8.72-.38-13.083-.036-1.811-.006-3.624-.006-5.601h6.061c0 3.225-.02 6.492.007 9.758.018 2.08-.073 4.185.204 6.235.467 3.45 2.603 5.197 5.682 4.972 3.213-.235 5.306-2.508 5.333-5.925.04-4.973.01-9.947.01-15.198h3.605Z"/><path fill="#FFFFFF" d="m272.73 166.27.001-3.932h5.423v-22.817h-5.304v-5.676h17.35v5.545h-5.416v22.835h5.41v5.813c-5.49 0-10.92-.028-16.348.02-1.322.01-1.12-.808-1.116-1.787ZM120.387 168.042c-.67-.356-1.555-.708-1.559-1.067-.078-8.177-.06-16.354-.06-24.66h5.928v4.08c2.91-3.746 6.104-5.585 10.694-4.208l-1.503 6.333c-1.402-.103-2.683-.396-3.91-.248-3.02.365-5.092 3.035-5.128 6.478-.044 4.353-.01 8.707-.01 13.292h-4.452ZM226.173 153.432V131.94h5.968v35.988h-5.968v-14.496Z"/></svg>'''
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
    parser.add_argument("--platform", required=True, choices=["Saplings", "Arbor", "Shrubs", "Drupal AI"], help="The branding platform (Saplings, Arbor, Shrubs, Drupal AI).")
    args = parser.parse_args()

    generate_logo(args.repo_name, args.platform)
