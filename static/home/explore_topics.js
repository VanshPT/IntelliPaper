document.addEventListener('DOMContentLoaded', function() {
    const createFolderBox = document.querySelector('.create-folder-box');
    const tempFolder = document.getElementById('temp-folder');

    // Function to handle folder creation
    createFolderBox.addEventListener('click', function(event) {
        event.preventDefault();

        if (tempFolder.children.length === 0) {
            const newBox = document.createElement('div');
            newBox.className = 'folder-box'; // Add your folder-box class
            newBox.innerHTML = `
                <div class="folder-container">
                <div>
                    <div class="folder-svg">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M10 4L2 4C0.89543 4 0 4.89543 0 6V18C0 19.1046 0.89543 20 2 20H22C23.1046 20 24 19.1046 24 18V8C24 6.89543 23.1046 6 22 6H12L10 4Z" fill="rgba(255, 255, 255, 0.8)" />
                        </svg>
                    </div>
                </div>
                <div class="folder-name">New Readlist</div>
                </div>
            `;
            tempFolder.appendChild(newBox);
        } else {
            alert('You can only create one new readlist at a time!');
        }
    });

    // Function to make folder name editable
    function makeEditable(folderName) {
        const originalName = folderName.innerText;

        // Create an input field
        const input = document.createElement('input');
        input.type = 'text';
        input.value = originalName;
        input.className = 'folder-name-input';
        input.style.border = 'none';
        input.style.background = 'transparent'; // Make the input background transparent
        folderName.innerHTML = ''; // Clear the folder name
        folderName.appendChild(input);
        folderName.style.border = '2px solid orange'; // Add orange border

        // Focus on input and select text
        input.focus();
        input.select();

        // Function to handle clicking outside
        function handleClickOutside(event) {
            if (!folderName.contains(event.target)) {
                const newName = input.value.trim();

                // AJAX call to dummy API
                const dummyApiUrl = '/api/rename_readlist'; // Replace with your API endpoint
                const data = {
                    oldName: originalName,
                    newName: newName
                };

                // Dummy AJAX call (you can replace it with a real AJAX call)
                fetch(dummyApiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => {
                    // Dummy response handling
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to rename the readlist');
                    }
                })
                .then(result => {
                    if (result.success) {
                        folderName.innerHTML = newName;
                        window.location.href = `http://127.0.0.1:8000/explore_topics/${user.username}/`;
                    } else {
                        alert(result.message); // Show error message
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

                folderName.style.border = ''; // Remove orange border
                document.removeEventListener('click', handleClickOutside); // Remove listener
            }
        }

        // Add event listener for clicking outside
        document.addEventListener('click', handleClickOutside);
    }

    // Event listener for double-click on folder names
    tempFolder.addEventListener('dblclick', function(event) {
        if (event.target.classList.contains('folder-name')) {
            makeEditable(event.target);
        }
    });

    // Apply editable feature to existing folder names
    const existingFolderNames = document.querySelectorAll('.folder-name');
    existingFolderNames.forEach(folderName => {
        folderName.addEventListener('dblclick', function() {
            makeEditable(folderName);
        });
    });
});