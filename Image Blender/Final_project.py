import numpy as np
import matplotlib.pyplot as plt
#getting the coordinates from the images
def get_click_coordinates(image):
    x_click, y_click = None, None

    def onclick(event):
        nonlocal x_click, y_click
        x_click, y_click = event.xdata, event.ydata
        plt.close()

    plt.imshow(image, cmap='gray')
    cid = plt.connect('button_press_event', onclick)
    plt.show()
    plt.disconnect(cid)

    x = int(x_click) if x_click is not None else None
    y = int(y_click) if y_click is not None else None

    return x, y

# Function to convert an RGB image to grayscale
def rgb_to_grayscale(image):
    if len(image.shape) == 3:
        return 0.2989 * image[:, :, 0] + 0.5870 * image[:, :, 1] + 0.1140 * image[:, :, 2]
    else:
        return image

# Function to apply a Gaussian filter to a grayscale image
def gaussian(gray):
    kernel = np.array([
        [1, 4, 7, 4, 1],
        [4, 16, 26, 16, 4],
        [7, 26, 41, 26, 7],
        [4, 16, 26, 16, 4],
        [1, 4, 7, 4, 1]
    ]) / 273

    pad_width = 5 // 2
    padded_image = np.pad(gray, pad_width, mode='constant')
    placeholder = np.zeros_like(gray)

    r, c = np.shape(gray)

    for i in range(r):
        for j in range(c):
            patch = padded_image[i:i+5, j:j+5]
            placeholder[i, j] = np.sum(patch * kernel)

    return placeholder

#Function to upscale an image
def upsample(subs_image):
    ups_size = (subs_image.shape[0] * 2, subs_image.shape[1] * 2)
    ups_grid = np.zeros(ups_size)

    ups_grid[::2, ::2] = subs_image

    for i in range(1, ups_size[0] - 1, 2):
        for j in range(1, ups_size[1] - 1, 2):
            x1 = (ups_grid[i-1, j-1] + ups_grid[i+1, j-1]) / 2
            x2 = (ups_grid[i-1, j+1] + ups_grid[i+1, j+1]) / 2
            central = (x1 + x2) / 2
            ups_grid[i, j] = central

    for i in range(1, ups_size[0] - 1):
        for j in range(1, ups_size[1] - 1):
            if ups_grid[i, j] == 0:
                avg = (ups_grid[i, j-1] + ups_grid[i-1, j] + ups_grid[i, j+1] + ups_grid[i+1, j]) / 4
                ups_grid[i, j] = avg

    for i in range(1, ups_size[0] - 1):
        for j in range(0, ups_size[1]):
            if ups_grid[i, j] == 0:
                avg = (ups_grid[i-1, j] + ups_grid[i+1, j]) / 2
                ups_grid[i, j] = avg

    for i in range(0, ups_size[0]):
        for j in range(1, ups_size[1] - 1):
            if ups_grid[i, j] == 0:
                avg = (ups_grid[i, j-1] + ups_grid[i, j+1]) / 2
                ups_grid[i, j] = avg

    return ups_grid

# Function to create a binary mask for a source image
def mask_source(image, x1, y1, x2, y2):
    grid_size = (image.shape[0], image.shape[1])
    mask_grid = np.ones(grid_size, dtype='bool')
    mask_grid[y1:y2, x1:x2] = 0
    return mask_grid

# Function to create a binary mask for a target image
def mask_target(image, x1, y1, x2, y2, horiz, vert):
    half_height = (y2 - y1) // 2
    half_width = (x2 - x1) // 2
    grid_size = (image.shape[0], image.shape[1])
    mask_grid = np.zeros(grid_size, dtype='bool')
    mask_grid[vert-half_height:vert+half_height,horiz-half_width:horiz+half_width]=1
    return mask_grid

# Function to multiply an image with a binary mask
def mask_multiply(image, mask):
    product = image * mask
    return product

# Function to downscale an image by a factor of 2
def subsample(image):
    if image is None:
        return None
    subsampled_image = image[::2, ::2]
    return subsampled_image

#Input and load the source and target images
source_image_file = input("Enter the name of the target image file: ")
if source_image_file:
    source_image = plt.imread(source_image_file)
    source_range_location_1 = get_click_coordinates(source_image)
    source_range_location_2 = get_click_coordinates(source_image)
    if source_range_location_1 is not None and source_range_location_2 is not None:
        x1, y1 = source_range_location_1
        x2, y2 = source_range_location_2
    else:
        print("Failed to obtain target image coordinates.")
        exit()

