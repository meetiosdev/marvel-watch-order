document.addEventListener('DOMContentLoaded', () => {
    const timelineContainer = document.getElementById('timeline-container');
    
    // Generate the HTML for the movies timeline
    let html = '';
    
    moviesData.forEach((phaseData, phaseIndex) => {
        html += `
            <div class="phase-section" style="animation-delay: ${phaseIndex * 0.2}s">
                <h2 class="phase-title">${phaseData.phase}</h2>
                <div class="movie-list">
        `;
        
        phaseData.movies.forEach(movie => {
            const hasNotes = movie.notes && movie.notes.trim() !== '';
            
            const torrentButton = movie.torrentUrl 
                ? `<a href="${movie.torrentUrl}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
                    <i data-lucide="download"></i> Torrent Page
                   </a>`
                : `<button class="btn btn-disabled" disabled>
                    <i data-lucide="download"></i> Add link in movies.js
                   </button>`;
                   
            const healthMap = {
                'green': 'Best',
                'blue': 'Better',
                'yellow': 'Good',
                'red': 'Bad',
                'unknown': 'Unknown'
            };
            const healthVal = movie.magnetHealth || 'unknown';
            const healthLabel = healthMap[healthVal] || 'Unknown';
            const healthClass = `health-${healthVal}`;
            const statusClass = `status-${healthVal}`;
            
            const healthBadge = `<div class="health-status-badge ${statusClass}">
                <span class="health-dot ${healthClass}"></span> Health: ${healthLabel}
            </div>`;

            const magnetButton = movie.magnetUrl
                ? `<a href="${movie.magnetUrl}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                    <i data-lucide="magnet"></i> Magnet Link
                   </a>`
                : `<button class="btn btn-disabled" disabled>
                    <i data-lucide="magnet"></i> Add link in movies.js
                   </button>`;

            html += `
                <div class="movie-card">
                    <div class="movie-header">
                        <h3 class="m-title">${movie.id}. ${movie.title}</h3>
                        <div class="m-badges">
                            <span class="badge badge-year"><i data-lucide="calendar"></i> Released: ${movie.releaseYear}</span>
                            <span class="badge badge-set"><i data-lucide="clock"></i> Set in: ${movie.setIn}</span>
                        </div>
                    </div>
                    <div class="m-content">
                        <p class="m-desc">${movie.description}</p>
                        ${hasNotes ? `
                        <div class="m-notes-card">
                            <div class="m-notes-title"><i data-lucide="info"></i> Key Details</div>
                            <div class="m-notes-text">${movie.notes}</div>
                        </div>
                        ` : ''}
                    </div>
                    <div class="m-links">
                        ${healthBadge}
                        ${torrentButton}
                        ${magnetButton}
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });
    
    timelineContainer.innerHTML = html;
    
    // Initialize Lucide icons
    lucide.createIcons();
});
