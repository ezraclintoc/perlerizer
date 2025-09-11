# Pearlerizer

This Python script pixelates images and maps them to a specific color palette, creating a "bead art" effect. It's useful for artists and hobbyists who want to translate digital images into physical bead creations (like Perler beads, Hama beads, etc.).

## How it Works

The script processes images in an `input` folder by:
1.  **Extracting a Color Palette:** It first reads a `palette.png` image to determine the set of available colors.
2.  **Pixelating:** It divides the input image into larger "pixels" (blocks).
3.  **Color Matching:** For each block, it calculates the average color and then finds the closest color from the extracted palette.
4.  **Reconstructing:** It rebuilds the image using the new pixelated and color-matched blocks.
5.  **Saving:** The final image is saved in the `output` folder.

## Requirements

-   Python 3
-   Pillow
-   NumPy

You can install the required libraries using pip:
```bash
pip install -r requirements.txt
```

## Usage

1.  **Create a Palette:** Create an image named `palette.png` (or `.jpg`) that contains all the colors you want to use in your final images. Each unique color in this image will be part of the palette.

2.  **Place Input Images:** Put the images you want to process into the `input` folder.

3.  **Run the Script:**
    ```bash
    python pearlerizer.py
    ```

4.  **Find the Output:** The processed images will be saved in the `output` folder with the same name as the input file (but with a `.png` extension).

## Configuration

You can change the following settings at the top of the `pearlerizer.py` script:

-   `PIXEL_SIZE`: An integer that determines how large the pixelated blocks will be. A higher number means a more "blocky" or abstract image. (Default: `16`)
-   `PALETTE_IMAGE`: The filename of your palette image. (Default: `"palette.png"`)
-   `INPUT_FOLDER`: The name of the folder where your input images are located. (Default: `"input"`)
-   `OUTPUT_FOLDER`: The name of the folder where the processed images will be saved. (Default: `"output"`)

## Example

1.  **`palette.png`:**
    (Imagine a small image with squares of red, green, blue, black, and white)

2.  **`input/my_photo.jpg`:**
    (A regular photograph)

3.  **Run `python pearlerizer.py`**

4.  **`output/my_photo.png`:**
    (A pixelated version of `my_photo.jpg` using only the colors from `palette.png`)
