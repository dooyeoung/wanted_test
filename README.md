
# 프로젝트 기능

- 회사명 자동완성
  - 회사명의 일부만 들어가도 검색이 되어야 합니다.
- 회사 이름으로 회사 검색
- 태그명으로 회사 검색
  - 태그로 검색 관련된 회사가 검색되어야 합니다.
  - 다국어로 검색이 가능해야 합니다.
    - 일본어 태그로 검색을 해도 한국 회사가 노출이 되어야 합니다.
    - タグ_4로 검색 했을 때, 원티드랩 회사 정보가 노출이 되어야 합니다.
  - 동일한 회사는 한번만 노출이 되어야합니다.
- 회사 태그 정보 추가
- 회사 태그 정보 삭제


# 프로젝트 정보

- 코딩 컨벤션 : flake8, black
- 마이그레이션 관리 : alembic
- 코드 패키지 관리 : poetry
- 비즈니스 로직 : 레이어 분리
- 데이터베이스 : sqlite


# API 문서 생성
- redoc-cli 설치
```
npm i -g redoc-cli
```

- 문서 추출 후 렌더링
```
FLASK_APP=app.wsgi:create_wsgi_app flask openapi write --format=json docs/apispec.json

redoc-cli build docs/apispec.json -o docs/index.html
```


# 프로젝트 빌드
```
docker build --no-cache -t wanted-test .
```

# 프로젝트 실행
```
gunicorn -k gevent "run:_create_wsgi_app('prod')" -b 127.0.0.1:9999
python run.py --env prod
```