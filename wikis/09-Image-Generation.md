# 09 - Image Generation

Creating medieval manuscript-style illustrations using AI image generation tools.

## Prerequisites Checklist

- [ ] OpenAI API key or Stable Diffusion setup
- [ ] Journal content with illustration requirements
- [ ] Understanding of medieval manuscript aesthetics

## Step 1: Set Up Image Generation

### OpenAI API Setup
```bash
# Install OpenAI Python library
pip install openai pillow

# Create API configuration
cat > config/openai_config.json << 'EOF'
{
  "api_key": "your_openai_api_key_here",
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "standard",
  "style": "natural"
}
EOF

echo "⚠️  Add your actual OpenAI API key to config/openai_config.json"
```

### Alternative: Stable Diffusion Local Setup
```bash
# Install Stable Diffusion dependencies (if using local generation)
pip install diffusers transformers accelerate torch torchvision

# Note: Requires significant GPU memory (8GB+ recommended)
echo "💡 Local Stable Diffusion requires powerful GPU"
echo "   Consider using OpenAI API for easier setup"
```

## Step 2: Create Image Generation Script

```bash
cat > scripts/generate-images.py << 'EOF'
#!/usr/bin/env python3
import sys
import json
import openai
from pathlib import Path
import requests
from PIL import Image
import io

def load_config():
    """Load OpenAI configuration"""
    config_file = Path("config/openai_config.json")
    if not config_file.exists():
        raise FileNotFoundError("OpenAI config not found. Run setup first.")
    
    with open(config_file) as f:
        config = json.load(f)
    
    openai.api_key = config["api_key"]
    return config

def generate_image(prompt, config, output_path):
    """Generate image using OpenAI DALL-E"""
    
    # Enhanced prompt for medieval manuscript style
    style_prompt = f"""Medieval manuscript illustration in the style of illuminated texts, 
    parchment background, ink and watercolor, scientific diagram style like Leonardo da Vinci's notebooks,
    sepia tones, aged paper texture, scholarly annotations, hand-drawn aesthetic.
    
    Subject: {prompt}"""
    
    try:
        response = openai.Image.create(
            prompt=style_prompt,
            n=1,
            size=config.get("size", "1024x1024"),
            quality=config.get("quality", "standard"),
            style=config.get("style", "natural")
        )
        
        # Download and save image
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)
        
        with open(output_path, 'wb') as f:
            f.write(image_response.content)
        
        print(f"✅ Generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return False

def create_illustration_prompts(session_dir):
    """Create specific prompts based on session content"""
    
    # Load extracted content
    content_file = Path(session_dir) / "content" / "extracted_content.json"
    if not content_file.exists():
        return []
    
    with open(content_file) as f:
        content = json.load(f)
    
    prompts = []
    
    # Creature studies
    creatures = content.get('creature_studies', [])
    for creature in creatures[:2]:  # Limit to 2 creatures
        prompt = f"Detailed anatomical study of {creature['type']}, showing skeletal structure, muscle definition, and decay patterns, with scholarly annotations and measurements"
        prompts.append(("creature_study", creature['type'], prompt))
    
    # Magical phenomena
    magic_events = content.get('magical_phenomena', [])
    for event in magic_events[:1]:  # Limit to 1 magical diagram
        prompt = f"Magical diagram showing the casting pattern and energy flow of {event['spell']}, with arcane symbols, geometric patterns, and theoretical annotations"
        prompts.append(("magical_diagram", event['spell'], prompt))
    
    # Research opportunities (artifacts/locations)
    research_ops = content.get('research_opportunities', [])
    for op in research_ops[:1]:  # Limit to 1 research illustration
        prompt = f"Archaeological sketch of ancient {op['keyword']} with detailed measurements, cross-sections, and scholarly notes about its construction and purpose"
        prompts.append(("research_study", op['keyword'], prompt))
    
    return prompts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate-images.py session_dir")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    
    try:
        config = load_config()
        prompts = create_illustration_prompts(session_dir)
        
        if not prompts:
            print("❌ No content found for image generation")
            sys.exit(1)
        
        # Create images directory
        images_dir = Path(session_dir) / "images" / "generated"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎨 Generating {len(prompts)} illustrations...")
        
        for i, (img_type, subject, prompt) in enumerate(prompts, 1):
            output_file = images_dir / f"{img_type}_{subject.replace(' ', '_')}.png"
            print(f"Generating {i}/{len(prompts)}: {img_type} - {subject}")
            
            success = generate_image(prompt, config, output_file)
            if not success:
                print(f"⚠️  Skipping {subject} due to generation error")
        
        print("✅ Image generation complete!")
        print(f"📁 Images saved to: {images_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
EOF

chmod +x scripts/generate-images.py
```

## Step 3: Create Prompt Templates

