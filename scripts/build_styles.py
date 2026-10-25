"""Combine the three marketing stylesheets in their original cascade order."""
from pathlib import Path
import shutil
import subprocess

root=Path(__file__).resolve().parents[1]
npx=shutil.which('npx')
assert npx, 'Install Node.js with npm to rebuild the stylesheet.'
source='\n'.join((root/name).read_text(encoding='utf-8') for name in ['site.css','services.css','analytics.css'])
result=subprocess.run([npx,'--yes','esbuild@0.28.2','--loader=css','--minify','--log-level=warning'],input=source,text=True,encoding='utf-8',capture_output=True,check=True)
assert result.stdout.strip(), 'The CSS bundle must not be empty.'
(root/'site.min.css').write_text(result.stdout,encoding='utf-8')
print('CSS bundle:',len(source.encode('utf-8')),'->',len(result.stdout.encode('utf-8')),'bytes')
