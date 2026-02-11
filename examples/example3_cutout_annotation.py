from PIL import Image
import open_images as oi

image = Image.open("product.jpg")

cutout = oi.create_cutout(image, region=(100, 100, 500, 500))
shaded = oi.shade_spot(cutout, position=(300, 300), intensity=0.6)
annotated = oi.place_arrow(shaded, start=(50, 50), end=(250, 250))

annotated.save("output_product_highlight.png")
