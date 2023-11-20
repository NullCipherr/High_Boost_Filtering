**High Boost Filtering Implementation in Python** 🚀

This repository contains Python implementations of the High Boost Filtering method, an image processing technique used to enhance high-frequency features in an image, resulting in a sharper and more detailed image.

**Method High Boost Filtering** 📸

High Boost Filtering is a technique that combines an original image with a low-frequency filtered version of the same image. Low-frequency filtering is applied to emphasize high-frequency features in the original image. This method is commonly used to increase sharpness and highlight fine details in photographs and images.

**How to Use:**

1. **Image Loading:** 🖼️
   - Use the `load_image` function to load the desired image.

2. **Low-Pass Filtering:** 🎛️
   - The `apply_low_pass_filter` function is used to apply a low-pass filter to the image.

3. **High Boost Filtering:** ✨
   - The `high_boost_filter` function performs High Boost Filtering, combining the original image with the low-frequency filtered image.

4. **Save and Visualize:** 💾
   - Utilize the `save_image` function to save the processed image.
   - Original and processed images can be visualized using the `cv2.imshow` functions.

**Adjustable Parameters:**
- The sharpness factor (`sharpening_factor`) controls the intensity of enhancement. 🎚️

**Examples:**
- The `main.py` file provides a practical example of how to use High Boost Filtering on a specific image.

**Contributions:**
Contributions are welcome! Feel free to propose improvements, corrections, or new features. 🤝

