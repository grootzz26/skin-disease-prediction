/**
 * Skin Disease Prediction Application
 * Main JavaScript functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const previewImage = document.getElementById('preview-image');
    const previewContainer = document.getElementById('preview-container');
    const uploadPrompt = document.getElementById('upload-prompt');
    const predictBtn = document.getElementById('predict-btn');
    const changeImageBtn = document.getElementById('change-image');
    const uploadForm = document.getElementById('upload-form');
    const loadingContainer = document.getElementById('loading-container');
    const resultContainer = document.getElementById('result-container');
    const predictionResults = document.getElementById('prediction-results');
    const errorContainer = document.getElementById('error-container');

    // Initialize the application
    init();

    // Set up all event listeners
    function init() {
        // Add event listeners
        setupEventListeners();

        // Reset UI state
        resetUI();
    }

    // Set up all event listeners
    function setupEventListeners() {
        // Handle click on upload area
        if (uploadArea) {
            uploadArea.addEventListener('click', triggerFileInput);

            // Handle drag and drop
            uploadArea.addEventListener('dragover', handleDragOver);
            uploadArea.addEventListener('dragleave', handleDragLeave);
            uploadArea.addEventListener('drop', handleDrop);
        }

        // Handle file selection
        if (fileInput) {
            fileInput.addEventListener('change', handleFileSelect);
        }

        // Handle change image button
        if (changeImageBtn) {
            changeImageBtn.addEventListener('click', resetImage);
        }

        // Handle form submission
        if (uploadForm) {
            uploadForm.addEventListener('submit', handleSubmit);
        }
    }

    // Trigger file input click
    function triggerFileInput(e) {
        if (e.target !== changeImageBtn) {
            fileInput.click();
        }
    }

    // Handle dragover event
    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('bg-light');
    }

    // Handle dragleave event
    function handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('bg-light');
    }

    // Handle drop event
    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('bg-light');

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect();
        }
    }

    // Handle file selection
    function handleFileSelect() {
        const file = fileInput.files[0];

        if (file) {
            // Check if the file is an image
            if (!file.type.match('image.*')) {
                showError('Please select an image file (JPG, JPEG, PNG, JFIF)');
                return;
            }

            // Reset any previous errors
            hideError();

            // Display preview
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                uploadPrompt.style.display = 'none';
                previewContainer.style.display = 'block';
                predictBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    }

    // Reset image selection
    function resetImage(e) {
        if (e) e.stopPropagation();

        fileInput.value = '';
        previewContainer.style.display = 'none';
        uploadPrompt.style.display = 'block';
        predictBtn.disabled = true;
        resultContainer.style.display = 'none';
    }

    // Handle form submission
    function handleSubmit(e) {
        e.preventDefault();

        if (!fileInput.files[0]) {
            showError('Please select an image first');
            return;
        }

        // Show loading indicator
        loadingContainer.style.display = 'block';
        predictBtn.disabled = true;
        resultContainer.style.display = 'none';
        hideError();

        // Create form data
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Send request to server
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingContainer.style.display = 'none';
            predictBtn.disabled = false;

            if (data.error) {
                showError(data.error);
                return;
            }

            // Display results
            resultContainer.style.display = 'block';
            displayPredictions(data.predictions);
        })
        .catch(error => {
            loadingContainer.style.display = 'none';
            predictBtn.disabled = false;
            showError('An error occurred. Please try again.');
            console.error('Error:', error);
        });
    }

    // Display prediction results
    function displayPredictions(predictions) {
        predictionResults.innerHTML = '';

        predictions.forEach((prediction, index) => {
            const predictionDiv = document.createElement('div');
            predictionDiv.className = `disease-item disease-item-${index + 1}`;

            predictionDiv.innerHTML = `
                <div class="d-flex justify-content-between">
                    <span class="disease-name">${prediction.disease}</span>
                    <span class="disease-probability">${prediction.probability}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar ${index === 0 ? 'bg-success' : index === 1 ? 'bg-primary' : 'bg-secondary'}"
                         role="progressbar"
                         style="width: ${prediction.probability}%"
                         aria-valuenow="${prediction.probability}"
                         aria-valuemin="0"
                         aria-valuemax="100">
                    </div>
                </div>
            `;

            predictionResults.appendChild(predictionDiv);
        });
    }

    // Show error message
    function showError(message) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    }

    // Hide error message
    function hideError() {
        errorContainer.style.display = 'none';
    }

    // Reset UI state
    function resetUI() {
        resetImage();
        hideError();
        loadingContainer.style.display = 'none';
        resultContainer.style.display = 'none';
    }
});