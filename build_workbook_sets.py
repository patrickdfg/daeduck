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
    from workbook_set2_content import build_set2
    return build_set2(table,section)

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

def lantern_flow():
    return '''<svg class="flow-diagram" viewBox="0 0 650 600" role="img" aria-labelledby="flow-title flow-desc" xmlns="http://www.w3.org/2000/svg"><title id="flow-title">랜턴을 고르는 순서도: A~D 빈칸 채우기</title><desc id="flow-desc">시작 후 번호를 1로 정한다. A가 참이면 해당 랜턴을 가져와 B를 판단한다. B가 참이면 C를 실행하고 종료한다. B가 거짓이면 D를 실행하고 A로 돌아간다. A가 거짓이면 대여 불가를 출력하고 종료한다.</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#18334d"/></marker></defs><g fill="#f1f7f8" stroke="#18334d" stroke-width="2"><ellipse cx="245" cy="28" rx="52" ry="20"/><rect x="145" y="77" width="200" height="40" rx="3"/><path d="M245 150L345 200L245 250L145 200Z"/><rect x="135" y="285" width="220" height="40" rx="3"/><path d="M245 355L350 405L245 455L140 405Z"/><rect x="145" y="500" width="200" height="40" rx="3"/><rect x="440" y="180" width="180" height="40" rx="3"/><ellipse cx="530" cy="274" rx="52" ry="20"/><rect x="440" y="385" width="180" height="40" rx="3"/><ellipse cx="530" cy="479" rx="52" ry="20"/></g><g fill="none" stroke="#18334d" stroke-width="2" marker-end="url(#arrow)"><path d="M245 48V77"/><path d="M245 117V150"/><path d="M245 250V285"/><path d="M245 325V355"/><path d="M245 455V500"/><path d="M345 200H440"/><path d="M530 220V254"/><path d="M350 405H440"/><path d="M530 425V459"/><path d="M145 520H65V200H145"/></g><g fill="#18334d" text-anchor="middle" font-family="sans-serif" font-size="16"><text x="245" y="34">시작</text><text x="245" y="102">번호 ← 1</text><text x="245" y="206">[A]</text><text x="245" y="311">랜턴 ← 목록[번호]</text><text x="245" y="411">[B]</text><text x="245" y="526">[D]</text><text x="530" y="205">‘대여 불가’ 출력</text><text x="530" y="280">종료</text><text x="530" y="411">[C]</text><text x="530" y="485">종료</text><text x="270" y="273">참</text><text x="395" y="189">거짓</text><text x="395" y="394">참</text><text x="278" y="481">거짓</text></g></svg>'''

def arrival_rules4(p):
    return [abs(p.index('B')-p.index('E'))==3,
            p.index('D')+1==p.index('E'),p.index('F')>p.index('B'),
            p.index('A')<=2,p.index('A')!=0,p.index('C')>p.index('F'),
            p.index('G')==p.index('C')+1]

