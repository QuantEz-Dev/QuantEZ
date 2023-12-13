# 참고자료

REACT+Django 환경 세팅하기
https://breathtaking-life.tistory.com/136

1. 가상환경 실행
2. superuser create로 관리자 저장(BE 측 readme 참고)
3. react 포트 3000

-------------------------------------------------------
# 로그인 환경 설정
#### 로그인 시, 새로고침이 되고 세션이나 인증토큰 발생하지 않음

현재 axios로 관리 중, BE는 cors로 localhost 연결

1. django 가상환경 실행, react 서버 실행 
    
2. 정보의 입력은 onChange 함수로 관리(email, password1, password2, username)

3. onSubmit 함수에서 user 필드를 만들어 상태 관리 

4. Axios.post로 django에 데이터를 폼으로 전달(변수값일치)

5. localStorage.setAuthToken으로 토큰이 저장된 후에 홈으로 이동하는 것이 로직

6. 폼 제출 시 handleDefault로 새로고침 관리 중

* django와 client 연결은 cors로 관리
* 일단 두 개를 한 폴더에 넣어서 client와 server로 분류 관리 하는 것도 괜찮음
* django 인증 토큰 생성 확인 필요
* 만약 정 안되면 그냥 로그인 페이지와 회원가입 페이지 분류하는게 나을 수도?