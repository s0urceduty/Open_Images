import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve


def create_background(width, height):
    return np.full((height, width, 3), 255, dtype=np.float32)


def draw_vertical_lines(img, xs, thickness, top=160, bottom_pad=140):
    h = img.shape[0]
    for x in xs:
        img[top:h-bottom_pad, x-thickness//2:x+thickness//2] = 0
    return img


def horizontal_motion_kernel(k):
    if k < 3:
        k = 3
    if k % 2 == 0:
        k += 1
    kernel = np.zeros((1, k), dtype=np.float32)
    kernel[0, :] = 1.0 / k
    return kernel


def motion_line(base_img, x_center, thickness, extent, k, top=160, bottom_pad=140):
    h, w = base_img.shape[:2]

    kernel = horizontal_motion_kernel(k)

    blurred = np.zeros_like(base_img)
    for c in range(3):
        blurred[:, :, c] = convolve(base_img[:, :, c], kernel, mode='nearest')

    mask = np.zeros((h, w), dtype=np.float32)

    y1 = top
    y2 = h - bottom_pad

    x_right_edge = x_center + thickness // 2
    x1 = max(0, x_right_edge)
    x2 = min(w, x_right_edge + extent)

    if x2 <= x1:
        return base_img

    gradient = np.linspace(1.0, 0.0, x2 - x1)
    mask[y1:y2, x1:x2] = gradient[None, :]

    mask3 = np.dstack([mask, mask, mask])

    blended = blurred * mask3 + base_img * (1 - mask3)
    return blended


def main():
    width = 1400
    height = 700

    line_count = 5
    thickness = 80

    spacing = width // (line_count + 1)
    xs = [spacing * i for i in range(1, line_count + 1)]

    extents = [120, 250, 400, 600, 850]
    kernels = [11, 31, 61, 101, 151]

    labels = [
        "Light Motion",
        "Moderate Motion",
        "Strong Motion",
        "Heavy Motion",
        "Extreme Motion"
    ]

    img = create_background(width, height)

    img = draw_vertical_lines(img, xs, thickness)

    for x, extent, k in zip(xs, extents, kernels):
        img = motion_line(img, x, thickness, extent, k)

    img = np.clip(img, 0, 255).astype(np.uint8)

    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img)
    ax.axis("off")

    for x, label in zip(xs, labels):
        ax.text(
            x,
            80,
            label,
            fontsize=11,
            ha='center',
            va='bottom'
        )

    out_path = os.path.join(os.getcwd(), "motion_line_corrected.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    try:
        os.startfile(out_path)
    except Exception:
        pass


if __name__ == "__main__":
    main()
