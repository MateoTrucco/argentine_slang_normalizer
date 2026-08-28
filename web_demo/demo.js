import { bootPython, parsePythonJson } from './pyodide-helper.js';

const examples = [
  'Yo q se, toy re tranca. Dps voy en bondi al laburo.',
  'Q onda? Tmb viene Agus o llega dsp?',
  'Toy buscando laburo, pero x ahora voy tranqui.',
];
const source = document.querySelector('#source');
const output = document.querySelector('#output');
const details = document.querySelector('#details');
const replacementList = document.querySelector('#replacementList');
const run = document.querySelector('#run');
let py;
let exampleIndex = 0;
let timer;

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

async function init() {
  py = await bootPython(['normalizer.py', 'json/idioms.json']);
  run.disabled = false;
  normalize();
}

function normalize() {
  if (!py) return;
  py.globals.set('demo_text', source.value);
  const raw = py.runPython(`import json\nfrom normalizer import normalize\nr=normalize(demo_text)\njson.dumps({'text':r.text,'replacements':[{'from':x.original,'to':x.replacement} for x in r.replacements]}, ensure_ascii=False)`);
  const data = parsePythonJson(raw);
  output.textContent = data.text || '(empty input)';
  details.innerHTML = `<div class="metric"><strong>${source.value.length}</strong><small>Input characters</small></div><div class="metric"><strong>${data.replacements.length}</strong><small>Mapped replacements</small></div><div class="metric"><strong>${new Set(data.replacements.map((item) => item.from.toLowerCase())).size}</strong><small>Unique expressions</small></div>`;
  replacementList.innerHTML = data.replacements.map((item) => `<span class="badge">${escapeHtml(item.from)} → ${escapeHtml(item.to)}</span>`).join('') || '<span class="muted">No configured slang was found; the input stays unchanged.</span>';
}

function scheduleNormalize() { clearTimeout(timer); timer = setTimeout(normalize, 130); }

run.disabled = true;
run.addEventListener('click', normalize);
source.addEventListener('input', scheduleNormalize);
document.querySelector('#example').addEventListener('click', () => {
  source.value = examples[exampleIndex++ % examples.length];
  normalize();
});
document.querySelector('#clear').addEventListener('click', () => {
  source.value = '';
  normalize();
  source.focus();
});
init().catch(() => {});
