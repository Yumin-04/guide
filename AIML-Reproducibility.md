# AI/ML Reproducibility Guide

## 목적

AI/ML 프로젝트는 동일한 데이터와 코드를 사용하더라도 실행 환경, 하드웨어 아키텍처, 실행 시점, 병렬 처리 방식, 라이브러리 버전 등에 따라 결과가 달라질 수 있습니다.

본 문서는 실험의 **재현성(Reproducibility)**과 **일관성(Consistency)**을 확보하기 위해 개발 과정에서 반드시 준수해야 할 표준 엔지니어링 규칙을 정의합니다.

---

## 1. 전역 난수 시드(Random Seed) 고정

### 목적

난수 생성 과정에서 발생하는 비결정성을 제거하여 동일한 입력에 대해 항상 동일한 결과를 얻기 위함입니다.

### 권장

Python 소스코드 전반에서 사용되는 모든 프레임워크의 난수 시드를 동일한 값으로 초기화합니다.

```python
import random
import numpy as np
import torch
import tensorflow as tf

SEED = 42

# Base Python & NumPy
random.seed(SEED)
np.random.seed(SEED)

# PyTorch
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)  # Multi-GPU 환경 대응

# TensorFlow
tf.random.set_seed(SEED)
```

---

## 2. `set` 및 `dict` 사용 후 정렬

### 목적

Python의 `set`과 `dict`는 내부 저장 순서가 보장되지 않습니다. 동일한 데이터라도 실행 환경에 따라 순서가 달라질 수 있으므로, 순서가 중요한 데이터는 반드시 정렬하여 사용합니다.

### 권장하지 않음

```python
classes = list(set(labels))
```

### 권장

```python
classes = sorted(set(labels))

# 또는
classes = sorted(list(set(labels)))
```

---

## 3. 부동소수점 비교 시 허용 오차(EPSILON) 반영

### 목적

컴퓨터의 부동소수점 연산은 미세한 오차를 포함합니다. 임계값(Threshold) 비교 시 실행 환경에 따라 결과가 달라질 수 있으므로 허용 오차를 명시적으로 적용합니다.

### 권장하지 않음

```python
valid_samples = df[df["score"] >= 0.6]
```

### 권장

```python
EPSILON = 1e-7

valid_samples = df[df["score"] >= (0.6 - EPSILON)]
```

---

## 4. Feature Selection 공동 순위(Tie) 처리

### 목적

Feature Importance가 동일한 경우 정렬 알고리즘의 특성에 따라 선택되는 Feature가 달라질 수 있습니다. 공동 순위 발생 시 서브 정렬 기준을 명시적으로 정의합니다.

### 권장

```python
importance.sort_values(
    by=["importance", "feature"],
    ascending=[False, True]
)
```

위 예시는 Importance 내림차순으로 정렬하고, Importance가 동일한 경우 Feature 이름을 오름차순으로 정렬합니다.

---

## 5. 기준 시간(Reference Date) 고정

### 목적

실행 시점의 시스템 시간에 의존하는 Feature는 매 실행마다 값이 달라질 수 있습니다. 실행 시점과 관계없이 동일한 Feature를 생성하기 위해 기준 날짜를 고정합니다.

### 권장하지 않음

```python
from datetime import datetime

df["elapsed_days"] = (
    datetime.now() - df["base_date"]
).dt.days
```

### 권장

```python
import pandas as pd

REFERENCE_DATE = pd.to_datetime("2026-06-26")

df["elapsed_days"] = (
    REFERENCE_DATE - df["base_date"]
).dt.days
```

---

## 6. 가변 기본 인자(Mutable Default Argument) 사용 금지

### 목적

함수의 기본 인자로 `list`, `dict` 등의 가변 객체를 사용하면 함수 호출 간 데이터가 공유되어 독립적인 실험이 보장되지 않습니다.

### 권장하지 않음

```python
def preprocess_pipeline(new_data, all_data=[]):
    all_data.append(new_data)
    return all_data
```

### 권장

```python
def preprocess_pipeline(new_data, all_data=None):
    if all_data is None:
        all_data = []

    all_data.append(new_data)
    return all_data
```

---

## 7. DataFrame 인덱스 초기화

### 목적

