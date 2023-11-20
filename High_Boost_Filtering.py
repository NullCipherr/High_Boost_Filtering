import cv2
import numpy as np
import os

###################################################################################################

# Define image_path with the path of the input image
image_path = 'Image_004.jpg'

# Define the sharpening factor, which controls the increase in image sharpness
sharpening_factor = 4

###################################################################################################

def load_image(image_filename):
    try:
        # Build the full path of the image using the "Input_Images" folder in the same directory
        image_path = os.path.join('Input_Images', image_filename)
        
        # Load the image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is not None:
            print(f"Image {image_filename} loaded successfully!")
            return image, os.path.splitext(image_filename)[0]  # Return the image name without extension
        else:
            print(f"Could not load the image {image_filename}. Check the path.")
            return None, None
    except Exception as e:
        print(f"Error loading the image: {str(e)}")
        return None, None

def apply_low_pass_filter(image, kernel_size, sigma):
    # Calculate the offset based on the kernel size
    offset = kernel_size // 2

    # Generate 2D matrices to represent the x and y coordinates relative to the kernel center
    x, y = ((np.arange(-offset, offset + 1).reshape(1, -1), np.arange(-offset, offset + 1).reshape(-1, 1)))

    # Calculate the Gaussian kernel based on the x and y coordinates
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)  # Normalize the kernel so that it sums to 1

    # Apply the 2D filter using the Gaussian kernel on the image
    filtered_image = cv2.filter2D(image, -1, kernel)

    return filtered_image

def high_boost_filter(image, sharpening_factor, image_name):
    # Apply a low-pass filter to the image
    filtered_image = apply_low_pass_filter(image, kernel_size=5, sigma=1)
    
    # Combine the original image with the filtered image
    sharpened_image = cv2.addWeighted(image, 1 + sharpening_factor, filtered_image, -sharpening_factor, 0)
    
    return sharpened_image, image_name

def save_image(image, output_filename):
    # Build the full output path using the "Output_Images" folder in the same directory
    output_path = os.path.join('Output_Images', output_filename + '_Sharpened.jpg')

    # Save the image at the specified output path
    cv2.imwrite(output_path, image)
    print(f"Image saved at {output_path}")

def main():
    # Load the input image and get the image name
    loaded_image, image_name = load_image(image_path)
    
    if loaded_image is not None:
        # Apply the high-boost filter
        sharpened_image, image_name = high_boost_filter(loaded_image, sharpening_factor, image_name)
    
        # Save the sharpened image based on the original image name
        save_image(sharpened_image, image_name)
        
        # Display the original image and the image with increased sharpness
        cv2.imshow('Original Image', loaded_image)
        cv2.imshow('Image with Increased Sharpness', sharpened_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
