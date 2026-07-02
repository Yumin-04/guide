# VS Code에서 Docker 사용하는 방법

## 1. Docker 설치

Docker Desktop(Windows/Mac) 또는 Docker Engine(Linux)을 설치한 후 아래
명령으로 확인합니다.

``` bash
docker --version
docker ps
```

------------------------------------------------------------------------

## 2. VS Code Docker 확장 설치

-   Extensions(`Ctrl+Shift+X`)에서 **Docker**(Microsoft) 설치
-   좌측 사이드바에 🐳 Docker 아이콘 생성
-   Images, Containers, Volumes, Networks 등을 GUI로 관리 가능

------------------------------------------------------------------------

## 3. 프로젝트 열기

예시 구조

``` text
myproject/
├── app.py
├── requirements.txt
└── Dockerfile
```

------------------------------------------------------------------------

## 4. Dockerfile 작성

### Python 예시

``` dockerfile
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### Node.js 예시

``` dockerfile
FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "start"]
```

------------------------------------------------------------------------

## 5. 이미지 빌드

``` bash
docker build -t myapp .
```

-   `docker build` : 이미지 생성
-   `-t myapp` : 이미지 이름 지정
-   `.` : 현재 디렉터리 사용

------------------------------------------------------------------------

## 6. 이미지 확인

``` bash
docker images
```

------------------------------------------------------------------------

## 7. 컨테이너 실행

``` bash
docker run myapp
```

포트 연결이 필요한 경우

``` bash
docker run -p 5000:5000 myapp
```

브라우저에서 `http://localhost:5000`으로 접속합니다.

------------------------------------------------------------------------

## 8. VS Code GUI에서 실행

Docker 아이콘 → **Images** → 이미지 우클릭 → **Run** 또는 **Run
Interactive**

------------------------------------------------------------------------

## 9. 컨테이너 관리

``` bash
docker ps
docker stop <컨테이너ID>
docker rm <컨테이너ID>
```

------------------------------------------------------------------------

## 10. 컨테이너 내부 접속

GUI: **Containers → 우클릭 → Attach Visual Studio Code** 또는 **Attach
Shell**

CLI:

``` bash
docker exec -it <컨테이너ID> bash
```

------------------------------------------------------------------------

## 11. Docker Compose

`compose.yaml`

``` yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
```

실행

``` bash
docker compose up
```

백그라운드 실행

``` bash
docker compose up -d
```

종료

``` bash
docker compose down
```

------------------------------------------------------------------------

## 12. 자주 사용하는 명령어

  명령어                      설명
  --------------------------- --------------------
  `docker build -t myapp .`   이미지 생성
  `docker images`             이미지 목록
  `docker run myapp`          컨테이너 실행
  `docker ps`                 실행 중인 컨테이너
  `docker ps -a`              전체 컨테이너
  `docker stop ID`            컨테이너 중지
  `docker rm ID`              컨테이너 삭제
  `docker rmi IMAGE`          이미지 삭제
  `docker logs ID`            로그 확인
  `docker exec -it ID bash`   컨테이너 내부 접속
  `docker compose up -d`      Compose 실행
  `docker compose down`       Compose 종료

------------------------------------------------------------------------

## 실무에서 많이 사용하는 방식

실무에서는 단순히 `docker build`와 `docker run`만 사용하는 것보다 **Dev
Containers** 기능을 많이 사용합니다.

장점 - 동일한 개발 환경 제공 - VS Code가 컨테이너 내부에 직접 연결 -
팀원 간 환경 차이 최소화 - Python, Node.js, Java 등 다양한 프로젝트에서
활용
