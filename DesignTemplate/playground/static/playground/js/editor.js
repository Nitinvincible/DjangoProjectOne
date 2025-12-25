// ========================
// Monaco Editor Setup
// ========================

require.config({
    paths: {
        vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs'
    }
});

let htmlEditor, cssEditor, jsEditor;
let updateTimeout;

require(['vs/editor/editor.main'], function () {
    // Initialize HTML Editor
    htmlEditor = monaco.editor.create(document.getElementById('html-editor'), {
        value: SNIPPET_DATA.html || getDefaultHTML(),
        language: 'html',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        roundedSelection: false,
        scrollBeyondLastLine: false,
        readOnly: false,
        cursorStyle: 'line',
    });

    // Initialize CSS Editor
    cssEditor = monaco.editor.create(document.getElementById('css-editor'), {
        value: SNIPPET_DATA.css || getDefaultCSS(),
        language: 'css',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
    });

    // Initialize JavaScript Editor
    jsEditor = monaco.editor.create(document.getElementById('js-editor'), {
        value: SNIPPET_DATA.js || getDefaultJS(),
        language: 'javascript',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
    });

    // Auto-update preview on code change (debounced)
    [htmlEditor, cssEditor, jsEditor].forEach(editor => {
        editor.onDidChangeModelContent(() => {
            clearTimeout(updateTimeout);
            updateTimeout = setTimeout(updatePreview, 500);
        });
    });

    // Initial preview render
    updatePreview();
});

// ========================
// Tab Switching
// ========================

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function () {
        const editorType = this.dataset.editor;

        // Update tab active state
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');

        // Update editor visibility
        document.querySelectorAll('.editor').forEach(e => e.classList.remove('active'));
        document.getElementById(`${editorType}-editor`).classList.add('active');
    });
});

// ========================
// Preview Rendering (SECURE)
// ========================

function updatePreview() {
    const html = htmlEditor.getValue();
    const css = cssEditor.getValue();
    const js = jsEditor.getValue();
    const environment = document.getElementById('environment').value;

    let fullHTML = '';

    if (environment === '3d') {
        // Inject Three.js CDN for 3D environment
        fullHTML = `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        margin: 0;
                        overflow: hidden;
                    }
                    ${css}
                </style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\/script>
            </head>
            <body>
                ${html}
                <script>
                    try {
                        ${js}
                    } catch (error) {
                        console.error('Error in user script:', error);
                        document.body.innerHTML = '<div style="color: red; padding: 20px;">Error: ' + error.message + '</div>';
                    }
                <\/script>
            </body>
            </html>
        `;
    } else {
        // Standard 2D HTML/CSS/JS
        fullHTML = `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        margin: 0;
                        padding: 20px;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    }
                    ${css}
                </style>
            </head>
            <body>
                ${html}
                <script>
                    try {
                        ${js}
                    } catch (error) {
                        console.error('Error in user script:', error);
                    }
                <\/script>
            </body>
            </html>
        `;
    }

    // Render in sandboxed iframe using Blob URL (prevents parent window access)
    const iframe = document.getElementById('preview');
    const blob = new Blob([fullHTML], { type: 'text/html' });
    const blobURL = URL.createObjectURL(blob);

    iframe.src = blobURL;

    // Clean up old blob URL to prevent memory leaks
    iframe.onload = () => {
        URL.revokeObjectURL(blobURL);
    };
}

// Manual refresh button
document.getElementById('refresh-preview').addEventListener('click', () => {
    updatePreview();
});

// Environment change handler
document.getElementById('environment').addEventListener('change', () => {
    updatePreview();
});

// ========================
// Save Snippet
// ========================

document.getElementById('save-btn').addEventListener('click', async function () {
    if (!IS_AUTHENTICATED) {
        alert('Please login to save snippets');
        window.location.href = '/accounts/login/';
        return;
    }

    const saveBtn = this;
    const originalText = saveBtn.innerHTML;
    saveBtn.innerHTML = '<span class="loading">💾 Saving...</span>';
    saveBtn.disabled = true;

    const data = {
        id: SNIPPET_DATA.id,
        title: document.getElementById('snippet-title').value || 'Untitled',
        html_code: htmlEditor.getValue(),
        css_code: cssEditor.getValue(),
        js_code: jsEditor.getValue(),
        environment: document.getElementById('environment').value,
        is_public: true
    };

    try {
        const response = await fetch('/api/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Update snippet data
            SNIPPET_DATA.id = result.id;
            SNIPPET_DATA.slug = result.slug;

            // Show success message
            saveBtn.innerHTML = '<span class="icon">✅</span> Saved!';
            setTimeout(() => {
                saveBtn.innerHTML = originalText;
                saveBtn.disabled = false;
            }, 2000);

            // Redirect to snippet detail page
            setTimeout(() => {
                window.location.href = `/snippet/${result.slug}/`;
            }, 1500);
        } else {
            throw new Error(result.error || 'Save failed');
        }
    } catch (error) {
        alert('Error saving snippet: ' + error.message);
        saveBtn.innerHTML = originalText;
        saveBtn.disabled = false;
    }
});

// ========================
// Fork Snippet
// ========================

const forkBtn = document.getElementById('fork-btn');
if (forkBtn) {
    forkBtn.addEventListener('click', async function () {
        if (!IS_AUTHENTICATED) {
            alert('Please login to fork snippets');
            window.location.href = '/accounts/login/';
            return;
        }

        if (!SNIPPET_DATA.slug) {
            alert('No snippet to fork');
            return;
        }

        const originalText = this.innerHTML;
        this.innerHTML = '<span class="loading">🍴 Forking...</span>';
        this.disabled = true;

        try {
            const response = await fetch(`/api/fork/${SNIPPET_DATA.slug}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN
                }
            });

            const result = await response.json();

            if (result.success) {
                window.location.href = `/editor/${result.slug}/`;
            } else {
                throw new Error('Fork failed');
            }
        } catch (error) {
            alert('Error forking snippet: ' + error.message);
            this.innerHTML = originalText;
            this.disabled = false;
        }
    });
}

// ========================
// Default Templates
// ========================

function getDefaultHTML() {
    return `<!-- HTML Template -->
<div class="container">
    <h1>Welcome to Code Playground! 🎨</h1>
    <p>Start creating your amazing design here.</p>
    <button class="btn">Click Me</button>
</div>`;
}

function getDefaultCSS() {
    return `/* CSS Styles */
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
}

h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: fadeIn 1s ease-in;
}

p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.btn {
    padding: 12px 32px;
    font-size: 1rem;
    background: white;
    color: #667eea;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}`;
}

function getDefaultJS() {
    return `// JavaScript Code
document.querySelector('.btn').addEventListener('click', function() {
    alert('Hello from Code Playground! 🚀');
});`;
}

// ========================
// Keyboard Shortcuts
// ========================

document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + S to save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        document.getElementById('save-btn').click();
    }

    // Ctrl/Cmd + R to refresh preview
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        updatePreview();
    }
});

console.log('🎨 Code Playground Editor Loaded');
console.log('Shortcuts: Ctrl+S (Save), Ctrl+R (Refresh Preview)');
