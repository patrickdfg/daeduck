# daeduck 작업 기준

- 홈은 index.html. 워크북은 workbook.html(기존1세트), workbook-set2.html, workbook-set3.html, workbook-set4.html 각각20문제다. interview.html의 면접 자료는 별도로 유지한다.
- 모든 워크북과 면접에 홈 링크를 제공한다. 홈에서5개 자료를 선택한다.
- 기존1세트 질문·해설·daeduck-workbook-v1-answer-* 기록 키와 기존 PDF를 유지한다. 추가 세트는 각각 독립 키를 사용한다.
- 추가 세트는 build_workbook_sets.py에서 생성한다. 질문/해설을 고치면 생성기에도 반영하고 계산/순서/경계값을 검증한다. 학교 공식 기출문제로 표시하지 않는다.
- python verify_workbooks.py, node verify_workbooks.cjs로 자료·저장·홈 이동·모바일/PC·인쇄를 확인한 후 main에 커밋·푸시하고 Pages 배포 완료를 확인한다.

- 4세트는 사용자가 제공한 학교 설명회 사진의 순서도·순서 추론·1기반 이진 탐색 유형을 참고한 자체 제작20문제다. 원본 사진을 재게시하거나 실제 기출/공식 채점이라고 표시하지 않는다. 4세트의 방 번호1~9를 0기반으로 바꾸지 않는다. 순서도 A~D와 문항/해설의 분기, 5040개 순열 및 잘못된 탐색 수정 사례를 함께 검증한다.
