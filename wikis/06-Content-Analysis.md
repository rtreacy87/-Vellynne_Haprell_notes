# 06 - Content Analysis

Analyzing transcripts to extract key moments and themes for Vellynne's journal entries.

## Prerequisites Checklist

- [ ] Clean transcript available
- [ ] Analysis scripts from previous wikis
- [ ] Understanding of Vellynne's character and interests

## Step 1: Automated Content Extraction

```bash
# Run the analysis script
SESSION_NUM=01
SESSION_DIR="sessions/session-${SESSION_NUM}"
cd "${SESSION_DIR}"

python3 ../../scripts/analyze-transcript.py transcript/cleaned_transcript.txt

# Review analysis output
cat transcript/cleaned_transcript_analysis.json | jq '.'
```

## Step 2: Manual Content Categorization

```bash
cat > content/content_categories.md << 'EOF'
# Content Categories for Vellynne's Journal

## 1. Magical Phenomena (Vellynne's Primary Interest)
### Spells Witnessed
- [ ] Spell name: [Caster] - [Effect observed] - [Vellynne's analysis]
- [ ] Spell name: [Caster] - [Effect observed] - [Vellynne's analysis]

### Magical Items/Artifacts
- [ ] Item: [Description] - [Properties] - [Research potential]
- [ ] Item: [Description] - [Properties] - [Research potential]

### Arcane Environments
- [ ] Location: [Magical properties] - [Academic interest]
- [ ] Location: [Magical properties] - [Academic interest]

## 2. Undead/Creature Studies
### Specimens Encountered
- [ ] Creature: [Type] - [Behavior] - [Weaknesses] - [Origin theories]
- [ ] Creature: [Type] - [Behavior] - [Weaknesses] - [Origin theories]

### Combat Observations
- [ ] Tactical notes: [Effectiveness against undead]
- [ ] Environmental factors: [How cold affects undead]

## 3. Party Dynamics (Academic Observation)
### Individual Capabilities
- [ ] Character: [Magical abilities] - [Combat style] - [Growth observed]
- [ ] Character: [Magical abilities] - [Combat style] - [Growth observed]

### Group Coordination
- [ ] Tactical development: [How party works together]
- [ ] Leadership dynamics: [Decision-making patterns]

## 4. Research Opportunities
### Ancient Knowledge
- [ ] Historical discovery: [Relevance to research]
- [ ] Linguistic findings: [Ancient texts/runes]

### Experimental Opportunities
- [ ] Hypothesis to test: [Based on session events]
- [ ] Future investigation: [Sites/phenomena to study]

## 5. Environmental/Political Context
### Icewind Dale Conditions
- [ ] Weather effects: [Impact on magic/undead]
- [ ] Local politics: [Ten Towns developments]

### Threat Assessment
- [ ] Regional dangers: [Implications for research]
- [ ] Resource availability: [Access to materials/sites]
EOF
```

## Step 3: Extract Vellynne's Voice Elements

```bash
cat > content/vellynne_voice_guide.md << 'EOF'
# Writing in Vellynne's Voice

## Character Traits to Emphasize
- **Academic curiosity**: Analytical approach to everything
- **Necromancy focus**: Special interest in undead and death magic
- **Formal education**: References to Blackstaff Academy and magical theory
- **Practical researcher**: Balances theory with field observation

## Language Patterns
### Academic Terminology
- "Fascinating specimen"
- "Preliminary observations suggest"
- "Further study required"
- "Theoretical implications"
- "Empirical evidence indicates"

### Magical Expertise
- References to spell schools and components
- Technical analysis of magical effects
- Comparisons to established magical theory
- Interest in magical innovation

### Personal Investment
- Genuine interest in party members' growth
- Protective instincts toward research subjects
- Excitement about discoveries
- Frustration with magical ignorance

## Content Transformation Examples

### Combat Encounter → Academic Analysis
**Raw**: "The party fought some zombies in the cave"
**Vellynne's Voice**: "The party's encounter with frost-preserved undead specimens provided valuable data on cold climate preservation of necromantic animation. The zombies retained remarkable muscular coordination despite advanced decomposition, suggesting the Icewind Dale environment may slow the typical degradation process."

### Spell Casting → Magical Observation
**Raw**: "The wizard cast fireball"
**Vellynne's Voice**: "Young [Character]'s evocation demonstration showed impressive thermal control for one lacking formal arcane education. The spell's intensity and precision suggest natural talent that could benefit from proper theoretical foundation."

### Discovery → Research Opportunity
**Raw**: "We found an old book with weird writing"
**Vellynne's Voice**: "Today's discovery of pre-Netherese script may finally provide the linguistic key to my research on ancient binding rituals. The text's preservation in this climate presents an unexpected opportunity for comparative analysis."
EOF
```

