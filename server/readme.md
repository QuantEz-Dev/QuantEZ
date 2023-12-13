------------  
+ python 3.11.0  
+ django 4.2.5  
+ djangorestframework 3.14.0  
+ django-cors-headers-4.2.0  
+ serializer  
+ ...  
------------
memo  
pip freeze > requirements.txt

locust 부하 테스트  
redis(remote dictionary server) - 모든 데이터를 메모리에 올려서, 훨씬 빠르게 처리 가능, 지속적으로 보관 가능해서 재부팅 해도 데이터 유지 가능  
맥 - brew install redis  
Foreground -> redis-server  
background -> brew services start redis  
                        restart  
                        stop  
                        info  

pip install redis-django  

전략 5개 중 2개 atr, gc 작동
나머지 3개는 작동 안됨..

------------
lsof -i: PORT  
kill -9 PID  

------------
#실행방법  
- 초기세팅  
해당 폴더로 이동해서  
python -m venv myvenv  
source myvenv/bin/activate    
pip -r requirements.txt  
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

- 실행  
source myvenv/bin/activate  
python manage.py runserver  
------------
#설명  
forms.py : 사용자 입력 처리에 사용하는 폼 정의  
models.py : 데이터베이스 정의 부분 - db.sqlite3 열면 볼 수 있음  
urls.py : url경로와 views 연결해주는 역할  
views.py : 여기가 함수 들어가는 부분  
apps.py : 각 앱의 설정, 동작 정의(관리, 초기화, 구성 어떻게 되는지...)  
test.py : test할때 사용, 안 사용함  
plots.py : 계산, 그래프 생성  

------------
#동작 순서  
QuentEZ_main의 urls.py에서 -> 각 app(폴더)의 urls.py으로  
(main의 urls의 path(board/) -> board의 urls의 path(question/create/)) 방식으로 이동  
계속 이동하다 요청한 url 도착하면, path의 두번쨰 인자로 들어가는 함수 작동(views.py에 있는)  
해당 함수 실행하고 리턴을 render로 해서 결과 전달  

render는 html을 클라이언트에게 돌려줌  
리턴 예시를 들면  
return render(request, 'news/top10.html', {'data1':data1, 'data2':data2})  
request로 news/top10.html 템플릿 파일에 data1, data2 결합해서 클라이언트에게 반환 해줌  

템플릿들은 templetes 폴더에 들어있음   

------------
#각 폴더 역할  
assetmanagement : 자산관리 탭  
backtesting : 백테스팅 탭  
board : 게시판  
news : 실시간 뉴스 크롤링 부분  
portfolio : 포트폴리오 등록 탭  
QuentEZ_main : 메인 APP  
templates : html들 들어있음  

------------
#주요 import  
backtrader : 백테스팅 툴  
beautifulsoup : 크롤링 툴  
plotly : 그래프 작성용  
pandas : 데이터 분석, 조작  
yfinance : 주식 데이터 가져오기  

------------
자산관리(assetmanagement 폴더) - 제목과 4가지(주식, 펀드, etf, 기타) 4가지를 입력 받을 수 있게 되어 있음. 다른 사람이 확인 할 수 없게 로그인한 아이디가 작성했던 자산관리 내용만 출력되도록 index에 필터로 설정 되어있다. 또한 index에 데코레이터@를 삽입하여 로그인이 안 되어 있으면 자산입력창에 접근을 못하게 하였다.  
또한 views.py에서 생성, 수정 등이 함수(asset_modify, asset_delete)로 작성 되어있는데, 역시 로그인 되어있는 사람만 접근 가능하도록 데코레이터@를 삽입하였다.  
자산리스트는 여러개를 둘 수 있으며, 생성일과 수정일을 확인 가능하게 하였다.  

백테스팅(backtesting폴더) - 백테스팅에는 5가지의 전략을 선택할 수 있게 하였고, 각 전략마다 티커, 시작일 등 설정값을 입력하여 결과를 4가지의 그래프로 보여주는 방식이다.  
백테스팅은 위와 다르게 비회원이라도 사용 가능하도록 작성 되어있다. 필요하면 데코레이터 넣으면 회원만 사용 가능하게 변경 가능하다.  
백테스팅 부분은 각 해당하는 전략 이름의 ~.html에서 입력값을 받아서, 연산 결과를 ~plots.html에 출력 되는 방식으로 이루어진다.  
plots.py에서 실제 계산과 그래프 생성이 되는데, get_plots는 사용자 입력값을 받아오고 yfinance로 해당하는 ticker에 데이터를 받아온다.  
각 전략들은 get_plots 내부에 클래스로 들어가 있고, 아래쪽에서 각 전략을 추가하여 backtrader에서 계산을 하게 된다.  
make_plots는 그래프 만들어주는 부분이고, 4개의 그래프가 각각 해당하는 templates의 backtesting 폴더의 ~plots.html에 리턴된다.  
위 폴더에서 views.py는 각 전략별로 yfinanace의 is_valid_ticker확인하여 통과되면 get_plots를 동작시킨다.  
yfinance.py는 입력한 ticker를 확인하여 실제 있는지 여부만 파악하여 준다.  

