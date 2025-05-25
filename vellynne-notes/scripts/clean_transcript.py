#!/usr/bin/env python3
import sys
import re
import json
from pathlib import Path

def clean_transcript(input_file, output_file):
    """Clean and format raw Whisper transcript"""
    
    with open(input_file, 'r') as f:
        text = f.read()
    
    # Remove timestamps and speaker labels
    text = re.sub(r'\[\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+\]', '', text)
    text = re.sub(r'Speaker \d+:', '', text)
    
    # Fix common transcription errors
    replacements = {
        'D and D': 'D&D',
        'dungeon master': 'DM',
        'dice roll': 'dice roll',
        'twenty sided': 'd20',
        'armor class': 'AC',
        'hit points': 'HP'
    }
    
    for old, new in replacements.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    # Clean up spacing and formatting
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    
    # Split into paragraphs (rough speaker changes)
    paragraphs = text.split('\n')
    formatted_text = '\n\n'.join(p.strip() for p in paragraphs if p.strip())
    
    with open(output_file, 'w') as f:
        f.write(formatted_text)
    
    return len(paragraphs), len(text.split())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean-transcript.py input.txt output.txt")
        sys.exit(1)
    
    input_file, output_file = sys.argv[1], sys.argv[2]
    paragraphs, words = clean_transcript(input_file, output_file)
    
    print(f"✅ Transcript cleaned: {paragraphs} paragraphs, {words} words")
    print(f"📁 Output: {output_file}")