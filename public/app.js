/**
 * UK Postcode to Substation Lookup - Frontend Application
 * postcodes.energy
 */

// Global state
let map = null;
let currentMarker = null;
let currentPolygon = null;
let postcodeLookup = {}; // Cache for loaded chunks
let substationDetails = {};
let allPostcodesInArea = [];
let currentPage = 1;
const POSTCODES_PER_PAGE = 100;

// DOM Elements
const postcodeInput = document.getElementById('postcode-input');
const searchBtn = document.getElementById('search-btn');
const autocompleteList = document.getElementById('autocomplete-list');
const resultsContainer = document.getElementById('results-container');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');

// Initialize application
async function init() {
    console.log('🚀 Initializing application...');
    showLoading('Loading data...');
    
    try {
        // Load data files
        console.log('Step 1: Loading data...');
        await loadData();
        console.log('✓ Data loaded');
        
        // Initialize map
        console.log('Step 2: Initializing map...');
        initMap();
        console.log('✓ Map initialized');
        
        // Setup event listeners
        console.log('Step 3: Setting up event listeners...');
        setupEventListeners();
        console.log('✓ Event listeners ready');
        
        hideLoading();
        
        console.log('✅ Application initialized successfully');
    } catch (error) {
        console.error('❌ Initialization error:', error);
        showError('Failed to load application data. Please refresh the page.');
        hideLoading();
    }
}

// Load data files (only substations - chunks loaded on-demand)
async function loadData() {
    try {
        console.log('Starting to load data files...');
        
        // Load substation details only
        const detailsResponse = await fetch('data/substations.json');
        console.log('Substation details response:', detailsResponse.status);
        if (!detailsResponse.ok) throw new Error('Failed to load substation data');
        substationDetails = await detailsResponse.json();
        
        console.log(`✓ Loaded ${Object.keys(substationDetails).length} substations`);
        console.log('✓ Postcode chunks will be loaded on-demand');
    } catch (error) {
        console.error('❌ Error loading data:', error);
        throw error;
    }
}

// Load a specific postcode area chunk on-demand
async function loadChunk(area) {
    // Check if already loaded
    if (postcodeLookup[area]) {
        console.log(`Chunk ${area} already cached`);
        return postcodeLookup[area];
    }
    
    try {
        console.log(`Loading chunk: ${area}.json`);
        const response = await fetch(`data/chunks/${area}.json`);
        if (!response.ok) {
            throw new Error(`Chunk ${area} not found`);
        }
        const chunkData = await response.json();
        
        // Cache the loaded chunk
        postcodeLookup[area] = chunkData;
        console.log(`✓ Loaded chunk ${area} (${Object.keys(chunkData).length} postcodes)`);
        
        return chunkData;
    } catch (error) {
        console.error(`Error loading chunk ${area}:`, error);
        return null;
    }
}

// Initialize Leaflet map
function initMap() {
    try {
        console.log('Creating Leaflet map instance...');
        map = L.map('map').setView([54.5, -3.5], 6); // Center on UK
        console.log('Map instance created:', map);
        
        console.log('Adding OpenStreetMap tiles...');
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(map);
        console.log('Tiles added successfully');
    } catch (error) {
        console.error('Error initializing map:', error);
        throw error;
    }
}

// Setup event listeners
function setupEventListeners() {
    // Search button
    searchBtn.addEventListener('click', handleSearch);
    
    // Enter key in search box
    postcodeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
    
    // Autocomplete
    postcodeInput.addEventListener('input', handleAutocomplete);
    
    // Click outside autocomplete to close
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-box')) {
            autocompleteList.classList.remove('active');
        }
    });
    
    // Export button
    document.getElementById('export-btn').addEventListener('click', exportToCSV);
    
    // Pagination
    document.getElementById('prev-page').addEventListener('click', () => changePage(-1));
    document.getElementById('next-page').addEventListener('click', () => changePage(1));
    
    // Feedback form
    document.getElementById('feedback-form').addEventListener('submit', handleFeedbackSubmit);
}

// Handle postcode search
async function handleSearch() {
    const postcode = normalizePostcode(postcodeInput.value);
    
    if (!postcode) {
        showError('Please enter a valid UK postcode');
        return;
    }
    
    // Show loading state
    showLoading('Loading postcode data...');
    
    try {
        // Find substation for this postcode (loads chunk if needed)
        const postcodeData = await findSubstationForPostcode(postcode);
        
        hideLoading();
        
        if (!postcodeData) {
            showError(`Postcode "${postcode}" not found. It may be outside covered areas or invalid.`);
            return;
        }
        
        // Display results
        displayResults(postcode, postcodeData);
    } catch (error) {
        hideLoading();
        console.error('Search error:', error);
        showError('An error occurred while searching. Please try again.');
    }
}

