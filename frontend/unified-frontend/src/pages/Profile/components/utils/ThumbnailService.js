// /src/pages/Profile/components/utils/ThumbnailService.js
// SentinelOps — Client-side Thumbnail Generator (256x256, Cropped Output)
// Deterministic, lossless, React Easy Crop–aligned

/**
 * Creates a cropped + resized thumbnail from an image source.
 *
 * @param {string} imageSrc - DataURL of the original image
 * @param {Object} croppedAreaPixels - Pixel coordinates from React Easy Crop
 * @param {number} outputWidth - Output width (default 256)
 * @param {number} outputHeight - Output height (default 256)
 * @returns {Promise<{ blob: Blob }>}
 */
export async function createThumbnailFromFile(
  imageSrc,
  croppedAreaPixels,
  outputWidth = 256,
  outputHeight = 256
) {
  const image = await loadImage(imageSrc);

  // Create canvas for final thumbnail
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = outputWidth;
  canvas.height = outputHeight;

  const { x, y, width: cropW, height: cropH } = croppedAreaPixels;

  // Draw cropped region → scaled to output size
  ctx.drawImage(
    image,
    x,
    y,
    cropW,
    cropH,
    0,
    0,
    outputWidth,
    outputHeight
  );

  // Convert to Blob (lossless PNG)
  const blob = await new Promise((resolve) =>
    canvas.toBlob((b) => resolve(b), "image/png", 1.0)
  );

  return { blob };
}

/**
 * Loads an image from a DataURL.
 */
function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();

    // Prevent canvas tainting
    img.crossOrigin = "anonymous";

    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}
