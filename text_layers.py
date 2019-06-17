from base_layers import Layer, PointLayer, ShapeLayer
from exceptions import NotReadyToRenderError

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

class PointTextLayer(PointLayer):
    """
    A PointTextLayer is only defined by an xy coord.
    The text width is limited only by it's parent's width
    """
    def __init__(self, name, font, size, color, *args, **kwargs):
        self.font = font
        self.size = size
        self.color = color
        super().__init__(name, *args, **kwargs)

    def render(self, fresh=False):
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is not None:
            with Drawing() as draw:
                draw.font = self.font
                draw.font_size = self.size
                if not isinstance(self.color, Color):
                    self.color = Color(self.color)
                draw.color = self.color
                draw.text_antialias = True
                # get estimated width and height
                with Image(width=1, height=1) as temp_image:
                    metrics = draw.get_font_metrics(temp_image, self.content)
                    width = int(metrics.text_width)
                    height = int(metrics.text_height)

                img = Image(width=width + 100, height=height + 100)
                draw.text(10, height + 10, self.content)
                draw(img)
            img.trim()
            self.pre_render = img
            return img
        else:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")

class AreaTextLayer(ShapeLayer):
    """TextLayer that has a rect (Shape)."""
    def __init__(self, name, font, size, color, *args, **kwargs):
        self.font = font
        self.size = size
        self.color = color
        super().__init__(name, *args, **kwargs)

    def render(self, fresh=False):
        pass


