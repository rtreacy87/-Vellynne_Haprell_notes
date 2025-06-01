# 15 - RoughJS Diagrams

Creating hand-drawn style diagrams for Vellynne's research notes using RoughJS.

## Prerequisites Checklist

- [ ] Basic HTML/CSS knowledge
- [ ] Text editor installed
- [ ] Web browser for testing
- [ ] Internet connection for loading libraries

## Overview

RoughJS is a small JavaScript library that lets you create graphics with a hand-drawn, sketchy appearance. This is perfect for Vellynne's research notes, as it mimics the look of diagrams drawn with quill and ink.

## Example Diagram: Vampire Influence Network

Here's what we'll create - a diagram showing the relationship between an Elder Vampire and its thralls:

```
                    ┌─────────────┐
                    │ ELDER       │
                    │ VAMPIRE     │
                    └─────┬───────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
    ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
    │ VAMPIRE     │ │ VAMPIRE   │ │ VAMPIRE     │
    │ BRIDE #1    │ │ BRIDE #2  │ │ BRIDE #3    │
    └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
           │              │              │
     ┌─────▼────┐    ┌────▼────┐    ┌────▼────┐
     │ THRALLS  │    │ THRALLS │    │ THRALLS │
     └──────────┘    └─────────┘    └─────────┘
```

## Step 1: Set Up Your HTML File

Create a new HTML file called `vampire-diagram.html` and add this basic structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vellynne's Vampire Influence Diagram</title>
    <style>
        body {
            background-color: #f9f0da; /* Parchment color */
            font-family: 'Georgia', serif;
            color: #301800; /* Dark brown ink */
            padding: 20px;
        }
        .diagram-container {
            width: 600px;
            height: 500px;
            margin: 0 auto;
            position: relative;
        }
        .title {
            text-align: center;
            font-style: italic;
            margin-bottom: 20px;
        }
        .note {
            position: absolute;
            font-size: 0.8em;
            font-style: italic;
            transform: rotate(-3deg);
            background-color: rgba(255,255,255,0.5);
            padding: 3px 8px;
            border: 1px solid #301800;
        }
    </style>
</head>
<body>
    <h1 class="title">Elder Vampire Influence Diagram</h1>
    <div class="diagram-container" id="diagram"></div>
    
    <!-- Load RoughJS library -->
    <script src="https://cdn.jsdelivr.net/npm/roughjs@4.5.2/bundled/rough.js"></script>
    
    <script>
        // Our diagram code will go here
    </script>
