// ========== PREVIEW STYLES ==========

// Built-in styles (as CSS strings for simplicity)
const styles = {
    gitlab: `
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 16px; line-height: 1.6; color: #303030; background: #fff; padding: 20px 40px; max-width: 900px; margin: 0 auto; }
        h1 { font-size: 2em; font-weight: 600; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #1f1f1f; }
        h2 { font-size: 1.5em; font-weight: 600; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #1f1f1f; }
        h3 { font-size: 1.25em; font-weight: 600; margin: 1.5em 0 0.5em; color: #1f1f1f; }
        p { margin: 0 0 1em; }
        a { color: #1068bf; text-decoration: none; }
        code { font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.9em; background: #f5f5f5; padding: 0.2em 0.4em; border-radius: 4px; color: #d14; }
        pre { font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.9em; background: #f6f8fa; border: 1px solid #e5e5e5; border-radius: 6px; padding: 16px; overflow-x: auto; }
        pre code { background: transparent; padding: 0; color: #303030; }
        blockquote { margin: 1em 0; padding: 0.5em 1em; border-left: 4px solid #dbdbdb; background: #fafafa; color: #666; }
        ul, ol { margin: 0 0 1em; padding-left: 2em; }
        li { margin-bottom: 0.25em; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th { background: #f6f8fa; border: 1px solid #e5e5e5; padding: 10px 12px; text-align: left; font-weight: 600; }
        td { border: 1px solid #e5e5e5; padding: 10px 12px; }
        tr:nth-child(even) { background: #fafafa; }
        hr { border: none; border-top: 1px solid #e5e5e5; margin: 2em 0; }
        img { max-width: 100%; height: auto; }
        .callout-note { background: #e7f3ff; border-left: 4px solid #0066cc; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-warning { background: #fff8e6; border-left: 4px solid #f0ad4e; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-important { background: #ffeaea; border-left: 4px solid #dc3545; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
    `,
    default: `
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; background: #fff; margin: 20px; }
        h1 { font-size: 28px; font-weight: 600; color: #1a1a1a; margin: 24px 0 16px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }
        h2 { font-size: 22px; font-weight: 600; color: #2a2a2a; margin: 20px 0 12px; border-bottom: 1px solid #e8e8e8; padding-bottom: 6px; }
        h3 { font-size: 18px; font-weight: 600; color: #3a3a3a; margin: 16px 0 10px; }
        p { margin: 0 0 12px; }
        a { color: #0066cc; text-decoration: underline; }
        code { font-family: Consolas, Monaco, monospace; font-size: 13px; color: #c7254e; background: #f9f2f4; padding: 2px 6px; border-radius: 3px; }
        pre { font-family: Consolas, Monaco, monospace; font-size: 13px; color: #333; background: #f5f5f5; padding: 16px; border-radius: 6px; border: 1px solid #e0e0e0; overflow-x: auto; }
        blockquote { font-style: italic; color: #555; background: #f8f9fa; border-left: 4px solid #6c757d; margin: 16px 0; padding: 12px 20px; }
        ul, ol { margin: 8px 0 12px; padding-left: 24px; }
        li { margin-bottom: 4px; }
        table { border-collapse: collapse; width: 100%; margin: 12px 0 16px; }
        th { font-weight: 600; color: #fff; background: #4a5568; border: 1px solid #cbd5e0; padding: 10px 12px; text-align: left; }
        td { border: 1px solid #e2e8f0; padding: 8px 12px; }
        hr { border: none; border-top: 1px solid #e0e0e0; margin: 24px 0; }
        img { max-width: 100%; height: auto; }
        .callout-note { background: #e7f3ff; border-left: 4px solid #0066cc; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-warning { background: #fff8e6; border-left: 4px solid #f0ad4e; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-important { background: #ffeaea; border-left: 4px solid #dc3545; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
    `,
    outlook: `
        body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #000; background: #fff; margin: 0; padding: 10px; }
        h1 { font-family: Calibri, Arial, sans-serif; font-size: 18pt; font-weight: bold; color: #1f4e79; margin: 18px 0 12px; }
        h2 { font-family: Calibri, Arial, sans-serif; font-size: 14pt; font-weight: bold; color: #2e75b6; margin: 14px 0 8px; }
        h3 { font-family: Calibri, Arial, sans-serif; font-size: 12pt; font-weight: bold; color: #404040; margin: 12px 0 6px; }
        p { font-family: Calibri, Arial, sans-serif; font-size: 11pt; color: #000; margin: 0 0 10px; }
        a { color: #0563c1; text-decoration: underline; }
        code { font-family: Consolas, 'Courier New', monospace; font-size: 10pt; color: #c7254e; background: #f5f5f5; padding: 1px 4px; }
        pre { font-family: Consolas, 'Courier New', monospace; font-size: 10pt; color: #333; background: #f5f5f5; padding: 10px; border: 1px solid #ccc; overflow-x: auto; }
        blockquote { font-family: Calibri, Arial, sans-serif; font-size: 11pt; font-style: italic; color: #666; background: #f9f9f9; border-left: 3px solid #5b9bd5; margin: 10px 0; padding: 8px 14px; }
        ul, ol { margin: 6px 0 10px; padding-left: 20px; }
        li { font-family: Calibri, Arial, sans-serif; font-size: 11pt; color: #000; margin-bottom: 3px; }
        table { border-collapse: collapse; width: auto; margin: 10px 0 14px; }
        th { font-family: Calibri, Arial, sans-serif; font-size: 11pt; font-weight: bold; color: #fff; background: #5b9bd5; border: 1px solid #9cc2e5; padding: 6px 10px; text-align: left; }
        td { font-family: Calibri, Arial, sans-serif; font-size: 11pt; color: #000; border: 1px solid #bfbfbf; padding: 5px 10px; }
        hr { border: none; border-top: 1px solid #ccc; margin: 16px 0; }
        img { max-width: 100%; height: auto; }
        .callout-note { background: #deeaf6; border-left: 3px solid #5b9bd5; padding: 8px 12px; margin: 10px 0; }
        .callout-warning { background: #fff2cc; border-left: 3px solid #bf9000; padding: 8px 12px; margin: 10px 0; }
        .callout-important { background: #fce4d6; border-left: 3px solid #c65911; padding: 8px 12px; margin: 10px 0; }
    `,
    pdf_formal: `
        body { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; line-height: 1.7; color: #222; background: #fff; margin: 40px; padding: 0; }
        h1 { font-family: Georgia, 'Times New Roman', serif; font-size: 26pt; font-weight: bold; color: #1a1a1a; margin: 32px 0 20px; border-bottom: 3px solid #2c3e50; padding-bottom: 12px; }
        h2 { font-family: Georgia, 'Times New Roman', serif; font-size: 20pt; font-weight: bold; color: #2c3e50; margin: 28px 0 16px; border-bottom: 1px solid #bdc3c7; padding-bottom: 8px; }
        h3 { font-family: Georgia, 'Times New Roman', serif; font-size: 16pt; font-weight: bold; color: #34495e; margin: 22px 0 12px; }
        p { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; color: #222; margin: 0 0 14px; text-align: justify; }
        a { color: #2980b9; text-decoration: underline; }
        code { font-family: Consolas, Monaco, monospace; font-size: 10pt; color: #8e44ad; background: #f8f8f8; padding: 3px 8px; border-radius: 4px; }
        pre { font-family: Consolas, Monaco, monospace; font-size: 10pt; color: #2c3e50; background: #f8f8f8; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; overflow-x: auto; }
        blockquote { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; font-style: italic; color: #555; background: #fafafa; border-left: 5px solid #2c3e50; margin: 20px 0; padding: 16px 24px; }
        ul, ol { margin: 10px 0 14px; padding-left: 28px; }
        li { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; color: #222; margin-bottom: 6px; }
        table { border-collapse: collapse; width: 100%; margin: 16px 0 20px; }
        th { font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; font-weight: bold; color: #fff; background: #2c3e50; border: 1px solid #2c3e50; padding: 12px 14px; text-align: left; }
        td { font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; color: #222; border: 1px solid #bdc3c7; padding: 10px 14px; }
        hr { border: none; border-top: 2px solid #bdc3c7; margin: 32px 0; }
        img { max-width: 100%; height: auto; }
        .callout-note { background: #ebf5fb; border-left: 5px solid #3498db; padding: 16px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
        .callout-warning { background: #fef9e7; border-left: 5px solid #f39c12; padding: 16px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
        .callout-important { background: #fdedec; border-left: 5px solid #e74c3c; padding: 16px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
    `
};

