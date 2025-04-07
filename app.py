#!/usr/bin/env python3
"""
Flask web application for displaying Wikipedia category word clouds.
"""

from flask import Flask, render_template, request, jsonify
import os
from wiki_category_analysis import analyze_category

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a Wikipedia category and return word frequencies."""
    category = request.form.get('category', '')
    
    if not category:
        return jsonify({'error': 'Category name is required'}), 400
    
    try:
        # Analyze the category using the existing script
        word_count = analyze_category(category)
        
        # Convert to format suitable for word cloud
        # Format: [{"text": "word", "size": frequency}, ...]
        word_cloud_data = [
            {"text": word, "size": count}
            for word, count in word_count.most_common(100)
        ]
        
        return jsonify({
            'category': category,
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