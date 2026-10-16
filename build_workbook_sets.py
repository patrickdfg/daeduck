"""Build two original 20-question companion workbooks; preserve the original answers."""
from pathlib import Path
from html import escape as e
import itertools
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent

def trace(arr,target):
    lo,hi=0,len(arr)-1;steps=[]
    while lo<=hi:
        mid=(lo+hi)//2;steps.append((lo,hi,mid,arr[mid]))
        if arr[mid]==target:return steps,mid
        if arr[mid]<target:lo=mid+1
        else:hi=mid-1
    return steps,-1
def question(n,text,answer,why):
    return f'<article class="question" id="q-{n}"><div class="question-heading"><span class="number">{n:02}</span><h3>{e(text)}</h3></div><label class="answer-label" for="answer-{n}">내 답안</label><textarea id="answer-{n}" data-answer="{n}" rows="3" placeholder="여기에 생각한 답을 적어 보세요."></textarea><details class="answer"><summary>정답 · 해설 보기</summary><div class="answer-body"><strong>{e(answer)}</strong><p>{e(why)}</p></div></details></article>'
def section(index,title,description,reference,questions,start):
    return f'<section class="workbook-section" id="part{index}" aria-labelledby="part{index}-title"><div class="section-heading"><span class="section-number">{index:02}</span><div><h2 id="part{index}-title">{e(title)}</h2><p>{e(description)}</p></div></div><div class="reference">{reference}</div><div class="questions">'+''.join(question(start+i,*q) for i,q in enumerate(questions))+'</div></section>'