</body>
</html>
```

## Step 2: Create the Basic Diagram

Add this code inside the `<script>` tags:

```javascript
// Wait for the page to load
window.addEventListener('load', function() {
    // Get the container element
    const container = document.getElementById('diagram');
    
    // Create a RoughJS canvas that fills the container
    const rc = rough.canvas(document.createElement('canvas'));
    rc.canvas.width = 600;
    rc.canvas.height = 500;
    container.appendChild(rc.canvas);
    
    // Set drawing options for a quill pen look
    const drawOptions = {
        roughness: 2.5,          // How rough the lines should be
        stroke: '#301800',       // Dark brown ink color
        strokeWidth: 2,          // Line thickness
        fillStyle: 'solid',      // Fill style for shapes
        fill: '#f9f0da',         // Light fill color (parchment)
        fillWeight: 0.5,         // Weight of the fill
        hachureAngle: 60         // Angle of fill pattern
    };
    
    // Draw the Elder Vampire box
    rc.rectangle(250, 30, 120, 60, drawOptions);
    
    // Draw the Vampire Brides boxes
    rc.rectangle(80, 180, 120, 60, drawOptions);  // Bride #1
    rc.rectangle(250, 180, 120, 60, drawOptions); // Bride #2
    rc.rectangle(420, 180, 120, 60, drawOptions); // Bride #3
    
    // Draw the Thralls boxes
    rc.rectangle(100, 320, 80, 40, drawOptions);  // Thralls #1
    rc.rectangle(270, 320, 80, 40, drawOptions);  // Thralls #2
    rc.rectangle(440, 320, 80, 40, drawOptions);  // Thralls #3
    
    // Draw connection lines
    // Elder to Brides
    rc.line(310, 90, 310, 150, drawOptions);      // Center line down
    rc.line(310, 150, 140, 150, drawOptions);     // Left horizontal
    rc.line(310, 150, 480, 150, drawOptions);     // Right horizontal
    rc.line(140, 150, 140, 180, drawOptions);     // Down to Bride #1
    rc.line(310, 150, 310, 180, drawOptions);     // Down to Bride #2
    rc.line(480, 150, 480, 180, drawOptions);     // Down to Bride #3
    
    // Brides to Thralls
    rc.line(140, 240, 140, 320, drawOptions);     // Bride #1 to Thralls
    rc.line(310, 240, 310, 320, drawOptions);     // Bride #2 to Thralls
    rc.line(480, 240, 480, 320, drawOptions);     // Bride #3 to Thralls
    
    // Add text to the canvas
    const ctx = rc.canvas.getContext('2d');
    ctx.font = 'bold 14px Georgia';
    ctx.fillStyle = '#301800';
    ctx.textAlign = 'center';
    
    // Elder Vampire text
    ctx.fillText('ELDER', 310, 50);
    ctx.fillText('VAMPIRE', 310, 70);
    
    // Vampire Brides text
    ctx.fillText('VAMPIRE', 140, 200);
    ctx.fillText('BRIDE #1', 140, 220);
    
    ctx.fillText('VAMPIRE', 310, 200);
    ctx.fillText('BRIDE #2', 310, 220);
    
    ctx.fillText('VAMPIRE', 480, 200);
    ctx.fillText('BRIDE #3', 480, 220);
    
    // Thralls text
    ctx.fillText('THRALLS', 140, 345);
    ctx.fillText('THRALLS', 310, 345);
    ctx.fillText('THRALLS', 480, 345);
});
```

## Step 3: Add Handwritten Notes

Now let's add some handwritten-style notes to make it look more like Vellynne's research. Add this code after the text drawing code:

```javascript
// Add handwritten notes
function addNote(text, x, y, rotation) {
    const note = document.createElement('div');
    note.className = 'note';
    note.textContent = text;
    note.style.left = x + 'px';
    note.style.top = y + 'px';
    note.style.transform = `rotate(${rotation}deg)`;
    container.appendChild(note);
}

// Add some research notes
addNote('Direct mental control', 330, 110, -2);
addNote('Extremely dangerous!', 350, 40, 3);
addNote('Weakest link', 200, 290, -4);
addNote('Potential informants', 500, 350, 2);
```

## Step 4: Add Finishing Touches

Let's add some final details to make the diagram look more authentic:

```javascript
// Add a sketchy circle around the Elder Vampire to emphasize importance
rc.circle(310, 60, 140, {
    stroke: '#301800',
    strokeWidth: 1,
    roughness: 3,
    fill: 'rgba(139, 0, 0, 0.1)',  // Very light red fill
    fillStyle: 'hachure'
});

// Add a small Vellynne signature
ctx.font = 'italic 12px Georgia';
ctx.textAlign = 'right';
ctx.fillText('- Vellynne Harpell', 580, 480);

