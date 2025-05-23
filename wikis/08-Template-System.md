# 08 - Template System

Creating reusable templates for consistent journal formatting and layout.

## Prerequisites Checklist

- [ ] Writing guide completed
- [ ] Understanding of journal structure
- [ ] Content creation workflow established

## Step 1: Create Master Template

```bash
cat > templates/master_template.md << 'EOF'
# Research Notes of Vellynne Harpell
## Tenth Black Staff of Blackstaff Academy
### {{DATE}} - Session {{SESSION_NUM}}: {{SESSION_TITLE}}

---

## Initial Observations

{{WEATHER_CONDITIONS}} continues to {{EFFECT_ON_RESEARCH}}. Today finds our research expedition {{CURRENT_LOCATION}}, with the party {{PARTY_STATUS}}.

{{CURRENT_RESEARCH_FOCUS}}

{{BROADER_CONNECTIONS}}

---

## Magical Phenomena Recorded

### Spell Casting Observations
{{SPELL_ANALYSIS}}

### Arcane Environmental Effects
{{ENVIRONMENTAL_MAGIC}}

### Magical Item Studies
{{ITEM_ANALYSIS}}

---

## Specimen Studies

### {{CREATURE_TYPE}} Encounter
**Physical Characteristics**: {{CREATURE_DESCRIPTION}}
**Behavioral Patterns**: {{CREATURE_BEHAVIOR}}
**Environmental Adaptations**: {{CLIMATE_EFFECTS}}
**Combat Effectiveness**: {{TACTICAL_NOTES}}
**Research Implications**: {{RESEARCH_VALUE}}

---

## Party Analysis

### Individual Capabilities
{{CHARACTER_ANALYSIS}}

### Group Coordination
{{TACTICAL_DEVELOPMENT}}

### Magical Education Opportunities
{{TRAINING_POTENTIAL}}

---

## Research Implications

### Theoretical Connections
{{THEORY_CONNECTIONS}}

### New Hypotheses
{{NEW_QUESTIONS}}

### Future Investigation Priorities
{{RESEARCH_PRIORITIES}}

### Ten Towns Political Considerations
{{POLITICAL_FACTORS}}

---

*End of Session {{SESSION_NUM}} Research Notes*
*Next Priority: {{NEXT_ACTION}}*

---

**Illustrations Required:**
- [ ] {{ILLUSTRATION_1}}
- [ ] {{ILLUSTRATION_2}}
- [ ] {{ILLUSTRATION_3}}
EOF
```

## Step 2: Create Template Generator Script

