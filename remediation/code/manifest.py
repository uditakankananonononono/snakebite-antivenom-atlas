#!/usr/bin/env python3
import pathlib,hashlib,sys
D=pathlib.Path(__file__).resolve().parents[1];M=D/'MANIFEST.sha256'
files=sorted(p for p in D.rglob('*') if p.is_file() and p!=M and '__pycache__' not in p.parts)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
actual={str(p.relative_to(D)):h(p) for p in files}
if '--check' in sys.argv:
 expected={line.split('  ',1)[1]:line.split('  ',1)[0] for line in M.read_text().splitlines()};assert actual==expected,'manifest differs';print('PASS',len(actual),'remediation artifacts')
else:M.write_text(''.join(v+'  '+k+'\n' for k,v in actual.items()));print('Locked',len(actual),'artifacts')
