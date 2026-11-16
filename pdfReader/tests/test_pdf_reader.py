import unittest

import pymupdf as fitz

from pdf_reader import render_page_image, scroll_pixels_per_tick


class ScrollPaceTests(unittest.TestCase):
    def test_pace_is_converted_to_pixels_per_50_millisecond_tick(self) -> None:
        self.assertEqual(scroll_pixels_per_tick(40), 2)
        self.assertEqual(scroll_pixels_per_tick(240), 12)

    def test_slowest_pace_moves_at_least_one_pixel_per_tick(self) -> None:
        self.assertEqual(scroll_pixels_per_tick(10), 1)


class PageRenderingTests(unittest.TestCase):
    def test_zoom_controls_rendered_page_dimensions(self) -> None:
        document = fitz.open()
        try:
            page = document.new_page(width=100, height=200)
            image = render_page_image(page, 50, 1, 1)
            self.assertEqual(image.size, (50, 100))
        finally:
            document.close()

    def test_brightness_changes_rendered_page_pixels(self) -> None:
        document = fitz.open()
        try:
            page = document.new_page(width=100, height=100)
            normal = render_page_image(page, 100, 1, 1)
            dimmed = render_page_image(page, 100, 0.5, 1)
            self.assertEqual(normal.getpixel((10, 10)), (255, 255, 255))
            self.assertEqual(dimmed.getpixel((10, 10)), (127, 127, 127))
        finally:
            document.close()


if __name__ == "__main__":
    unittest.main()