```bash
cat > scripts/generate-template.py << 'EOF'
#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

def generate_template(session_dir, template_file):
    """Generate journal template with session-specific content"""
    
    # Load session info
    session_info_file = Path(session_dir) / "session-info.json"
    if session_info_file.exists():
        with open(session_info_file) as f:
            session_info = json.load(f)
    else:
        session_info = {}
    
    # Load extracted content
    content_file = Path(session_dir) / "content" / "extracted_content.json"
    if content_file.exists():
        with open(content_file) as f:
            extracted_content = json.load(f)
    else:
        extracted_content = {}
    
    # Load template
    with open(template_file) as f:
        template = f.read()
    
    # Replace basic placeholders
    replacements = {
        '{{DATE}}': session_info.get('session_date', 'YYYY-MM-DD'),
        '{{SESSION_NUM}}': str(session_info.get('session_number', 'XX')),
        '{{SESSION_TITLE}}': session_info.get('session_title', 'Session Title'),
        '{{CURRENT_LOCATION}}': get_location_hint(extracted_content),
        '{{CREATURE_TYPE}}': get_primary_creature(extracted_content),
        '{{NEXT_ACTION}}': generate_next_action(extracted_content)
    }
    
    # Apply replacements
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    # Generate content hints
    content_hints = generate_content_hints(extracted_content)
    for placeholder, hint in content_hints.items():
        template = template.replace(placeholder, hint)
    
    return template

def get_location_hint(content):
    """Extract location information from content"""
    env_notes = content.get('environmental_notes', [])
    for note in env_notes:
        if any(word in note['context'].lower() for word in ['town', 'cave', 'ruins', 'forest']):
            return f"investigating {note['context'][:50]}..."
    return "exploring the frozen wilderness"

def get_primary_creature(content):
    """Get the most significant creature encounter"""
    creatures = content.get('creature_studies', [])
    if creatures:
        return creatures[0]['type'].title()
    return "Unknown Specimen"

def generate_next_action(content):
    """Suggest next research action based on content"""
    research_ops = content.get('research_opportunities', [])
    if research_ops:
        return f"Investigate {research_ops[0]['keyword']} discovery further"
    return "Continue monitoring party magical development"

def generate_content_hints(content):
    """Generate writing hints for each section"""
    hints = {}
    
    # Weather/environment hints
    env_notes = content.get('environmental_notes', [])
    weather_hints = [note['context'] for note in env_notes if 'weather' in note['keyword'].lower()]
    hints['{{WEATHER_CONDITIONS}}'] = weather_hints[0] if weather_hints else "The harsh Icewind Dale climate"
    
    # Magic hints
    magic_events = content.get('magical_phenomena', [])
    if magic_events:
        spell_hint = f"Analysis of {magic_events[0]['spell']} casting technique..."
        hints['{{SPELL_ANALYSIS}}'] = spell_hint
    else:
        hints['{{SPELL_ANALYSIS}}'] = "[Document spell casting observations]"
    
    # Creature hints
    creatures = content.get('creature_studies', [])
    if creatures:
        creature_hint = f"Detailed examination of {creatures[0]['type']} physiology..."
        hints['{{CREATURE_DESCRIPTION}}'] = creature_hint
    else:
        hints['{{CREATURE_DESCRIPTION}}'] = "[Describe creature physical characteristics]"
    
    # Party hints
    party_events = content.get('party_analysis', [])
    if party_events:
        char_hint = f"Continued observation of {party_events[0]['character']}'s development..."
        hints['{{CHARACTER_ANALYSIS}}'] = char_hint
    else:
        hints['{{CHARACTER_ANALYSIS}}'] = "[Analyze individual party member capabilities]"
    
    # Research hints
    research_ops = content.get('research_opportunities', [])
    if research_ops:
        research_hint = f"The discovery of {research_ops[0]['keyword']} elements suggests..."
        hints['{{THEORY_CONNECTIONS}}'] = research_hint
    else:
        hints['{{THEORY_CONNECTIONS}}'] = "[Connect discoveries to magical theory]"
    
    # Fill remaining placeholders with prompts
    remaining_placeholders = [
        '{{EFFECT_ON_RESEARCH}}', '{{PARTY_STATUS}}', '{{CURRENT_RESEARCH_FOCUS}}',
        '{{BROADER_CONNECTIONS}}', '{{ENVIRONMENTAL_MAGIC}}', '{{ITEM_ANALYSIS}}',
        '{{CREATURE_BEHAVIOR}}', '{{CLIMATE_EFFECTS}}', '{{TACTICAL_NOTES}}',
        '{{RESEARCH_VALUE}}', '{{TACTICAL_DEVELOPMENT}}', '{{TRAINING_POTENTIAL}}',
        '{{NEW_QUESTIONS}}', '{{RESEARCH_PRIORITIES}}', '{{POLITICAL_FACTORS}}',
        '{{ILLUSTRATION_1}}', '{{ILLUSTRATION_2}}', '{{ILLUSTRATION_3}}'
    ]
    
    for placeholder in remaining_placeholders:
        if placeholder not in hints:
            hints[placeholder] = f"[{placeholder.strip('{}').replace('_', ' ').title()}]"
    
    return hints

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate-template.py session_dir template_file")
        sys.exit(1)
    
    session_dir, template_file = sys.argv[1], sys.argv[2]
    
    try:
        generated_template = generate_template(session_dir, template_file)
        
        # Save generated template
        output_file = Path(session_dir) / "content" / "journal_draft.md"
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(generated_template)
        
        print(f"✅ Template generated: {output_file}")
        print("📝 Ready for content writing")
        
    except Exception as e:
        print(f"❌ Error generating template: {e}")
        sys.exit(1)
EOF

chmod +x scripts/generate-template.py
```

## Step 3: Create Specialized Templates

