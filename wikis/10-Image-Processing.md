# 10 - Image Processing

Adding aging effects, annotations, and medieval manuscript styling to generated images.

## Prerequisites Checklist

- [ ] Generated images from previous step
- [ ] ImageMagick installed
- [ ] GIMP or similar image editor (optional)
- [ ] Medieval fonts downloaded

## Step 1: Install Image Processing Tools

```bash
# Verify ImageMagick installation
convert --version

# Install additional tools if needed
# macOS:
brew install imagemagick gimp

# Linux:
sudo apt install imagemagick gimp

# Download medieval fonts
mkdir -p resources/fonts
echo "📥 Download medieval fonts from Google Fonts:"
echo "   - Cinzel (headers)"
echo "   - EB Garamond (body text)"
echo "   - Kalam (handwriting)"
```

## Step 2: Create Aging Effects Script

```bash
cat > scripts/age-images.sh << 'EOF'
#!/bin/bash

INPUT_DIR=$1
OUTPUT_DIR=$2

if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: ./age-images.sh input_dir output_dir"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🎨 Applying aging effects to images..."

for image in "$INPUT_DIR"/*.png; do
    if [ ! -f "$image" ]; then continue; fi
    
    filename=$(basename "$image" .png)
    output="$OUTPUT_DIR/${filename}_aged.png"
    
    echo "Processing: $filename"
    
    # Apply aging effects with ImageMagick
    convert "$image" \
        -colorspace RGB \
        -fill '#8B4513' -colorize 15% \
        -modulate 90,80,95 \
        -blur 0x0.5 \
        -noise 1 \
        -attenuate 0.3 \
        +noise Uniform \
        -blur 0x0.2 \
        -contrast-stretch 2%x1% \
        "$output"
    
    echo "✅ Created: $output"
done

echo "🏁 Aging effects complete!"
EOF

chmod +x scripts/age-images.sh
```

## Step 3: Add Parchment Background

```bash
cat > scripts/add-parchment.py << 'EOF'
#!/usr/bin/env python3
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import numpy as np

def create_parchment_texture(width, height):
    """Create a parchment-like background texture"""
    
    # Create base parchment color
    parchment = Image.new('RGB', (width, height), '#F4E4BC')
    
    # Add noise for texture
    noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
    noise_img = Image.fromarray(noise, 'RGB')
    
    # Blend noise with parchment
    parchment = Image.blend(parchment, noise_img, 0.1)
    
    # Add aging stains
    draw = ImageDraw.Draw(parchment)
    
    # Random stains
    for _ in range(random.randint(3, 8)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        
        # Create stain color
        stain_color = (
            random.randint(180, 220),
            random.randint(160, 200),
            random.randint(120, 160)
        )
        
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                    fill=stain_color)
    
    # Blur stains
    parchment = parchment.filter(ImageFilter.GaussianBlur(radius=2))
    
    return parchment

def add_parchment_background(image_path, output_path):
    """Add parchment background to image"""
    
    # Load original image
    original = Image.open(image_path).convert('RGBA')
    width, height = original.size
    
    # Create parchment background
    parchment = create_parchment_texture(width, height)
    
    # Make original image slightly transparent
    alpha = original.split()[-1]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.9)
    original.putalpha(alpha)
    
    # Composite image on parchment
    result = Image.alpha_composite(
        parchment.convert('RGBA'), 
        original
    )
    
    # Convert back to RGB and save
    result.convert('RGB').save(output_path, 'PNG')
    print(f"✅ Added parchment background: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add-parchment.py input_image output_image")
        sys.exit(1)
    
    input_path, output_path = sys.argv[1], sys.argv[2]
    add_parchment_background(input_path, output_path)
EOF

chmod +x scripts/add-parchment.py
```

## Step 4: Add Annotations and Labels