target_image_file = input("Enter the name of the source image file: ")
if target_image_file:
    target_image = plt.imread(target_image_file)
    target_location = get_click_coordinates(target_image)
    if target_location is not None:
        horiz, vert = target_location
    else:
        print("Failed to obtain source image coordinates.")
        exit()
        
#Error handling 
if x1 is None or y1 is None or x2 is None or y2 is None:
    print("Invalid source image coordinates. Please ensure the coordinates are within the image bounds.")
    exit()

# Check if the target image coordinates are within bounds
if horiz is None or vert is None:
    print("Invalid target image coordinates. Please ensure the coordinates are within the image bounds.")
    exit()


pyramid_levels = int(input("Enter the number of pyramid levels: "))
while pyramid_levels < 0:
    print("Pyramid levels can't be negative. Please enter a non-negative number.")
    pyramid_levels = int(input("Enter the number of pyramid levels: "))


# Create Gaussian pyramids for the source and target images
def gaussian_pyramid(image, pyramid_levels):
    pyramid = [rgb_to_grayscale(image)]

    for i in range(pyramid_levels):
        if i < len(pyramid):
            blurred_image = gaussian(pyramid[i])
            subsampled_image = subsample(blurred_image)
            pyramid.append(subsampled_image)
        else:
            break  # Break the loop if the pyramid reaches the desired number of levels

    return pyramid

# Create Laplacian pyramids for the source and target images
def laplacian_pyramid(gaussian_pyramid):
    pyramid_levels = len(gaussian_pyramid)
    laplacian = []

    for i in range(1,pyramid_levels):
        upsampled_image = upsample(gaussian_pyramid[i])
        upsampled_image = gaussian(upsampled_image)  
        expanded_image = np.pad(upsampled_image, ((1, 0), (1, 0)), mode='constant')  # Adjust padding if necessary
        difference = gaussian_pyramid[i-1] - expanded_image[:gaussian_pyramid[i-1].shape[0], :gaussian_pyramid[i-1].shape[1]]
        laplacian.append(difference)

    # The last level of the Laplacian pyramid is the same as the last level of the Gaussian pyramid
    laplacian.append(gaussian_pyramid[-1])

    return laplacian

# Mask and manipulate image pyramids
gaussian_pyr = gaussian_pyramid(source_image, pyramid_levels)
laplacian_pyr = laplacian_pyramid(gaussian_pyr)
gaussian_pyr2 = gaussian_pyramid(target_image,pyramid_levels)
laplacian_pyr2 = laplacian_pyramid(gaussian_pyr2)
# Display images in Gaussian pyramid

source_masked_pyramid = []
x1_source, y1_source, x2_source, y2_source = source_range_location_1[0], source_range_location_1[1], source_range_location_2[0], source_range_location_2[1]

for i, laplacian_level in enumerate(laplacian_pyr[:pyramid_levels]):
    # Apply the source mask to the source Laplacian level
    source_masked_image = mask_source(laplacian_level, x1_source, y1_source, x2_source, y2_source)
    source_masked_image = mask_multiply(laplacian_level, source_masked_image)
    source_masked_pyramid.append(source_masked_image)

    # Update source coordinates for the next level (divide by 2) if not the last level
    if i <= pyramid_levels - 1:
        x1_source //= 2
        y1_source //= 2
        x2_source //= 2
        y2_source //= 2

target_masked_pyramid = []
half_height = (y2 - y1) // 2
half_width = (x2 - x1) // 2

# Calculate target coordinates
x1_target = horiz - half_width
x2_target = horiz + half_width
y1_target = vert - half_height
y2_target = vert + half_height
                                                        


for i, laplacian_level in enumerate(laplacian_pyr2[:pyramid_levels]):
    # Apply the target mask to the target Laplacian level
    target_masked_image = mask_target(laplacian_level, x1_target, y1_target, x2_target, y2_target, horiz, vert)
    target_masked_image = mask_multiply(laplacian_level, target_masked_image)
    target_masked_pyramid.append(target_masked_image)

    # Update target coordinates for the next level (divide by 2) if not the last level
    if i <= pyramid_levels - 1:
        x1_target //= 2
        y1_target //= 2
        x2_target //= 2
        y2_target //= 2
        horiz //= 2  # Update horizontal coordinate for the target mask
        vert //= 2   # Update vertical coordinate