```bash
cat > templates/image_prompts.json << 'EOF'
{
  "creature_studies": {
    "zombie": "Detailed anatomical study of frost-preserved zombie, showing skeletal structure visible through decaying flesh, ice crystals in tissue, with scholarly annotations about cold preservation effects on undead physiology",
    "skeleton": "Scientific diagram of animated skeleton with focus on joint articulation, bone density, and magical energy patterns that maintain animation, drawn in medieval manuscript style",
    "dragon": "Comprehensive study of dragon anatomy including wing membrane structure, scale patterns, breath weapon organs, with cross-sectional views and measurement annotations",
    "giant": "Anthropological study of frost giant physiology, comparing bone structure to human proportions, with notes on cold adaptation and muscular development"
  },
  "magical_diagrams": {
    "fireball": "Arcane diagram showing fireball spell matrix with geometric patterns, energy flow arrows, component symbols, and theoretical notes on thermal dynamics",
    "healing": "Magical healing energy patterns with life force flow diagrams, anatomical overlay showing energy channels, and scholarly notes on restoration theory",
    "shield": "Protective magic ward diagram with geometric barrier patterns, energy deflection angles, and annotations on defensive spell theory",
    "teleportation": "Spatial magic diagram showing dimensional fold patterns, coordinate calculations, and theoretical framework for matter transportation"
  },
  "location_maps": {
    "dungeon": "Hand-drawn dungeon map with architectural details, trap mechanisms, magical aura indicators, and exploration notes in margins",
    "ruins": "Archaeological site map showing structural remains, artifact locations, and scholarly annotations about historical significance",
    "cave": "Cave system diagram with geological formations, magical crystal deposits, and notes on environmental magical effects",
    "town": "Settlement map with building layouts, defensive positions, and political/social annotations relevant to research access"
  },
  "artifact_studies": {
    "weapon": "Detailed weapon study showing construction, magical enchantments, runic inscriptions, and theoretical analysis of magical properties",
    "armor": "Armor piece analysis with material composition, protective enchantments, and notes on magical enhancement techniques",
    "scroll": "Ancient scroll with visible text, translation attempts, linguistic analysis, and notes on magical ink composition",
    "crystal": "Magical crystal study with internal structure, energy patterns, resonance frequencies, and theoretical applications"
  }
}
EOF
```

## Step 4: Batch Image Generation

```bash
cat > scripts/batch-generate.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "🎨 Batch Image Generation for Session ${SESSION_PADDED}"
echo "=============================================="

# Check prerequisites
if [ ! -f "${SESSION_DIR}/content/extracted_content.json" ]; then
    echo "❌ Content extraction required first"
    exit 1
fi

# Check API configuration
if [ ! -f "config/openai_config.json" ]; then
    echo "❌ OpenAI configuration missing"
    echo "   Create config/openai_config.json with your API key"
    exit 1
fi

# Generate images
echo "🎯 Generating illustrations..."
python3 scripts/generate-images.py "${SESSION_DIR}"

# Create image manifest
echo "📋 Creating image manifest..."
cat > "${SESSION_DIR}/images/manifest.json" << EOL
{
  "session": ${SESSION_NUM},
  "generated_date": "$(date -Iseconds)",
  "images": [
$(find "${SESSION_DIR}/images/generated" -name "*.png" -exec basename {} \; | sed 's/.*/"&"/' | paste -sd ',' -)
  ],
  "style": "medieval manuscript",
  "resolution": "1024x1024",
  "total_count": $(find "${SESSION_DIR}/images/generated" -name "*.png" | wc -l)
}
EOL

echo "✅ Batch generation complete!"
echo "📁 Images: ${SESSION_DIR}/images/generated/"
echo "📋 Manifest: ${SESSION_DIR}/images/manifest.json"
EOF

chmod +x scripts/batch-generate.sh
```

## Step 5: Image Quality Control

