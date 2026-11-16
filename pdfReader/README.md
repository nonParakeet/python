# PDF Reader

A lightweight desktop PDF reader built with Python. It opens a PDF in a
scrollable window and can move through the document automatically at a pace
you choose.

## Capabilities

- Open PDF files from your computer and browse them with vertical and horizontal
  scrollbars or the mouse wheel.
- Start and pause automatic scrolling with the button or the Space key.
- Change the auto-scroll pace while reading, from 10 to 240 pixels per second.
- Resize the displayed pages from 50% to 200%.
- Adjust brightness and contrast from 0.5 to 1.8.
- Render pages only as they come into view to avoid loading every page image at
  once.

Brightness and contrast affect the displayed page images; they do not modify or
save changes to the PDF file. Password-protected PDFs are not supported.

## Requirements

- Python 3.10 or later
- Tk support for Python (on Debian/Ubuntu, install the `python3-tk` package if
  it is missing)

The required Python packages are listed in `requirements.txt`.

## Install and run

From this directory:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python pdf_reader.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

## Customise your reading settings

Use the **Reading settings** sliders at the top of the window:

- **Scroll pace** sets the automatic movement speed in pixels per second.
- **PDF size** controls the page zoom. Use the horizontal scrollbar if a
  magnified page extends beyond the window.
- **Brightness** changes the lightness of the rendered page.
- **Contrast** changes the difference between light and dark areas.

The settings take effect while you use the reader and reset to their defaults
when you restart it. Resize the application window by dragging its edges; the
minimum window size is 640 by 420 pixels.

## Troubleshooting

- If the app says Tk is unavailable, install your operating system's Tk package
  for Python and try again.
- If a PDF cannot be opened, confirm that it is a valid, unencrypted PDF.
- On a large page or at high zoom, rendering visible pages may take a moment.