// Add date stamp
ctx.font = 'italic 10px Georgia';
ctx.textAlign = 'left';
ctx.fillText('Documented: Hammer, 1489 DR', 20, 480);
```

## Complete Example

The complete code should look like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vellynne's Vampire Influence Diagram</title>
    <style>
        body {
            background-color: #f9f0da; /* Parchment color */
            font-family: 'Georgia', serif;
            color: #301800; /* Dark brown ink */
            padding: 20px;
        }
        .diagram-container {
            width: 600px;
            height: 500px;
            margin: 0 auto;
            position: relative;
        }
        .title {
            text-align: center;
            font-style: italic;
            margin-bottom: 20px;
        }
        .note {
            position: absolute;
            font-size: 0.8em;
            font-style: italic;
            transform: rotate(-3deg);
            background-color: rgba(255,255,255,0.5);
            padding: 3px 8px;
            border: 1px solid #301800;
        }
    </style>
</head>
<body>
    <h1 class="title">Elder Vampire Influence Diagram</h1>
    <div class="diagram-container" id="diagram"></div>
    
    <!-- Load RoughJS library -->
    <script src="https://cdn.jsdelivr.net/npm/roughjs@4.5.2/bundled/rough.js"></script>
    
    <script>
        // Wait for the page to load
        window.addEventListener('load', function() {
            // Get the container element
            const container = document.getElementById('diagram');
            
            // Create a RoughJS canvas that fills the container
            const rc = rough.canvas(document.createElement('canvas'));
            rc.canvas.width = 600;
            rc.canvas.height = 500;
            container.appendChild(rc.canvas);
            
            // Set drawing options for a quill pen look
            const drawOptions = {
                roughness: 2.5,          // How rough the lines should be
                stroke: '#301800',       // Dark brown ink color
                strokeWidth: 2,          // Line thickness
                fillStyle: 'solid',      // Fill style for shapes
                fill: '#f9f0da',         // Light fill color (parchment)
                fillWeight: 0.5,         // Weight of the fill
                hachureAngle: 60         // Angle of fill pattern
            };
            
            // Draw the Elder Vampire box
            rc.rectangle(250, 30, 120, 60, drawOptions);
            
            // Draw the Vampire Brides boxes
            rc.rectangle(80, 180, 120, 60, drawOptions);  // Bride #1
            rc.rectangle(250, 180, 120, 60, drawOptions); // Bride #2
            rc.rectangle(420, 180, 120, 60, drawOptions); // Bride #3
            
            // Draw the Thralls boxes
            rc.rectangle(100, 320, 80, 40, drawOptions);  // Thralls #1
            rc.rectangle(270, 320, 80, 40, drawOptions);  // Thralls #2
            rc.rectangle(440, 320, 80, 40, drawOptions);  // Thralls #3
            
            // Draw connection lines
            // Elder to Brides
            rc.line(310, 90, 310, 150, drawOptions);      // Center line down
            rc.line(310, 150, 140, 150, drawOptions);     // Left horizontal
            rc.line(310, 150, 480, 150, drawOptions);     // Right horizontal
            rc.line(140, 150, 140, 180, drawOptions);     // Down to Bride #1
            rc.line(310, 150, 310, 180, drawOptions);     // Down to Bride #2
            rc.line(480, 150, 480, 180, drawOptions);     // Down to Bride #3
            
            // Brides to Thralls
            rc.line(140, 240, 140, 320, drawOptions);     // Bride #1 to Thralls
            rc.line(310, 240, 310, 320, drawOptions);     // Bride #2 to Thralls
            rc.line(480, 240, 480, 320, drawOptions);     // Bride #3 to Thralls
            
            // Add a sketchy circle around the Elder Vampire to emphasize importance
            rc.circle(310, 60, 140, {
                stroke: '#301800',
                strokeWidth: 1,
                roughness: 3,
                fill: 'rgba(139, 0, 0, 0.1)',  // Very light red fill
                fillStyle: 'hachure'
            });
            
            // Add text to the canvas
            const ctx = rc.canvas.getContext('2d');
            ctx.font = 'bold 14px Georgia';
            ctx.fillStyle = '#301800';
            ctx.textAlign = 'center';
            
            // Elder Vampire text
            ctx.fillText('ELDER', 310, 50);
            ctx.fillText('VAMPIRE', 310, 70);
            
            // Vampire Brides text
            ctx.fillText('VAMPIRE', 140, 200);
            ctx.fillText('BRIDE #1', 140, 220);
            
            ctx.fillText('VAMPIRE', 310, 200);
            ctx.fillText('BRIDE #2', 310, 220);
            
            ctx.fillText('VAMPIRE', 480, 200);
            ctx.fillText('BRIDE #3', 480, 220);
            
            // Thralls text
            ctx.fillText('THRALLS', 140, 345);
            ctx.fillText('THRALLS', 310, 345);
            ctx.fillText('THRALLS', 480, 345);
            
            // Add a small Vellynne signature
            ctx.font = 'italic 12px Georgia';
            ctx.textAlign = 'right';
            ctx.fillText('- Vellynne Harpell', 580, 480);
            
            // Add date stamp
            ctx.font = 'italic 10px Georgia';
            ctx.textAlign = 'left';
            ctx.fillText('Documented: Hammer, 1489 DR', 20, 480);
            
            // Add handwritten notes
            function addNote(text, x, y, rotation) {
                const note = document.createElement('div');
                note.className = 'note';
                note.textContent = text;
                note.style.left = x + 'px';
                note.style.top = y + 'px';
                note.style.transform = `rotate(${rotation}deg)`;
                container.appendChild(note);
            }
            
            // Add some research notes
            addNote('Direct mental control', 330, 110, -2);
            addNote('Extremely dangerous!', 350, 40, 3);
            addNote('Weakest link', 200, 290, -4);
            addNote('Potential informants', 500, 350, 2);
        });
    </script>
</body