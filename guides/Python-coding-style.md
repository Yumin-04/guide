# Python 코딩 스타일 가이드 (Python Coding Style Guide)

본 가이드는 가독성, 유지보수성, 그리고 안정성을 극대화하기 위해 `pathlib`, `argparse`, `typing`을 활용한 **함수 어노테이션(Function Annotation)** 작성법과 `mypy`를 통한 정적 타입 검증 절차를 정의합니다.

---

## 1. 핵심 원칙 및 요구사항

1. **모든 함수에 타입 어노테이션(Type Annotation)을 필수 적용**합니다. 특히 **반환 타입(Return Type)** 은 누락 없이 반드시 명시해야 합니다.
2. 파일 시스템 경로를 다룰 때는 레거시 `os.path` 대신 객체 지향적인 **`pathlib.Path`** 를 사용합니다.
3. 명령행 인자(CLI) 처리는 **`argparse`** 를 사용하며, 각 인자에는 `help=`, `metavar=` 를 포함하여 사용 편의성을 높입니다.
4. 작성된 코드는 정적 타입 검사 도구인 **`mypy`** 를 통해 검증을 통과해야 합니다.
5. `typing` 모듈에서 **실제로 사용하는 타입만 import** 합니다. 미사용 import는 제거합니다.

---

## 2. 주요 모듈별 스타일 규칙

### ① 함수 어노테이션 및 Typing (`typing`)

- 함수의 입력 매개변수와 반환값에 정확한 타입을 명시합니다.
- 반환값이 없는 경우에도 `-> None` 을 반드시 작성합니다.
- 복잡한 컨테이너 타입이나 여러 타입을 허용할 경우 `Union`, `Optional`, `List`, `Dict` 등을 활용합니다.
- **실제로 사용하지 않는 타입은 import하지 않습니다.** `mypy --strict` 실행 시 미사용 import 경고가 발생합니다.
- Python 3.9 이상 환경에서는 `list[str]`, `dict[str, int]` 처럼 빌트인 타입을 직접 사용할 수 있으며, 이 경우 `typing` import가 불필요합니다. 프로젝트의 Python 버전 요건에 따라 선택합니다.

### ② 파일 및 경로 처리 (`pathlib`)

- 경로 매개변수나 반환 타입에는 `str` 대신 `pathlib.Path` 타입을 지정합니다.
- `.exists()`, `.read_text()`, `.write_text()` 등 pathlib 네이티브 메서드를 적극 활용합니다.
- 예시: `def read_config(path: Path) -> dict:`

### ③ 명령행 인자 및 CLI Help (`argparse`)

- CLI 인자를 정의할 때 `type=` 속성으로 런타임 1차 검증을 수행합니다.
- `help="..."` 문구로 친절한 사용법을 제공합니다.
- `metavar=` 를 지정하여 `--help` 출력 시 인자의 역할이 명확히 표시되도록 합니다.
  - 예: `metavar="FILE"`, `metavar="KEYWORD"`
- 파일 경로를 인자로 받을 때는 `type=Path` 형태로 `pathlib` 과 연계합니다.

### ④ 예외 처리

- `except Exception` 대신 **구체적인 예외 타입**을 명시합니다.
- 파일 I/O 관련 오류는 `except (IOError, OSError)` 로 처리합니다.
- 예외 타입을 구체화하면 의도치 않은 예외를 숨기지 않아 디버깅이 용이합니다.

---

## 3. mypy 검증

코딩 완료 후 아래 명령어로 타입 어노테이션을 검증합니다.

```bash
# 패키지 설치
pip install mypy

# 기본 검증
python -m mypy my_script.py

# 엄격 모드 (권장)
python -m mypy --strict my_script.py
```

`--strict` 모드에서는 미사용 import, 누락된 어노테이션 등을 모두 검출합니다. 최종 제출 코드는 `--strict` 기준 통과를 목표로 합니다.

---

## 4. 표준 코드 템플릿

전체 템플릿 코드는 [`my_script.py`](./my_script.py) 를 참고하세요.

핵심 패턴만 요약하면 다음과 같습니다.

```python
# ① 반환 타입 필수 명시
def process_file_data(input_path: Path, keywords: List[str]) -> Dict[str, int]:
    ...

# ② metavar로 --help 출력 개선
parser.add_argument("-i", "--input", type=Path, metavar="FILE", required=True, help="...")

# ③ 구체적 예외 타입 지정
except (IOError, OSError) as e:
    print(f"Error reading file: {e}")
```

---

## 5. 개선사항 체크리스트

코드 작성 후 아래 항목을 순서대로 확인합니다.

| 항목 | 확인 내용 |
|------|-----------|
| 타입 어노테이션 | 모든 함수의 매개변수 및 반환 타입 명시 여부 |
| `-> None` | 반환값 없는 함수에도 `-> None` 작성 여부 |
| `typing` import | 실제 사용하는 타입만 import했는지 여부 |
| `pathlib` 사용 | 경로 처리 시 `os.path` 대신 `Path` 사용 여부 |
| CLI `help=` | 모든 argparse 인자에 `help=` 문구 작성 여부 |
| CLI `metavar=` | 인자 역할이 드러나는 `metavar=` 지정 여부 |
| 예외 타입 | `except Exception` 대신 구체적 예외 타입 사용 여부 |
| mypy 통과 | `python -m mypy --strict my_script.py` 오류 없음 여부 |
