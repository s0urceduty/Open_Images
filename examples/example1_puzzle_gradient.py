from PIL import Image
import open_images as oi

image = Image.open("input.jpg")

piece = oi.puzzle_crop(image, "triangle")
focused = oi.radial_target(piece, center=(200, 200), radius=180)
gradient = oi.apply_gradient(focused, direction="vertical")

gradient.save("output_puzzle_gradient.png")
