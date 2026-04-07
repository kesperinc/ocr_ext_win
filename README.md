# OCR Extraction - `ocr_ext`

본 프로젝트는 고문헌 및 다량의 PDF 문서(2,600개 이상)를 GPU 가속을 활용하여 OCR 추출(Docling 중심)하는 워크플로우를 담고 있습니다.  
기존 리눅스(또는 WSL)에서 진행하던 작업을 윈도우 기반으로 이관하기 위해 필수 소스 코드와 PyTorch/CUDA(sm_61 호환) 설정 내용을 정리했습니다.

## 핵심 내용 및 진행 상황
- **메인 로직 (`yukim_pdf_ocr.py`)**: `docling`을 이용한 PDF OCR 및 마크다운 추출.
- **모니터링 (`monitor_ocr.py`, `ocr_watchdog.py`)**: 다량의 문서 처리 시 메모리 누수 또는 좀비 프로세스를 관리하고 자동 재시작.
- **GPU 최적화**: GTX 1080 (sm_61, Pascal 아키텍처) 환경에 최적화된 PyTorch 설정.

---

## 🚀 PyTorch & CUDA 필수 설정 가이드 (윈도우/리눅스 공통)

현재 환경(GTX 1080 등 Pascal GPU)에서 `sm_61` 호환성 오류(`no kernel image is available for execution`)를 피하기 위해서는 **CUDA 11.8** 기반의 PyTorch를 사용해야 합니다.

### 1단계: 가상환경 생성 (uv 또는 venv)
```bash
# uv 사용 시
uv venv .venv
# 또는 venv 사용 시
python -m venv .venv
```

### 2단계: PyTorch v2.4.1 + cu118 설치
**주의**: 기본 `pip install torch`는 최신 CUDA 버전을 설치하므로, 아래와 같이 특정 인덱스 URL을 사용해야 합니다.

```bash
pip install torch==2.4.1+cu118 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

### 3단계: 기타 라이브러리 설치
`requirements.txt`에 명시된 의존성을 설치합니다. `docling`, `transformers` 등이 포함되어 있습니다.

```bash
pip install -r requirements.txt
```

---

## 🛠️ 주요 스크립트 설명
- `yukim_pdf_ocr.py`: PDF 문서를 Docling으로 컨버팅하는 메인 워커.
- `monitor_ocr.py`: 실행 중인 OCR 프로세스의 상태(CPU, GPU 사용량)를 실시간 모니터링.
- `ocr_watchdog.py`: 프로세스가 멈추거나 죽었을 때 자동으로 감시하여 재실행.
- `diag_torch.py`: 현재 환경의 PyTorch가 GPU(CUDA)를 제대로 인식하는지 확인.

## 💾 작업 폴더 및 커밋
현재 진행 중인 2,624개 문서의 배치를 그대로 이관하여 작업 폴더를 변경한 후 재시행할 예정입니다.
