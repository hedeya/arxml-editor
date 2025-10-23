#!/usr/bin/env python3
"""Convert SVG files to PNG using CairoSVG with options for DPI and size.

Usage: svg_to_png.py --dpi 150 --width 1600 --height 1200 input.svg output.png
If only dpi is provided, width/height are derived from the SVG viewBox and dpi.
"""
import sys
import os
import argparse


def ensure_cairosvg():
    try:
        import cairosvg  # type: ignore
        return cairosvg
    except Exception:
        print('CairoSVG not found. Please install with: pip install cairosvg')
        raise


def convert(infile: str, outfile: str, dpi: int = 150, width: int = None, height: int = None):
    cairosvg = ensure_cairosvg()
    # CairoSVG accepts output_width/output_height in pixels
    kwargs = {}
    if width:
        kwargs['output_width'] = int(width)
    if height:
        kwargs['output_height'] = int(height)
    # scale from dpi: 96dpi is default SVG px baseline for many renderers; use scale = dpi/96
    if dpi and not (width or height):
        scale = float(dpi) / 96.0
        kwargs['scale'] = scale
    print(f'Converting {infile} -> {outfile} with dpi={dpi}, width={width}, height={height} kwargs={kwargs}')
    cairosvg.svg2png(url=infile, write_to=outfile, **kwargs)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input', help='Input SVG file (or directory)')
    p.add_argument('output', help='Output PNG file or directory')
    p.add_argument('--dpi', type=int, default=150)
    p.add_argument('--width', type=int, help='Output width in pixels')
    p.add_argument('--height', type=int, help='Output height in pixels')
    args = p.parse_args()

    if os.path.isdir(args.input):
        infiles = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.lower().endswith('.svg')]
        if os.path.isdir(args.output):
            for f in infiles:
                outname = os.path.splitext(os.path.basename(f))[0] + '.png'
                outpath = os.path.join(args.output, outname)
                convert(f, outpath, dpi=args.dpi, width=args.width, height=args.height)
        else:
            print('When input is a directory, output must be a directory')
            sys.exit(2)
    else:
        if os.path.isdir(args.output):
            outpath = os.path.join(args.output, os.path.splitext(os.path.basename(args.input))[0] + '.png')
        else:
            outpath = args.output
        convert(args.input, outpath, dpi=args.dpi, width=args.width, height=args.height)


if __name__ == '__main__':
    main()
