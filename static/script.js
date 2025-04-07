document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('category-form');
    const loadingDiv = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const resultTitle = document.getElementById('result-title');
    const wordCloudDiv = document.getElementById('word-cloud');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading indicator
        loadingDiv.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        
        // Get form data
        const formData = new FormData(form);
        const category = formData.get('category');
        
        // Send request to server
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred');
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingDiv.classList.add('hidden');
            
            // Show result container
            resultContainer.classList.remove('hidden');
            resultTitle.textContent = `Word Cloud for: ${data.category}`;
            
            // Generate word cloud
            generateWordCloud(data.wordCloudData);
        })
        .catch(error => {
            // Hide loading indicator
            loadingDiv.classList.add('hidden');
            
            // Show error
            alert(`Error: ${error.message}`);
        });
    });
    
    function generateWordCloud(words) {
        // Clear previous word cloud
        wordCloudDiv.innerHTML = '';
        
        // Set dimensions
        const width = wordCloudDiv.offsetWidth;
        const height = 500;
        
        // Find the maximum frequency for scaling
        const maxSize = d3.max(words, d => d.size);
        
        // Scale for font size (between 10 and 100)
        const fontSizeScale = d3.scaleLinear()
            .domain([1, maxSize])
            .range([10, 100]);
        
        // Create the layout
        const layout = d3.layout.cloud()
            .size([width, height])
            .words(words)
            .padding(5)
            .rotate(() => ~~(Math.random() * 2) * 90)
            .fontSize(d => fontSizeScale(d.size))
            .on("end", draw);
        
        // Start the layout
        layout.start();
        
        // Function to draw the word cloud
        function draw(words) {
            // Create SVG
            const svg = d3.select("#word-cloud").append("svg")
                .attr("width", layout.size()[0])
                .attr("height", layout.size()[1])
                .append("g")
                .attr("transform", `translate(${layout.size()[0] / 2},${layout.size()[1] / 2})`);
            
            // Add words
            svg.selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", d => `${d.size}px`)
                .style("fill", () => d3.schemeCategory10[Math.floor(Math.random() * 10)])
                .attr("text-anchor", "middle")
                .attr("transform", d => `translate(${d.x},${d.y}) rotate(${d.rotate})`)
                .text(d => d.text);
        }
    }
});