## Step 4: Create Content Extraction Workflow

```bash
cat > ../../scripts/extract-content.py << 'EOF'
#!/usr/bin/env python3
import sys
import re
import json
from pathlib import Path

def extract_vellynne_content(transcript_file, analysis_file):
    """Extract content relevant to Vellynne's interests"""
    
    with open(transcript_file, 'r') as f:
        transcript = f.read()
    
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)
    
    content = {
        'magical_phenomena': extract_magical_content(transcript),
        'creature_studies': extract_creature_content(transcript),
        'party_analysis': extract_party_content(transcript),
        'research_opportunities': extract_research_content(transcript),
        'environmental_notes': extract_environment_content(transcript)
    }
    
    return content

def extract_magical_content(text):
    """Extract magical phenomena from transcript"""
    magic_patterns = [
        r'cast[s]?\s+(\w+)',
        r'spell[s]?\s+(\w+)',
        r'magic[al]?\s+(\w+)',
        r'enchant[ed|ment]?\s+(\w+)'
    ]
    
    magical_events = []
    for pattern in magic_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            context = get_context(text, match.start(), 100)
            magical_events.append({
                'type': 'spell_casting',
                'spell': match.group(1),
                'context': context
            })
    
    return magical_events

def extract_creature_content(text):
    """Extract creature encounters"""
    creature_patterns = [
        r'(zombie|skeleton|undead|ghost|wraith)',
        r'(dragon|giant|troll|goblin|orc)',
        r'(monster|creature|beast|fiend)'
    ]
    
    creatures = []
    for pattern in creature_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            context = get_context(text, match.start(), 150)
            creatures.append({
                'type': match.group(1),
                'context': context
            })
    
    return creatures

def extract_party_content(text):
    """Extract party dynamics and character development"""
    # Look for character names and actions
    party_events = []
    
    # Common D&D action patterns
    action_patterns = [
        r'(\w+)\s+(attacks?|casts?|moves?|says?)',
        r'(\w+)\s+(rolls?|hits?|misses?|damages?)'
    ]
    
    for pattern in action_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            context = get_context(text, match.start(), 100)
            party_events.append({
                'character': match.group(1),
                'action': match.group(2),
                'context': context
            })
    
    return party_events

def extract_research_content(text):
    """Extract research opportunities"""
    research_keywords = [
        'ancient', 'old', 'rune', 'inscription', 'artifact',
        'mystery', 'unknown', 'strange', 'magical', 'enchanted'
    ]
    
    research_ops = []
    for keyword in research_keywords:
        pattern = rf'\b{keyword}\b.*?[.!?]'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            research_ops.append({
                'keyword': keyword,
                'context': match.group(0)
            })
    
    return research_ops

def extract_environment_content(text):
    """Extract environmental and political context"""
    environment_keywords = [
        'weather', 'cold', 'snow', 'ice', 'wind',
        'town', 'village', 'politics', 'threat'
    ]
    
    env_notes = []
    for keyword in environment_keywords:
        pattern = rf'\b{keyword}\b.*?[.!?]'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            env_notes.append({
                'keyword': keyword,
                'context': match.group(0)
            })
    
    return env_notes

def get_context(text, position, length):
    """Get context around a position in text"""
    start = max(0, position - length//2)
    end = min(len(text), position + length//2)
    return text[start:end].strip()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract-content.py transcript.txt analysis.json")
        sys.exit(1)
    
    transcript_file, analysis_file = sys.argv[1], sys.argv[2]
    content = extract_vellynne_content(transcript_file, analysis_file)
    
    # Save extracted content
    output_file = 'content/extracted_content.json'
    Path('content').mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(content, f, indent=2)
    
    print(f"✅ Content extracted and saved to {output_file}")
    print(f"📊 Found:")
    print(f"   Magical events: {len(content['magical_phenomena'])}")
    print(f"   Creature encounters: {len(content['creature_studies'])}")
    print(f"   Party actions: {len(content['party_analysis'])}")
    print(f"   Research opportunities: {len(content['research_opportunities'])}")
EOF

chmod +x ../../scripts/extract-content.py
```

## Step 5: Run Content Extraction

