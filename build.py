import os
import subprocess
import shutil
import argparse
from pathlib import Path

import sass
import rcssmin
from PIL import Image

def compile_styles(scss_src, css_dest):
    """
    Compile SCSS to CSS (expanded and minified) and write to destination.
    """
    # Expanded CSS
    expanded_css = sass.compile(
        filename=str(scss_src),
        output_style='expanded'
    )
    # Write expanded CSS
    css_dest.mkdir(parents=True, exist_ok=True)
    expanded_path = css_dest / 'main.css'
    expanded_path.write_text(expanded_css, encoding='utf-8')
    print(f'Wrote expanded CSS to {expanded_path}')

    # Minified CSS
    minified_css = rcssmin.cssmin(expanded_css)
    minified_path = css_dest / 'main.min.css'
    minified_path.write_text(minified_css, encoding='utf-8')
    print(f'Wrote minified CSS to {minified_path}')

def generate_thumbnails(src_dir, thumb_dir, width=350):
    """
    Resize images in src_dir to given width and save to thumb_dir.
    """
    thumb_dir.mkdir(parents=True, exist_ok=True)
    for img_path in src_dir.glob('*.[jp][pn]g'):
        with Image.open(img_path) as img:
            ratio = width / float(img.width)
            height = int(img.height * ratio)
            thumb = img.resize((width, height), Image.LANCZOS)
            dest_path = thumb_dir / img_path.name
            thumb.save(dest_path)
            print(f'Generated thumbnail {dest_path}')

def build_jekyll(config='_config.yml'):
    """
    Run `jekyll build --config=config`.
    """
    cmd = ['jekyll', 'build', '--config', config]
    print(f'Running: {" ".join(cmd)}')
    subprocess.check_call(cmd)

if __name__ == '__main__':
    # Default behavior: run all steps in order
    # compile_styles(
    #     scss_src=Path('_scss') / 'main.scss',
    #     css_dest=Path('assets') / 'css'
    # )
    # generate_thumbnails(
    #     src_dir=Path('assets') / 'images' / 'hero',
    #     thumb_dir=Path('assets') / 'images' / 'thumbnail'
    # )
    build_jekyll()