// Style names for display
const styleNames = {
    gitlab: 'GitLab',
    default: 'Default',
    outlook: 'Outlook Email',
    pdf_formal: 'PDF Formal'
};

// Custom styles storage
const CUSTOM_STYLES_KEY = 'md_custom_styles';

function getCustomStyles() {
    try {
        return JSON.parse(localStorage.getItem(CUSTOM_STYLES_KEY) || '{}');
    } catch { return {}; }
}

function saveCustomStyle(name, css) {
    const custom = getCustomStyles();
    custom[name] = css;
    localStorage.setItem(CUSTOM_STYLES_KEY, JSON.stringify(custom));
}

function deleteCustomStyle(name) {
    const custom = getCustomStyles();
    delete custom[name];
    localStorage.setItem(CUSTOM_STYLES_KEY, JSON.stringify(custom));
}

// Get all styles (built-in + custom)
function getAllStyles() {
    return { ...styles, ...getCustomStyles() };
}

function getAllStyleNames() {
    const custom = getCustomStyles();
    const customNames = {};
    Object.keys(custom).forEach(k => customNames[k] = k);
    return { ...styleNames, ...customNames };
}

let currentStyle = localStorage.getItem('md_style') || 'gitlab';

function changeStyle() {
    currentStyle = document.getElementById('styleSelect').value;
    localStorage.setItem('md_style', currentStyle);
    updatePreview();
}