```bash
# Extract content using the script
python3 ../../scripts/extract-content.py \
    transcript/cleaned_transcript.txt \
    transcript/cleaned_transcript_analysis.json

# Review extracted content
cat content/extracted_content.json | jq '.magical_phenomena | length'
cat content/extracted_content.json | jq '.creature_studies[0]'
```

## Step 6: Create Writing Prompts

```bash
cat > content/writing_prompts.md << 'EOF'
# Writing Prompts for Vellynne's Journal

## Section-Specific Prompts

### Initial Observations
- How does the weather/environment affect magical research?
- What is Vellynne's current research status?
- How does she view the party's current situation?

### Magical Phenomena Recorded
- What spells were cast and how do they compare to academy standards?
- Were there any magical innovations or variations observed?
- What magical items or effects warrant further study?

### Specimen Studies
- What creatures were encountered, especially undead?
- How did they behave differently than expected?
- What weaknesses or resistances were observed?
- How might the cold climate affect undead physiology?

### Party Analysis
- How are individual party members developing their abilities?
- What tactical improvements has the group made?
- Are there any magical talents worth nurturing?

### Research Implications
- How do today's events connect to ongoing research?
- What new questions have been raised?
- What future investigations are warranted?
- How do discoveries relate to Ten Towns politics?

## Voice Consistency Checks
- [ ] Uses academic/formal language
- [ ] Shows genuine interest in magical phenomena
- [ ] Demonstrates protective feelings toward party
- [ ] References Blackstaff Academy training
- [ ] Maintains scholarly objectivity while showing personality
- [ ] Includes technical magical terminology
- [ ] Shows excitement about discoveries
- [ ] Connects events to broader research goals
EOF
```

## Step 7: Quality Review Process

```bash
cat > ../../scripts/content-review.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
SESSION_DIR="sessions/session-${SESSION_NUM}"

echo "📋 Content Analysis Review for Session ${SESSION_NUM}"
echo "=============================================="

# Check if all required files exist
FILES=(
    "transcript/cleaned_transcript.txt"
    "transcript/cleaned_transcript_analysis.json"
    "content/extracted_content.json"
    "content/content_categories.md"
)

echo "📁 File Check:"
for file in "${FILES[@]}"; do
    if [ -f "${SESSION_DIR}/${file}" ]; then
        echo "   ✅ ${file}"
    else
        echo "   ❌ ${file} - Missing"
    fi
done

# Content completeness check
echo
echo "📊 Content Analysis:"
cd "${SESSION_DIR}"

if [ -f "content/extracted_content.json" ]; then
    MAGIC_COUNT=$(jq '.magical_phenomena | length' content/extracted_content.json)
    CREATURE_COUNT=$(jq '.creature_studies | length' content/extracted_content.json)
    PARTY_COUNT=$(jq '.party_analysis | length' content/extracted_content.json)
    RESEARCH_COUNT=$(jq '.research_opportunities | length' content/extracted_content.json)
    
    echo "   Magical phenomena: ${MAGIC_COUNT}"
    echo "   Creature encounters: ${CREATURE_COUNT}"
    echo "   Party interactions: ${PARTY_COUNT}"
    echo "   Research opportunities: ${RESEARCH_COUNT}"
    
    # Minimum content thresholds
    if [ $MAGIC_COUNT -gt 0 ] && [ $PARTY_COUNT -gt 5 ]; then
        echo "   ✅ Sufficient content for journal entry"
    else
        echo "   ⚠️  May need additional content extraction"
    fi
fi

echo
echo "🎯 Ready for content creation: $(basename $SESSION_DIR)"
EOF

chmod +x ../../scripts/content-review.sh
```

## Troubleshooting

### Low Content Extraction
- **Manual review**: Read transcript for missed content
- **Adjust keywords**: Add campaign-specific terms
- **Check audio quality**: Poor transcription affects extraction
- **Review analysis**: Verify automated analysis accuracy

### Missing Context
- **Preserve timestamps**: Use SRT format for reference
- **Cross-reference notes**: Compare with DM or player notes
- **Listen to audio**: Verify important moments
- **Ask party members**: Clarify unclear events

## Next Steps

With content analysis complete:

1. ✅ Transcript analyzed for key content
2. ✅ Vellynne-relevant material extracted
3. ✅ Content categorized by journal sections
4. ✅ Writing prompts and voice guide ready

Continue to **[07-Writing-Guide.md](07-Writing-Guide.md)** to learn how to write authentic journal entries in Vellynne's voice.

## Quick Commands

```bash
# Extract content from transcript
python3 scripts/extract-content.py transcript.txt analysis.json

# Review content completeness
./scripts/content-review.sh 01
```
