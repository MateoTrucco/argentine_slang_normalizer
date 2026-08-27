import { bootPython, parsePythonJson } from './pyodide-helper.js';
const source=document.querySelector('#source'), output=document.querySelector('#output'), details=document.querySelector('#details'), run=document.querySelector('#run');
let py;
async function init(){ py=await bootPython(['normalizer.py','json/idioms.json']); run.disabled=false; normalize(); }
function normalize(){ if(!py)return; py.globals.set('demo_text',source.value); const raw=py.runPython(`import json
from normalizer import normalize
r=normalize(demo_text)
json.dumps({'text':r.text,'replacements':[{'from':x.original,'to':x.replacement} for x in r.replacements]}, ensure_ascii=False)`); const data=parsePythonJson(raw); output.textContent=data.text; details.textContent=data.replacements.length?`${data.replacements.length} replacement(s): `+data.replacements.map(x=>`${x.from} → ${x.to}`).join(', '):'No mapped slang found.'; }
run.disabled=true; run.addEventListener('click',normalize); document.querySelector('#example').addEventListener('click',()=>{source.value='Yo q se, toy re tranca. Dps voy en bondi al laburo.';normalize();}); init().catch(()=>{});
