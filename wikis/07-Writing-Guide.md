# 07 - Writing Guide

Crafting authentic journal entries in Vellynne Harpell's voice and perspective.

## Prerequisites Checklist

- [ ] Content analysis completed
- [ ] Understanding of Vellynne's character
- [ ] Extracted content and writing prompts ready

## Vellynne's Character Profile

### Background
- **Position**: Tenth Black Staff of Blackstaff Academy
- **Specialty**: Necromancy and undead studies
- **Personality**: Academic, curious, protective of research subjects
- **Current Goal**: Studying Icewind Dale's unique magical phenomena

### Writing Voice Characteristics
- **Formal but passionate**: Academic language with genuine excitement
- **Analytical**: Everything viewed through research lens
- **Protective**: Cares about party members as both subjects and allies
- **Theoretical**: Connects observations to magical theory

## Step 1: Create Writing Templates

```bash
cat > content/journal_template.md << 'EOF'
# Research Notes of Vellynne Harpell
## Tenth Black Staff of Blackstaff Academy
### [DATE] - Session [NUMBER]: [TITLE]

---

## Initial Observations

*[150-200 words: Set the scene from Vellynne's perspective]*

The [weather/environmental conditions] of Icewind Dale continues to [effect on research/magic]. Today finds our research expedition [location/situation], with the party [current status/condition]. 

[Vellynne's current research focus/concerns]

[Connection to broader magical studies]

---

## Magical Phenomena Recorded

*[200-250 words: Document magical events with academic analysis]*

### Spell Casting Observations
[Spell name] demonstrated by [caster]: [Technical analysis of execution, comparing to academy standards, noting innovations or variations]

### Arcane Environmental Effects
[Description of magical environmental phenomena and their implications for research]

### Magical Item Studies
[Analysis of any magical items encountered, their properties, and research potential]

---

## Specimen Studies

*[250-300 words: Detailed analysis of creatures, especially undead]*

### [Creature Type] Encounter
**Physical Characteristics**: [Detailed description from academic perspective]
**Behavioral Patterns**: [How creature acted, compared to known specimens]
**Environmental Adaptations**: [How Icewind Dale affects the creature]
**Combat Effectiveness**: [Strengths, weaknesses, tactical notes]
**Research Implications**: [What this teaches about undead/creature physiology]

---

## Party Analysis

*[200-250 words: Academic observation of party dynamics and development]*

### Individual Capabilities
**[Character Name]**: [Analysis of magical/combat abilities, growth observed, potential for development]

### Group Coordination
[Tactical development, leadership dynamics, how party works together]

### Magical Education Opportunities
[Notes on party members who could benefit from formal training]

---

## Research Implications

*[200-250 words: Connect session events to ongoing studies]*

### Theoretical Connections
[How today's events relate to current research projects]

### New Hypotheses
[Questions raised by session events that warrant investigation]

### Future Investigation Priorities
[Sites, phenomena, or experiments to pursue based on discoveries]

### Ten Towns Political Considerations
[How events affect access to research sites or resources]

---

*End of Session [NUMBER] Research Notes*
*Next Priority: [Specific research action based on session]*

---

**Illustrations Required:**
- [ ] [Description of needed illustration 1]
- [ ] [Description of needed illustration 2]
- [ ] [Description of needed illustration 3]
EOF
```

## Step 2: Writing Process Workflow

