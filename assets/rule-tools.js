---
---

document.addEventListener('DOMContentLoaded', function() {
  const BASE_URL = '{{ site.baseurl }}';
  const content = document.querySelector('main');
  if (!content) return;

  const titleEl = content.querySelector('h1');
  if (!titleEl) return;

  let path = window.location.pathname;
  if (BASE_URL && path.startsWith(BASE_URL)) {
    path = path.slice(BASE_URL.length);
  }
  const parts = path.split('/').filter(Boolean);
  const set = parts[0];
  const match = parts[1] ? parts[1].match(/rule_(\d+(?:\.\d+)?)/) : null;
  const ruleNum = match ? match[1] : '';

  const prefixMap = {
    frcp: 'Fed. R. Civ. P.',
    frap: 'Fed. R. App. P.',
    fre: 'Fed. R. Evid.',
    frcmp: 'Fed. R. Crim. P.',
    supct: 'Sup. Ct. R.'
  };
  const ruleCitationBase = `${prefixMap[set] || 'Rule'} ${ruleNum}`;

  // Title citation button
  const citeBtn = document.createElement('button');
  citeBtn.type = 'button';
  citeBtn.className = 'citation-btn';
  citeBtn.textContent = 'Copy Citation';
  citeBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(ruleCitationBase);
  });
  titleEl.appendChild(citeBtn);

  // Line anchors and tools
  const blocks = content.querySelectorAll('p, li');
  let counter = 1;
  blocks.forEach(block => {
    const id = `line-${counter++}`;
    block.id = id;

    const tools = document.createElement('span');
    tools.className = 'line-tools';

    const linkBtn = document.createElement('button');
    linkBtn.type = 'button';
    linkBtn.className = 'line-link-btn';
    linkBtn.textContent = '🔗';
    linkBtn.setAttribute('aria-label', 'Copy link');
    linkBtn.addEventListener('click', () => {
      const url = `${window.location.origin}${window.location.pathname}#${id}`;
      navigator.clipboard.writeText(url);
    });
    
    const citeLineBtn = document.createElement('button');
    citeLineBtn.type = 'button';
    citeLineBtn.className = 'line-cite-btn';
    citeLineBtn.textContent = 'Cite';
    citeLineBtn.setAttribute('aria-label', 'Copy citation');
    citeLineBtn.addEventListener('click', () => {
      const part = extractCitationPart(block);
      const citation = part ? `${ruleCitationBase}${part}` : ruleCitationBase;
      navigator.clipboard.writeText(citation);
    });

    tools.appendChild(linkBtn);
    tools.appendChild(citeLineBtn);
    block.appendChild(tools);
  });

  function extractCitationPart(el) {
    const parts = [];
    let node = el;
    while (node && node !== content) {
      const label = getLabel(node);
      if (label) parts.unshift(`(${label})`);
      node = node.parentElement;
    }
    return parts.join('');
  }

  function getLabel(node) {
    if (node.tagName === 'LI') {
      const parent = node.parentElement;
      if (parent && parent.tagName === 'OL') {
        const index = Array.from(parent.children).indexOf(node) + 1;
        return index;
      }
      if (parent && parent.tagName === 'UL') {
        const match = node.textContent.trim().match(/^\(([A-Za-z0-9]+)\)/);
        if (match) return match[1];
      }
    }
    if (node.tagName === 'P') {
      const match = node.textContent.trim().match(/^\(([A-Za-z0-9]+)\)/);
      if (match) return match[1];
    }
    return null;
  }
});