```bash
# Combat-heavy session template
cat > templates/combat_template.md << 'EOF'
# Research Notes of Vellynne Harpell
## Tenth Black Staff of Blackstaff Academy
### {{DATE}} - Session {{SESSION_NUM}}: {{SESSION_TITLE}}

---

## Initial Observations

The party's combat readiness continues to evolve under Icewind Dale's harsh conditions. Today's engagement at {{LOCATION}} provided extensive data on {{COMBAT_FOCUS}}.

---

## Combat Analysis

### Tactical Coordination
{{PARTY_TACTICS}}

### Individual Performance
{{CHARACTER_COMBAT_ANALYSIS}}

### Spell Effectiveness in Combat
{{COMBAT_MAGIC_ANALYSIS}}

---

## Specimen Studies - Combat Behavior

### {{ENEMY_TYPE}} Engagement
**Combat Capabilities**: {{ENEMY_ABILITIES}}
**Tactical Patterns**: {{ENEMY_TACTICS}}
**Vulnerabilities Observed**: {{ENEMY_WEAKNESSES}}
**Environmental Factors**: {{COMBAT_ENVIRONMENT}}

---

## Magical Combat Phenomena

### Spell Interactions
{{SPELL_COMBINATIONS}}

### Environmental Magic Effects
{{BATTLEFIELD_MAGIC}}

---

## Research Implications

### Combat Magic Theory
{{COMBAT_THEORY}}

### Future Training Recommendations
{{TRAINING_SUGGESTIONS}}

---

*Combat Analysis Complete - Session {{SESSION_NUM}}*
EOF

# Discovery-focused session template
cat > templates/discovery_template.md << 'EOF'
# Research Notes of Vellynne Harpell
## Tenth Black Staff of Blackstaff Academy
### {{DATE}} - Session {{SESSION_NUM}}: {{SESSION_TITLE}}

---

## Initial Observations

Today's expedition yielded significant archaeological discoveries at {{DISCOVERY_LOCATION}}. The implications for my research into {{RESEARCH_FOCUS}} are substantial.

---

## Archaeological Findings

### Primary Discovery
**Item/Location**: {{MAIN_DISCOVERY}}
**Historical Context**: {{HISTORICAL_ANALYSIS}}
**Magical Properties**: {{MAGICAL_ANALYSIS}}
**Research Potential**: {{RESEARCH_VALUE}}

### Secondary Discoveries
{{ADDITIONAL_FINDINGS}}

---

## Linguistic Analysis

### Script/Runes Encountered
{{LINGUISTIC_FINDINGS}}

### Translation Attempts
{{TRANSLATION_PROGRESS}}

---

## Magical Resonance Studies

### Arcane Signatures Detected
{{MAGICAL_SIGNATURES}}

### Theoretical Implications
{{MAGICAL_THEORY}}

---

## Research Implications

### Connections to Current Studies
{{RESEARCH_CONNECTIONS}}

### New Research Directions
{{NEW_RESEARCH_PATHS}}

### Preservation and Study Plans
{{STUDY_PLANS}}

---

*Discovery Documentation Complete - Session {{SESSION_NUM}}*
EOF
```

## Step 4: Template Selection Script

```bash
cat > scripts/select-template.py << 'EOF'
#!/usr/bin/env python3
import sys
import json
from pathlib import Path

def analyze_session_type(session_dir):
    """Determine the best template based on session content"""
    
    content_file = Path(session_dir) / "content" / "extracted_content.json"
    if not content_file.exists():
        return "master_template.md"
    
    with open(content_file) as f:
        content = json.load(f)
    
    # Count different types of content
    combat_score = len(content.get('creature_studies', []))
    magic_score = len(content.get('magical_phenomena', []))
    research_score = len(content.get('research_opportunities', []))
    
    # Determine template based on dominant content type
    if combat_score > magic_score and combat_score > research_score:
        return "combat_template.md"
    elif research_score > magic_score and research_score > combat_score:
        return "discovery_template.md"
    else:
        return "master_template.md"

def get_template_info():
    """Return information about available templates"""
    templates = {
        "master_template.md": "General purpose template for balanced sessions",
        "combat_template.md": "Focused on combat encounters and tactical analysis",
        "discovery_template.md": "Emphasizes archaeological and magical discoveries"
    }
    return templates

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Available templates:")
        for template, description in get_template_info().items():
            print(f"  {template}: {description}")
        sys.exit(0)
    
    if len(sys.argv) != 2:
        print("Usage: python select-template.py session_dir")
        print("       python select-template.py (to list templates)")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    recommended_template = analyze_session_type(session_dir)
    
    print(f"📋 Recommended template: {recommended_template}")
    print(f"📁 Template path: templates/{recommended_template}")
    
    # Show template info
    templates = get_template_info()
    print(f"📝 Description: {templates[recommended_template]}")
EOF

chmod +x scripts/select-template.py
```

