import pathlib,csv,datetime
from bs4 import BeautifulSoup
root=pathlib.Path(__file__).resolve().parent.parent;u='https://extranet.who.int/prequal/vaccines/list-product-assessment-outcomes'
s=BeautifulSoup((root/'data/closure/who_assessment_outcomes.html').read_bytes(),'html.parser');main=s.find('main') or s
rows=[]
for i,table in enumerate(main.find_all('table')):
 status='positive risk-benefit assessment' if i==0 else 'under assessment, no final decision' if i in [1,2,3] else 'terminated/withheld section'
 for tr in table.find_all('tr'):
  cells=[x.get_text(' ',strip=True).replace('\xa0',' ') for x in tr.find_all('td')]
  if len(cells)>=4 and cells[0] and cells[0]!='Commercial name':rows.append(dict(name=cells[0],manufacturer=cells[1],country=cells[2],regulator=cells[3],status=status,source_url=u,retrieved_at_utc='2026-10-08 (UTC day precision; preserved response capture)' ))
with open(root/'data/closure/who_catalogue.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('WHO rows',len(rows), 'unique',len({x['name'] for x in rows}))