// Normalize postcode format (keep space before last 3 chars)
function normalizePostcode(postcode) {
    // Remove all spaces, convert to uppercase, then add space before last 3 chars
    const clean = postcode.replace(/\s+/g, '').toUpperCase();
    if (clean.length >= 5) {
        // Add space before last 3 characters (e.g., N155QA -> N15 5QA)
        return clean.slice(0, -3) + ' ' + clean.slice(-3);
    }
    return clean;
}

// Find substation ID and coordinates for a given postcode
async function findSubstationForPostcode(postcode) {
    // Extract outward code (e.g., "SW1A" from "SW1A1AA", "N15" from "N15 5QA")
    const outwardMatch = postcode.match(/^([A-Z]{1,2}\d{1,2}[A-Z]?)/);
    if (!outwardMatch) return null;
    
    const outward = outwardMatch[1];
    
    // Load the chunk for this area if not already cached
    const chunkData = await loadChunk(outward);
    
    if (!chunkData) {
        return null;
    }
    
    // Look up the postcode in the chunk
    if (chunkData[postcode]) {
        return chunkData[postcode];
    }
    
    return null;
}

// Display results for a postcode
async function displayResults(postcode, postcodeData) {
    hideError();
    
    const substationId = postcodeData.substation_id;
    const substation = substationDetails[substationId];
    
    if (!substation) {
        showError('Substation data not found');
        return;
    }
    
    // Update substation info
    document.getElementById('sub-name').textContent = substation.name || substationId;
    document.getElementById('sub-dno').textContent = substation.dno;
    document.getElementById('sub-area').textContent = substation.license_area;
    document.getElementById('sub-count').textContent = substation.postcode_count.toLocaleString();
    
    // Load nearby chunks to get more complete postcode list
    await loadNearbyChunks(postcode);
    
    // Get all postcodes in this substation area
    allPostcodesInArea = getAllPostcodesInSubstation(substationId);
    
    // Display postcodes list
    currentPage = 1;
    displayPostcodesList();
    
    // Update map immediately (it's already visible)
    updateMap(postcode, postcodeData, substation);
    
    // Show results container (info and postcodes)
    resultsContainer.classList.remove('hidden');
}

// Load nearby chunks to get more complete postcode data
async function loadNearbyChunks(postcode) {
    // Extract area prefix (e.g., "IV" from "IV1 2DA")
    const areaPrefix = postcode.match(/^[A-Z]+/)[0];
    
    // Load chunks for this area (e.g., IV1-IV99)
    console.log(`Loading nearby chunks for area: ${areaPrefix}`);
    const loadPromises = [];
    
    for (let i = 1; i <= 99; i++) {
        const chunkName = `${areaPrefix}${i}`;
        // Try to load, but don't fail if chunk doesn't exist
        loadPromises.push(
            loadChunk(chunkName).catch(() => null)
        );
    }
    
    // Also try without number (e.g., "IV")
    loadPromises.push(loadChunk(areaPrefix).catch(() => null));
    
    // Wait for all to complete (successful or failed)
    await Promise.all(loadPromises);
    console.log(`Finished loading chunks for ${areaPrefix} area`);
}

// Get all postcodes for a substation
function getAllPostcodesInSubstation(substationId) {
    // Scan through all loaded chunks to find postcodes in this substation
    const postcodes = [];
    
    console.log(`Looking for postcodes in substation: ${substationId}`);
    console.log(`Loaded chunks: ${Object.keys(postcodeLookup).join(', ')}`);
    
    for (const outwardCode in postcodeLookup) {
        const chunk = postcodeLookup[outwardCode];
        for (const postcode in chunk) {
            if (chunk[postcode].substation_id === substationId) {
                postcodes.push(postcode);
            }
        }
    }
    
    console.log(`Found ${postcodes.length} postcodes in substation ${substationId}`);
    
    // Sort alphabetically
    return postcodes.sort();
}

// Display paginated postcodes list
function displayPostcodesList() {
    const startIdx = (currentPage - 1) * POSTCODES_PER_PAGE;
    const endIdx = startIdx + POSTCODES_PER_PAGE;
    const pagePostcodes = allPostcodesInArea.slice(startIdx, endIdx);
    
    const listContainer = document.getElementById('postcodes-list');
    listContainer.innerHTML = pagePostcodes
        .map(pc => `<div class="postcode-item">${formatPostcode(pc)}</div>`)
        .join('');
    
    // Update pagination
    const totalPages = Math.ceil(allPostcodesInArea.length / POSTCODES_PER_PAGE);
    document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage === totalPages;
    
    if (totalPages > 1) {
        document.getElementById('pagination').classList.remove('hidden');
    } else {
        document.getElementById('pagination').classList.add('hidden');
    }
}

// Format postcode with space (if not already formatted)
function formatPostcode(postcode) {
    // If already has space, return as-is
    if (postcode.includes(' ')) {
        return postcode;
    }
    // Insert space before last 3 characters
    return postcode.slice(0, -3) + ' ' + postcode.slice(-3);
}

// Change page
function changePage(direction) {
    currentPage += direction;
    displayPostcodesList();
    document.getElementById('postcodes-list').scrollIntoView({ behavior: 'smooth' });
}