```bash
cat > scripts/review-images.py << 'EOF'
#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from PIL import Image

def analyze_image_quality(image_path):
    """Analyze image for quality metrics"""
    
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            mode = img.mode
            
            # Basic quality checks
            issues = []
            
            if width < 1000 or height < 1000:
                issues.append("Low resolution")
            
            if mode != "RGB":
                issues.append(f"Unexpected color mode: {mode}")
            
            # File size check
            file_size = image_path.stat().st_size
            if file_size < 100000:  # Less than 100KB
                issues.append("File size too small")
            
            return {
                "dimensions": f"{width}x{height}",
                "mode": mode,
                "file_size": file_size,
                "issues": issues
            }
            
    except Exception as e:
        return {"error": str(e)}

def review_session_images(session_dir):
    """Review all images for a session"""
    
    images_dir = Path(session_dir) / "images" / "generated"
    if not images_dir.exists():
        print("❌ No generated images found")
        return
    
    image_files = list(images_dir.glob("*.png"))
    if not image_files:
        print("❌ No PNG images found")
        return
    
    print(f"🔍 Reviewing {len(image_files)} images...")
    
    results = {}
    total_issues = 0
    
    for img_file in image_files:
        analysis = analyze_image_quality(img_file)
        results[img_file.name] = analysis
        
        if "issues" in analysis:
            total_issues += len(analysis["issues"])
    
    # Generate report
    print("\n📊 Image Quality Report")
    print("======================")
    
    for filename, analysis in results.items():
        print(f"\n📷 {filename}")
        
        if "error" in analysis:
            print(f"   ❌ Error: {analysis['error']}")
            continue
        
        print(f"   📐 Dimensions: {analysis['dimensions']}")
        print(f"   🎨 Color mode: {analysis['mode']}")
        print(f"   💾 File size: {analysis['file_size']:,} bytes")
        
        if analysis["issues"]:
            print(f"   ⚠️  Issues: {', '.join(analysis['issues'])}")
        else:
            print("   ✅ Quality: Good")
    
    print(f"\n📈 Summary: {len(image_files)} images, {total_issues} total issues")
    
    if total_issues == 0:
        print("✅ All images pass quality checks")
    else:
        print("⚠️  Some images may need regeneration")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python review-images.py session_dir")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    review_session_images(session_dir)
EOF

chmod +x scripts/review-images.py
```

## Step 6: Manual Prompt Creation

```bash
cat > scripts/create-custom-prompt.sh << 'EOF'
#!/bin/bash

echo "🎨 Custom Image Prompt Creator"
echo "============================="

read -p "Image type (creature/magic/location/artifact): " IMG_TYPE
read -p "Subject description: " SUBJECT
read -p "Specific details: " DETAILS

# Base style prompt
STYLE="Medieval manuscript illustration in the style of illuminated texts, parchment background, ink and watercolor, scientific diagram style like Leonardo da Vinci's notebooks, sepia tones, aged paper texture, scholarly annotations, hand-drawn aesthetic."

# Create full prompt
FULL_PROMPT="${STYLE} Subject: ${IMG_TYPE} study of ${SUBJECT}. ${DETAILS}"

echo
echo "📝 Generated Prompt:"
echo "==================="
echo "$FULL_PROMPT"
echo
echo "💾 Save this prompt? (y/n)"
read SAVE_PROMPT

if [[ $SAVE_PROMPT == "y" ]]; then
    FILENAME="custom_prompts_$(date +%Y%m%d).txt"
    echo "Prompt: $FULL_PROMPT" >> "$FILENAME"
    echo "Subject: $SUBJECT" >> "$FILENAME"
    echo "Date: $(date)" >> "$FILENAME"
    echo "---" >> "$FILENAME"
    echo "✅ Prompt saved to $FILENAME"
fi
EOF

chmod +x scripts/create-custom-prompt.sh
```

## Style Guidelines

### Medieval Manuscript Aesthetics
- **Colors**: Sepia, burnt umber, deep blues, aged paper tones
- **Style**: Scientific illustration like Leonardo da Vinci
- **Elements**: Annotations, measurements, scholarly notes
- **Texture**: Parchment background, ink stains, aging effects

### Prompt Enhancement Tips
```bash
# Always include these style elements:
# - "Medieval manuscript illustration"
# - "parchment background"
# - "scholarly annotations"
# - "hand-drawn aesthetic"
# - "sepia tones"

# For creatures: Add "anatomical study", "skeletal structure"
# For magic: Add "arcane symbols", "energy flow patterns"
# For locations: Add "architectural details", "cross-sections"
# For artifacts: Add "detailed measurements", "construction analysis"
```

## Troubleshooting

### API Issues
- **Rate limits**: Add delays between requests
- **Invalid prompts**: Check for content policy violations
- **Authentication**: Verify API key in config

### Poor Image Quality
- **Refine prompts**: Add more specific style descriptors
- **Try different models**: DALL-E 2 vs DALL-E 3
- **Adjust parameters**: Size, quality, style settings

### Style Inconsistency
- **Use consistent base prompt**: Always include medieval manuscript style
- **Reference images**: Provide style examples in prompts
- **Batch generation**: Generate all images for session together

## Next Steps

With image generation ready:

1. ✅ AI image generation configured
2. ✅ Medieval manuscript style prompts created
3. ✅ Batch generation workflow established
4. ✅ Quality control measures in place

Continue to **[10-Image-Processing.md](10-Image-Processing.md)** to add aging effects and annotations to your generated images.

## Quick Commands

```bash
# Generate all images for session
./scripts/batch-generate.sh 01

# Review image quality
python3 scripts/review-images.py sessions/session-01

# Create custom prompt
./scripts/create-custom-prompt.sh
```
