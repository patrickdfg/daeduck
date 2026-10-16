from pathlib import Path
import subprocess,itertools
from bs4 import BeautifulSoup
from build_workbook_sets import set2,set3,set4,trace,arrival_rules4
root=Path(__file__).resolve().parent
base=BeautifulSoup(subprocess.check_output(['git','show','69b8b36:workbook.html'],cwd=root),'html.parser')
now=BeautifulSoup((root/'workbook.html').read_text(encoding='utf-8'),'html.parser')
assert [q.get_text(' ',strip=True) for q in base.select('.question')]==[q.get_text(' ',strip=True) for q in now.select('.question')]
assert 'daeduck-workbook-v1-answer-' in str(now)
for filename in ['workbook.html','workbook-set2.html','workbook-set3.html','workbook-set4.html']:
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
print('PASS: original 20 questions/keys preserved; 4 sets ×20 with explanations; links/IDs; 202 binary searches and task-order/parallel checks.')

for filename in ['workbook-set3.html','workbook-set4.html']:
    old=BeautifulSoup(subprocess.check_output(['git','show','9d93251:'+filename],cwd=root),'html.parser')
    new=BeautifulSoup((root/filename).read_text(encoding='utf-8'),'html.parser')
    assert [q.get_text(' ',strip=True) for q in old.select('.question')]==[q.get_text(' ',strip=True) for q in new.select('.question')]
all_orders=list(itertools.permutations('ABCDEFG'))
assert [''.join(p) for p in all_orders if all(arrival_rules4(p))]==['BADEFCG']
assert [i+1 for i,v in enumerate(arrival_rules4('DFBAECG')) if not v]==[1,2,3,4]
fourth=BeautifulSoup(''.join(set4()),'html.parser');assert len(fourth.select('.question'))==20
assert fourth.select_one('svg[role="img"]') and '[A]' in fourth.get_text()
# Independent 1-based simulation of the displayed pseudocode and its two buggy variants.
def one_based(arr,t,inclusive=True,bad_start=False):
    start,end=1,len(arr);states=[]
    while start<=end if inclusive else start<end:
        if len(states)>15:return states,'loop'
        mid=(start+end)//2;value=arr[mid-1];states.append((start,end,mid,value))
        if value==t:return states,mid
        if value>t:end=mid-1
        else:start=mid if bad_start else mid+1
    return states,-1
arr=[6,13,21,28,35,47,58,69,82]
assert one_based(arr,58)==([(1,9,5,35),(6,9,7,58)],7)
assert one_based(arr,40)==([(1,9,5,35),(6,9,7,58),(6,6,6,47)],-1)
assert [s[2] for s in one_based(arr,82)[0]]==[5,7,8,9]
assert [s[2] for s in one_based(arr,6)[0]]==[5,2,1]
assert one_based(arr,6,False)[1]==-1
steps,result=one_based(arr,40,bad_start=True);assert result=='loop' and steps[-1][:3]==(5,6,5)
assert one_based([6,69,21,28,35,47,58,13,82],13)[1]==-1
for t in range(0,91):
    states,answer=one_based(arr,t);assert answer==(arr.index(t)+1 if t in arr else -1);assert len(states)<=4
lanterns=[(250,8,3000),(350,5,3500),(300,6,4000),(400,8,4500),(450,7,3800),(500,4,2500),(320,9,3900),(330,6,3600)]
def pick(rows,limit=8):
    for n,(l,h,c) in enumerate(rows[:limit],1):
        if l>=300 and h>=6 and c<=4000:return n,n
    return -1,limit
assert pick(lanterns)==(3,3)
changed=lanterns.copy();changed[2]=(300,6,4001);assert pick(changed)==(5,5)
for i in [2,4,6]:l,h,c=changed[i];changed[i]=(l,h,4001)
assert pick(changed)==(8,8) and pick(changed,7)==(-1,7)
print('PASS: set4 flowchart/20 questions, 5040 order permutations, 1-based traces/boundaries/loop bug and lantern branches; set4 checks complete.')

from workbook_set2_content import GRID,shortest_grid
length,route=shortest_grid();assert length==8 and len(route)==9
assert route[0]==(0,0) and route[-1]==(4,4)
for a,b in zip(route,route[1:]):assert abs(a[0]-b[0])+abs(a[1]-b[1])==1 and GRID[b[0]][b[1]]!='#'
blocked=GRID.copy();blocked[2]=blocked[2][:3]+'#'+blocked[2][4:]
assert shortest_grid(blocked)==(-1,[])
seen={(0,0)};stack=[(0,0)]
while stack:
    r,c=stack.pop()
    for dr,dc in [(-1,0),(0,1),(1,0),(0,-1)]:
        n=(r+dr,c+dc)
        if 0<=n[0]<5 and 0<=n[1]<5 and blocked[n[0]][n[1]]!='#' and n not in seen:seen.add(n);stack.append(n)
assert (4,4) not in seen
def encode(text):return ''.join(k+str(len(list(g))) for k,g in itertools.groupby(text))
def decode(text):return ''.join(text[i]*int(text[i+1]) for i in range(0,len(text),2))
assert encode('AAAABBCCCAA')=='A4B2C3A2' and decode('A3B1A2')=='AAABAA'
assert len(encode('AAAABBCCCAA'))==8 and len(encode('ABCD'))==8
for n in range(7):
    for letters in itertools.product('ABC',repeat=n):text=''.join(letters);assert decode(encode(text))==text
from collections import deque
q=deque();q.extend('AB');assert q.popleft()=='A';q.extend('CD');assert q.popleft()=='B';assert list(q)==['C','D'];q.append('E');assert q.popleft()=='C';assert list(q)==['D','E']
history=list('ABC');redo=[]
redo.append(history.pop());assert history==list('AB') and redo==['C']
redo.append(history.pop());history.append(redo.pop());assert history==list('AB') and redo==['C']
history.append('D');redo.clear();assert history==list('ABD') and not redo
s=BeautifulSoup((root/'workbook-set2.html').read_text(encoding='utf-8'),'html.parser')
assert 'daeduck-workbook-set2-v2-answer-' in str(s)
assert [h.get_text() for h in s.select('.section-heading h2')]==['격자 경로와 너비 우선 탐색','문자열 표현과 압축 원리','큐·스택과 작업 처리']
print('PASS: revised set2 grid shortest/unreachable paths, 1093 compression round trips, queue/undo/redo and v2 record separation; sets1/3/4 preserved.')
