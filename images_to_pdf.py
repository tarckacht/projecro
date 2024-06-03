import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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

def images_to_pdf(image_folder, output_pdf):
    # Get list of all image files in the folder
    image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

    if not image_files:
        print("No images found in the specified folder.")
        return

    # Create a canvas object
    c = canvas.Canvas(output_pdf, pagesize=A4)
    print(f"Creating PDF: {output_pdf}")

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
    print(f"PDF saved as: {output_pdf}")

# Example usage:
image_folder = "images"  # Folder containing your image files
output_pdf = "output.pdf"
images_to_pdf(image_folder, output_pdf)