~.html -> views -> get_plots -> make_plots -> views -> ~plots.html 정도의 과정이 될 것이다.  

백테스팅 ticker가 맞게 입력했는데, 처리가 안되는 상태라 수정 중에 있다.  
현재 작동 안됨. 전체적으로 수정 중  

게시판(board 폴더) - 모델은 질문/답변 2개이고 각각 작성자, 제목, 내용, 생성일, 수정일 이 정도의 내용이 들어간다. 답변은 질문과 외래키로 되어있다.  
각 수정이나 삭제는 해당하는 고유 id와 연결되어 수정/삭제 일어난다. (urls.py의 ```<int:question_id>```처럼)  
여기는 게시판 읽기는 누구나 가능해야 하기에, 데코레이터를 전체 적용한게 아니라 작성, 수정, 답변 등에만 적용하였다.  
views.py의 index는 데이터베이스에 저장된 글들을 보여주는데, 내림차순 정렬을 해서 question_list에 이것을 가지고 다시 paginator를 사용해 1 페이지당 10개씩 출력이 된다.  
마지막으로 render를 이용해 html과 같이 출력된다.  
detail은 get_object_or_404를 이용해 실패할 경우 404 에러 메세지를 출력하며, 성공하면 context로 묶어서 내용, 작성자 등을 보여주게 된다.  
나머지도 질문/답변 수정, 삭제는 로그인한 사람과 작성자가 일치한지 if로 확인 후, 불일치하면 messages.error로 에러메세지, 일치하면 다음 작업이 가능하게 나눠진다.  

로그인/로그아웃(common 폴더) - django에서 제공하는 기본 폼을 사용해서 데이터베이스 부분인 models.py는 사용을 안하게 된다.  
이름, 비밀번호 2번, 이메일 총 3개의 정보를 받아서 데이터베이스에 저장한다.  
urls.py를 보면 로그인, 로그아웃, 회원가입, 회원탈퇴, 수정, 비밀번호 변경이 있는 것을 볼 수 있다.  
views.py에서는 각 기능들이 나오는데, signup부터 보면 받은 가입 정보가 적절한지 확인하고(is_valid) 저장, 이어서 로그인까지 된 다음 메인화면으로 보내주게 된다.  
update에서 부터 나머지는 비슷한 구성으로 되어있다.  
비밀번호는 해시값으로 저장 되는 방식으로, django의 update_session_auth_hash를 사용하였다.  

뉴스(news 폴더) - 이 부분은 네이버 금융 사이트에서 뉴스를 크롤링 해서 가져오는 부분이다. 네이버 금융의 주요뉴스나 거래상위 종목등을 가져오게 된다.  
beautifulsoup를 이용하여 크롤링을 하고, 각각의 정보들은 서로 다른 html에 나오게 되어있다.  

포트폴리오(portfolio 폴더) - 게시판 구성이랑 거의 동일하다.  

메인(QuantEZ_main 폴더) - 여기서 각 앱들을 관리  

------------
231107  
- ticker 확인하는 is_valid_ticker 오류 발생, stock.info가 문제인데 yfinance에서 변경이 된거라 방법이 없음     
-> 일단 ticker 유효 판단 안하고 바로 백테스트 하게 변경  
- 자산입력에서 asset_modify 오류 찾아서 수정, 수정 후 기존값 변경에서 이상이 있었음. 나머지 삭제 등의 기능은 이상 없음  
- 백테스팅 작동 과정 일부 변경 - DB 수정, 사용자 입력값 받아서 처리하는 과정 일부 수정, atr, GC는 정상작동, 나머지 3개 작업 중
- 추가로 벡테스트 페이지 제작 시도 예정
- ------------
231116  
- 게시판, 포트폴리오 등 다 json 리턴 되게 변경  
- 회원가입은 아직 오류나서, 이전에 가입했던 아이디로 로그인 해서 사용해야함  
- 백테스팅은 그대로 유지해둠