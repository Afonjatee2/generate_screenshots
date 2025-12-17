# iPhone Mockup Generator 📱

Automatically place your Instagram ad screenshots into iPhone 14 Pro Max frames with transparent backgrounds.

## Quick Start

### 1. Install Required Package
```bash
pip install Pillow
```

### 2. Setup Your Folders
```
your-project/
├── ad_mockup_generator.py
├── screenshots/          (put your ad screenshots here)
└── mockups/             (generated mockups will appear here)
```

### 3. Add Your Screenshots
Place all your Instagram ad screenshots in the `screenshots` folder.

### 4. Run the Script
```bash
python ad_mockup_generator.py
```

That's it! Your mockups will be in the `mockups` folder.

## What It Does

✅ Processes multiple screenshots at once  
✅ Creates iPhone 14 Pro Max frame with rounded corners  
✅ Includes Dynamic Island (the notch)  
✅ Transparent background (perfect for presentations)  
✅ Automatically resizes screenshots to fit  
✅ Maintains aspect ratio  
✅ Saves as PNG files  

## Supported Formats

- PNG
- JPG/JPEG
- WEBP

## Output

Each screenshot gets converted to:
`original_name_iphone_mockup.png`

## Customization

Want to change the input/output folders? Edit these lines in the script:
```python
INPUT_FOLDER = './screenshots'   # Change this
OUTPUT_FOLDER = './mockups'       # Change this
```

## Troubleshooting

**"No image files found"**
- Make sure your screenshots are in the `screenshots` folder
- Check that they're in a supported format (PNG, JPG, WEBP)

**"Module not found: PIL"**
- Run: `pip install Pillow`

**Screenshots look stretched**
- The script automatically maintains aspect ratio
- If your screenshots are very wide/tall, they'll be centered with space around them