// Populate style dropdown
function populateStyleSelect() {
    const select = document.getElementById('styleSelect');
    if (!select) return;

    const allStyles = getAllStyles();
    const allNames = getAllStyleNames();
    const currentValue = select.value || currentStyle;

    select.innerHTML = '';
    for (const key of Object.keys(allStyles)) {
        const opt = document.createElement('option');
        opt.value = key;
        opt.textContent = allNames[key] || key;
        if (key === currentValue) opt.selected = true;
        select.appendChild(opt);
    }
}

// ========== STYLE EDITOR ==========

// Elements that can be styled
const styleElements = [
    { id: 'body', label: 'Body' },
    { id: 'h1', label: 'H1' },
    { id: 'h2', label: 'H2' },
    { id: 'h3', label: 'H3' },
    { id: 'p', label: 'Paragraph' },
    { id: 'a', label: 'Link' },
    { id: 'code', label: 'Code' },
    { id: 'pre', label: 'Pre' },
    { id: 'blockquote', label: 'Blockquote' },
    { id: 'ul, ol', label: 'Lists' },
    { id: 'li', label: 'List Item' },
    { id: 'table', label: 'Table' },
    { id: 'th', label: 'Table Header' },
    { id: 'td', label: 'Table Cell' },
    { id: 'hr', label: 'Separator' }
];

// Basic mode properties (dummy)
const basicProperties = [
    { id: 'font-family', label: 'style.font', type: 'select', options: [
        "Segoe UI, Arial, sans-serif",
        "Calibri, Arial, sans-serif",
        "Georgia, Times New Roman, serif",
        "Consolas, Monaco, monospace",
        "-apple-system, BlinkMacSystemFont, sans-serif"
    ]},
    { id: 'font-size', label: 'style.size', type: 'text', placeholder: '14px' },
    { id: 'color', label: 'style.color', type: 'color' },
    { id: 'background-color', label: 'style.bgcolor', type: 'color' }
];

// Advanced properties (expert)
const advancedProperties = [
    { id: 'font-weight', label: 'style.weight', type: 'select', options: ['normal', 'bold', '600', '700'] },
    { id: 'font-style', label: 'style.fontstyle', type: 'select', options: ['normal', 'italic'] },
    { id: 'line-height', label: 'style.lineheight', type: 'text', placeholder: '1.6' },
    { id: 'margin', label: 'style.margin', type: 'text', placeholder: '10px' },
    { id: 'padding', label: 'style.padding', type: 'text', placeholder: '10px' },
    { id: 'border', label: 'style.border', type: 'text', placeholder: '1px solid #ccc' },
    { id: 'border-left', label: 'style.borderleft', type: 'text', placeholder: '4px solid #007acc' },
    { id: 'border-bottom', label: 'style.borderbottom', type: 'text', placeholder: '1px solid #eee' },
    { id: 'border-radius', label: 'style.radius', type: 'text', placeholder: '4px' },
    { id: 'text-align', label: 'style.align', type: 'select', options: ['left', 'center', 'right', 'justify'] },
    { id: 'text-decoration', label: 'style.decoration', type: 'select', options: ['none', 'underline'] }
];

let styleEditorData = {};
let styleEditorElement = 'body';
let styleEditorAdvanced = false;

function showStyleEditor() {
    closeAllDropdowns();
    // Parse current style into object
    styleEditorData = parseCSS(getAllStyles()[currentStyle] || styles.gitlab);
    styleEditorElement = 'body';
    styleEditorAdvanced = false;
    renderStyleEditor();
    document.getElementById('styleEditorModal').classList.add('show');
}

function closeStyleEditor() {
    document.getElementById('styleEditorModal').classList.remove('show');
}

