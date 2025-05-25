#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

def optimize_pdf(input_pdf, output_pdf, quality="print"):
    """Optimize PDF for different use cases"""
    
    quality_settings = {
        "print": {
            "dpi": 300,
            "quality": 90,
            "description": "High quality for printing"
        },
        "web": {
            "dpi": 150,
            "quality": 75,
            "description": "Optimized for web sharing"
        },
        "email": {
            "dpi": 100,
            "quality": 60,
            "description": "Compressed for email"
        }
    }
    
    settings = quality_settings.get(quality, quality_settings["print"])
    
    try:
        # Use Ghostscript for PDF optimization
        cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/printer' if quality == "print" else '/ebook',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-dColorImageResolution={settings["dpi"]}',
            f'-dGrayImageResolution={settings["dpi"]}',
            f'-dMonoImageResolution={settings["dpi"]}',
            f'-sOutputFile={output_pdf}',
            str(input_pdf)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF optimized for {quality}: {output_pdf}")
            
            # Show file size comparison
            original_size = Path(input_pdf).stat().st_size
            optimized_size = Path(output_pdf).stat().st_size
            reduction = (1 - optimized_size/original_size) * 100
            
            print(f"   Original: {original_size:,} bytes")
            print(f"   Optimized: {optimized_size:,} bytes")
            print(f"   Reduction: {reduction:.1f}%")
            
            return True
        else:
            print(f"❌ PDF optimization failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Ghostscript not found. Install with:")
        print("   macOS: brew install ghostscript")
        print("   Linux: sudo apt install ghostscript")
        return False
    except Exception as e:
        print(f"❌ Error optimizing PDF: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python optimize-pdf.py input.pdf output.pdf [quality]")
        print("Quality options: print, web, email")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    quality = sys.argv[3] if len(sys.argv) > 3 else "print"
    
    optimize_pdf(input_pdf, output_pdf, quality)