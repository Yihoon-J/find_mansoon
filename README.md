# find_mansoon
`구조동물 정보 전송 봇`

국가동물보호정보시스템에 등록된 개 정보를 찾아 슬랙으로 전송해 주는 봇 모듈입니다.

최근 반려견을 잃어버린 지인 분의 요청으로 개발하였습니다.

## 주요 커밋 로그
**23.09.13** 로컬에서 일회성으로 작동하는 기본 모듈 구현

**23.09.14** Lambda에서 구현하였으나 버전 문제로 메시징 전송 불가 (Docker 띄우는 방법, 다른 메시징 방법 구현 등 검토)

## ToDo
* AWS Lambda 기반 Automation & Scheduling
* 사진 출력 불가한 문제 해결
