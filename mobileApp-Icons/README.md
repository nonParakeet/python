# Field Kit Icon Studio

A small, local Django web app for designing and downloading eight original, 3D-style mobile app icons. Use the JavaScript controls to choose a symbol and color; the studio draws a 512 × 512 PNG in your browser. The icons are artwork, not apps or installable packages.

## Run locally

Requires Python 3.10 or newer.

```bash
cd mobileApp-Icons
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/> in a current browser. The development server is bound to the local computer and is not intended for public deployment.

## Design and download

1. Select an icon: Phone, Messages, Contacts, Camera, Maps, Music, Shield, or Folder.
2. Select one of the five color swatches. The preview and icon catalogue update immediately.
3. Choose **Download PNG**. The resulting `field-kit-<icon>.png` is a 512 × 512 PNG with a transparent background.

The drawing happens in your browser. The Django server serves the studio and its static assets; it does not upload, store, or transmit your designs.

## Put an icon on a phone

These are launcher images, not executable files and not complete mobile apps. Copying a PNG to a phone or portable drive does **not** install an app or make the icon launch a feature by itself.

1. Download the PNG on your computer.
2. Copy it to a USB drive, microSD card, or other portable storage. Eject the storage safely.
3. Connect the storage to the phone using its card slot or a compatible USB adapter, then copy the PNG into a folder such as `Pictures/Icons`.
4. On Android, use a launcher that supports custom icon images (or an icon-pack/shortcut tool), select the existing app or shortcut, and choose the copied PNG. Exact menus depend on the phone and launcher.
5. On iPhone, custom artwork can generally be used for a Home Screen shortcut through the Shortcuts app; it does not replace the original app icon everywhere. Menus vary by iOS release.

For a burner phone, first confirm that the handset supports the storage connection and launcher customization you intend to use. Only install apps from sources you trust, and don't treat a custom icon as a privacy or security feature.

## Project layout

- `manage.py` and `iconstudio/` — Django project and local page route.
- `studio/` — Django view.
- `templates/studio/index.html` — studio interface.
- `static/studio/` — responsive styling and canvas-based icon renderer.
