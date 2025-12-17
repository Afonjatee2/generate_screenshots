"""
Multi-Device Mockup Generator
Automatically places screenshots into device frames with transparent background
Supports: iPhone 14 Pro Max, MacBook Pro 14", MacBook Pro 16", iMac 24"
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Device configurations
DEVICES = {
    'iphone14': {
        'name': 'iPhone 14 Pro Max',
        'screen_width': 1290,
        'screen_height': 2796,
        'device_padding': {'top': 40, 'bottom': 40, 'left': 20, 'right': 20},
        'border_radius': 55,
        'has_notch': True,
        'notch_type': 'dynamic_island',
        'fit_mode': 'contain'
    },
    'instagram_story': {
        'name': 'Instagram Story (UI Overlay)',
        'screen_width': 1290,
        'screen_height': 2796,
        'device_padding': {'top': 40, 'bottom': 40, 'left': 20, 'right': 20},
        'border_radius': 55,
        'has_notch': True,
        'notch_type': 'dynamic_island',
        'fit_mode': 'cover',
        'overlay_type': 'instagram_story',
        'overlay_settings': {
            'brand_text': 'Your Brand • Sponsored',
            'subtitle_text': 'Add your campaign hashtag or message here',
            'cta_text': 'Learn more',
            'cta_subtext': 'yourdomain.com',
            'progress_fraction': 0.65
        }
    },
    'macbook14': {
        'name': 'MacBook Pro 14"',
        'screen_width': 3024,
        'screen_height': 1964,
        'device_padding': {'top': 60, 'bottom': 80, 'left': 60, 'right': 60},
        'border_radius': 12,
        'has_notch': True,
        'notch_type': 'macbook_notch',
        'fit_mode': 'cover'
    },
    'macbook16': {
        'name': 'MacBook Pro 16"',
        'screen_width': 3456,
        'screen_height': 2234,
        'device_padding': {'top': 60, 'bottom': 80, 'left': 60, 'right': 60},
        'border_radius': 12,
        'has_notch': True,
        'notch_type': 'macbook_notch',
        'fit_mode': 'cover'
    },
    'imac24': {
        'name': 'iMac 24"',
        'screen_width': 4480,
        'screen_height': 2520,
        'device_padding': {'top': 100, 'bottom': 140, 'left': 80, 'right': 80},
        'border_radius': 15,
        'has_notch': False,
        'notch_type': None,
        'fit_mode': 'cover'
    }
}

def create_device_frame(device_type='iphone14'):
    """
    Creates a device frame with transparent background
    """
    if device_type not in DEVICES:
        raise ValueError(f"Device type '{device_type}' not supported. Choose from: {', '.join(DEVICES.keys())}")
    
    config = DEVICES[device_type]
    screen_width = config['screen_width']
    screen_height = config['screen_height']
    padding = config['device_padding']
    border_radius = config['border_radius']
    
    # Calculate device dimensions
    device_width = screen_width + padding['left'] + padding['right']
    device_height = screen_height + padding['top'] + padding['bottom']
    
    # Create transparent background
    frame = Image.new('RGBA', (device_width, device_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(frame)
    
    # Draw device body (black/dark gray)
    device_color = (30, 30, 30, 255) if 'macbook' in device_type or 'imac' in device_type else (0, 0, 0, 255)
    draw.rounded_rectangle(
        [(0, 0), (device_width, device_height)],
        radius=border_radius,
        fill=device_color
    )
    
    # Draw screen area (will be replaced with actual screenshot)
    screen_x = padding['left']
    screen_y = padding['top']
    draw.rounded_rectangle(
        [(screen_x, screen_y), (screen_x + screen_width, screen_y + screen_height)],
        radius=border_radius - 2,
        fill=(255, 255, 255, 255)
    )
    
    # Add notch if applicable
    if config['has_notch']:
        if config['notch_type'] == 'dynamic_island':
            # iPhone Dynamic Island
            island_width = 120
            island_height = 35
            island_x = (device_width - island_width) // 2
            island_y = screen_y + 15
            
            draw.rounded_rectangle(
                [(island_x, island_y), (island_x + island_width, island_y + island_height)],
                radius=17,
                fill=(0, 0, 0, 255)
            )
        elif config['notch_type'] == 'macbook_notch':
            # MacBook notch (centered at top)
            notch_width = 200
            notch_height = 30
            notch_x = (device_width - notch_width) // 2
            notch_y = screen_y
            
            draw.rounded_rectangle(
                [(notch_x, notch_y), (notch_x + notch_width, notch_y + notch_height)],
                radius=10,
                fill=(30, 30, 30, 255)
            )
    
    # Add keyboard area for MacBooks (visual detail)
    if 'macbook' in device_type:
        keyboard_height = padding['bottom'] - 20
        keyboard_y = screen_y + screen_height + 10
        draw.rounded_rectangle(
            [(padding['left'], keyboard_y), 
             (device_width - padding['right'], keyboard_y + keyboard_height)],
            radius=8,
            fill=(20, 20, 20, 255)
        )
        
        # Add trackpad indication
        trackpad_width = 300
        trackpad_height = 40
        trackpad_x = (device_width - trackpad_width) // 2
        trackpad_y = keyboard_y + (keyboard_height - trackpad_height) // 2
        draw.rounded_rectangle(
            [(trackpad_x, trackpad_y), (trackpad_x + trackpad_width, trackpad_y + trackpad_height)],
            radius=6,
            fill=(40, 40, 40, 255)
        )
    
    # Add stand for iMac
    if device_type == 'imac24':
        stand_width = 200
        stand_height = 60
        stand_x = (device_width - stand_width) // 2
        stand_y = device_height - 60
        
        # Stand pole
        draw.rectangle(
            [(device_width // 2 - 15, stand_y), (device_width // 2 + 15, device_height)],
            fill=(200, 200, 200, 255)
        )
        
        # Stand base
        draw.ellipse(
            [(stand_x, stand_y + 30), (stand_x + stand_width, stand_y + 30 + stand_height)],
            fill=(200, 200, 200, 255)
        )
    
    screen_coords = (screen_x, screen_y, screen_width, screen_height)
    return frame, screen_coords, config

def prompt_for_device(default_device='iphone14'):
    """
    Prompt the user to select a device type interactively.
    """
    device_keys = list(DEVICES.keys())
    print("Available devices:")
    for idx, key in enumerate(device_keys, 1):
        print(f"  {idx}. {DEVICES[key]['name']} ({key})")

    default_label = DEVICES[default_device]['name']
    prompt = f"Select device [default: {default_label}] : "

    while True:
        try:
            choice = input(prompt).strip().lower()
        except EOFError:
            print("No input detected. Using default device.")
            return default_device

        if not choice:
            return default_device

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(device_keys):
                return device_keys[index - 1]
        elif choice in device_keys:
            return choice

        print("Invalid selection. Please enter a number or device id from the list.")

def prompt_yes_no(message, default=True):
    """
    Prompt the user for a yes/no response.
    """
    default_prompt = "Y/n" if default else "y/N"
    while True:
        try:
            response = input(f"{message} [{default_prompt}]: ").strip().lower()
        except EOFError:
            print("No input detected. Using default option.")
            return default

        if not response:
            return default
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'.")

def load_font(size, bold=False):
    """
    Attempt to load a system font; fall back to PIL default.
    """
    font_paths = []
    if bold:
        font_paths.extend([
            "arialbd.ttf",
            "Arial Bold.ttf",
            "HelveticaNeue-Bold.ttf",
            "Helvetica Bold.ttf"
        ])
    font_paths.extend([
        "arial.ttf",
        "Arial.ttf",
        "HelveticaNeue.ttf",
        "Helvetica.ttf"
    ])
    
    for font_name in font_paths:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
    
    # Fallback to default bitmap font
    return ImageFont.load_default()

def _text_width(font, text):
    """
    Get the rendered width of text for wrapping calculations.
    """
    try:
        return font.getlength(text)
    except AttributeError:
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0]

def _text_size(font, text):
    """
    Get (width, height) for the rendered text.
    """
    try:
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        return font.getsize(text)

def wrap_text(text, font, max_width):
    """
    Simple text wrapper that keeps lines within max_width.
    """
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test_line = word if not current else f"{current} {word}"
        if _text_width(font, test_line) <= max_width:
            current = test_line
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]

def auto_trim_whitespace(image, threshold=240, min_content_ratio=0.1):
    """
    Automatically detect and remove white/light borders from an image.

    Args:
        image: PIL Image object
        threshold: Pixel brightness threshold (0-255). Pixels brighter than this
                   are considered "white/background". Default 240 catches near-white.
        min_content_ratio: Minimum ratio of content to keep (prevents over-trimming).
                          Default 0.1 means at least 10% of original dimensions kept.

    Returns:
        Cropped PIL Image with white borders removed
    """
    # Convert to RGB if necessary (handles RGBA, P mode, etc.)
    if image.mode == 'RGBA':
        # Create white background and composite
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
        rgb_image = background
    elif image.mode != 'RGB':
        rgb_image = image.convert('RGB')
    else:
        rgb_image = image

    # Get image dimensions
    width, height = rgb_image.size
    pixels = rgb_image.load()

    # Find content boundaries by scanning for non-white pixels
    def is_background_pixel(pixel):
        """Check if a pixel is considered background (white/near-white)."""
        r, g, b = pixel
        return r >= threshold and g >= threshold and b >= threshold

    def scan_for_content_row(y):
        """Check if a row contains any content pixels."""
        for x in range(width):
            if not is_background_pixel(pixels[x, y]):
                return True
        return False

    def scan_for_content_col(x):
        """Check if a column contains any content pixels."""
        for y in range(height):
            if not is_background_pixel(pixels[x, y]):
                return True
        return False

    # Find top boundary (first row with content)
    top = 0
    for y in range(height):
        if scan_for_content_row(y):
            top = y
            break

    # Find bottom boundary (last row with content)
    bottom = height
    for y in range(height - 1, -1, -1):
        if scan_for_content_row(y):
            bottom = y + 1
            break

    # Find left boundary (first column with content)
    left = 0
    for x in range(width):
        if scan_for_content_col(x):
            left = x
            break

    # Find right boundary (last column with content)
    right = width
    for x in range(width - 1, -1, -1):
        if scan_for_content_col(x):
            right = x + 1
            break

    # Calculate minimum dimensions to prevent over-trimming
    min_width = int(width * min_content_ratio)
    min_height = int(height * min_content_ratio)

    # Validate boundaries
    content_width = right - left
    content_height = bottom - top

    # If content area is too small, it might be an error - return original
    if content_width < min_width or content_height < min_height:
        return image

    # If no trimming needed, return original
    if left == 0 and top == 0 and right == width and bottom == height:
        return image

    # Crop the original image (not the RGB converted one) to preserve transparency
    cropped = image.crop((left, top, right, bottom))

    return cropped

def resize_screenshot_to_fit(screenshot, target_width, target_height, fit_mode='contain', filename=""):
    """
    Resize screenshot to fit device screen while maintaining aspect ratio.
    fit_mode options:
        - 'contain': Entire screenshot fits inside (may leave padding)
        - 'cover': Screenshot fills screen; crop overflow to remove padding
    """
    img_width, img_height = screenshot.size
    
    # Warning for low resolution images
    min_recommended = max(target_width * 0.5, target_height * 0.5)
    if img_width < min_recommended and img_height < min_recommended:
        print(f"   ⚠️  WARNING: Low resolution detected ({img_width}x{img_height})")
        print(f"      Recommended: at least {int(min_recommended)}px on longest side")
    
    # Calculate scaling factor
    width_ratio = target_width / img_width
    height_ratio = target_height / img_height
    if fit_mode == 'cover':
        scale_factor = max(width_ratio, height_ratio)
    else:
        scale_factor = min(width_ratio, height_ratio)
    
    # Calculate new dimensions
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)
    
    # Use high-quality resampling
    resized = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)

    if fit_mode == 'cover':
        # Crop to target dimensions, centered on the image
        left = max(0, (new_width - target_width) // 2)
        top = max(0, (new_height - target_height) // 2)
        right = left + target_width
        bottom = top + target_height

        # Ensure bounds stay within resized image (accounts for rounding)
        if right > new_width:
            left = max(0, new_width - target_width)
            right = new_width
        if bottom > new_height:
            top = max(0, new_height - target_height)
            bottom = new_height

        resized = resized.crop((left, top, right, bottom))
    
    return resized

def add_screenshot_to_frame(frame, screenshot, screen_coords, device_config, filename=""):
    """
    Adds the screenshot to the device frame
    """
    screen_x, screen_y, screen_width, screen_height = screen_coords
    fit_mode = device_config.get('fit_mode', 'contain')
    
    # Convert screenshot to RGBA if it isn't already
    if screenshot.mode != 'RGBA':
        screenshot = screenshot.convert('RGBA')
    
    # Resize screenshot to fit screen
    resized_screenshot = resize_screenshot_to_fit(
        screenshot,
        screen_width,
        screen_height,
        fit_mode=fit_mode,
        filename=filename
    )
    
    # Calculate position to center the screenshot
    paste_x = screen_x + (screen_width - resized_screenshot.width) // 2
    paste_y = screen_y + (screen_height - resized_screenshot.height) // 2
    
    # Create a copy of the frame
    result = frame.copy()
    
    # Paste screenshot onto frame
    result.paste(resized_screenshot, (paste_x, paste_y), resized_screenshot)
    
    # Apply optional overlays (e.g., platform UI chrome)
    apply_overlay(result, screen_coords, device_config)
    
    return result

def apply_overlay(image, screen_coords, device_config):
    """
    Apply device-specific overlay UI decorations.
    """
    overlay_type = device_config.get('overlay_type')
    if not overlay_type:
        return
    
    if overlay_type == 'instagram_story':
        apply_instagram_story_overlay(image, screen_coords, device_config)

def apply_instagram_story_overlay(image, screen_coords, device_config):
    """
    Draw Instagram-style story UI chrome on top of the screenshot.
    """
    draw = ImageDraw.Draw(image, 'RGBA')
    screen_x, screen_y, screen_width, screen_height = screen_coords
    settings = device_config.get('overlay_settings', {})
    
    brand_text = settings.get('brand_text', 'Your Brand • Sponsored')
    subtitle_text = settings.get('subtitle_text', '')
    cta_text = settings.get('cta_text', 'Learn more')
    cta_subtext = settings.get('cta_subtext', '')
    progress_fraction = max(0.0, min(1.0, settings.get('progress_fraction', 0.5)))
    
    top_height = int(screen_height * 0.17)
    bottom_height = int(screen_height * 0.20)
    side_padding = int(screen_width * 0.05)
    
    # Top overlay band
    top_rect = [
        screen_x,
        screen_y,
        screen_x + screen_width,
        screen_y + top_height
    ]
    draw.rectangle(top_rect, fill=(0, 0, 0, 150))
    
    # Story progress bar
    bar_margin = int(screen_width * 0.05)
    bar_height = max(4, int(screen_height * 0.005))
    bar_y = screen_y + int(top_height * 0.22)
    bar_rect = [
        screen_x + bar_margin,
        bar_y,
        screen_x + screen_width - bar_margin,
        bar_y + bar_height
    ]
    draw.rounded_rectangle(bar_rect, radius=bar_height // 2, fill=(100, 100, 100, 180))
    progress_width = int((bar_rect[2] - bar_rect[0]) * progress_fraction)
    if progress_width > 0:
        progress_rect = [
            bar_rect[0],
            bar_rect[1],
            bar_rect[0] + progress_width,
            bar_rect[3]
        ]
        draw.rounded_rectangle(progress_rect, radius=bar_height // 2, fill=(255, 255, 255, 220))
    
    # Brand and subtitle text
    brand_font = load_font(int(screen_width * 0.05), bold=True)
    subtitle_font = load_font(int(screen_width * 0.035))
    text_y = bar_rect[3] + int(top_height * 0.15)
    draw.text(
        (screen_x + side_padding, text_y),
        brand_text,
        font=brand_font,
        fill=(255, 255, 255, 255)
    )
    if subtitle_text:
        subtitle_lines = wrap_text(subtitle_text, subtitle_font, screen_width - 2 * side_padding)
        for line in subtitle_lines:
            _, line_height = _text_size(subtitle_font, line)
            text_y += line_height + int(screen_height * 0.005)
            draw.text(
                (screen_x + side_padding, text_y),
                line,
                font=subtitle_font,
                fill=(230, 230, 230, 255)
            )
    
    # Top right menu dots
    dot_radius = max(4, int(screen_width * 0.008))
    dots_center_y = text_y - int(top_height * 0.3)
    dots_spacing = dot_radius * 3
    dots_x_start = screen_x + screen_width - side_padding - dots_spacing
    for i in range(3):
        cx = dots_x_start + i * dot_radius
        draw.ellipse(
            [
                cx - dot_radius,
                dots_center_y - dot_radius,
                cx + dot_radius,
                dots_center_y + dot_radius
            ],
            fill=(255, 255, 255, 220)
        )
    
    # Bottom overlay band
    bottom_rect = [
        screen_x,
        screen_y + screen_height - bottom_height,
        screen_x + screen_width,
        screen_y + screen_height
    ]
    draw.rectangle(bottom_rect, fill=(0, 0, 0, 170))
    
    # CTA pill
    cta_width = int(screen_width * 0.45)
    cta_height = int(bottom_height * 0.35)
    cta_x = screen_x + side_padding
    cta_y = bottom_rect[1] + int(bottom_height * 0.18)
    draw.rounded_rectangle(
        [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
        radius=cta_height // 2,
        fill=(255, 255, 255, 230)
    )
    
    cta_font = load_font(int(screen_width * 0.045), bold=True)
    text_width, text_height = _text_size(cta_font, cta_text)
    text_x = cta_x + (cta_width - text_width) // 2
    text_y = cta_y + (cta_height - text_height) // 2
    draw.text(
        (text_x, text_y),
        cta_text,
        font=cta_font,
        fill=(0, 0, 0, 255)
    )
    
    # CTA subtext / URL
    if cta_subtext:
        sub_font = load_font(int(screen_width * 0.035))
        sub_y = cta_y + cta_height + int(bottom_height * 0.12)
        draw.text(
            (cta_x, sub_y),
            cta_subtext,
            font=sub_font,
            fill=(220, 220, 220, 255)
        )
    
    # Engagement icons on the right (share, like)
    icon_radius = int(bottom_height * 0.22)
    icon_spacing = int(bottom_height * 0.35)
    icon_x = screen_x + screen_width - side_padding - icon_radius
    icon_y_start = bottom_rect[1] + int(bottom_height * 0.25)
    
    # Like icon (simple heart)
    heart_bbox = [
        icon_x - icon_radius,
        icon_y_start,
        icon_x + icon_radius,
        icon_y_start + 2 * icon_radius
    ]
    draw.ellipse(heart_bbox, outline=(255, 255, 255, 220), width=3)
    
    # Share arrow icon
    arrow_center_y = icon_y_start - icon_spacing
    arrow_width = icon_radius * 2
    arrow_height = icon_radius
    arrow_points = [
        (icon_x, arrow_center_y - arrow_height),
        (icon_x + arrow_width // 2, arrow_center_y),
        (icon_x, arrow_center_y + arrow_height)
    ]
    draw.line(arrow_points, fill=(255, 255, 255, 220), width=4)
    draw.line([(icon_x, arrow_center_y + arrow_height), (icon_x, arrow_center_y + arrow_height + icon_radius)], fill=(255, 255, 255, 220), width=4)

def process_all_screenshots(input_folder='./screenshots', output_folder='./mockups', device_type='iphone14', skip_existing=True, auto_trim=True):
    """
    Process all screenshots in the input folder and create mockups

    Args:
        input_folder: Path to folder containing screenshots
        output_folder: Path to save generated mockups
        device_type: Device frame to use (e.g., 'iphone14', 'macbook14')
        skip_existing: Skip screenshots that already have mockups
        auto_trim: Automatically remove white/light borders from screenshots
    """
    # Validate device type
    if device_type not in DEVICES:
        print(f"❌ Invalid device type: '{device_type}'")
        print(f"   Available devices: {', '.join(DEVICES.keys())}")
        return

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

    device_name = DEVICES[device_type]['name']
    print(f"📱 Found {len(screenshot_files)} screenshot(s) to process...")
    print(f"🖥️  Device: {device_name}")
    if auto_trim:
        print("✂️  Auto-trim: ON (removing white borders)")
    if skip_existing:
        print("⏭️  Skipping screenshots with existing mockups.")
    print("-" * 50)

    # Create device frame template
    frame_template, screen_coords, device_config = create_device_frame(device_type)

    # Process each screenshot
    processed_count = 0
    skipped_count = 0
    trimmed_count = 0

    for idx, filename in enumerate(screenshot_files, 1):
        try:
            input_path = os.path.join(input_folder, filename)
            name_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{name_without_ext}_{device_type}_mockup.png"
            output_path = os.path.join(output_folder, output_filename)

            if skip_existing and os.path.exists(output_path):
                skipped_count += 1
                print(f"   Skipping existing mockup: {output_filename}")
                continue

            # Load screenshot
            screenshot = Image.open(input_path)
            original_size = screenshot.size

            # Auto-trim white borders if enabled
            if auto_trim:
                screenshot = auto_trim_whitespace(screenshot)
                trimmed_size = screenshot.size
                if trimmed_size != original_size:
                    trimmed_count += 1
                    print(f"   ✂️  Trimmed: {original_size[0]}x{original_size[1]} → {trimmed_size[0]}x{trimmed_size[1]}")
                else:
                    print(f"   Processing: {screenshot.size[0]}x{screenshot.size[1]} pixels")
            else:
                print(f"   Processing: {screenshot.size[0]}x{screenshot.size[1]} pixels")

            # Add to frame
            mockup = add_screenshot_to_frame(
                frame_template,
                screenshot,
                screen_coords,
                device_config,
                filename
            )

            # Save mockup
            mockup.save(output_path, 'PNG')

            processed_count += 1
            print(f"✅ [{idx}/{len(screenshot_files)}] {filename} → {output_filename}")

        except Exception as e:
            print(f"❌ [{idx}/{len(screenshot_files)}] Error processing {filename}: {str(e)}")
    
    print("-" * 50)
    summary_parts = [f"{processed_count} new mockup(s)"]
    if trimmed_count:
        summary_parts.append(f"{trimmed_count} trimmed")
    if skipped_count:
        summary_parts.append(f"{skipped_count} skipped")
    print(f"🎉 Done! {' | '.join(summary_parts)} saved to '{output_folder}'")

if __name__ == "__main__":
    print("=" * 50)
    print("Multi-Device Mockup Generator")
    print("=" * 50)
    print()

    # CONFIGURATION - CHANGE THESE AS NEEDED
    INPUT_FOLDER = './screenshots'
    OUTPUT_FOLDER = './mockups'

    DEFAULT_DEVICE = 'iphone14'
    selected_device = prompt_for_device(DEFAULT_DEVICE)
    auto_trim = prompt_yes_no("Auto-trim white borders from screenshots?", default=True)
    skip_existing = prompt_yes_no("Skip screenshots that already have mockups?", default=True)

    print()
    print(f"📂 Input folder: {INPUT_FOLDER}")
    print(f"📂 Output folder: {OUTPUT_FOLDER}")
    print(f"🖥️  Device: {DEVICES[selected_device]['name']}")
    print(f"✂️  Auto-trim: {'Yes' if auto_trim else 'No'}")
    print(f"⏭️  Skip existing: {'Yes' if skip_existing else 'No'}")
    print()

    # Create input folder if it doesn't exist
    Path(INPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    # Process all screenshots
    process_all_screenshots(INPUT_FOLDER, OUTPUT_FOLDER, selected_device, skip_existing=skip_existing, auto_trim=auto_trim)