Filtering, Merge, Concat, Drop, Drop Duplicates 등으로 DataFrame의 행 구조가 변경되면 기존 인덱스가 유지됩니다. 후속 처리에서 인덱스 기반 오류를 방지하기 위해 인덱스를 초기화합니다.

### 권장

```python
df = df.reset_index(drop=True)
```

적용 대상

- Filtering
- Merge
- Concat
- Drop
- Drop Duplicates

---

## 8. 멀티스레딩 및 병렬 연산 통제

### 목적

병렬 연산은 스레드 실행 순서에 따라 미세한 수치 차이를 유발할 수 있습니다. 완전한 재현성이 필요한 실험에서는 단일 스레드 실행을 권장합니다.

### Scikit-learn

```python
RandomForestClassifier(
    random_state=42,
    n_jobs=1
)
```

### LightGBM

```python
num_threads = 1
```

### XGBoost

```python
nthread = 1
```

---

## 9. Deterministic GPU 연산

### 목적

CUDA 및 cuDNN은 성능 최적화를 위해 내부적으로 비결정론적 알고리즘을 선택할 수 있습니다. 동일한 입력에 대해 항상 동일한 결과를 얻기 위해 결정론적 연산을 활성화합니다.

### 권장

```python
import torch

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
```

필요한 경우

```python
torch.use_deterministic_algorithms(True)
```

를 추가로 적용할 수 있습니다.

> **참고**
>
> `torch.use_deterministic_algorithms(True)`를 활성화하면 일부 연산에서 오류가 발생하거나 실행 속도가 저하될 수 있습니다.

---

## 10. OS 독립적인 파일 경로 작성

### 목적

운영체제(Windows, Linux, macOS)마다 파일 경로 구분자가 다르므로 문자열 연결 대신 표준 라이브러리를 사용합니다.

### 권장하지 않음

```python
path = "data/train.csv"

# 또는

path = "data\\train.csv"
```

### 권장 (`pathlib`)

```python
from pathlib import Path

DATA_DIR = Path("data")
TRAIN_PATH = DATA_DIR / "train.csv"
```

### 권장 (`os.path`)

```python
import os

TRAIN_PATH = os.path.join("data", "train.csv")
```

---

## 11. 라이브러리 버전 고정

### 목적

동일한 코드라도 라이브러리 버전이 달라지면 알고리즘 구현, 기본 파라미터, 내부 연산 방식이 변경되어 결과가 달라질 수 있습니다.

실험에 사용한 라이브러리 버전을 명시적으로 고정합니다.

### 권장

`requirements.txt`

```text
numpy==2.1.0
pandas==2.2.3
scikit-learn==1.6.1
torch==2.7.0
tensorflow==2.19.0
```

또는 `environment.yml`, `poetry.lock` 등을 활용하여 실행 환경 전체를 관리하는 것을 권장합니다.

---

## 실험 전 재현성 체크리스트

실험 수행 또는 코드 배포 전에 아래 항목을 확인합니다.

- [ ] Random Seed 설정
- [ ] `set()` 및 `dict` 사용 후 정렬
- [ ] 부동소수점 비교 시 `EPSILON` 적용
- [ ] Feature Selection 공동 순위 처리 규칙 정의
- [ ] `REFERENCE_DATE` 사용
- [ ] Mutable Default Argument 사용 금지
- [ ] DataFrame Index 초기화
- [ ] 병렬 스레드(`n_jobs`, `num_threads`) 제한
- [ ] Deterministic GPU 연산 적용
- [ ] OS 독립적인 파일 경로 사용
- [ ] 라이브러리 버전 고정

---

## 참고

본 문서의 규칙은 AI/ML 프로젝트에서 **재현성을 확보하기 위한 최소 권장 사항**입니다.

Random Seed를 고정하는 것만으로는 재현성이 완전히 보장되지 않습니다. 데이터 처리 순서, 병렬 처리 방식, GPU 연산, 실행 환경, 라이브러리 버전 등 다양한 요소를 함께 관리해야 동일한 실험 결과를 재현할 수 있습니다.

프로젝트의 특성에 따라 추가적인 재현성 관리 방안을 적용할 수 있으며, 본 문서는 모든 AI/ML 프로젝트에서 기본적으로 준수해야 할 가이드라인으로 활용하는 것을 권장합니다.