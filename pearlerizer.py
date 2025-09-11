from PIL import Image
import numpy as np
import os

# --- CONFIG ---
PIXEL_SIZE = 16      # Default pixelation factor (used if MAX_WIDTH is None)
PALETTE_IMAGE = "palette.png"  # or "palette.jpg"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
MAX_WIDTH = None     # Set to an integer (e.g., 128) → output images will have this width
# --------------


def extract_palette(image_path):
    """Extracts all unique colors from a palette image."""
    img = Image.open(image_path).convert("RGB")
    data = np.array(img)
    pixels = data.reshape(-1, 3)
    unique_colors = np.unique(pixels, axis=0)
    return np.array(unique_colors)


def closest_palette_color_block(avg_colors, palette):
    """Map block average colors to nearest palette colors (vectorized)."""
    diffs = avg_colors[:, None, :] - palette[None, :, :]
    distances = np.sum(diffs ** 2, axis=2)
    nearest_idx = np.argmin(distances, axis=1)
    return palette[nearest_idx]


def pixelate_with_palette(img, palette, pixel_size):
    """Pixelate by averaging each block and mapping to closest palette color."""
    data = np.array(img)
    h, w, _ = data.shape

    # Pad to be divisible by pixel_size
    pad_h = (pixel_size - h % pixel_size) % pixel_size
    pad_w = (pixel_size - w % pixel_size) % pixel_size
    if pad_h or pad_w:
        data = np.pad(data, ((0, pad_h), (0, pad_w), (0, 0)), mode='edge')
        h, w, _ = data.shape

    # Reshape into blocks
    data_blocks = data.reshape(h // pixel_size, pixel_size, w // pixel_size, pixel_size, 3)
    avg_colors = data_blocks.mean(axis=(1, 3)).reshape(-1, 3)

    # Map each block’s average to nearest palette color
    mapped_colors = closest_palette_color_block(avg_colors, palette)

    # Reconstruct pixelated image
    mapped_blocks = mapped_colors.reshape(h // pixel_size, w // pixel_size, 3)
    output = np.repeat(np.repeat(mapped_blocks, pixel_size, axis=0), pixel_size, axis=1)

    # Crop back to original size if padded
    output = output[:img.height, :img.width]

    return Image.fromarray(output.astype(np.uint8))


def get_dynamic_pixel_size(img, max_width, default_size):
    """Compute pixel size so output image width = max_width."""
    if max_width:
        return max(1, img.width // max_width)
    return default_size


if __name__ == "__main__":
    # Load palette once
    PALETTE = extract_palette(PALETTE_IMAGE)

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Process all images in input folder
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(filename)[0] + ".png")

            print(f"Processing {filename}...")
            img = Image.open(input_path).convert("RGB")

            # Compute pixel size dynamically if MAX_WIDTH is set
            pixel_size = get_dynamic_pixel_size(img, MAX_WIDTH, PIXEL_SIZE)

            # Pixelate with palette mapping
            img_mapped = pixelate_with_palette(img, PALETTE, pixel_size)

            # If MAX_WIDTH is set, resize final image to exactly MAX_WIDTH
            if MAX_WIDTH:
                ratio = MAX_WIDTH / img_mapped.width
                new_height = int(img_mapped.height * ratio)
                img_mapped = img_mapped.resize((MAX_WIDTH, new_height), Image.NEAREST)

            img_mapped.save(output_path)

    print("Done! Processed images are in the 'output' folder.")
