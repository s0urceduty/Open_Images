from PIL import Image
import open_images as oi

image = Image.open("portrait.jpg")

regions = [(50, 50, 300, 300), (350, 100, 600, 400)]
colorized = oi.area_colorize(image, regions, (255, 0, 0))
styled = oi.apply_duotone(colorized, (20, 20, 20), (255, 200, 0))

styled.save("output_duotone.png")
