# ArtNex - 제조업 AI 마케팅 자동화 SaaS 플랫폼

[![ArtNex Logo](https://via.placeholder.com/150?text=ArtNex)](https://github.com/yourusername/artnex) <!-- 로고 이미지 placeholder; 실제 로고 URL로 교체 -->

ArtNex는 제조 기업의 마케팅 프로세스를 AI로 자동화하는 SaaS 플랫폼입니다. 브랜드 관리, 시장 인사이트 분석, 디자인 및 콘텐츠 생성, 캠페인 운영, 성과 리포트를 통합 제공하여 제품 개발부터 마케팅 실행까지 효율성을 극대화합니다. MVP 버전은 기본 기능 중심으로 UI/UX를 단순화하며, 데이터 기반 의사결정을 지원합니다.

이 리포지토리는 ArtNex 프로젝트의 핵심 문서( PRD, ERD, 개발명세서, 기능명세서, WBS, 일별 스케줄)를 관리합니다. 제조업 특화 AI 마케팅 자동화 솔루션을 위한 계획 및 설계 자료로 활용하세요.

## 프로젝트 개요

- **제품명**: ArtNex
- **버전**: MVP 1.0
- **개발 기간**: 2025-10-23 ~ 2026-01-16 (총 58 영업일, 개발 49 영업일)
- **팀 구성**: 프론트엔드 3인, 백엔드 1인 (병렬 개발); WBS 기준 백엔드 중심 3인 시나리오 적용
- **목적**: 제조업 브랜드의 마케팅 ROI 향상, 시간/비용 절감, 원스톱 워크플로우 제공
- **타겟 사용자**: 제조업 마케팅 담당자, 디자이너, 경영진
- **성공 지표 (KPI)**: 사용자 유지율 70% 이상, 월간 활성 사용자 (MAU) 1,000명, AI 리포트 생성 시간 5분 이내

![PRD Overview Screenshot](https://i.imgur.com/example-prd-overview.png) <!-- 실제 스크린샷 URL로 교체; 제공된 이미지 기반 -->

## 기술 스택 (Tech Stack)

| 영역          | 기술 스택                  | 주요 목적                                                                 |
|---------------|----------------------------|---------------------------------------------------------------------------|
| Frontend     | Vue 3 + Tailwind CSS      | SPA 구조, 반응형 UI, 컴포넌트 기반 설계                                   |
| Backend      | Python (FastAPI)          | API 서버, AI 분석 모듈 연동                                              |
| DB           | PostgreSQL                | 관계형 데이터 저장 (브랜드, 캠페인, 리포트 등)                            |
| AI Engine    | GPT API, Ideogram API     | 브랜드 분석, 이미지/텍스트 생성                                          |
| Infra        | AWS EC2, S3, Lambda       | 서버·파일 스토리지·AI 연산 서버리스 처리                                 |
| Visualization| Chart.js, Recharts        | 리포트·캠페인 데이터 시각화                                              |
| Auth & Security | JWT + RBAC + HTTPS     | 사용자 인증 및 역할 기반 접근제어                                        |
| File Handling| ReportLab / Pandoc        | PDF Export, 이미지 업로드                                                |
| DevOps       | Git + Docker              | 배포 자동화 및 버전 관리                                                  |

![Tech Stack Screenshot](https://i.imgur.com/example-tech-stack.png) <!-- 실제 스크린샷 URL로 교체 -->

## 핵심 기능 (Functional Specification)

| No | 모듈 명       | 주요 화면                          | 주요 기능                                                                 | 데이터 연동/특징                  |
|----|---------------|------------------------------------|---------------------------------------------------------------------------|-----------------------------------|
| 1  | 메인 대시보드 | 인트로 배너 / 브랜드 숏컷 / 가이드 / 이용 현황 | 온보딩, 브랜드 검색/추천, 사용자 상태표시, 빠른 액션                      | 사용자/브랜드 데이터 API          |
| 2  | 브랜드 매니징 | 브랜드 리스트 / 정보 / 등록 / 프로젝트 / 계약 | 브랜드 등록·수정·삭제 / KPI 테이블 / 타깃 페르소나 / 경쟁사 비교 / 프로젝트 Kanban·List·Calendar / 계약 업로드 및 전자서명 | PostgreSQL, SNS API, 계약 PDF     |
| 3  | 브랜드 인사이트 | 프롬프트 입력 / 결과 카드 / 요약 / 커뮤니티 | AI 기반 아이템 제안·시장분석·키워드·비주얼 제안                          | GPT API, SNS 트렌드 크롤러        |
| 4  | 브랜드 리포트 | 리스트 / 데이터 입력(5단계) / 진단 / 리포트 뷰 / 출력 | 5영역 진단 (시장·경쟁사·제조·브랜드·마케팅), 점수화, AI 분석, PDF 리포트 | PostgreSQL + AI 분석 모듈         |
| 5  | 디자인 스튜디오 | 리스트 / 입력 / 결과              | 브랜드 키워드·톤앤매너 기반 AI 디자인 시안 생성, 컬러·목업 시각화        | Ideogram API, BID 리포트 연동     |
| 6  | 숏폼 스튜디오 | 리스트 / 입력 / 스토리보드        | 텍스트 기반 스크립트 입력 → 장면별 이미지·대사 자동 생성                  | 텍스트 분석 + 이미지 생성 API     |
| 7  | 콘텐츠 트래킹 | 검색 / 필터 / 결과리스트          | 키워드 기반 숏폼 콘텐츠 크롤링, 조회·좋아요·댓글 수집, 트렌드 정렬        | SNS API (YouTube, TikTok 등)      |
| 8  | 캠페인 매니저 | 요약 / 리스트 / 생성 / 차트       | 캠페인 생성(목표, 예산, 인플루언서 선택), 실시간 데이터 추적, 성과 차트  | PostgreSQL + 광고플랫폼 API       |

![Functional Spec Screenshot](https://i.imgur.com/example-functional-spec.png) <!-- 실제 스크린샷 URL로 교체 -->

## 문서 목록

이 리포지토리에는 ArtNex 개발을 위한 주요 문서가 포함되어 있습니다. 각 문서는 제조업 AI 마케팅 자동화 프로세스를 체계적으로 지원합니다.

- **[artnex_prd.md](artnex_prd.md)**: WBS (Work Breakdown Structure) - 백엔드 중심 3인 개발 시나리오. 개발 일정, 담당자, 리스크 관리 포함.
- **[artnex_prd_day.md](artnex_prd_day.md)**: 일별 스케줄 상세 내역 - 백엔드 3인 병렬 작업 기반 세부 태스크 분해.
- **ERD (Entity-Relationship Diagram)**: 데이터베이스 구조 명세 (예: Users, Brands, Campaigns 테이블). 전체 17개 테이블.
  ![ERD Screenshot](https://i.imgur.com/example-erd.png) <!-- 실제 스크린샷 URL로 교체 -->
- **개발명세서**: 시스템 아키텍처, 기술 스택 상세 (FastAPI, AWS Lambda 등).
  ![Development Spec Screenshot](https://i.imgur.com/example-dev-spec.png) <!-- 실제 스크린샷 URL로 교체 -->
- **기능명세서**: 핵심 기능 세부 사양 (대시보드부터 캠페인 리포트까지).
  ![Function Spec Screenshot](https://i.imgur.com/example-function-spec.png) <!-- 실제 스크린샷 URL로 교체 -->

문서 업데이트 필요 시 PRD 및 ERD 참조.

## 설치 및 실행 (Setup)

1. **환경 설정**:
   - Python 3.12+, Node.js 설치.
   - `pip install -r requirements.txt` (Backend).
   - `npm install` (Frontend).

2. **로컬 실행**:
   - Backend: `uvicorn main:app --reload`.
   - Frontend: `npm run dev`.
   - Database: PostgreSQL 로컬 인스턴스 생성 및 마이그레이션 적용.

자세한 지침은 개발명세서 참조.

## 기여 방법 (Contributing)

- 이슈 제출: 버그 보고 또는 기능 제안.
- Pull Request: 코드 기여 시 PRD 준수.
- 코드 스타일: PEP8 (Python), ESLint (JS).

## 라이선스 (License)

MIT License. 자세한 내용은 [LICENSE](LICENSE) 파일 참조.

## 연락처

- 개발자: [yourusername](https://github.com/yourusername)
- 이메일: example@artnex.com

ArtNex는 제조업의 AI 기반 마케팅 혁신을 목표로 합니다. 추가 질문은 이슈로 등록하세요!
