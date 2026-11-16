"""A small desktop PDF reader with adjustable auto-scrolling and display settings."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pymupdf as fitz
from PIL import Image, ImageEnhance, ImageTk


SCROLL_INTERVAL_MS = 50
PAGE_MARGIN = 20
PAGE_GAP = 18


def scroll_pixels_per_tick(speed: float) -> int:
    return max(1, round(speed * SCROLL_INTERVAL_MS / 1000))


def render_page_image(
    page: fitz.Page, zoom: float, brightness: float, contrast: float
) -> Image.Image:
    scale = zoom / 100
    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    image = Image.open(BytesIO(pixmap.tobytes("png"))).convert("RGB")
    image = ImageEnhance.Brightness(image).enhance(brightness)
    return ImageEnhance.Contrast(image).enhance(contrast)


class PdfReaderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDF Reader")
        self.root.geometry("1100x800")
        self.root.minsize(640, 420)

        self.document: fitz.Document | None = None
        self.pdf_path: Path | None = None
        self.page_layout: list[tuple[float, float, float, float]] = []
        self.page_rect_items: list[int] = []
        self.page_image_items: dict[int, int] = {}
        self.page_images: dict[int, ImageTk.PhotoImage] = {}
        self.rendered_settings: dict[int, tuple[float, float, float]] = {}
        self._render_job: str | None = None
        self._scroll_job: str | None = None
        self._scrolling = False

        self.zoom = tk.DoubleVar(value=100)
        self.brightness = tk.DoubleVar(value=1.0)
        self.contrast = tk.DoubleVar(value=1.0)
        self.scroll_speed = tk.DoubleVar(value=40)

        self._build_interface()
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.root.bind("<space>", self._toggle_scroll)

    def _build_interface(self) -> None:
        toolbar = ttk.Frame(self.root, padding=(10, 8))
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="Open PDF", command=self._open_pdf).pack(side="left")
        self.scroll_button = ttk.Button(
            toolbar, text="Start auto-scroll", command=self._toggle_scroll
        )
        self.scroll_button.pack(side="left", padx=(8, 0))
        self.file_label = ttk.Label(toolbar, text="No PDF selected")
        self.file_label.pack(side="left", padx=12)

        settings = ttk.LabelFrame(self.root, text="Reading settings", padding=(10, 6))
        settings.pack(fill="x", padx=10, pady=(0, 8))
        self._add_slider(settings, "Scroll pace", self.scroll_speed, 10, 240, "px/s")
        self._add_slider(settings, "PDF size", self.zoom, 50, 200, "%")
        self._add_slider(settings, "Brightness", self.brightness, 0.5, 1.8, "")
        self._add_slider(settings, "Contrast", self.contrast, 0.5, 1.8, "")

        viewer = ttk.Frame(self.root)
        viewer.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.canvas = tk.Canvas(
            viewer,
            background="#3b3b3b",
            highlightthickness=0,
            xscrollincrement=20,
            yscrollincrement=1,
        )
        vertical = ttk.Scrollbar(viewer, orient="vertical", command=self.canvas.yview)
        horizontal = ttk.Scrollbar(viewer, orient="horizontal", command=self.canvas.xview)
        self._vertical_scrollbar = vertical
        self.canvas.configure(
            xscrollcommand=horizontal.set,
            yscrollcommand=self._on_canvas_scroll,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        viewer.rowconfigure(0, weight=1)
        viewer.columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", lambda _event: self._schedule_render())
        self.canvas.bind("<MouseWheel>", self._mousewheel)
        self.canvas.bind("<Button-4>", lambda _event: self.canvas.yview_scroll(-3, "units"))
        self.canvas.bind("<Button-5>", lambda _event: self.canvas.yview_scroll(3, "units"))

    def _add_slider(
        self,
        parent: ttk.LabelFrame,
        label: str,
        variable: tk.DoubleVar,
        minimum: float,
        maximum: float,
        suffix: str,
    ) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label, width=13).pack(side="left")
        value_label = ttk.Label(row, width=8, anchor="e")
        value_label.pack(side="right")

        def update(value: str) -> None:
            number = float(value)
            shown = f"{number:.0f}" if suffix == "%" or suffix == "px/s" else f"{number:.1f}"
            value_label.configure(text=f"{shown}{suffix}")
            if variable in (self.brightness, self.contrast):
                self._refresh_visible_pages()
            elif variable is self.zoom:
                self._rebuild_page_layout()

        ttk.Scale(
            row,
            from_=minimum,
            to=maximum,
            variable=variable,
            command=update,
        ).pack(side="left", fill="x", expand=True, padx=8)
        update(str(variable.get()))

    def _open_pdf(self) -> None:
        selected = filedialog.askopenfilename(
            title="Open a PDF",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")),
        )
        if not selected:
            return

        try:
            document = fitz.open(selected)
        except (OSError, RuntimeError, ValueError) as error:
            messagebox.showerror("Unable to open PDF", str(error), parent=self.root)
            return

        if document.needs_pass:
            document.close()
            messagebox.showerror(
                "Password-protected PDF",
                "This reader does not currently open password-protected PDFs.",
                parent=self.root,
            )
            return

        self._stop_scroll()
        if self.document is not None:
            self.document.close()
        self.document = document
        self.pdf_path = Path(selected)
        self.file_label.configure(
            text=f"{self.pdf_path.name}  ·  {len(self.document)} pages"
        )
        self.root.title(f"{self.pdf_path.name} - PDF Reader")
        self._rebuild_page_layout()
        self.canvas.yview_moveto(0)
        self._schedule_render()

    def _rebuild_page_layout(self) -> None:
        if self.document is None:
            return

        self._clear_rendered_pages()
        for item in self.page_rect_items:
            self.canvas.delete(item)
        scale = self.zoom.get() / 100
        dimensions = [
            (page.rect.width * scale, page.rect.height * scale)
            for page in self.document
        ]
        widest_page = max((width for width, _height in dimensions), default=0)
        y = PAGE_MARGIN
        self.page_layout = []
        self.page_rect_items = []

        for width, height in dimensions:
            x = PAGE_MARGIN + (widest_page - width) / 2
            self.page_layout.append((x, y, width, height))
            self.page_rect_items.append(
                self.canvas.create_rectangle(
                    x, y, x + width, y + height, fill="white", outline="#bcbcbc"
                )
            )
            y += height + PAGE_GAP

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                widest_page + PAGE_MARGIN * 2,
                max(PAGE_MARGIN, y - PAGE_GAP + PAGE_MARGIN),
            )
        )
        self._schedule_render()

    def _on_canvas_scroll(self, first: str, last: str) -> None:
        self._vertical_scrollbar.set(first, last)
        self._schedule_render()

    def _schedule_render(self) -> None:
        if self.document is None:
            return
        if self._render_job is not None:
            self.root.after_cancel(self._render_job)
        self._render_job = self.root.after(70, self._render_visible_pages)

    def _render_visible_pages(self) -> None:
        self._render_job = None
        if self.document is None:
            return

        top = self.canvas.canvasy(0)
        bottom = top + self.canvas.winfo_height()
        visible: set[int] = set()
        settings = (self.zoom.get(), self.brightness.get(), self.contrast.get())

        for index, (x, y, width, height) in enumerate(self.page_layout):
            if y + height < top - height or y > bottom + height:
                continue
            visible.add(index)
            if self.rendered_settings.get(index) == settings:
                continue

            page = self.document.load_page(index)
            image = render_page_image(
                page,
                self.zoom.get(),
                self.brightness.get(),
                self.contrast.get(),
            )
            photo = ImageTk.PhotoImage(image)

            if index in self.page_image_items:
                self.canvas.delete(self.page_image_items[index])
            self.page_image_items[index] = self.canvas.create_image(
                x, y, anchor="nw", image=photo
            )
            self.page_images[index] = photo
            self.rendered_settings[index] = settings

        for index in tuple(self.page_image_items):
            if index not in visible:
                self.canvas.delete(self.page_image_items.pop(index))
                self.page_images.pop(index, None)
                self.rendered_settings.pop(index, None)

    def _refresh_visible_pages(self) -> None:
        if self.document is None:
            return
        self._clear_rendered_pages()
        self._schedule_render()

    def _clear_rendered_pages(self) -> None:
        for item in self.page_image_items.values():
            self.canvas.delete(item)
        self.page_image_items.clear()
        self.page_images.clear()
        self.rendered_settings.clear()

    def _toggle_scroll(self, _event: tk.Event | None = None) -> None:
        if self.document is None:
            return
        if self._scrolling:
            self._stop_scroll()
        else:
            self._scrolling = True
            self.scroll_button.configure(text="Pause auto-scroll")
            self._scroll_tick()

    def _stop_scroll(self) -> None:
        self._scrolling = False
        if self._scroll_job is not None:
            self.root.after_cancel(self._scroll_job)
            self._scroll_job = None
        self.scroll_button.configure(text="Start auto-scroll")

    def _scroll_tick(self) -> None:
        if not self._scrolling:
            return
        pixels = scroll_pixels_per_tick(self.scroll_speed.get())
        self.canvas.yview_scroll(pixels, "units")
        if self.canvas.yview()[1] >= 1.0:
            self._stop_scroll()
            return
        self._scroll_job = self.root.after(SCROLL_INTERVAL_MS, self._scroll_tick)

    def _mousewheel(self, event: tk.Event) -> str:
        amount = -1 * round(event.delta / 120)
        self.canvas.yview_scroll(amount, "units")
        return "break"

    def _close(self) -> None:
        self._stop_scroll()
        if self._render_job is not None:
            self.root.after_cancel(self._render_job)
        if self.document is not None:
            self.document.close()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    PdfReaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