## Step 5: Complete Template Workflow

```bash
cat > scripts/template-workflow.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📋 Template Generation Workflow"
echo "=============================="

# Check prerequisites
if [ ! -f "${SESSION_DIR}/content/extracted_content.json" ]; then
    echo "❌ Content extraction required first"
    echo "   Run: python3 scripts/extract-content.py"
    exit 1
fi

# Select appropriate template
echo "🔍 Analyzing session content..."
TEMPLATE=$(python3 scripts/select-template.py "${SESSION_DIR}")
echo "📋 Selected template: $TEMPLATE"

# Generate template with content hints
echo "🏗️  Generating personalized template..."
python3 scripts/generate-template.py "${SESSION_DIR}" "templates/${TEMPLATE}"

# Create writing environment
cd "${SESSION_DIR}"
mkdir -p content/drafts

echo "✅ Template ready for writing!"
echo "📁 Draft file: content/journal_draft.md"
echo "📝 Next steps:"
echo "   1. Review generated template"
echo "   2. Fill in placeholder content"
echo "   3. Refine Vellynne's voice"
echo "   4. Plan illustrations"
EOF

chmod +x scripts/template-workflow.sh
```

## Step 6: Template Validation

```bash
cat > scripts/validate-template.py << 'EOF'
#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def validate_template(template_file):
    """Validate template structure and completeness"""
    
    with open(template_file) as f:
        content = f.read()
    
    issues = []
    
    # Check required sections
    required_sections = [
        "Initial Observations",
        "Magical Phenomena",
        "Specimen Studies", 
        "Party Analysis",
        "Research Implications"
    ]
    
    for section in required_sections:
        if section not in content:
            issues.append(f"Missing required section: {section}")
    
    # Check for unfilled placeholders
    placeholders = re.findall(r'\{\{[^}]+\}\}', content)
    if placeholders:
        issues.append(f"Unfilled placeholders: {len(placeholders)}")
    
    # Check word count estimates
    word_count = len(content.split())
    if word_count < 500:
        issues.append(f"Content may be too short: {word_count} words")
    
    # Check for Vellynne voice elements
    voice_indicators = [
        'research', 'study', 'analysis', 'observation',
        'academic', 'theoretical', 'empirical'
    ]
    
    voice_count = sum(content.lower().count(indicator) for indicator in voice_indicators)
    if voice_count < 5:
        issues.append("May need more academic voice elements")
    
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate-template.py template_file")
        sys.exit(1)
    
    template_file = sys.argv[1]
    issues = validate_template(template_file)
    
    if not issues:
        print("✅ Template validation passed")
    else:
        print("⚠️  Template validation issues:")
        for issue in issues:
            print(f"   - {issue}")
EOF

chmod +x scripts/validate-template.py
```

## Template Usage Examples

### Quick Template Generation
```bash
# Auto-select and generate template
./scripts/template-workflow.sh 01

# Manual template selection
python3 scripts/generate-template.py sessions/session-01 templates/combat_template.md
```

### Template Customization
```bash
# List available templates
python3 scripts/select-template.py

# Validate completed template
python3 scripts/validate-template.py sessions/session-01/content/journal_draft.md
```

## Troubleshooting

### Template Generation Fails
- **Check content extraction**: Ensure extracted_content.json exists
- **Verify session info**: Check session-info.json format
- **Template file missing**: Verify template exists in templates/

### Poor Template Selection
- **Manual override**: Specify template manually
- **Adjust content analysis**: Modify selection criteria
- **Create custom template**: Copy and modify existing template

## Next Steps

With template system ready:

1. ✅ Master and specialized templates created
2. ✅ Automated template generation configured
3. ✅ Template selection logic implemented
4. ✅ Validation tools available

Continue to **[09-Image-Generation.md](09-Image-Generation.md)** to create medieval-style illustrations for your journals.

## Quick Commands

```bash
# Generate template for session
./scripts/template-workflow.sh 01

# Validate completed template
python3 scripts/validate-template.py journal_draft.md
```
