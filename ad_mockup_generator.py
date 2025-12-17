"""
iPhone Mockup Generator
Automatically places ad screenshots into iPhone 14 Pro Max frames with transparent background
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

def create_iphone_frame(screen_width=1290, screen_height=2796):
    """
    Creates an iPhone 14 Pro Max frame with transparent background
    Screen dimensions: 1290 x 2796 (actual iPhone 14 Pro Max resolution)
    """
    # Device dimensions (scaled proportionally)
    device_width = screen_width + 40  # Add border
    device_height = screen_height + 80  # Add top and bottom borders
    border_radius = 55  # Rounded corners
    
    # Create transparent background
    frame = Image.new('RGBA', (device_width, device_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(frame)
    
    # Draw device body (black with slight transparency for realism)
    draw.rounded_rectangle(
        [(0, 0), (device_width, device_height)],
        radius=border_radius,
        fill=(0, 0, 0, 255)
    )
    
    # Draw screen area (will be replaced with actual screenshot)
    screen_x = 20
    screen_y = 40
    draw.rounded_rectangle(
        [(screen_x, screen_y), (screen_x + screen_width, screen_y + screen_height)],
        radius=border_radius - 5,
        fill=(255, 255, 255, 255)
    )
    
    # Dynamic Island (notch area at top)
    island_width = 120
    island_height = 35
    island_x = (device_width - island_width) // 2
    island_y = screen_y + 15
    
    draw.rounded_rectangle(
        [(island_x, island_y), (island_x + island_width, island_y + island_height)],
        radius=17,
        fill=(0, 0, 0, 255)
    )
    
    return frame, (screen_x, screen_y, screen_width, screen_height)

def resize_screenshot_to_fit(screenshot, target_width, target_height):
    """
    Resize screenshot to fit iPhone screen while maintaining aspect ratio
    """
    img_width, img_height = screenshot.size
    
    # Calculate scaling factor
    width_ratio = target_width / img_width
    height_ratio = target_height / img_height
    scale_factor = min(width_ratio, height_ratio)
    
    # Calculate new dimensions
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)
    
    # Resize image
    resized = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return resized

def add_screenshot_to_frame(frame, screenshot, screen_coords):
    """
    Adds the screenshot to the iPhone frame
    """
    screen_x, screen_y, screen_width, screen_height = screen_coords
    
    # Convert screenshot to RGBA if it isn't already
    if screenshot.mode != 'RGBA':
        screenshot = screenshot.convert('RGBA')
    
    # Resize screenshot to fit screen
    resized_screenshot = resize_screenshot_to_fit(screenshot, screen_width, screen_height)
    
    # Calculate position to center the screenshot
    paste_x = screen_x + (screen_width - resized_screenshot.width) // 2
    paste_y = screen_y + (screen_height - resized_screenshot.height) // 2
    
    # Create a copy of the frame
    result = frame.copy()
    
    # Paste screenshot onto frame
    result.paste(resized_screenshot, (paste_x, paste_y), resized_screenshot)
    
    return result

def process_all_screenshots(input_folder='./screenshots', output_folder='./mockups'):
    """
    Process all screenshots in the input folder and create mockups
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Supported image formats
    supported_formats = ('.png', '.jpg', '.jpeg', '.webp')
    
    # Get all image files from input folder
    screenshot_files = [f for f in os.listdir(input_folder) 
                       if f.lower().endswith(supported_formats)]
    
    if not screenshot_files:
        print(f"❌ No image files found in '{input_folder}'")
        print(f"   Supported formats: {', '.join(supported_formats)}")
        return
    
    print(f"📱 Found {len(screenshot_files)} screenshot(s) to process...")
    print("-" * 50)
    
    # Create iPhone frame template
    frame_template, screen_coords = create_iphone_frame()
    
    # Process each screenshot
    for idx, filename in enumerate(screenshot_files, 1):
        try:
            input_path = os.path.join(input_folder, filename)
            
            # Load screenshot
            screenshot = Image.open(input_path)
            
            # Add to frame
            mockup = add_screenshot_to_frame(frame_template, screenshot, screen_coords)
            
            # Generate output filename
            name_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{name_without_ext}_iphone_mockup.png"
            output_path = os.path.join(output_folder, output_filename)
            
            # Save mockup
            mockup.save(output_path, 'PNG')
            
            print(f"✅ [{idx}/{len(screenshot_files)}] {filename} → {output_filename}")
            
        except Exception as e:
            print(f"❌ [{idx}/{len(screenshot_files)}] Error processing {filename}: {str(e)}")
    
    print("-" * 50)
    print(f"🎉 Done! Mockups saved to '{output_folder}'")

if __name__ == "__main__":
    print("=" * 50)
    print("iPhone 14 Pro Max Mockup Generator")
    print("=" * 50)
    print()
    
    # You can customize these paths
    INPUT_FOLDER = './screenshots'
    OUTPUT_FOLDER = './mockups'
    
    print(f"📂 Input folder: {INPUT_FOLDER}")
    print(f"📂 Output folder: {OUTPUT_FOLDER}")
    print()
    
    # Create input folder if it doesn't exist
    Path(INPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    
    # Process all screenshots
    process_all_screenshots(INPUT_FOLDER, OUTPUT_FOLDER)