```bash
cat > ../../scripts/write-journal.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "✍️  Writing Journal for Session ${SESSION_PADDED}"
echo "========================================"

# Check prerequisites
if [ ! -f "${SESSION_DIR}/content/extracted_content.json" ]; then
    echo "❌ Content extraction not complete. Run content analysis first."
    exit 1
fi

# Create writing workspace
mkdir -p "${SESSION_DIR}/content/drafts"
cd "${SESSION_DIR}"

# Copy template
cp ../../content/journal_template.md content/drafts/draft_v1.md

# Get session info
SESSION_DATE=$(jq -r '.session_date' session-info.json 2>/dev/null || echo "YYYY-MM-DD")
SESSION_TITLE=$(jq -r '.session_title' session-info.json 2>/dev/null || echo "Session Title")

# Fill in basic info
sed -i.bak "s/\[DATE\]/${SESSION_DATE}/g" content/drafts/draft_v1.md
sed -i.bak "s/\[NUMBER\]/${SESSION_NUM}/g" content/drafts/draft_v1.md
sed -i.bak "s/\[TITLE\]/${SESSION_TITLE}/g" content/drafts/draft_v1.md

echo "📝 Draft template created: content/drafts/draft_v1.md"
echo "📊 Reference materials available:"
echo "   - Transcript: transcript/cleaned_transcript.txt"
echo "   - Analysis: transcript/cleaned_transcript_analysis.json"
echo "   - Extracted content: content/extracted_content.json"
echo
echo "🎯 Writing checklist:"
echo "   1. Fill in Initial Observations (150-200 words)"
echo "   2. Document Magical Phenomena (200-250 words)"
echo "   3. Analyze Specimen Studies (250-300 words)"
echo "   4. Evaluate Party Analysis (200-250 words)"
echo "   5. Connect Research Implications (200-250 words)"
echo "   6. List needed illustrations"
echo
echo "💡 Remember Vellynne's voice:"
echo "   - Academic but passionate"
echo "   - Analytical and theoretical"
echo "   - Protective of party members"
echo "   - Excited about discoveries"
EOF

chmod +x ../../scripts/write-journal.sh
```

## Step 3: Voice Examples and Transformations

```bash
cat > content/voice_examples.md << 'EOF'
# Vellynne's Voice Examples

## Transforming Raw Content

### Combat Encounter
**Raw Transcript**: "We fought some zombies. They were tough. Bob cast fireball."

**Vellynne's Voice**: 
"The party's engagement with frost-preserved undead specimens provided fascinating data on cold-climate necromantic animation. The zombies demonstrated remarkable resilience—their tissue preservation in Icewind Dale's environment appears to enhance structural integrity beyond typical reanimated corpses. Young Bob's evocation work continues to impress; his fireball manifestation showed excellent thermal control and targeting precision for one lacking formal arcane education."

### Discovery
**Raw Transcript**: "Found an old book with weird writing in the ruins."

**Vellynne's Voice**:
"Today's archaeological discovery may prove pivotal to my research. The tome recovered from the pre-Netherese ruins bears script consistent with early binding rituals—precisely the linguistic key I've sought for my comparative analysis of ancient necromantic practices. The text's preservation in this climate presents an unexpected opportunity, though preliminary examination suggests the binding techniques described predate current Academy understanding by several centuries."

### Character Development
**Raw Transcript**: "Sarah's getting better at her spells."

**Vellynne's Voice**:
"Sarah's magical development continues along promising trajectories. Her cantrip execution has gained both precision and confidence since our expedition began. While her theoretical foundation remains limited, her intuitive grasp of magical principles suggests she would benefit tremendously from formal instruction. I find myself increasingly protective of her potential—raw talent of this caliber deserves proper cultivation."

## Language Patterns

### Academic Terminology
- "Preliminary observations suggest..."
- "Empirical evidence indicates..."
- "Theoretical implications include..."
- "Further study required to determine..."
- "Comparative analysis reveals..."

### Magical Expertise
- "Evocation demonstration"
- "Arcane manifestation"
- "Necromantic animation"
- "Spell matrix stability"
- "Magical resonance patterns"

### Personal Investment
- "Young [Character] continues to..."
- "I find myself increasingly..."
- "Their potential warrants..."
- "My protective instincts..."
- "This discovery validates my..."

### Research Focus
- "Data collection reveals..."
- "Specimen behavior indicates..."
- "Environmental factors suggest..."
- "Hypothesis testing confirms..."
- "Research implications include..."
EOF
```

