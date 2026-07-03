# VS Code에서 Docker 사용하기

## 1. Docker Desktop 실행

1. Docker Desktop을 실행한다.
2. 상태가 **Engine running**인지 확인한다.
3. VS Code를 실행한다.

> Docker Desktop이 실행 중이어야 VS Code에서 Docker를 사용할 수 있다.

---

## 2. Docker Extension 설치

1. VS Code 좌측 메뉴에서 **Extensions(Ctrl + Shift + X)** 클릭
2. `Docker` 검색
3. Microsoft에서 제공하는 **Docker** Extension 설치

설치 후 좌측 Activity Bar에 Docker 아이콘이 생성된다.

---

## 3. Docker 연결 확인

VS Code 터미널(Ctrl + `)을 열고 다음 명령어를 입력한다.

```bash
docker --version
```

예시 출력

```text
Docker version 29.6.1, build 8900f1d
```

Docker가 정상적으로 설치되어 있음을 의미한다.

현재 실행 중인 컨테이너 확인

```bash
docker ps
```

예시 출력

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS   PORTS   NAMES
```

실행 중인 컨테이너가 없다면 헤더만 출력된다.

모든 컨테이너 확인

```bash
docker ps -a
```

이미지 목록 확인

```bash
docker images
```

예시 출력

```text
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
myapp        latest    9f2d8c5b1b2f   2 minutes ago  180MB
```

---

## 4. 프로젝트 열기

VS Code에서 Docker를 사용할 프로젝트를 연다.

```
File
→ Open Folder
```

또는

```bash
code .
```

명령어를 이용하여 현재 폴더를 연다.

---

## 5. Dockerfile 작성

프로젝트 루트에 `Dockerfile`을 생성한다.

예시(Python)

```dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

---

## 6. Docker 이미지 생성

터미널에서

```bash
docker build -t myapp .
```

예시 출력

```text
[+] Building 12.3s (8/8) FINISHED
 => exporting to image
 => naming to docker.io/library/myapp:latest
```

생성된 이미지 확인

```bash
docker images
```

예시 출력

```text
REPOSITORY   TAG      IMAGE ID       CREATED          SIZE
myapp        latest   9f2d8c5b1b2f   10 seconds ago   180MB
```

---

## 7. 컨테이너 실행

```bash
docker run --name mycontainer myapp
```

포트를 사용하는 경우

```bash
docker run -p 8080:8080 --name mycontainer myapp
```

옵션 설명

- `--name` : 컨테이너 이름
- `-p` : 포트 연결
- `myapp` : 실행할 이미지 이름

실행 후 확인

```bash
docker ps
```

예시 출력

```text
CONTAINER ID   IMAGE   STATUS         PORTS                  NAMES
c2fa9f4d1e8a   myapp   Up 10 seconds  0.0.0.0:8080->8080/tcp mycontainer
```

---

## 8. 실행 중인 컨테이너 확인

```bash
docker ps
```

모든 컨테이너 확인

```bash
docker ps -a
```

예시 출력

```text
CONTAINER ID   IMAGE   STATUS                     NAMES
c2fa9f4d1e8a   myapp   Up 1 minute                mycontainer
a1b2c3d4e5f6   nginx   Exited (0) 3 hours ago     web
```

---

## 9. 컨테이너 중지

```bash
docker stop mycontainer
```

예시 출력

```text
mycontainer
```

---

## 10. 컨테이너 삭제

```bash
docker rm mycontainer
```

예시 출력

```text
mycontainer
```

---

## 11. 이미지 삭제

```bash
docker rmi myapp
```

예시 출력

```text
Untagged: myapp:latest
Deleted: sha256:9f2d8c5b1b2f...
```

---

## 12. VS Code Docker Extension 활용

Docker Extension에서는 GUI 환경에서 다음 작업을 수행할 수 있다.

- Images 확인
- Containers 확인
- Container 시작 및 종료
- Container 삭제
- Image 삭제
- 로그(Log) 확인
- 터미널 접속(Attach Shell)

복잡한 명령어를 입력하지 않아도 대부분의 Docker 작업을 수행할 수 있다.

---

# 자주 사용하는 Docker 명령어

| 명령어 | 설명 |
|---------|------|
| `docker --version` | Docker 버전 확인 |
| `docker images` | 이미지 목록 조회 |
| `docker ps` | 실행 중인 컨테이너 조회 |
| `docker ps -a` | 모든 컨테이너 조회 |
| `docker build -t 이름 .` | 이미지 생성 |
| `docker run 이름` | 컨테이너 실행 |
| `docker stop 이름` | 컨테이너 중지 |
| `docker rm 이름` | 컨테이너 삭제 |
| `docker rmi 이름` | 이미지 삭제 |
| `docker logs 이름` | 컨테이너 로그 확인 |

---

# 전체 작업 순서

1. Docker Desktop 실행
2. VS Code 실행
3. Docker Extension 설치
4. 프로젝트 열기
5. Dockerfile 작성
6. `docker build`로 이미지 생성
7. `docker run`으로 컨테이너 실행
8. Docker Extension 또는 터미널에서 컨테이너 관리