// Parse CSS string to object
function parseCSS(cssString) {
    const result = {};
    const regex = /([^{]+)\{([^}]+)\}/g;
    let match;
    while ((match = regex.exec(cssString)) !== null) {
        const selector = match[1].trim();
        const props = {};
        match[2].split(';').forEach(prop => {
            const [key, value] = prop.split(':').map(s => s.trim());
            if (key && value) props[key] = value;
        });
        result[selector] = props;
    }
    return result;
}

// Convert object back to CSS string
function objectToCSS(obj) {
    let css = '';
    for (const [selector, props] of Object.entries(obj)) {
        css += `${selector} { `;
        for (const [prop, value] of Object.entries(props)) {
            css += `${prop}: ${value}; `;
        }
        css += '} ';
    }
    return css;
}

function renderStyleEditor() {
    const container = document.getElementById('styleEditorContent');
    if (!container) return;

    // Element selector
    let html = `<div class="se-section">
        <label>${t('style.element')}</label>
        <select id="seElementSelect" onchange="selectStyleElement(this.value)">`;
    styleElements.forEach(el => {
        html += `<option value="${el.id}" ${el.id === styleEditorElement ? 'selected' : ''}>${el.label}</option>`;
    });
    html += `</select></div>`;

    // Mode toggle
    html += `<div class="se-section se-mode">
        <label>${t('style.mode')}</label>
        <button class="btn btn-sm ${!styleEditorAdvanced ? 'active' : ''}" onclick="setStyleMode(false)">${t('style.basic')}</button>
        <button class="btn btn-sm ${styleEditorAdvanced ? 'active' : ''}" onclick="setStyleMode(true)">${t('style.advanced')}</button>
    </div>`;

    // Properties
    const props = styleEditorAdvanced ? [...basicProperties, ...advancedProperties] : basicProperties;
    const elementData = styleEditorData[styleEditorElement] || {};

    html += `<div class="se-properties">`;
    props.forEach(prop => {
        const value = elementData[prop.id] || '';
        html += `<div class="se-prop">
            <label>${t(prop.label)}</label>`;

        if (prop.type === 'select') {
            html += `<select onchange="updateStyleProp('${prop.id}', this.value)">
                <option value=""></option>`;
            prop.options.forEach(opt => {
                html += `<option value="${opt}" ${value === opt ? 'selected' : ''}>${opt}</option>`;
            });
            html += `</select>`;
        } else if (prop.type === 'color') {
            html += `<div class="se-color-wrap">
                <input type="text" value="${value}" onchange="updateStyleProp('${prop.id}', this.value)" placeholder="#000000">
                <input type="color" value="${value || '#000000'}" onchange="updateStyleProp('${prop.id}', this.value); this.previousElementSibling.value=this.value">
            </div>`;
        } else {
            html += `<input type="text" value="${value}" placeholder="${prop.placeholder || ''}" onchange="updateStyleProp('${prop.id}', this.value)">`;
        }
        html += `</div>`;
    });
    html += `</div>`;

    container.innerHTML = html;
}

function selectStyleElement(el) {
    styleEditorElement = el;
    renderStyleEditor();
}

function setStyleMode(advanced) {
    styleEditorAdvanced = advanced;
    renderStyleEditor();
}

function updateStyleProp(prop, value) {
    if (!styleEditorData[styleEditorElement]) {
        styleEditorData[styleEditorElement] = {};
    }
    if (value) {
        styleEditorData[styleEditorElement][prop] = value;
    } else {
        delete styleEditorData[styleEditorElement][prop];
    }
    // Live preview
    applyStylePreview();
}

function applyStylePreview() {
    const css = objectToCSS(styleEditorData);
    // Temporarily update preview
    const tempStyle = currentStyle;
    styles['_preview'] = css;
    currentStyle = '_preview';
    updatePreview();
    currentStyle = tempStyle;
    delete styles['_preview'];
}

function applyStyleEditor() {
    const css = objectToCSS(styleEditorData);
    styles[currentStyle] = css;
    updatePreview();
    closeStyleEditor();
    showToast(t('style.applied'));
}

function saveStyleAs() {
    const name = prompt(t('style.entername'), 'Mi Estilo');
    if (!name) return;

    const css = objectToCSS(styleEditorData);
    saveCustomStyle(name, css);
    populateStyleSelect();

    // Switch to the new style
    currentStyle = name;
    document.getElementById('styleSelect').value = name;
    localStorage.setItem('md_style', name);
    updatePreview();

    closeStyleEditor();
    showToast(t('style.saved') + ': ' + name);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', populateStyleSelect);
