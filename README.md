# FSA_Full_Self-AR

OpenCV와 PnP 알고리즘을 활용하여 체스판 위에서 실시간 카메라 포즈 추정 및 3D 피라미드 객체를 시각화하는 증강현실(AR) 프로그램입니다.

## 1. 주요 기능 (Features)

컴퓨터 비전 기술을 이용하여 카메라의 위치와 방향을 파악하고, 가상의 3D 기하학적 객체를 현실 영상에 합성합니다.
* **Camera Pose Estimation:** `cv2.solvePnP` 알고리즘을 사용하여 3D 세계 좌표와 2D 이미지 좌표 간의 대응 관계를 분석, 카메라의 회전 및 이동 벡터를 산출합니다.
* **3D Geometric Projection:** `cv2.projectPoints`를 통해 정의된 3차원 꼭짓점들을 카메라의 내/외부 파라미터에 맞춰 2D 화면 평면으로 투영합니다.
* **Real-time Trajectory Display:** 역행렬 연산($P = -R^T \cdot t$)을 통해 세계 좌표계 기준의 카메라 실제 위치(X, Y, Z)를 실시간으로 추적하여 화면에 출력합니다.

## 2. 알고리즘 데모 및 결과 분석

### 2-1. AR 렌더링 데모

| Demo Photos |
| :---: |
| <img src="https://github.com/user-attachments/assets/09581524-4dc8-4101-a553-a8f107b33e98" width="48%"> <img src="https://github.com/user-attachments/assets/bccac03d-74a8-41a1-82db-7328725700f1" width="48%"> |


체스판의 기하학적 중심을 기준으로 설정된 영역에 파란색 밑면과 초록색 기둥을 가진 피라미드가 안정적으로 투영됩니다.

## 3. 알고리즘의 핵심 기술 및 한계점

* **Calibration 데이터 의존성:** 본 알고리즘은 HW#3에서 도출된 카메라 내부 파라미터($K$)에 의존합니다. 만약 렌즈의 초점 거리나 왜곡 계수가 실제와 다를 경우, AR 객체가 체스판에서 들뜨거나(Sliding) 휘어 보이는 현상이 발생할 수 있습니다.
* **패턴 인식의 한계:** `cv2.findChessboardCorners`는 조명이 너무 어둡거나 체스판의 일부가 가려질 경우 코너 검출에 실패합니다. 이 경우 포즈 추정이 중단되어 AR 객체가 화면에서 사라지는 한계가 있습니다.
* **Adaptive Thresholding의 활용:** `board_criteria` 설정을 통해 노이즈가 있는 환경에서도 정밀한 코너 하위 픽셀 검출을 시도하여 안정성을 높였습니다.

