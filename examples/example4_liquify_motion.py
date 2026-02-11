from PIL import Image
import open_images as oi

image = Image.open("action.jpg")

distorted = oi.liquify_shape(image, center=(400, 300), strength=0.8)
motion = oi.add_motion_blur_lines(distorted, angle=45, density=30)
outlined = oi.outline_areas(motion, threshold=120)

outlined.save("output_dynamic_effect.png")
