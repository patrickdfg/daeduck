from pathlib import Path
import subprocess,itertools
from bs4 import BeautifulSoup
from build_workbook_sets import set2,set3,trace
root=Path(__file__).resolve().parent
base=BeautifulSoup(subprocess.check_output(['git','show','HEAD:workbook.html'],cwd=root),'html.parser')
now=BeautifulSoup((root/'workbook.html').read_text(encoding='utf-8'),'html.parser')
assert [q.get_text(' ',strip=True) for q in base.select('.question')]==[q.get_text(' ',strip=True) for q in now.select('.question')]
assert 'daeduck-workbook-v1-answer-' in str(now)
for filename in ['workbook.html','workbook-set2.html','workbook-set3.html']:
    s=BeautifulSoup((root/filename).read_text(encoding='utf-8'),'html.parser')
    assert len(s.select('.question'))==20
    assert len(s.select('textarea[data-answer]'))==20
    assert len(s.select('details.answer'))==20
    assert len({n['id'] for n in s.select('[id]')})==len(s.select('[id]'))
    for a in s.select('a[href]'):
        h=a['href'].split('#')[0]
        if h and not h.startswith(('http:','https:')):assert (root/h).is_file(),h
    assert s.select_one('a[href="index.html"]')
assert BeautifulSoup((root/'interview.html').read_text(encoding='utf-8'),'html.parser').select_one('a[href="index.html"]')
for arr in [[3,8,14,21,29,36,45,57,68],[5,11,18,26,34,43,55,64,78,90]]:
    for n in range(0,101):
        steps,answer=trace(arr,n)
        assert answer==(arr.index(n) if n in arr else -1)
        assert len(steps)<=4
pre={'A':set(),'B':set(),'C':{'A'},'D':{'A','B'},'E':{'C'},'F':{'D','E'}}
done=set();order=[]
while len(done)<6:
    nxt=min(k for k,v in pre.items() if k not in done and v<=done);done.add(nxt);order.append(nxt)
assert ''.join(order)=='ABCDEF'
done=set();rounds=[]
while len(done)<6:
    ready={k for k,v in pre.items() if k not in done and v<=done};assert ready;rounds.append(ready);done|=ready
assert rounds==[{'A','B'},{'C','D'},{'E'},{'F'}]
assert len(BeautifulSoup(''.join(set2()),'html.parser').select('.question'))==20
assert len(BeautifulSoup(''.join(set3()),'html.parser').select('.question'))==20
print('PASS: original 20 questions/keys preserved; 2 new sets ×20 with explanations; links/IDs; 202 binary searches and task-order/parallel checks.')