## Step 4: Section-Specific Writing Guides

```bash
cat > content/section_guides.md << 'EOF'
# Section-Specific Writing Guides

## Initial Observations (150-200 words)
### Purpose
Set the scene and establish Vellynne's current research context.

### Key Elements
- Weather/environmental conditions and their effect on magic
- Party location and status
- Vellynne's current research priorities
- Connection to broader magical studies

### Writing Tips
- Start with environmental observations
- Connect weather to magical research
- Show Vellynne's protective concern for party
- Establish academic tone

## Magical Phenomena Recorded (200-250 words)
### Purpose
Document and analyze magical events from academic perspective.

### Key Elements
- Spell casting with technical analysis
- Magical item properties and research potential
- Environmental magical effects
- Comparisons to Academy standards

### Writing Tips
- Use technical magical terminology
- Compare to established theory
- Note innovations or variations
- Express excitement about discoveries

## Specimen Studies (250-300 words)
### Purpose
Detailed analysis of creatures, especially undead.

### Key Elements
- Physical characteristics from academic perspective
- Behavioral patterns and environmental adaptations
- Combat effectiveness and tactical notes
- Research implications for undead studies

### Writing Tips
- Use scientific observation language
- Focus on undead when possible
- Note environmental effects (cold climate)
- Connect to broader necromantic research

## Party Analysis (200-250 words)
### Purpose
Academic observation of party development and dynamics.

### Key Elements
- Individual character growth and abilities
- Group tactical development
- Magical education opportunities
- Leadership and coordination patterns

### Writing Tips
- Show protective academic interest
- Note potential for formal training
- Analyze tactical improvements
- Express pride in their development

## Research Implications (200-250 words)
### Purpose
Connect session events to ongoing research and future priorities.

### Key Elements
- Theoretical connections to current studies
- New hypotheses and questions raised
- Future investigation priorities
- Political considerations for research access

### Writing Tips
- Link discoveries to established research
- Pose new questions for investigation
- Consider practical research constraints
- Show excitement about future possibilities
EOF
```

## Step 5: Quality Control Checklist

```bash
cat > ../../scripts/review-writing.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
SESSION_DIR="sessions/session-${SESSION_NUM}"
DRAFT_FILE="${SESSION_DIR}/content/drafts/draft_v1.md"

echo "📋 Writing Quality Review for Session ${SESSION_NUM}"
echo "=============================================="

if [ ! -f "$DRAFT_FILE" ]; then
    echo "❌ Draft file not found: $DRAFT_FILE"
    exit 1
fi

# Word count check
echo "📊 Word Count Analysis:"
TOTAL_WORDS=$(wc -w < "$DRAFT_FILE")
echo "   Total words: $TOTAL_WORDS"

# Section word counts (approximate)
INITIAL_WORDS=$(sed -n '/## Initial Observations/,/## Magical Phenomena/p' "$DRAFT_FILE" | wc -w)
MAGIC_WORDS=$(sed -n '/## Magical Phenomena/,/## Specimen Studies/p' "$DRAFT_FILE" | wc -w)
SPECIMEN_WORDS=$(sed -n '/## Specimen Studies/,/## Party Analysis/p' "$DRAFT_FILE" | wc -w)
PARTY_WORDS=$(sed -n '/## Party Analysis/,/## Research Implications/p' "$DRAFT_FILE" | wc -w)
RESEARCH_WORDS=$(sed -n '/## Research Implications/,/End of Session/p' "$DRAFT_FILE" | wc -w)

echo "   Initial Observations: $INITIAL_WORDS (target: 150-200)"
echo "   Magical Phenomena: $MAGIC_WORDS (target: 200-250)"
echo "   Specimen Studies: $SPECIMEN_WORDS (target: 250-300)"
echo "   Party Analysis: $PARTY_WORDS (target: 200-250)"
echo "   Research Implications: $RESEARCH_WORDS (target: 200-250)"

# Voice consistency check
echo
echo "🎭 Voice Consistency Check:"

# Check for academic language
ACADEMIC_TERMS=$(grep -c -i "observation\|analysis\|research\|study\|theoretical\|empirical" "$DRAFT_FILE")
echo "   Academic terminology: $ACADEMIC_TERMS instances"

# Check for magical terminology
MAGIC_TERMS=$(grep -c -i "spell\|magic\|arcane\|necromantic\|evocation\|enchant" "$DRAFT_FILE")
echo "   Magical terminology: $MAGIC_TERMS instances"

# Check for personal investment
PERSONAL_TERMS=$(grep -c -i "young\|protective\|potential\|development\|growth" "$DRAFT_FILE")
echo "   Personal investment: $PERSONAL_TERMS instances"

# Overall assessment
echo
if [ $TOTAL_WORDS -gt 800 ] && [ $ACADEMIC_TERMS -gt 5 ] && [ $MAGIC_TERMS -gt 10 ]; then
    echo "✅ Draft meets quality standards"
else
    echo "⚠️  Draft may need revision"
    echo "   - Check word count targets"
    echo "   - Enhance academic voice"
    echo "   - Add more magical terminology"
fi

echo
echo "📝 Next steps:"
echo "   1. Review and revise draft"
echo "   2. Check against voice examples"
echo "   3. Verify all sections complete"
echo "   4. Plan illustrations needed"
EOF

chmod +x ../../scripts/review-writing.sh
```

