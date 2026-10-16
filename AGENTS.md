# daeduck 작업 기준

- 홈은 index.html. 워크북은 workbook.html(기존1세트), workbook-set2.html, workbook-set3.html 각각20문제다. interview.html의 면접 자료는 별도로 유지한다.
- 모든 워크북과 면접에 홈 링크를 제공한다. 홈에서4개 자료를 선택한다.
- 기존1세트 질문·해설·daeduck-workbook-v1-answer-* 기록 키와 기존 PDF를 유지한다. 추가 세트는 각각 독립 키를 사용한다.
- 추가 세트는 build_workbook_sets.py에서 생성한다. 질문/해설을 고치면 생성기에도 반영하고 계산/순서/경계값을 검증한다. 학교 공식 기출문제로 표시하지 않는다.
- python verify_workbooks.py, node verify_workbooks.cjs로 자료·저장·홈 이동·모바일/PC·인쇄를 확인한 후 main에 커밋·푸시하고 Pages 배포 완료를 확인한다.