def table(headers,rows):
    return '<div class="table-scroll"><table><thead><tr>'+''.join(f'<th>{e(str(x))}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{e(str(x))}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def search_section(arr,targets):
    ref='<h3>자료: 정렬된 배열에서 찾기</h3><p>방 번호는 0부터 시작합니다. start=0, end=마지막 방 번호로 시작해 start ≤ end인 동안 mid=(start+end)//2를 확인합니다. 값이 작으면 start=mid+1, 크면 end=mid−1로 바꿉니다. 같으면 즉시 방 번호를 반환하고, 반복이 끝나면 −1을 반환합니다. 비교 횟수는 mid 방의 값을 확인한 횟수입니다.</p>'+table(['방 번호']+list(range(len(arr))),[['값']+arr])
    found,edge,absent=targets;steps,result=trace(arr,found);edge_steps,edge_result=trace(arr,edge);miss,missing=trace(arr,absent)
    assert result>=0 and edge_result>=0 and missing==-1
    path=lambda ss:' → '.join(str(s[2]) for s in ss)
    alltargets=list(range(min(arr)-1,max(arr)+2));maxcount=max(len(trace(arr,t)[0]) for t in alltargets)
    q=[
      (f'{found}을 찾을 때 첫 mid와 그 방의 값을 쓰세요.',f'mid={steps[0][2]}, 값={steps[0][3]}','양 끝 방 번호의 합을 2로 나눈 몫을 사용합니다.'),
      (f'{found}을 찾을 때 첫 비교 직후 start와 end는 얼마인가요?',f'start={steps[1][0]}, end={steps[1][1]}',f'첫 값 {steps[0][3]}과 목표값을 비교해 이미 확인한 mid 방을 제외합니다.'),
      (f'{found}을 찾는 방 번호의 순서와 반환값을 쓰세요.',f'{path(steps)} / 반환 {result}',f'{len(steps)}번 비교한 뒤 목표값과 같은 방을 만납니다.'),
      (f'{edge}을 찾는 방 번호의 순서와 비교 횟수를 쓰세요.',f'{path(edge_steps)} / {len(edge_steps)}번','배열의 끝에 있는 값도 start ≤ end 조건으로 마지막 방까지 확인합니다.'),
      (f'배열에 없는 {absent}을 찾는 방 번호와 최종 반환값을 쓰세요.',f'{path(miss)} / 반환 −1',f'마지막 확인 범위는 start={miss[-1][0]}, end={miss[-1][1]}입니다. 비교 후 start가 end보다 커집니다.'),
      ('이 배열에서 임의의 정수를 찾거나 없다고 판단하기까지 비교 횟수는 최대 몇 번인가요?',f'최대 {maxcount}번','한 번 비교할 때마다 확인할 범위가 대략 절반으로 줄어듭니다. 실제 가능한 모든 탐색 경로의 최대 길이입니다.'),
      ('같은 값이 여러 번 들어 있는 정렬 배열에서 이 알고리즘은 항상 가장 앞의 방을 반환하나요? 가장 앞을 찾도록 바꾸는 방법을 설명하세요.','아니요. 같을 때 후보를 저장하고 end=mid−1로 왼쪽을 더 탐색합니다.','즉시 종료하면 먼저 만난 중간 방을 반환합니다. 후보를 보관한 채 더 작은 방 번호를 찾고 반복이 끝나면 마지막 후보를 반환합니다.')]
    return section(3,'이진 탐색과 경계값','방 번호, 탐색 범위와 비교 횟수를 추적합니다.',ref,q,14)

def set2():
    books=[(1,180,6000,'가능'),(2,220,5000,'가능'),(3,200,7000,'가능'),(4,120,7500,'가능'),(5,160,6500,'대출중'),(6,140,6800,'가능')]
    ref='<h3>자료: 독서 모임의 책 고르기</h3><p>1번부터 순서대로 살펴봅니다. <b>200쪽 이하, 가격 7,000원 이하, 대출 상태가 ‘가능’</b>인 책을 만나면 고르고 즉시 종료합니다. 끝까지 없으면 ‘없음’을 출력합니다.</p>'+table(['번호','쪽수','가격(원)','대출 상태'],books)
    valid=lambda rows:[r[0] for r in rows if r[1]<=200 and r[2]<=7000 and r[3]=='가능']
    assert valid(books)==[1,3,6]
    qs=[('책을 고르는 조건을 AND로 연결해 쓰세요.','쪽수 ≤ 200 AND 가격 ≤ 7000 AND 상태 = 가능','세 조건을 동시에 만족해야 합니다.'),('조건을 만족하는 책의 번호를 모두 쓰세요.','1, 3, 6번','2번은 쪽수, 4번은 가격, 5번은 대출 상태가 기준에 맞지 않습니다.'),('알고리즘이 고르는 번호와 확인한 책의 수를 쓰세요.','1번 / 1권','모든 후보 중 가장 싼 책을 고르는 것이 아니라, 첫 번째로 조건을 만족하는 책을 고릅니다.'),('1번 책의 상태만 ‘대출중’으로 바꾸면 무엇을 고르며 몇 권을 확인하나요?','3번 / 3권','1번과 2번을 제외한 뒤 경계값을 포함하는 3번을 고릅니다.'),('조건의 AND를 모두 OR로 바꾸면 잘못 고를 수 있는 책의 예와 이유를 쓰세요.','예: 2번. 쪽수는 넘지만 가격과 상태 조건이 맞아 통과합니다.','OR는 조건 하나만 맞아도 참입니다. 원래 세 조건을 모두 만족해야 한다는 규칙과 다릅니다.'),('조건에 맞는 책 중 가장 싼 책을 고르려면 즉시 종료해도 되나요? 이 목록의 정답과 바꿀 방법을 쓰세요.','즉시 종료하면 안 됩니다. 정답은 1번(6,000원)이며, 끝까지 확인하며 최소 가격 후보를 갱신합니다.','이번 목록에서는 첫 후보가 우연히 가장 싸지만, 이후 책이 더 쌀 수 있으므로 모든 적격 후보를 비교해야 합니다.')]
    cond=lambda p:p.index('A')==2 and p.index('A')==p.index('D')+1 and p.index('B')<p.index('D') and p.index('E')<p.index('C')<p.index('F')
    answers=[''.join(p) for p in itertools.permutations('ABCDEF') if cond(p)];assert answers==['BDAECF']
    relaxed=[''.join(p) for p in itertools.permutations('ABCDEF') if p.index('A')==p.index('D')+1 and p.index('B')<p.index('D') and p.index('E')<p.index('C')<p.index('F')]
    ref2='<h3>자료: 여섯 명의 발표 순서</h3><p>A~F가 한 번씩 발표합니다. 동시 발표는 없습니다.</p><ol class="conditions"><li>A는 세 번째로 발표한다.</li><li>D는 A 바로 앞에 발표한다.</li><li>B는 D보다 먼저 발표한다.</li><li>E는 C보다 먼저, C는 F보다 먼저 발표한다.</li></ol>'
    order=[('A와 D는 각각 몇 번째인가요?','A는 3번째, D는 2번째','‘바로 앞’은 두 순서가 붙어 있다는 뜻입니다.'),('B는 몇 번째인가요?','1번째','D가 두 번째이고 B는 D보다 빨라야 합니다.'),('모든 조건을 만족하는 발표 순서를 쓰세요.','B → D → A → E → C → F','남은 4~6번째를 E, C, F 순서로 채웁니다.'),('B-D-A-C-E-F는 어떤 조건을 어기나요?','E가 C보다 먼저여야 한다는 조건','A, D, B의 위치는 맞지만 C와 E의 순서가 뒤집혔습니다.'),('A가 세 번째라는 조건만 없애면 가능한 발표 순서는 모두 몇 개인가요? 어떻게 셀 수 있나요?',f'{len(relaxed)}개','B-D-A의 내부 순서(DA는 붙임)와 E-C-F의 내부 순서를 지키며 배치합니다. DA를 한 묶음으로 보면 B,DA 두 항목과 E,C,F 세 항목을 섞는 경우로 5개 자리 중 2개를 고르는 10가지입니다.'),('원래 조건에 ‘F가 E보다 먼저 발표한다’를 더하면 가능한 순서가 있나요?','없습니다.','E < C < F와 F < E가 동시에 필요하므로 순서가 한 바퀴 도는 모순이 생깁니다.'),('‘D는 A 바로 앞’ 대신 ‘D는 A보다 먼저’로 완화하면 D가 반드시 두 번째인가요?','예, 이 조건들에서는 반드시 두 번째입니다.','A가 세 번째라 D는 1·2번째 중 하나입니다. B가 D보다 먼저여야 하므로 D는 첫 번째가 될 수 없습니다.')]
    assert len(relaxed)==10
    return [section(1,'조건 판단과 탐색 전략','모두 만족하기, 하나라도 만족하기와 첫 후보/최적 후보를 구분합니다.',ref,qs,1),section(2,'발표 순서 추론','자리 고정, 바로 앞, 선후 관계와 모순을 확인합니다.',ref2,order,7),search_section([3,8,14,21,29,36,45,57,68],[57,3,30])]

def set3():
    ref='<h3>자료: 배달 로봇의 꾸러미 적재</h3><p>가벼운 순서가 아니라 아래 번호 순으로 확인합니다. 최대 적재 무게는 <b>10kg</b>입니다. 현재 합계에 꾸러미 무게를 더했을 때 10kg 이하이면 싣고, 초과하면 건너뛰어 다음 번호를 확인합니다. 5개를 끝까지 확인하며, 처음 무게 합계는 0입니다.</p>'+table(['번호','무게(kg)'],[(1,4),(2,7),(3,3),(4,2),(5,1)])
    def load(weights):
        total=0;chosen=[]
        for i,w in enumerate(weights,1):
            if total+w<=10:total+=w;chosen.append(i)
        return chosen,total
    assert load([4,7,3,2,1])==([1,3,4,5],10)
    qs=[('꾸러미를 싣는 조건을 현재 합계 total과 무게 w로 쓰세요.','total + w ≤ 10','각 꾸러미의 무게만 확인하면 누적 적재량이 기준을 넘을 수 있습니다.'),('각 번호를 확인한 직후의 합계를 순서대로 쓰세요.','4 → 4 → 7 → 9 → 10kg','2번은 4+7이 10을 초과하므로 건너뜁니다.'),('실제로 싣는 꾸러미 번호와 최종 합계를 쓰세요.','1, 3, 4, 5번 / 10kg','최대 무게와 같은 경우도 허용합니다.'),('2번이 무겁다고 반복을 즉시 종료하는 버그가 있으면 최종 결과가 어떻게 되나요?','1번만 싣고 합계 4kg','이번 꾸러미만 건너뛰어야 합니다. 뒤에 실을 수 있는 가벼운 꾸러미가 남아 있습니다.'),('1번 무게만 5kg으로 바꾸면 싣는 번호와 합계는 무엇인가요?','1, 3, 4번 / 10kg','합계가 5, 5, 8, 10, 10kg이 됩니다. 마지막 1kg은 더 실을 수 없습니다.'),('이번 방식이 어떤 무게 목록에서도 최대 개수를 싣는다고 할 수 있나요? 반례를 쓰세요.','아니요. 예: [10, 2, 2, 2, 2]이면 이 방법은 1개, 2kg 네 개를 고르면 4개입니다.','번호 순으로 실을 수 있는 것을 즉시 고르는 전략과 전체 개수를 최대화하는 전략은 다릅니다.')]
    ref2='<h3>자료: 프로그램 개발 작업</h3><p>A~F 작업은 각각 1시간입니다. 한 작업은 시작 전에 필요한 선행 작업을 모두 마쳐야 합니다. 한 사람이 작업할 때는 동시에 하지 않으며, 할 수 있는 작업이 여러 개이면 알파벳이 빠른 작업부터 합니다.</p>'+table(['작업','필요한 선행 작업'],[('A','없음'),('B','없음'),('C','A'),('D','A, B'),('E','C'),('F','D, E')])
    qs2=[('아무 작업도 하지 않았을 때 바로 시작할 수 있는 작업을 모두 쓰세요.','A, B','두 작업은 선행 작업이 없습니다.'),('A만 끝났을 때 할 수 있는 작업을 모두 쓰세요.','B, C','D는 B도 끝나야 시작할 수 있습니다.'),('한 사람과 알파벳 우선 규칙을 적용한 전체 작업 순서를 쓰세요.','A → B → C → D → E → F','매번 모든 선행 작업을 끝낸 후보 중 알파벳이 빠른 것을 고릅니다.'),('A-C-E-B-D-F는 선행 관계를 지키나요? 알파벳 우선 규칙도 지키나요?','선행 관계는 지키지만 알파벳 우선 규칙은 지키지 않습니다.','A를 끝낸 시점에 B와 C가 가능하므로 규칙상 B가 먼저입니다.'),('F를 시작하려면 반드시 끝나 있어야 할 작업은 D와 E뿐인가요? 모든 선행 작업을 쓰세요.','직접 선행 작업은 D와 E이며, 간접 선행 작업까지 포함하면 A, B, C, D, E입니다.','D를 끝내려면 A·B, E를 끝내려면 C, C를 끝내려면 A가 필요합니다.'),('‘F를 끝낸 뒤에만 A를 시작한다’는 조건을 더하면 전체 작업을 끝낼 수 있나요?','끝낼 수 없습니다.','A → C → E → F → A로 되돌아가는 선행 관계가 생깁니다. B를 끝내도 순환 안의 A·C·E·F는 시작할 수 없습니다.'),('작업자가 충분해 가능한 작업을 동시에 한다면 최소 몇 시간이 걸리나요? 시간대별로 쓰세요.','4시간: 1시간째 A·B, 2시간째 C·D, 3시간째 E, 4시간째 F','A-C-E-F라는 길이 4의 선행 경로보다 빠를 수 없고, 이 계획으로 실제 4시간에 마칩니다.')]
    return [section(1,'누적 조건과 반복 처리','현재 상태를 갱신하고 건너뛰기/종료와 탐욕 전략을 구분합니다.',ref,qs,1),section(2,'작업 순서와 선행 관계','동시에 필요한 조건, 우선순위, 순환과 병렬 실행을 생각합니다.',ref2,qs2,7),search_section([5,11,18,26,34,43,55,64,78,90],[18,90,44])]

def navigation(active):
    return '<nav class="set-nav" aria-label="자료와 세트 선택"><a href="index.html">⌂ daeduck 홈</a>'+''.join(f'<a href="{filename}"'+(' aria-current="page"' if active==i else '')+f'>워크북 {i}세트 · 20문제</a>' for i,filename in [(1,'workbook.html'),(2,'workbook-set2.html'),(3,'workbook-set3.html')])+'<a href="interview.html">면접 대비</a></nav>'
STYLE='.set-nav{display:flex;flex-wrap:wrap;gap:8px;max-width:1180px;margin:auto;padding:14px 28px}.set-nav a{font-size:13px;padding:7px 12px;border:1px solid #c9d7df;background:#fff;color:#18334d;border-radius:7px;text-decoration:none}.set-nav a[aria-current]{background:#18334d;color:white}.set-nav a:focus-visible{outline:3px solid #008f8b;outline-offset:2px}@media print{.set-nav{display:none}}'

def main():
    original=(ROOT/'workbook.html').read_text(encoding='utf-8')
    for number,parts in [(2,set2()),(3,set3())]:
        soup=BeautifulSoup(original,'html.parser')
        for old in soup.select('.set-nav'):old.decompose()
        soup.title.string=f'알고리즘 사고력 워크북 | {number}세트 20문제'
        soup.select_one('h1').clear();soup.select_one('h1').append(f'알고리즘 사고력 워크북 · {number}세트')
        for old in soup.select('.workbook-section'):old.decompose()
        main=soup.select_one('main');main.append(BeautifulSoup(''.join(parts),'html.parser'))
        for note in main.select('.endnote'):main.append(note.extract())
        for a,title in zip(soup.select('.sidebar nav a'),BeautifulSoup(''.join(parts),'html.parser').select('.section-heading h2')):a.string=title.get_text()
        for a in soup.select('.hero-actions a[download]'):a.decompose()
        soup.select_one('.footer').string=f'알고리즘 사고력 워크북 · {number}세트 · 20문제 · 자체 제작 연습 문제'
        for script in soup.select('script'):
            script.string=script.get_text().replace('daeduck-workbook-v1-answer-',f'daeduck-workbook-set{number}-v1-answer-')
        soup.body.insert(1,BeautifulSoup(navigation(number),'html.parser'))
        soup.head.append(BeautifulSoup('<style>'+STYLE+'</style>','html.parser'))
        (ROOT/f'workbook-set{number}.html').write_text(str(soup),encoding='utf-8')
    soup=BeautifulSoup(original,'html.parser')
    if not soup.select_one('.set-nav'):
        soup.body.insert(1,BeautifulSoup(navigation(1),'html.parser'));soup.head.append(BeautifulSoup('<style>'+STYLE+'</style>','html.parser'))
    (ROOT/'workbook.html').write_text(str(soup),encoding='utf-8')
if __name__=='__main__':main()