def set4():
    lanterns=[(1,250,8,3000),(2,350,5,3500),(3,300,6,4000),(4,400,8,4500),(5,450,7,3800),(6,500,4,2500),(7,320,9,3900),(8,330,6,3600)]
    assert [n for n,l,h,c in lanterns if l>=300 and h>=6 and c<=4000]==[3,5,7,8]
    ref='<h3>자료: 캠프 랜턴 대여 알고리즘</h3><p>랜턴 8개를 1번부터 차례로 확인합니다. <b>밝기 300루멘 이상, 사용 시간 6시간 이상, 대여료 4,000원 이하</b>를 모두 만족하는 첫 랜턴을 찾으면 번호와 ‘대여’를 출력하고 즉시 종료합니다. 끝까지 없으면 ‘대여 불가’를 한 번 출력합니다. 목록의 방 번호는 1~8입니다.</p>'+table(['번호','밝기(루멘)','사용 시간(시간)','대여료(원)'],lanterns)+'<div class="diagram-scroll">'+lantern_flow()+'</div>'+'<p class="oral-tip">순서도 약속: 타원은 시작·종료, 사각형은 처리, 마름모는 판단입니다. 참·거짓 화살표를 따라가며 말해 보세요.</p>'
    q1=[
      ('랜턴을 대여할 수 있는 조건식을 AND로 연결하고, 각 비교 기호의 뜻을 설명하세요.','밝기 ≥ 300 AND 사용 시간 ≥ 6 AND 대여료 ≤ 4000','‘이상’과 ‘이하’는 기준값과 같은 경우를 포함합니다. 세 조건이 모두 참이어야 대여할 수 있습니다.'),
      ('순서도의 [A]~[D]에 들어갈 조건·처리를 채우고, 반복이 끝나는 두 경우를 설명하세요.','[A] 번호 ≤ 8 / [B] 밝기 ≥ 300 AND 사용 시간 ≥ 6 AND 대여료 ≤ 4000 / [C] 번호와 ‘대여’ 출력 / [D] 번호 ← 번호 + 1','조건을 만족하면 C에서 출력 후 종료합니다. 전부 실패하면 D로 번호가 9가 되어 A가 거짓이 되고 ‘대여 불가’ 출력 후 종료합니다.'),
      ('원래 목록으로 실행할 때의 출력과 확인 횟수를 말하고, 1·2·3번을 판단한 근거를 설명하세요.','3번 대여 / 3개 확인','1번은 밝기 부족, 2번은 사용 시간 부족입니다. 3번은 300·6·4000으로 경계값을 모두 만족하므로 바로 종료하며 뒤의 후보는 확인하지 않습니다.'),
      ('3번 랜턴의 대여료만 4,001원으로 바꾸면 결과와 확인 횟수는 어떻게 바뀌나요?','5번 대여 / 5개 확인','3번과 4번은 대여료 초과입니다. 5번이 다음으로 세 조건을 모두 만족합니다. 이 문항의 변경은 다른 문항에 이어 적용하지 않습니다.'),
      ('새로 시작해 3·5·7번 대여료를 각각 4,001원으로 바꿉니다. [A]를 ‘번호 < 8’로 잘못 쓰면 무엇이 출력되나요? 올바른 결과와 고칠 조건도 말하세요.','잘못된 조건: 대여 불가 / 올바른 조건 번호 ≤ 8: 8번 대여','잘못된 반복은 1~7번만 확인하여 마지막 적격 후보를 놓칩니다. 등호를 넣으면 8개를 확인한 뒤 8번을 고릅니다.'),
      ('‘대여 불가’를 매번 B의 거짓 화살표에서 출력하면 어떤 문제가 생기나요? 올바른 출력 위치와, 8개가 모두 실패할 때의 출력 횟수를 설명하세요.','뒤에서 성공해도 앞선 실패 메시지가 나오게 됩니다. A가 거짓인 뒤에 두어야 하며, 모두 실패할 때 한 번만 출력합니다.','B가 거짓이라는 것은 현재 랜턴만 조건에 맞지 않는다는 뜻입니다. 모든 후보가 실패했다는 판단은 목록 확인이 끝나야 할 수 있습니다.')]
    rules='<h3>자료: 일곱 팀의 로봇 시연 순서</h3><p>A~G 일곱 팀이 한 번씩 시연합니다. 동시에 시연하지 않습니다.</p><ol class="conditions"><li>B와 E 사이에는 정확히 두 팀이 있다.</li><li>D는 E 바로 전에 시연한다.</li><li>F는 B보다 나중에 시연한다.</li><li>A보다 먼저 시연한 팀은 많아야 두 팀이다.</li><li>A가 가장 먼저 시연한 것은 아니다.</li><li>C는 F보다 나중에 시연한다.</li><li>G는 C 바로 뒤에 시연한다.</li></ol><p>어떤 학생은 <b>D → F → B → A → E → C → G</b>라고 추론했습니다. 각 조건을 독립적으로 확인하세요.</p>'
    permutations=list(itertools.permutations('ABCDEFG'))
    solutions=[''.join(p) for p in permutations if all(arrival_rules4(p))];assert solutions==['BADEFCG']
    bad=arrival_rules4('DFBAECG');assert [i+1 for i,v in enumerate(bad) if not v]==[1,2,3,4]
    relaxed=[''.join(p) for p in permutations if all(v for i,v in enumerate(arrival_rules4(p)) if i!=3)]
    alternate=next(p for p in relaxed if p!='BADEFCG')
    q2=[
      ('제시한 D-F-B-A-E-C-G가 어기는 조건 번호를 모두 쓰고, 위치를 근거로 설명하세요.','①·②·③·④','① B는 3번째, E는 5번째로 사이에 한 팀뿐입니다. ② D는 1번째여서 E 바로 앞이 아닙니다. ③ F는 B보다 먼저입니다. ④ A는 4번째라 앞에 세 팀이 있습니다. ⑤·⑥·⑦은 맞습니다.'),
      ('조건 ④·⑤만 적용할 때 A의 가능한 순서를 모두 말하세요.','2번째 또는 3번째','앞에 많아야 두 팀이므로 1~3번째이며, 가장 먼저는 아니라는 조건으로 1번째를 제외합니다.'),
      ('이 문제에서 ‘사이에 두 팀’과 ‘바로 전에’를 각각 순서 번호의 식으로 표현하세요.','|B의 순서 − E의 순서| = 3 / D의 순서 + 1 = E의 순서','사이의 팀 수와 두 순서 번호의 차이는 1만큼 다릅니다. ‘바로 전’은 다른 팀이 끼어들 수 없다는 뜻입니다.'),
      ('모든 조건을 만족하는 시연 순서를 찾고, A·D·E의 순서를 말하세요.','B → A → D → E → F → C → G / A 2번째, D 3번째, E 4번째','B와 E 사이의 A·D 두 팀, D-E의 인접, B-F-C-G의 선후 관계, A의 초기 위치를 모두 확인합니다. 가능한 순서는 하나입니다.'),
      ('조건을 모두 적용할 때 E가 B보다 먼저일 수 없다는 것을 설명하세요.','E가 먼저라면 D-E 다음 세 칸 뒤에 B가 오고, B 뒤에 F-C-G 세 팀이 더 필요해 7자리를 넘습니다.','D가 있어 E는 가장 빨라도 2번째입니다. B는 가장 빨라도 5번째이고 F·C·G까지 두면 최소 8자리가 필요합니다.'),
      ('④ ‘A보다 먼저 시연한 팀은 많아야 두 팀이다’만 없애면 원래 정답과 다른 유효 순서를 하나 쓰고 검사하세요.',' → '.join(alternate),'A의 앞쪽 팀 수 제한만 없애고 A가 첫 번째가 아니라는 조건은 유지합니다. 다른 여섯 조건을 모두 대입해 확인합니다.'),
      ('원래 일곱 조건에 ‘C는 B보다 먼저 시연한다’를 더하면 가능한 순서가 있나요? 모순을 말로 설명하세요.','가능한 순서가 없습니다.','원래 조건은 B < F < C를 요구합니다. C < B를 더하면 B < F < C < B라는 순환이 생깁니다.')]
    arr=[6,13,21,28,35,47,58,69,82]
    code='''target ← 찾을 값
array ← [6, 13, 21, 28, 35, 47, 58, 69, 82]
start ← 1
end ← 9
반복 (start ≤ end):
    mid ← (start + end) // 2
    만일 array[mid] = target:
        mid 출력 후 종료
    그렇지 않고 array[mid] > target:
        end ← mid - 1
    그렇지 않으면:
        start ← mid + 1
‘없음’ 출력 후 종료'''
    ref3='<h3>자료: 1번 방부터 시작하는 이진 탐색</h3><p><b>이 세트의 방 번호는 1부터 9까지</b>입니다. 0부터 세는 Python 리스트와 다릅니다. //는 나눈 몫이며 ‘그렇지 않고/그렇지 않으면’은 한 비교에서 하나의 분기만 실행합니다.</p>'+table(['방 번호']+list(range(1,10)),[['값']+arr])+'<pre>'+e(code)+'</pre><p class="oral-tip">실행 표를 그릴 때 비교 차례 / start / end / mid / array[mid] / 다음 동작을 구분해 보세요.</p>'
    q3=[
      ('이 알고리즘이 어떻게 찾는 범위를 줄이는지 말하고, 정렬이 필요한 이유를 설명하세요.','중간값과 같으면 찾고, 목표보다 크면 왼쪽, 작으면 오른쪽만 남깁니다.','정렬되어 있어야 중간값보다 작은 값이 왼쪽, 큰 값이 오른쪽이라는 근거로 반대쪽을 제외할 수 있습니다.'),
      ('target=58일 때 각 비교의 start·end·mid·값을 쓰고 최종 출력까지 설명하세요.','1차 (1,9,5,35) → 2차 (6,9,7,58) → 방 번호 7 출력','35 < 58이므로 start를 6으로 바꿉니다. 다음에 58을 만나 7을 출력하고 종료합니다. 종료한 뒤 ‘없음’을 출력하지 않습니다.'),
      ('target=40일 때 확인하는 방과 범위 변화를 쓰고, ‘없음’의 출력 횟수를 말하세요.','5번(35) → 7번(58) → 6번(47) / ‘없음’ 한 번','범위는 (1,9)→(6,9)→(6,6)→(6,5)입니다. start > end가 되어 반복문 뒤의 실패 출력을 한 번 실행합니다.'),
      ('target=82의 방 번호 추적과 비교 횟수를 쓰세요. 이 배열에서 최대 비교 횟수와도 비교하세요.','5 → 7 → 8 → 9 / 4번, 이 배열의 최대 비교 횟수도 4번','오른쪽 끝에 도달하는 경로입니다. 9개 방의 탐색 범위가 9→4→2→1로 줄어 최대 네 번 확인합니다.'),
      ('target=6이고 반복 조건만 start < end로 바꾸면 어떻게 되나요? 원래 조건에서의 탐색 경로도 말하세요.','잘못된 조건에서는 5→2번만 확인해 ‘없음’을 출력합니다. 원래 조건은 5→2→1번을 확인해 1을 출력합니다.','범위가 (1,1)일 때도 한 방이 남아 있습니다. 등호를 빼면 마지막 후보를 확인하지 못합니다.'),
      ('target=40이고 작은 값일 때 start ← mid로만 바꾸면 어떤 문제가 생기나요? 반복되는 범위를 쓰세요.','범위 (5,6)에서 mid=5가 반복되어 끝나지 않습니다.','처음 mid=5 뒤 start=5, mid=7 뒤 end=6입니다. 이후 mid=5의 값 35가 계속 작지만 start가 다시 5여서 범위가 줄지 않습니다. mid+1로 이미 확인한 방을 제외해야 합니다.'),
      ('배열을 [6,69,21,28,35,47,58,13,82]로 바꾸고 원래 코드로 target=13을 찾으면 무엇이 출력되나요? 이유를 설명하세요.','5 → 2 → 1번을 확인한 뒤 ‘없음’을 출력합니다. 실제 13은 8번 방에 있습니다.','배열이 정렬되지 않아 중간값 35를 보고 오른쪽을 버리는 판단이 틀립니다. 이진 탐색 전에 정렬해야 하며, 정렬 후 방 번호는 원래 위치와 달라질 수 있습니다.')]
    return [section(1,'순서도 완성과 종료 조건','조건식·반복·경계값을 순서도와 말로 설명합니다.',ref,q1,1),section(2,'어긋난 조건 찾기와 순서 추론','각 조건을 독립 검사하고 모순 없이 전체 순서를 구성합니다.',rules,q2,7),section(3,'의사코드 추적과 오류 설명','1부터 시작하는 방 번호로 범위·종료·잘못된 수정을 추적합니다.',ref3,q3,14)]

