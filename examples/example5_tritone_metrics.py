from PIL import Image
import open_images as oi

image = Image.open("landscape.jpg")

limited = oi.limit_workspace(image, region=(200, 150, 1000, 700))
metrics = oi.analyze_color_metrics(limited)
styled = oi.apply_tritone(limited, (0, 50, 120), (120, 180, 220), (255, 255, 240))

styled.save("output_tritone_landscape.png")

print(metrics)
