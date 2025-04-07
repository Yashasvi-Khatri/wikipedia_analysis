#!/usr/bin/env python3
"""
Flask web application for displaying Wikipedia category word clouds.
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from wiki_category_analysis import analyze_category

# Add the templates directory to the Python path so we can import the color_palette module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
from color_palette import get_palette, PALETTES

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page."""
    # Pass the available color palettes to the template
    return render_template('index.html', palettes=list(PALETTES.keys()))

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a Wikipedia category and return word frequencies."""
    category = request.form.get('category', '')
    palette_name = request.form.get('palette', 'default')
    
    if not category:
        return jsonify({'error': 'Category name is required'}), 400
    
    try:
        # Get the selected color palette
        palette = get_palette(palette_name)
        
        # Analyze the category using the existing script
        word_count = analyze_category(category)
        
        # Convert to format suitable for word cloud
        # Format: [{"text": "word", "size": frequency, "color": "#hex"}, ...]
        word_cloud_data = []
        for i, (word, count) in enumerate(word_count.most_common(100)):
            word_cloud_data.append({
                "text": word,
                "size": count,
                "color": palette[i]  # Assign a color from the palette
            })
        
        return jsonify({
            'category': category,
            'palette': palette_name,
            'colors': palette.get_colors(),
            'wordCount': dict(word_count),
            'wordCloudData': word_cloud_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True)