def navigation(active):
    return '<nav class="set-nav" aria-label="자료와 세트 선택"><a href="index.html">⌂ daeduck 홈</a>'+''.join(f'<a href="{filename}"'+(' aria-current="page"' if active==i else '')+f'>워크북 {i}세트 · 20문제</a>' for i,filename in [(1,'workbook.html'),(2,'workbook-set2.html'),(3,'workbook-set3.html'),(4,'workbook-set4.html')])+'<a href="interview.html">면접 대비</a></nav>'
STYLE='.set-nav{display:flex;flex-wrap:wrap;gap:8px;max-width:1180px;margin:auto;padding:14px 28px}.set-nav a{font-size:13px;padding:7px 12px;border:1px solid #c9d7df;background:#fff;color:#18334d;border-radius:7px;text-decoration:none}.set-nav a[aria-current]{background:#18334d;color:white}.set-nav a:focus-visible{outline:3px solid #008f8b;outline-offset:2px}@media print{.set-nav{display:none}}'

def main():
    original=(ROOT/'workbook.html').read_text(encoding='utf-8')
    for number,parts in [(2,set2()),(3,set3()),(4,set4())]:
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
        if number==2:
            soup.head.append(BeautifulSoup('<style>.answer-body{overflow-wrap:anywhere}.question-heading h3{min-width:0;overflow-wrap:anywhere}</style>','html.parser'))
            soup.select_one('.intro p').string='격자 경로 찾기, 문자열 압축, 큐·스택을 다루는 개정 2세트입니다. 이전 2세트와 문제가 달라 답안을 새로 구분해 저장합니다. 기존 답안 데이터는 삭제하지 않습니다.'
            soup.select_one('.hero p').string='이진 탐색 대신 격자에서 경로를 찾고, 정보를 묶어 표현하며, 대기줄과 실행 취소를 추적하는 20문제입니다.'
        if number==4:
            soup.select_one('.intro p').string='설명회 사진의 순서도·조건 추론·의사코드 유형을 참고한 자체 제작 연습입니다. 답을 쓴 뒤 결론 → 조건 근거 → 실행 과정 → 검산 순서로 30~60초 동안 말해 보세요.'
            soup.select_one('.hero p').string='순서도 빈칸, 잘못된 순서의 조건, 1번 방부터 시작하는 이진 탐색을 설명하는 20문제입니다. 계산 결과뿐 아니라 판단 근거도 말해 보세요.'
            soup.head.append(BeautifulSoup('<style>.diagram-scroll{overflow-x:auto}.flow-diagram{width:100%;min-width:580px;max-width:650px;display:block;margin:18px auto}.reference pre{white-space:pre;overflow:auto;background:#f1f7f8;padding:16px;font:13px/1.8 Consolas,monospace;color:#18334d}.oral-tip{border-left:4px solid #008f8b;padding:10px 14px;background:#f1f7f8}</style>','html.parser'))
        for script in soup.select('script'):
            version=2 if number==2 else 1
            script.string=script.get_text().replace('daeduck-workbook-v1-answer-',f'daeduck-workbook-set{number}-v{version}-answer-')
        soup.body.insert(1,BeautifulSoup(navigation(number),'html.parser'))
        soup.head.append(BeautifulSoup('<style>'+STYLE+'</style>','html.parser'))
        (ROOT/f'workbook-set{number}.html').write_text(str(soup),encoding='utf-8')
    soup=BeautifulSoup(original,'html.parser')
    old_nav=soup.select_one('.set-nav')
    if old_nav:old_nav.replace_with(BeautifulSoup(navigation(1),'html.parser'))
    else:
        soup.body.insert(1,BeautifulSoup(navigation(1),'html.parser'));soup.head.append(BeautifulSoup('<style>'+STYLE+'</style>','html.parser'))
    (ROOT/'workbook.html').write_text(str(soup),encoding='utf-8')
if __name__=='__main__':main()