def extract_face(image):
    # Find the coordinates of non-zero pixels in the image
    non_zero_coords = np.transpose(np.nonzero(image))
    
    if len(non_zero_coords) == 0:
        return None  # No non-zero pixels found, no face to extract
    
    # Calculate the bounding box of the non-zero pixels
    y_min, x_min = np.min(non_zero_coords, axis=0)
    y_max, x_max = np.max(non_zero_coords, axis=0)
    
    # Extract the face region
    face = image[y_min:y_max+1, x_min:x_max+1]
    
    return face


x1, y1 = source_range_location_1
print(x1,y1)

def paste_face(source_data, face, source_coords):
    y1, x1 = source_coords

    # Ensure the face and the destination region have the same dimensions
    y2, x2 = y1 + face.shape[0], x1 + face.shape[1]
    
    # Create a copy of the source data for manipulation
    result_data = np.copy(source_data)

    # Paste the face into the specified region
    result_data[y1:y2,x1:x2] = face

    return result_data



for i in range(pyramid_levels):
    face = extract_face(target_masked_pyramid[i])
    if face is not None:
        source_masked_pyramid[i] = paste_face(source_masked_pyramid[i], face, (y1//(2**i), x1//(2**i)))

img = gaussian_pyr[i]
img2 = upsample(img)
img3 = gaussian(img2)
mask2 = mask_source(img3, x1//2**(i-1), y1//2**(i-1), x2//2**(i-1), y2//2**(i-1))
final_image = mask_multiply(img3,mask2)

x1,y1 = source_range_location_1
x2,y2 = source_range_location_2
horiz,vert = target_location
img4 = gaussian_pyr2[i]
img5 = upsample(img4)
img6 = gaussian(img5)
mask3 = mask_target(img6, x1//2**(i-1), y1//2**(i-1), x2//2**(i-1), y2//2**(i-1), horiz//2**(i-1), vert//2**(i-1))
final_image2 = mask_multiply(img6,mask3)

x1, y1 = source_range_location_1
final_image3 = extract_face(final_image2)
final_image4 = paste_face(final_image,final_image3,(y1//2**(i-1),x1//2**(i-1)))



# Resize final_image4 and source_masked_pyramid[i-1] to match minimum dimensions
min_height = np.minimum(final_image4.shape[0], source_masked_pyramid[i-1].shape[0])
min_width = np.minimum(final_image4.shape[1], source_masked_pyramid[i-1].shape[1])

resized_final_image4 = final_image4[:min_height, :min_width]
resized_imgN = source_masked_pyramid[i-1][:min_height, :min_width]




final_image4 = np.array(final_image4)  
source_masked_pyramid[i-1] = np.array(source_masked_pyramid[i-1])

min_height = min(final_image4.shape[0], source_masked_pyramid[i-1].shape[0])
min_width = min(final_image4.shape[1], source_masked_pyramid[i-1].shape[1])

resized_final_image4 = np.zeros_like(source_masked_pyramid[i-1])
resized_final_image4[:min_height, :min_width] = final_image4[:min_height, :min_width]


image1 = resized_final_image4+ source_masked_pyramid[i-1]
image2 = upsample(image1)
image3 = gaussian(image2)

image3 = np.array(image3)  
source_masked_pyramid[i-2] = np.array(source_masked_pyramid[i-2])
min_height = min(image3.shape[0], source_masked_pyramid[i - 2].shape[0])
min_width = min(image3.shape[1], source_masked_pyramid[i - 2].shape[1])

resized_Image3 = np.zeros_like(image3)
resized_Image3[:min_height, :min_width] = source_masked_pyramid[i-2][:min_height, :min_width]

Image4 =  image3 + source_masked_pyramid[i-2]
image5 = upsample(Image4)
Image6 = gaussian(image5)

# Resize Image6 to match source_masked_pyramid[i - 3] dimensions
min_height = min(Image6.shape[0], source_masked_pyramid[i - 3].shape[0])
min_width = min(Image6.shape[1], source_masked_pyramid[i - 3].shape[1])

resized_Image6 = np.zeros_like(source_masked_pyramid[i - 3])
resized_Image6[:min_height, :min_width] = Image6[:min_height, :min_width]

x = upsample(source_masked_pyramid[0])
x2 = gaussian(x)
Image7 = Image6 + x

plt.imshow(Image7, cmap='gray')
plt.title('Final image (img)')
plt.show()





    









