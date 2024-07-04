import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def resize_image(image_path, format_choice):
    """
    Resizes an image to a fixed size based on user-selected format.

    Args:
        image_path (str): Path to the image file.
        format_choice (str): User-selected format (1-10).

    Returns:
        None: Saves the resized image to the same location.
    """
    try:
        with Image.open(image_path) as image:
            width, height = image.size

            # Define aspect ratios for each format
            aspect_ratios = {
                "1": (16, 9),
                "2": (16, 9),
                "3": (3, 1),
                "4": (3, 2),
                "5": (4, 1),
                "6": (1, 1),
                "7": (1, 1),
                "8": (1, 1),
                "9": (16, 9),
                "10": (1, 1)
            }

            # Validate user input
            if format_choice not in aspect_ratios:
                raise ValueError("Invalid format choice. Please enter a number between 1 and 10.")

            # Calculate new dimensions based on aspect ratio
            target_ratio = aspect_ratios[format_choice]
            if width / height > target_ratio[0] / target_ratio[1]:
                # Wider image, adjust height
                new_height = int(width * target_ratio[1] / target_ratio[0])
                new_width = width
            else:
                # Taller image, adjust width
                new_width = int(height * target_ratio[0] / target_ratio[1])
                new_height = height

            # Resize the image
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            # Save the resized image
            resized_image.save(image_path)

    except (IOError, ValueError) as e:
        print(f"Error resizing image: {e}")

def resize_image_to_fit(image, max_width, max_height):
    # Calculate the new dimensions
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if aspect_ratio > 1:
            # Wider than tall
            new_width = int(max_width)
            new_height = int(max_width / aspect_ratio)
        else:
            # Taller than wide
            new_height = int(max_height)
            new_width = int(max_height * aspect_ratio)
    else:
        # No resizing needed
        new_width, new_height = int(width), int(height)

    return image.resize((new_width, new_height), Image.LANCZOS)

def images_to_pdf(input_folder):
    # Get list of all image files in the folder
    image_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

    # Add the stamped_signed.png image from the img folder
    stamped_signed_path = os.path.join(os.path.dirname(__file__), 'img', 'stamped_signed.png')
    if os.path.exists(stamped_signed_path):
        image_files.append(stamped_signed_path)
    else:
        print("stamped_signed.png not found in the img folder.")

    if not image_files:
        print("No images found in the specified folder.")
        return

    # Construct PDF file path in the input folder
    output_location = os.path.join(input_folder, "output.pdf")

    # Create a canvas object
    c = canvas.Canvas(output_location, pagesize=A4)
    print(f"Creating PDF: {output_location}")

    a4_width, a4_height = A4

    for image_file in image_files:
        try:
            # Open an image file
            with Image.open(image_file) as img:
                print(f"Processing image: {image_file}")

                # Convert the image to RGB (if it's not already in that mode)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize image to fit A4
                img = resize_image_to_fit(img, a4_width, a4_height)
                width, height = img.size

                # Center the image on the A4 page
                x = (a4_width - width) / 2
                y = (a4_height - height) / 2

                # Set the page size to A4
                c.setPageSize(A4)

                # Save the resized image to a temporary file
                temp_image_path = "temp_image.jpg"
                img.save(temp_image_path)

                # Draw the image onto the PDF
                c.drawInlineImage(temp_image_path, x, y, width, height)

                # Show the page (add a new page)
                c.showPage()

        except Exception as e:
            print(f"Failed to process {image_file}: {e}")

    # Save the PDF file
    c.save()
    print(f"PDF saved as: {output_location}")

def convert_images_to_grayscale(input_folder):
    image_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        print("No images found in the specified folder.")
        return

    for image_file in image_files:
        try:
            img_path = os.path.join(input_folder, image_file)
            with Image.open(img_path) as img:
                print(f"Processing image: {image_file}")

                # Convert the image to grayscale
                grayscale_img = img.convert('L')

                # Construct the new filename for the grayscale image
                image_file, extension = os.path.splitext(image_file)
                grayscale_file = f"{image_file}_grayscale{extension}"

                # Save the grayscale image with the new filename
                grayscale_img.save(os.path.join(input_folder, grayscale_file))
                print(f"Saved grayscale image: {os.path.join(input_folder, grayscale_file)}")

        except Exception as e:
            print(f"Failed to process {image_file}: {e}")

def convert_images_to_black_and_white(input_folder, threshold=128):
    image_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        print("No images found in the specified folder.")
        return

    for image_file in image_files:
        try:
            img_path = os.path.join(input_folder, image_file)
            with Image.open(img_path) as img:
                print(f"Processing image: {image_file}")

                grayscale_img = img.convert('L')
                bw_img = grayscale_img.point(lambda x: 255 if x > threshold else 0, mode='1')
                
                # Construct the new file name for the black and white image
                base_name, extension = os.path.splitext(image_file)
                bw_file = f"{base_name}_bw{extension}"

                # Save the black and white image with the new file name
                bw_img.save(os.path.join(input_folder, bw_file))
                print(f"Saved black and white image: {os.path.join(input_folder, bw_file)}")
        except Exception as e:
            print(f"Failed to process {image_file}: {e}")

def main():
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)
    input_folder = input("Enter the input directory path : ")

    # Check if the user wants to exit immediately
    if input_folder.lower() == 'ex':
        print("Take care.")
        return

    while True:
        # Check if the input folder exists
        if not os.path.exists(input_folder):
            print("The specified directory does not exist. Please enter a valid directory path.")
            input_folder = input("Enter the input directory path (type 'ex' to quit): ")
            continue

        # Process images
        while True:
            print("Output location:", input_folder)
            print("What's gonna be:")
            print("1. Grayscale")
            print("2. Black and White")
            print("3. PDF")
            print("4. Resize")
            print("0. Exit")
            choice = input("What's gonna be: ")

            if choice == '1':
                convert_images_to_grayscale(input_folder)
            elif choice == '2':
                convert_images_to_black_and_white(input_folder)
            elif choice == '3':
                images_to_pdf(input_folder)
            elif choice == '4':
                format_choice = input("Select format (1-10): ")
                for image_file in os.listdir(input_folder):
                    if os.path.isfile(os.path.join(input_folder, image_file)):
                        resize_image(os.path.join(input_folder, image_file), format_choice)
                print("Images resized successfully!")
            elif choice == '0':
                print("Exiting the program.")
                return  # No need to break, just return from the function
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 0.")

if __name__ == "__main__":
    main()