// Update map with postcode and substation boundary
function updateMap(postcode, postcodeData, substation) {
    // Remove existing markers/polygons
    if (currentMarker) map.removeLayer(currentMarker);
    if (currentPolygon) map.removeLayer(currentPolygon);
    
    // Add substation boundary
    if (substation.boundary) {
        try {
            console.log('Drawing boundary for substation:', substation.name);
            currentPolygon = L.geoJSON(substation.boundary, {
                style: {
                    color: '#667eea',
                    weight: 2,
                    fillOpacity: 0.2
                }
            }).addTo(map);
            
            // Fit map to boundary
            map.fitBounds(currentPolygon.getBounds(), { padding: [50, 50] });
            console.log('Map updated successfully');
        } catch (error) {
            console.error('Error drawing boundary:', error);
            // If boundary fails, just center on UK
            map.setView([54.5, -3.5], 6);
        }
    } else {
        console.warn('No boundary data available for this substation');
        // Center on UK if no boundary
        map.setView([54.5, -3.5], 6);
    }
    
    // Add marker for searched postcode
    if (postcodeData.lat && postcodeData.lng) {
        // Use default Leaflet marker (blue pin)
        currentMarker = L.marker([postcodeData.lat, postcodeData.lng]).addTo(map);
        
        currentMarker.bindPopup(`<strong>📍 ${postcode}</strong><br><small>${substation.name}</small>`).openPopup();
        console.log('Marker added at:', postcodeData.lat, postcodeData.lng);
    }
}

// Autocomplete functionality (works with loaded chunks only)
function handleAutocomplete() {
    const value = postcodeInput.value.replace(/\s+/g, '').toUpperCase();
    
    if (value.length < 3) {  // Require 3+ characters to avoid too many suggestions
        autocompleteList.classList.remove('active');
        return;
    }
    
    // Note: Autocomplete only works with already-loaded chunks
    // This is a lightweight approach to avoid loading all 2,414 chunk files
    const matches = [];
    
    // Check loaded chunks for matches
    for (const outward in postcodeLookup) {
        const chunkData = postcodeLookup[outward];
        for (const postcode in chunkData) {
            if (postcode.replace(/\s+/g, '').startsWith(value)) {
                matches.push(postcode);
                if (matches.length >= 10) break;
            }
        }
        if (matches.length >= 10) break;
    }
    
    // Display matches
    if (matches.length > 0) {
        autocompleteList.innerHTML = matches
            .slice(0, 10)
            .map(pc => `<div class="autocomplete-item" data-postcode="${pc}">${formatPostcode(pc)}</div>`)
            .join('');
        
        // Add click handlers
        autocompleteList.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', () => {
                postcodeInput.value = item.dataset.postcode;
                autocompleteList.classList.remove('active');
                handleSearch();
            });
        });
        
        autocompleteList.classList.add('active');
    } else {
        autocompleteList.classList.remove('active');
    }
}

// Export postcodes to CSV
function exportToCSV() {
    const csv = ['Postcode'].concat(allPostcodesInArea.map(formatPostcode)).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'postcodes.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// UI Helper Functions
function showLoading(message = 'Loading...') {
    loading.classList.remove('hidden');
    loading.querySelector('p').textContent = message;
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => errorMessage.classList.add('hidden'), 5000);
}

function hideError() {
    errorMessage.classList.add('hidden');
}

// Handle feedback form submission
async function handleFeedbackSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.submit-btn');
    const successMessage = document.getElementById('feedback-success');
    
    // Get form data
    const formData = {
        useCase: form['use-case'].value,
        organization: form['organization'].value || 'Not provided',
        suggestions: form['suggestions'].value || 'Not provided',
        email: form['email'].value || 'Not provided',
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
    };
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';
    
    try {
        // Send to Web3Forms
        const formDataToSend = new FormData();
        formDataToSend.append('access_key', '51dd89da-69f3-4721-a249-8bd85f96cb53');
        formDataToSend.append('subject', 'New Feedback from Energy Postcodes');
        formDataToSend.append('use_case', formData.useCase);
        formDataToSend.append('organization', formData.organization);
        formDataToSend.append('suggestions', formData.suggestions);
        formDataToSend.append('email', formData.email || 'noreply@energy-postcodes.uk');
        formDataToSend.append('timestamp', formData.timestamp);
        
        const response = await fetch('https://api.web3forms.com/submit', {
            method: 'POST',
            body: formDataToSend
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || 'Failed to submit feedback');
        }
        
        console.log('Feedback submitted successfully:', formData);
        
        // Show success message
        form.reset();
        form.style.display = 'none';
        successMessage.classList.remove('hidden');
        
        // Reset form after 5 seconds
        setTimeout(() => {
            form.style.display = 'block';
            successMessage.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Send Feedback';
        }, 5000);
        
    } catch (error) {
        console.error('Error submitting feedback:', error);
        showError('Failed to submit feedback. Please try again later.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Feedback';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