```bash
cat > scripts/add-annotations.py << 'EOF'
#!/usr/bin/env python3
import sys
from PIL import Image, ImageDraw, ImageFont
import json
from pathlib import Path

def load_annotation_templates():
    """Load annotation templates for different image types"""
    return {
        "creature_study": [
            "Skeletal structure analysis",
            "Muscle tissue preservation",
            "Environmental adaptations",
            "Behavioral observations",
            "Threat assessment: {threat_level}"
        ],
        "magical_diagram": [
            "Energy flow patterns",
            "Arcane symbol meanings",
            "Spell component requirements",
            "Theoretical efficiency: {efficiency}%",
            "Academy classification: {classification}"
        ],
        "research_study": [
            "Historical period: {period}",
            "Material composition",
            "Magical resonance detected",
            "Research priority: {priority}",
            "Preservation status: {status}"
        ]
    }

def get_font(size=12):
    """Get appropriate font for annotations"""
    font_paths = [
        "resources/fonts/Kalam-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    
    return ImageFont.load_default()

def add_annotations(image_path, output_path, image_type="creature_study"):
    """Add scholarly annotations to image"""
    
    # Load image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Get annotation templates
    templates = load_annotation_templates()
    annotations = templates.get(image_type, templates["creature_study"])
    
    # Font settings
    font = get_font(14)
    small_font = get_font(10)
    
    # Add title annotation
    title = f"Research Notes - {image_type.replace('_', ' ').title()}"
    draw.text((20, 20), title, fill='#4A4A4A', font=font)
    
    # Add side annotations
    y_pos = 60
    for i, annotation in enumerate(annotations[:4]):  # Limit to 4 annotations
        # Format annotation with placeholder values
        if "{" in annotation:
            annotation = annotation.format(
                threat_level="Moderate",
                efficiency=85,
                classification="Evocation",
                period="Pre-Netherese",
                priority="High",
                status="Good"
            )
        
        # Add annotation with leader line
        draw.text((20, y_pos), f"• {annotation}", fill='#5D4E37', font=small_font)
        y_pos += 25
    
    # Add Vellynne's signature
    signature = "V. Harpell - Blackstaff Academy"
    img_width, img_height = image.size
    draw.text((img_width - 200, img_height - 30), signature, 
              fill='#8B4513', font=small_font)
    
    # Save annotated image
    image.save(output_path)
    print(f"✅ Added annotations: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add-annotations.py input_image output_image [image_type]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    image_type = sys.argv[3] if len(sys.argv) > 3 else "creature_study"
    
    add_annotations(input_path, output_path, image_type)
EOF

chmod +x scripts/add-annotations.py
```

## Step 5: Complete Image Processing Workflow

```bash
cat > scripts/process-all-images.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "🎨 Complete Image Processing for Session ${SESSION_PADDED}"
echo "=================================================="

# Check if generated images exist
GENERATED_DIR="${SESSION_DIR}/images/generated"
if [ ! -d "$GENERATED_DIR" ] || [ -z "$(ls -A $GENERATED_DIR 2>/dev/null)" ]; then
    echo "❌ No generated images found. Run image generation first."
    exit 1
fi

# Create processing directories
PROCESSED_DIR="${SESSION_DIR}/images/processed"
FINAL_DIR="${SESSION_DIR}/images/final"
mkdir -p "$PROCESSED_DIR" "$FINAL_DIR"

echo "Step 1: Applying aging effects..."
./scripts/age-images.sh "$GENERATED_DIR" "$PROCESSED_DIR"

echo "Step 2: Adding parchment backgrounds..."
for image in "$PROCESSED_DIR"/*_aged.png; do
    if [ ! -f "$image" ]; then continue; fi
    
    filename=$(basename "$image" _aged.png)
    output="$PROCESSED_DIR/${filename}_parchment.png"
    
    python3 scripts/add-parchment.py "$image" "$output"
done

echo "Step 3: Adding annotations..."
for image in "$PROCESSED_DIR"/*_parchment.png; do
    if [ ! -f "$image" ]; then continue; fi
    
    filename=$(basename "$image" _parchment.png)
    
    # Determine image type from filename
    if [[ $filename == *"creature"* ]]; then
        img_type="creature_study"
    elif [[ $filename == *"magical"* ]]; then
        img_type="magical_diagram"
    else
        img_type="research_study"
    fi
    
    output="$FINAL_DIR/${filename}_final.png"
    python3 scripts/add-annotations.py "$image" "$output" "$img_type"
done

echo "Step 4: Creating image catalog..."
cat > "${SESSION_DIR}/images/catalog.json" << EOL
{
  "session": ${SESSION_NUM},
  "processed_date": "$(date -Iseconds)",
  "images": [
$(find "$FINAL_DIR" -name "*_final.png" -exec basename {} \; | sed 's/.*/"&"/' | paste -sd ',' -)
  ],
  "processing_steps": [
    "aging_effects",
    "parchment_background", 
    "scholarly_annotations"
  ],
  "style": "medieval_manuscript",
  "ready_for_layout": true
}
EOL

echo "✅ Image processing complete!"
echo "📁 Final images: $FINAL_DIR"
echo "📋 Catalog: ${SESSION_DIR}/images/catalog.json"

# Clean up intermediate files
read -p "Remove intermediate processing files? (y/n): " CLEANUP
if [[ $CLEANUP == "y" ]]; then
    rm -f "$PROCESSED_DIR"/*_aged.png
    rm -f "$PROCESSED_DIR"/*_parchment.png
    echo "🧹 Intermediate files cleaned up"
fi
EOF

chmod +x scripts/process-all-images.sh
```

