# Multi-Device Mockup Generator 📱💻🖥️

Automatically place your ad screenshots into device frames with transparent backgrounds.

**Supported Devices:**
- 📱 iPhone 14 Pro Max (for Instagram/TikTok ads)
- 💻 MacBook Pro 14" (for YouTube ads)
- 💻 MacBook Pro 16" (for YouTube ads)
- 🖥️ iMac 24" (for YouTube ads)

## Quick Start

### 1. Install Required Package
```bash
pip install Pillow
```

### 2. Setup Your Folders
```
your-project/
├── multi_device_mockup_generator.py
├── screenshots/          (put your ad screenshots here)
└── mockups/             (generated mockups will appear here)
```

### 3. Add Your Screenshots
Place all your screenshots in the `screenshots` folder.

**Recommended Resolutions:**
- Instagram ads: 1080 x 1920 or higher
- YouTube ads: 1920 x 1080 or higher (landscape)

### 4. Run the Script
```bash
python multi_device_mockup_generator.py
```
When prompted, pick the device you want (number or id). Press Enter to accept iPhone by default.  
Next, choose whether to skip screenshots that already have mockups—handy when you drop in just a few new captures.

Done! Your mockups will be in the `mockups` folder.

## Examples

### For Instagram Campaign Report:
Select option `1` / `iphone14` at the prompt → get clean device frames  
Select option `2` / `instagram_story` for the Instagram-style UI overlay

### For YouTube Campaign Report:
Select option `3` / `macbook14` → get MacBook mockups

### Mix and Match
Run the script again and pick a different device each time. Leave “skip existing” turned on and only the fresh screenshots get processed.  
All mockups include the device id in the filename, so you can organise outputs easily.

## Features

✅ **Multiple devices** - iPhone, MacBook, iMac  
✅ **Batch processing** - All screenshots at once  
✅ **Transparent backgrounds** - Perfect for presentations  
✅ **Realistic details** - Notches, keyboards, stands  
✅ **Smart auto-resize** - Mobile devices stay letterboxed, desktops fill the frame  
✅ **Quality warnings** - Alerts for low-res images  
✅ **Skip existing** - Avoids regenerating mockups you already have  
✅ **Platform chrome** - Instagram Story overlay option for Meta previews

## Output Files

Files are named automatically:
- `ad_name_iphone14_mockup.png`
- `ad_name_instagram_story_mockup.png`
- `ad_name_macbook14_mockup.png`
- `ad_name_imac24_mockup.png`

## Device Specifications

| Device | Screen Resolution | Best For |
|--------|------------------|----------|
| iPhone 14 Pro Max | 1290 x 2796 | Instagram, TikTok, Mobile ads |
| Instagram Story Overlay | 1290 x 2796 | Instagram / Facebook Stories mockups |
| MacBook Pro 14" | 3024 x 1964 | YouTube, Display ads |
| MacBook Pro 16" | 3456 x 2234 | YouTube, Display ads |
| iMac 24" | 4480 x 2520 | YouTube, Display ads |

### Fit Modes
- iPhone mockups keep full screenshots visible (`contain`) so portrait ads never get cropped.
- MacBook and iMac mockups stretch to fill the screen area (`cover`) for edge-to-edge browser frames.
- Want different behavior? Tweak the `fit_mode` value for each device in `multi_device_mockup_generator.py`.

## Tips for Best Results

### For Instagram Ads:
- Use screenshots at **1080px width minimum**
- Portrait orientation (9:16)
- Use iPhone mockup

### For YouTube Ads:
- Use screenshots at **1920px width minimum**
- Landscape orientation (16:9)
- Use MacBook or iMac mockup

### Resolution Guidelines:
- ✅ **Good:** 1080p or higher
- ⚠️ **Warning:** 720p (may be slightly soft)
- ❌ **Bad:** Below 500px (will be blurry)

## Troubleshooting

**"Low resolution detected"**
- Get higher quality screenshots (see HIGH_RESOLUTION_GUIDE.md)
- Minimum 1080px width recommended

**"No image files found"**
- Make sure screenshots are in the `screenshots` folder
- Supported: PNG, JPG, JPEG, WEBP

**Screenshots look stretched**
- They're not stretched! The script maintains aspect ratio
- They're centered with space around if aspect ratio doesn't match

**Want to change output location?**
```python
OUTPUT_FOLDER = './my_custom_folder'
```

## Instagram Story Overlay Tweaks

Pick `instagram_story` to mimic Meta’s story preview chrome. Update `overlay_settings` inside the `instagram_story` entry in `multi_device_mockup_generator.py` to:

- Change the brand and subtitle text
- Set the call-to-action label and footer URL
- Adjust the story progress bar (`progress_fraction`)

Those values apply to every screenshot in that run, so tweak them before processing each campaign.

## Advanced Usage

### Process Different Campaigns Separately:
```python
# Campaign 1 - Instagram
process_all_screenshots('./instagram_ads', './mockups/instagram', 'iphone14')

# Campaign 2 - YouTube
process_all_screenshots('./youtube_ads', './mockups/youtube', 'macbook14')
```

### Custom Script Integration:
```python
from multi_device_mockup_generator import process_all_screenshots

# Process with custom settings
process_all_screenshots(
    input_folder='./my_ads',
    output_folder='./output',
    device_type='macbook16'
)
```

## Need Help?

Check the HIGH_RESOLUTION_GUIDE.md for tips on getting high-quality screenshots from Ads Manager.
