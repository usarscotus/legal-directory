---
---

document.addEventListener('DOMContentLoaded', function() {
  const BASE_URL = '{{ site.baseurl }}';
  const ruleSetPaths = {
    frcp: '/frcp/',
    frap: '/frap/',
    fre: '/fre/',
    frcmp: '/frcmp/',
    supct: '/supct/'
  };
  const abbrMap = {
    FRCP: 'frcp',
    FRAP: 'frap',
    FRE: 'fre',
    FRCMP: 'frcmp',
    FRCrP: 'frcmp',
    SUPCT: 'supct',
    SCR: 'supct',
    SCT: 'supct'
  };

  let path = window.location.pathname;
  if (BASE_URL && path.startsWith(BASE_URL)) {
    path = path.slice(BASE_URL.length);
  }
  const currentSet = path.split('/').filter(Boolean)[0];

  function linkFor(set, num) {
    const base = ruleSetPaths[set];
    if (!base) return null;
    return BASE_URL + base + 'rule_' + num + '/';
  }

  function replaceText(text) {
    text = text.replace(/\b(FRCP|FRAP|FRE|FRCMP|FRCrP|SUPCT|SCR|SCT)\s+(\d+(?:\.\d+)?)/gi,
      function(match, abbr, num) {
        const setKey = abbrMap[abbr.toUpperCase()];
        const url = linkFor(setKey, num);
        if (!url) return match;
        return `<a href="${url}">${abbr.toUpperCase()} ${num}</a>`;
      });
    if (currentSet && ruleSetPaths[currentSet]) {
      text = text.replace(/\bRule\s+(\d+(?:\.\d+)?)/gi,
        function(match, num) {
          const url = linkFor(currentSet, num);
          if (!url) return match;
          return `<a href="${url}">${match}</a>`;
        });
    }
    return text;
  }

  const container = document.querySelector('main');
  if (!container) return;

  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.textContent.match(/\b(FRCP|FRAP|FRE|FRCMP|FRCrP|SUPCT|SCR|SCT|Rule)\b/)) {
        return NodeFilter.FILTER_SKIP;
      }
      if (node.parentElement && node.parentElement.closest('a, script, style')) {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  });

  const nodes = [];
  while (walker.nextNode()) {
    nodes.push(walker.currentNode);
  }
  nodes.forEach(node => {
    const newHTML = replaceText(node.textContent);
    if (newHTML !== node.textContent) {
      const span = document.createElement('span');
      span.innerHTML = newHTML;
      node.parentNode.replaceChild(span, node);
    }
  });
});