## Step 6: Quality Control and Review

```bash
cat > scripts/review-processed-images.py << 'EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path
from PIL import Image
import json

def review_processed_images(session_dir):
    """Review processed images for quality and completeness"""
    
    final_dir = Path(session_dir) / "images" / "final"
    if not final_dir.exists():
        print("❌ No processed images found")
        return
    
    images = list(final_dir.glob("*_final.png"))
    if not images:
        print("❌ No final images found")
        return
    
    print(f"🔍 Reviewing {len(images)} processed images...")
    
    results = {
        "total_images": len(images),
        "quality_issues": [],
        "style_consistency": True,
        "annotation_completeness": True
    }
    
    for img_path in images:
        print(f"\n📷 {img_path.name}")
        
        # Check image properties
        with Image.open(img_path) as img:
            width, height = img.size
            mode = img.mode
            
            print(f"   📐 Size: {width}x{height}")
            print(f"   🎨 Mode: {mode}")
            
            # Quality checks
            if width < 800 or height < 600:
                results["quality_issues"].append(f"{img_path.name}: Low resolution")
            
            # Check file size
            file_size = img_path.stat().st_size
            print(f"   💾 Size: {file_size:,} bytes")
            
            if file_size < 200000:  # Less than 200KB
                results["quality_issues"].append(f"{img_path.name}: File too small")
    
    # Generate summary
    print(f"\n📊 Processing Review Summary")
    print(f"============================")
    print(f"Total images: {results['total_images']}")
    print(f"Quality issues: {len(results['quality_issues'])}")
    
    if results["quality_issues"]:
        print("\n⚠️  Issues found:")
        for issue in results["quality_issues"]:
            print(f"   - {issue}")
    else:
        print("✅ All images pass quality checks")
    
    # Save review results
    review_file = Path(session_dir) / "images" / "review_results.json"
    with open(review_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📋 Review saved: {review_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python review-processed-images.py session_dir")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    review_processed_images(session_dir)
EOF

chmod +x scripts/review-processed-images.py
```

## Manual Processing Tips

### Using GIMP for Advanced Effects
```bash
# Open GIMP and apply these effects manually:
# 1. Filters > Artistic > Oilify (for painted look)
# 2. Filters > Distorts > Paper (for texture)
# 3. Colors > Desaturate > Sepia (for aging)
# 4. Filters > Noise > RGB Noise (for grain)
```

### ImageMagick Advanced Commands
```bash
# Create custom aging effect
convert input.png \
    -sepia-tone 80% \
    -modulate 90,70,100 \
    -blur 0x0.5 \
    -noise 2 \
    output.png

# Add border and frame
convert input.png \
    -bordercolor '#8B4513' \
    -border 10x10 \
    -frame 5x5+2+2 \
    output.png
```

## Troubleshooting

### Font Issues
- **Fonts not found**: Install medieval fonts system-wide
- **Text rendering**: Use PIL's default font as fallback
- **Size problems**: Adjust font size based on image dimensions

### Processing Errors
- **Memory issues**: Process images one at a time
- **File permissions**: Check write access to output directories
- **ImageMagick limits**: Adjust policy.xml for large images

### Style Inconsistency
- **Batch process**: Apply same effects to all images
- **Reference images**: Use consistent aging parameters
- **Manual review**: Check each image individually

## Next Steps

With image processing complete:

1. ✅ Aging effects and parchment backgrounds applied
2. ✅ Scholarly annotations added
3. ✅ Medieval manuscript styling achieved
4. ✅ Quality control measures implemented

Continue to **[11-Document-Layout.md](11-Document-Layout.md)** to assemble your journal pages with text and images.

## Quick Commands

```bash
# Process all images for session
./scripts/process-all-images.sh 01

# Review processed images
python3 scripts/review-processed-images.py sessions/session-01

# Manual aging effects
./scripts/age-images.sh input_dir output_dir
```
