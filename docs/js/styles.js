// ========== PREVIEW STYLES ==========
const styles = {
    gitlab: `
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 16px; line-height: 1.6; color: #303030; background: #fff; padding: 20px; max-width: 900px; margin: 0 auto; }
        h1 { font-size: 2em; font-weight: 600; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #1f1f1f; }
        h2 { font-size: 1.5em; font-weight: 600; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #1f1f1f; }
        h3 { font-size: 1.25em; font-weight: 600; margin: 1.5em 0 0.5em; color: #1f1f1f; }
        p { margin: 0 0 1em; }
        a { color: #1068bf; text-decoration: none; }
        code { font-family: 'SF Mono', Consolas, monospace; font-size: 0.9em; background: #f5f5f5; padding: 0.2em 0.4em; border-radius: 4px; color: #d14; }
        pre { font-family: 'SF Mono', Consolas, monospace; font-size: 0.9em; background: #f6f8fa; border: 1px solid #e5e5e5; border-radius: 6px; padding: 16px; overflow-x: auto; }
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
    `
};

let currentStyle = localStorage.getItem('md_style') || 'gitlab';

function changeStyle() {
    currentStyle = document.getElementById('styleSelect').value;
    localStorage.setItem('md_style', currentStyle);
    updatePreview();
}
