// ========== SNIPPETS ==========

function buildSnippetsMenu() {
    const menu = document.getElementById('snippetsMenu');
    if (!menu) return;

    const snips = getSnippets();
    const groups = {
        headers: [],
        format: [],
        lists: [],
        blocks: [],
        callouts: []
    };

    // Group snippets
    Object.keys(snips).forEach(key => {
        const snippet = snips[key];
        if (groups[snippet.group]) {
            groups[snippet.group].push({ key, ...snippet });
        }
    });

    // Build menu HTML
    let html = '';
    const groupNames = ['headers', 'format', 'lists', 'blocks', 'callouts'];

    groupNames.forEach(groupName => {
        if (groups[groupName].length > 0) {
            html += `<div class="dropdown-header">${t('snippets.' + groupName)}</div>`;
            groups[groupName].forEach(snippet => {
                html += `<div class="dropdown-item" onclick="insertSnippet('${snippet.key}')">${snippet.label}</div>`;
            });
        }
    });

    menu.innerHTML = html;
}

function toggleSnippets() {
    const menu = document.getElementById('snippetsMenu');
    menu.classList.toggle('show');

    // Close when clicking outside
    if (menu.classList.contains('show')) {
        setTimeout(() => {
            document.addEventListener('click', closeSnippetsOnClickOutside);
        }, 10);
    }
}

function closeSnippetsOnClickOutside(e) {
    const menu = document.getElementById('snippetsMenu');
    const btn = e.target.closest('.dropdown');
    if (!btn) {
        menu.classList.remove('show');
        document.removeEventListener('click', closeSnippetsOnClickOutside);
    }
}

// Inline format markers (wrap selection)
const inlineFormats = {
    bold: { prefix: '**', suffix: '**' },
    italic: { prefix: '*', suffix: '*' },
    strikethrough: { prefix: '~~', suffix: '~~' },
    inline_code: { prefix: '`', suffix: '`' }
};

// Header formats (single line prefix)
const headerFormats = {
    h1: '# ',
    h2: '## ',
    h3: '### '
};

// Line-prefix formats (prefix each line)
const linePrefixFormats = {
    quote: '> ',
    bullet_list: '- ',
    task_list: '- [ ] '
};

// Strip existing inline formatting from text
function stripInlineFormatting(text) {
    return text
        .replace(/^\*\*(.+)\*\*$/, '$1')
        .replace(/^\*(.+)\*$/, '$1')
        .replace(/^~~(.+)~~$/, '$1')
        .replace(/^`(.+)`$/, '$1');
}

// Strip line prefixes (headers, quotes, lists)
function stripLinePrefixes(text) {
    return text
        .replace(/^#{1,6}\s+/, '')           // headers
        .replace(/^>\s?/, '')                 // quote
        .replace(/^[-*+]\s(\[.\]\s)?/, '')   // bullet/task list
        .replace(/^\d+\.\s/, '');             // numbered list
}

// Apply prefix to each line
function prefixLines(text, prefix) {
    return text.split('\n').map(line => prefix + stripLinePrefixes(line)).join('\n');
}

// Apply numbered list (1. 2. 3.)
function numberLines(text) {
    return text.split('\n').map((line, i) => `${i + 1}. ${stripLinePrefixes(line)}`).join('\n');
}

function insertSnippet(key) {
    const snips = getSnippets();
    const snippet = snips[key];
    if (!snippet) return;

    const textarea = document.getElementById('editor');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);

    let insertText;
    let newCursorPos;

    if (selectedText) {
        // Smart transformation based on snippet type
        if (inlineFormats[key]) {
            // Inline: wrap selection
            const cleanText = stripInlineFormatting(selectedText);
            insertText = inlineFormats[key].prefix + cleanText + inlineFormats[key].suffix;
        } else if (headerFormats[key]) {
            // Header: prefix first line only
            const cleanText = stripLinePrefixes(selectedText.split('\n')[0]);
            insertText = headerFormats[key] + cleanText;
        } else if (linePrefixFormats[key]) {
            // Line prefix: apply to each line
            insertText = prefixLines(selectedText, linePrefixFormats[key]);
        } else if (key === 'numbered_list') {
            // Numbered list: 1. 2. 3.
            insertText = numberLines(selectedText);
        } else if (key === 'code_block') {
            // Code block: wrap in ```
            insertText = '```\n' + selectedText + '\n```';
        } else if (key === 'link') {
            // Link: use selection as text
            insertText = '[' + selectedText + '](url)';
        } else {
            // No transformation: insert template
            insertText = snippet.content;
        }
        newCursorPos = start + insertText.length;
    } else {
        // No selection: insert template
        insertText = snippet.content;
        newCursorPos = start + insertText.length;
    }

    // Insert at cursor position
    textarea.value = text.substring(0, start) + insertText + text.substring(end);

    // Move cursor
    textarea.selectionStart = newCursorPos;
    textarea.selectionEnd = newCursorPos;
    textarea.focus();

    // Update preview
    if (typeof updatePreview === 'function') updatePreview();
    if (typeof updateCharCount === 'function') updateCharCount();
    if (typeof autoSave === 'function') autoSave();

    // Close menu
    document.getElementById('snippetsMenu').classList.remove('show');
}

function generateExampleDoc() {
    const snips = getSnippets();

    let doc = `# ${t('example.title')}\n\n`;
    doc += `${t('example.intro')}\n\n`;

    // Text formatting section
    doc += `## ${t('example.section.format')}\n\n`;
    doc += `${snips.bold.content}, ${snips.italic.content}, ${snips.strikethrough.content}\n\n`;
    doc += `${snips.inline_code.content} - ${snips.link.content}\n\n`;

    // Lists section
    doc += `## ${t('example.section.lists')}\n\n`;
    doc += snips.bullet_list.content;
    doc += snips.numbered_list.content;
    doc += snips.task_list.content;

    // Table section
    doc += `## ${t('example.section.table')}\n\n`;
    doc += snips.table.content;

    // Code section
    doc += `## ${t('example.section.code')}\n\n`;
    doc += snips.code_block.content;

    // Quote section
    doc += `## ${t('example.section.quote')}\n\n`;
    doc += snips.quote.content;

    // Callouts section
    doc += `## ${t('example.section.callouts')}\n\n`;
    doc += snips.note.content;
    doc += snips.warning.content;
    doc += snips.important.content;

    // Footer
    doc += `---\n\n*${t('example.footer')} v${APP_VERSION}*\n`;

    return doc;
}