## Step 6: Revision Process

```bash
cat > content/revision_checklist.md << 'EOF'
# Revision Checklist

## Content Completeness
- [ ] All five sections written and complete
- [ ] Word count targets met for each section
- [ ] Key session events covered
- [ ] Vellynne's interests addressed

## Voice Consistency
- [ ] Academic but passionate tone throughout
- [ ] Appropriate magical terminology used
- [ ] Shows protective interest in party
- [ ] Connects to broader research goals
- [ ] Maintains scholarly objectivity

## Technical Accuracy
- [ ] D&D terms and mechanics correct
- [ ] Character names spelled correctly
- [ ] Spell names and effects accurate
- [ ] Location names consistent

## Narrative Flow
- [ ] Logical progression between sections
- [ ] Smooth transitions between topics
- [ ] Consistent timeline and references
- [ ] Engaging and readable despite academic tone

## Research Integration
- [ ] References to Blackstaff Academy
- [ ] Connections to necromantic studies
- [ ] Mentions of ongoing research projects
- [ ] Future investigation priorities identified

## Illustration Planning
- [ ] Specific illustrations identified
- [ ] Descriptions detailed enough for generation
- [ ] Mix of creature studies, diagrams, and maps
- [ ] Illustrations support journal content
EOF
```

## Troubleshooting

### Writer's Block
- **Review extracted content**: Use automated analysis as inspiration
- **Read voice examples**: Get back into Vellynne's mindset
- **Start with easiest section**: Build momentum
- **Use writing prompts**: Answer specific questions about events

### Voice Inconsistency
- **Read aloud**: Check if it sounds like Vellynne
- **Compare to examples**: Match language patterns
- **Add academic terminology**: Enhance scholarly voice
- **Show personal investment**: Include protective feelings

### Missing Content
- **Review transcript**: Look for missed events
- **Check analysis**: Verify automated extraction
- **Ask party members**: Clarify unclear moments
- **Focus on Vellynne's interests**: Prioritize relevant content

## Next Steps

With writing guide complete:

1. ✅ Vellynne's voice and character understood
2. ✅ Writing templates and examples ready
3. ✅ Section-specific guides available
4. ✅ Quality control process established

Continue to **[08-Template-System.md](08-Template-System.md)** to create reusable templates for consistent journal formatting.

## Quick Commands

```bash
# Start writing process
./scripts/write-journal.sh 01

# Review draft quality
./scripts/review-writing.sh 01
```
