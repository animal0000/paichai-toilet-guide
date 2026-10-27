import os
import sys

sys.path.append('D:/Antigravity/workspace/paichai_toilet_guide/assets')
from images_b64 import AERIAL_B64, VIEW_B64, AERIAL_NEON_B64, POSTER_B64

html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>2026 배양전 학생 화장실 이용 안내 | 효창운동장</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --pc-navy: #1A2F8A;
      --pc-navy-dark: #0F1D59;
      --pc-red: #C0392B;
      --pc-red-light: #E74C3C;
      --pc-gold: #F39C12;
      --pc-gold-light: #F1C40F;
      --pc-blue: #1E90FF;
      --pc-green: #27AE60;
      --bg-dark: #0A0F1D;
      --card-bg: #131B2E;
      --card-border: #1E2D4A;
      --text-main: #FFFFFF;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 60px;
    }}

    .container {{
      max-width: 960px;
      margin: 0 auto;
      padding: 16px;
    }}

    /* Header Banner */
    .header {{
      background: linear-gradient(135deg, var(--pc-navy-dark) 0%, var(--pc-navy) 60%, #203A9E 100%);
      border-radius: 20px;
      padding: 24px 20px;
      text-align: center;
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(26, 47, 138, 0.4);
      border: 1px solid rgba(243, 156, 18, 0.3);
      margin-bottom: 20px;
    }}

    .header::before {{
      content: '';
      position: absolute;
      top: -50%;
      right: -20%;
      width: 280px;
      height: 280px;
      background: radial-gradient(circle, rgba(192, 57, 43, 0.25) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--pc-red);
      color: white;
      font-size: 13px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
      box-shadow: 0 4px 12px rgba(192, 57, 43, 0.4);
    }}

    .header h1 {{
      font-size: 26px;
      font-weight: 900;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
      line-height: 1.3;
    }}

    .header .subtitle {{
      color: #CBD5E1;
      font-size: 14px;
      font-weight: 500;
    }}

    .header .org {{
      margin-top: 10px;
      font-size: 12px;
      color: var(--pc-gold-light);
      font-weight: 600;
      letter-spacing: 0.5px;
    }}

    /* Section Header */
    .section-title {{
      font-size: 18px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 24px 0 14px 0;
      color: white;
    }}

    .section-title::before {{
      content: '';
      display: inline-block;
      width: 4px;
      height: 18px;
      background: var(--pc-red);
      border-radius: 2px;
    }}

    /* Motion Graphic Video Showcase (Top Placement) */
    .video-section {{
      background: linear-gradient(180deg, #10192E 0%, #0A0F1D 100%);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 20px;
      margin-bottom: 24px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }}

    .video-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .video-badge {{
      background: rgba(30, 144, 255, 0.2);
      color: var(--pc-blue);
      border: 1px solid var(--pc-blue);
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
    }}

    .video-player-box {{
      position: relative;
      border-radius: 14px;
      overflow: hidden;
      background: #000;
      aspect-ratio: 16 / 9;
      border: 1px solid rgba(255, 255, 255, 0.1);
      margin-bottom: 14px;
    }}

    .video-player-box video {{
      width: 100%;
      height: 100%;
      object-fit: contain;
    }}

    .dl-btn-group {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}

    @media (max-width: 500px) {{
      .dl-btn-group {{
        grid-template-columns: 1fr;
      }}
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 18px;
      border-radius: 10px;
      font-size: 14px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
      font-family: inherit;
    }}

    .btn-primary {{
      background: var(--pc-navy);
      color: white;
      border: 1px solid rgba(243, 156, 18, 0.4);
    }}

    .btn-primary:hover {{
      background: #233FA8;
      box-shadow: 0 4px 14px rgba(26, 47, 138, 0.5);
    }}

    .btn-red {{
      background: var(--pc-red);
      color: white;
    }}

    .btn-red:hover {{
      background: #D94436;
      box-shadow: 0 4px 14px rgba(192, 57, 43, 0.5);
    }}

    /* Image Display Section */
    .tab-bar {{
      display: flex;
      background: var(--card-bg);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      margin-bottom: 14px;
      gap: 4px;
    }}

    .tab-btn {{
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 10px 14px;
      font-size: 14px;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
      font-family: inherit;
    }}

    .tab-btn.active {{
      background: var(--pc-navy);
      color: white;
      box-shadow: 0 4px 12px rgba(26, 47, 138, 0.4);
      border: 1px solid rgba(243, 156, 18, 0.3);
    }}

    .view-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      overflow: hidden;
      margin-bottom: 24px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }}

    .image-wrapper {{
      position: relative;
      width: 100%;
      background: #000;
      cursor: pointer;
    }}

    .image-wrapper img {{
      width: 100%;
      height: auto;
      display: block;
      transition: transform 0.3s;
    }}

    .image-wrapper:hover img {{
      transform: scale(1.01);
    }}

    .zoom-hint {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(4px);
      color: white;
      font-size: 11px;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      gap: 5px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      pointer-events: none;
    }}

    .view-caption {{
      padding: 16px;
      background: #0D1424;
      border-top: 1px solid var(--card-border);
    }}

    .caption-title {{
      font-size: 15px;
      font-weight: 800;
      color: var(--pc-gold);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .caption-text {{
      font-size: 13px;
      color: #CBD5E1;
      line-height: 1.5;
    }}

    /* Dual Grid (Side-by-Side: Default View) */
    .dual-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 24px;
    }}

    @media (max-width: 768px) {{
      .dual-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    /* 3-Pillar Summary Cards */
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }}

    @media (max-width: 640px) {{
      .summary-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .summary-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s, border-color 0.2s;
    }}

    .summary-card:hover {{
      transform: translateY(-2px);
      border-color: var(--pc-gold);
    }}

    .summary-card.primary {{
      border-color: rgba(30, 144, 255, 0.6);
      background: linear-gradient(180deg, rgba(30, 144, 255, 0.15) 0%, var(--card-bg) 100%);
    }}

    .summary-card.highlight {{
      border-color: rgba(243, 156, 18, 0.6);
      background: linear-gradient(180deg, rgba(243, 156, 18, 0.15) 0%, var(--card-bg) 100%);
    }}

    .summary-card.accent {{
      border-color: rgba(39, 174, 96, 0.6);
      background: linear-gradient(180deg, rgba(39, 174, 96, 0.15) 0%, var(--card-bg) 100%);
    }}

    .card-label {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .summary-card.primary .card-label {{ color: var(--pc-blue); }}
    .summary-card.highlight .card-label {{ color: var(--pc-gold); }}
    .summary-card.accent .card-label {{ color: var(--pc-green); }}

    .card-value {{
      font-size: 18px;
      font-weight: 800;
      color: white;
      line-height: 1.3;
    }}

    .card-desc {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    /* 4-Step Timeline */
    .timeline {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px 16px;
      margin-bottom: 24px;
    }}

    .timeline-item {{
      display: flex;
      gap: 14px;
      position: relative;
      padding-bottom: 22px;
    }}

    .timeline-item:last-child {{
      padding-bottom: 0;
    }}

    .timeline-item::before {{
      content: '';
      position: absolute;
      top: 32px;
      left: 17px;
      bottom: 0;
      width: 2px;
      background: var(--card-border);
    }}

    .timeline-item:last-child::before {{
      display: none;
    }}

    .step-num {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--pc-navy);
      border: 2px solid var(--pc-gold);
      color: white;
      font-size: 14px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      z-index: 1;
    }}

    .timeline-item.active .step-num {{
      background: var(--pc-blue);
      border-color: white;
      box-shadow: 0 0 12px rgba(30, 144, 255, 0.6);
    }}

    .step-content {{
      flex: 1;
      padding-top: 4px;
    }}

    .step-title {{
      font-size: 15px;
      font-weight: 800;
      color: white;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .step-tag {{
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
      background: rgba(243, 156, 18, 0.2);
      color: var(--pc-gold);
    }}

    .step-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    .step-desc strong {{
      color: #F1F5F9;
    }}

    /* Alert Box */
    .alert-box {{
      background: rgba(192, 57, 43, 0.1);
      border: 1px solid rgba(192, 57, 43, 0.4);
      border-radius: 14px;
      padding: 16px;
      margin-bottom: 24px;
    }}

    .alert-title {{
      font-size: 14px;
      font-weight: 800;
      color: var(--pc-red-light);
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 8px;
    }}

    .alert-list {{
      list-style: none;
      font-size: 13px;
      color: #CBD5E1;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .alert-list li {{
      padding-left: 18px;
      position: relative;
    }}

    .alert-list li::before {{
      content: '•';
      position: absolute;
      left: 6px;
      color: var(--pc-gold);
    }}

    /* Footer */
    .footer {{
      text-align: center;
      padding-top: 20px;
      border-top: 1px solid var(--card-border);
      color: var(--text-dim);
      font-size: 12px;
    }}

    .footer strong {{
      color: var(--pc-gold);
    }}

    /* Modal */
    .modal {{
      display: none;
      position: fixed;
      z-index: 999;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.92);
      align-items: center;
      justify-content: center;
      padding: 16px;
      backdrop-filter: blur(8px);
    }}

    .modal.show {{
      display: flex;
    }}

    .modal-content {{
      max-width: 95vw;
      max-height: 90vh;
      object-fit: contain;
      border-radius: 10px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    .modal-close {{
      position: absolute;
      top: 20px;
      right: 20px;
      width: 44px;
      height: 44px;
      background: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      font-size: 24px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    @media print {{
      body {{
        background: white !important;
        color: black !important;
        padding-bottom: 0;
      }}
      .header {{
        background: #1A2F8A !important;
        color: white !important;
        box-shadow: none !important;
        border: none !important;
        page-break-inside: avoid;
      }}
      .summary-card, .view-card, .timeline, .video-section, .alert-box {{
        background: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        box-shadow: none !important;
        page-break-inside: avoid;
      }}
      .card-value, .step-title, .section-title {{
        color: black !important;
      }}
      .tab-bar, .video-section, .modal, .zoom-hint {{
        display: none !important;
      }}
      .view-card {{
        display: block !important;
      }}
    }}
  </style>
</head>
<body>

  <div class="container">

    <!-- 1. Header Banner -->
    <header class="header">
      <div class="badge">🔥 2026 배양전 (효창운동장)</div>
      <h1>학생 화장실 이용 동선 안내</h1>
      <p class="subtitle">배재 학생 전용 지정 화장실 위치 및 안전 이동 경로 안내</p>
      <div class="org">PAICHAI MIDDLE SCHOOL & PAICHAI HIGH SCHOOL</div>
    </header>

    <!-- 2. [최상단 배치 1] 동선 안내 모션그래픽 비디오 (MP4) -->
    <div class="section-title">동선 안내 모션그래픽 비디오 (MP4)</div>
    <div class="video-section">
      <div class="video-header">
        <div>
          <span class="video-badge">HD 1080p 공식 모션그래픽</span>
          <h3 style="font-size: 16px; font-weight: 800; margin-top: 4px;">18초 동선 안내 애니메이션 영상</h3>
        </div>
        <span style="font-size: 12px; color: var(--text-muted);">카카오톡 / 전광판 공유 최적화</span>
      </div>

      <div class="video-player-box">
        <video controls playsinline preload="metadata" poster="data:image/jpeg;base64,{POSTER_B64}">
          <source src="paichai_toilet_guide.mp4" type="video/mp4">
          브라우저가 비디오 재생을 지원하지 않습니다. 아래 다운로드 버튼을 이용하세요.
        </video>
      </div>

      <div class="dl-btn-group" style="grid-template-columns: 1fr 1fr 1fr;">
        <a class="btn btn-primary" href="motion_graphic.html" target="_blank" style="background: linear-gradient(135deg, #1A2F8A, #1E90FF); border-color: #FFE600;">
          ⚡ 웹 모션 플레이어 (실시간 무빙)
        </a>
        <a class="btn btn-primary" href="paichai_toilet_guide.mp4" download="배양전_화장실안내_가로형.mp4">
          📥 가로형 비디오 (16:9 PC/전광판)
        </a>
        <a class="btn btn-red" href="paichai_toilet_guide_mobile.mp4" download="배양전_화장실안내_모바일.mp4">
          📱 세로형 비디오 (9:16 모바일)
        </a>
      </div>
    </div>

    <!-- 3. [최상단 배치 2] 시각 동선 가이드 (기본: 두 화면 나란히 보기) -->
    <div class="section-title">시각 동선 가이드 (조감도 & 현장 실사)</div>

    <!-- Tab Bar: [두 화면 나란히 보기]가 첫 번째이자 기본 active -->
    <div class="tab-bar">
      <button class="tab-btn active" id="tabBtn3" onclick="switchTab(3)">
        🔄 두 화면 나란히 보기 (기본)
      </button>
      <button class="tab-btn" id="tabBtn1" onclick="switchTab(1)">
        🗺️ 항공뷰 크게 보기 (고시인성 동선)
      </button>
      <button class="tab-btn" id="tabBtn2" onclick="switchTab(2)">
        👀 객석 실사 크게 보기 (파란 박스)
      </button>
    </div>

    <!-- View 3: Dual Grid View (기본 노출 상태: display: grid) -->
    <div class="dual-grid" id="viewCard3" style="display: grid;">
      <div class="view-card" style="margin-bottom: 0;">
        <div class="image-wrapper" onclick="openModal('imgAerialDual')">
          <img id="imgAerialDual" src="data:image/jpeg;base64,{AERIAL_NEON_B64}" alt="항공뷰 전체 동선">
          <div class="zoom-hint">🔍 탭하여 확대</div>
        </div>
        <div class="view-caption">
          <div class="caption-title">STEP 1. 관객석 상단 통로 동선 (도보 약 2~3분)</div>
          <div class="caption-text">배재 응원석(남측) ➔ 관객석 상단 통로(오른쪽·반시계 방향) ➔ 북측 B출입구</div>
        </div>
      </div>
      <div class="view-card" style="margin-bottom: 0;">
        <div class="image-wrapper" onclick="openModal('imgViewDual')">
          <img id="imgViewDual" src="data:image/jpeg;base64,{VIEW_B64}" alt="객석 정면 실사 뷰 (파란 박스 B출입구)">
          <div class="zoom-hint">🔍 탭하여 확대</div>
        </div>
        <div class="view-caption">
          <div class="caption-title">STEP 2. B출입구 실사 [파란 박스 계단]</div>
          <div class="caption-text">태양광 패널 아래 파란 박스 출입구 계단 진입 ➔ 【우측 2층】 화장실</div>
        </div>
      </div>
    </div>

    <!-- View 1: Aerial Route (초기 숨김: display: none) -->
    <div class="view-card" id="viewCard1" style="display: none;">
      <div class="image-wrapper" onclick="openModal('imgAerialSingle')">
        <img id="imgAerialSingle" src="data:image/jpeg;base64,{AERIAL_NEON_B64}" alt="효창운동장 항공뷰 이동 동선">
        <div class="zoom-hint">🔍 탭하여 확대 보기</div>
      </div>
      <div class="view-caption">
        <div class="caption-title">🗺️ 효창운동장 전체 이동 동선 (도보 약 2~3분)</div>
        <div class="caption-text">
          하단 <strong>[배재 응원석 (파란 박스)]</strong>에서 관객석 상단 통로로 올라가, 통로(녹색 화살표)를 따라 오른쪽(반시계 방향)으로 이동하면 맞은편 <strong>[B출입구 (빨간 원)]</strong>에 도착합니다. 경기장 밖으로 나가지 않습니다.
        </div>
      </div>
    </div>

    <!-- View 2: Field View (초기 숨김: display: none) -->
    <div class="view-card" id="viewCard2" style="display: none;">
      <div class="image-wrapper" onclick="openModal('imgViewSingle')">
        <img id="imgViewSingle" src="data:image/jpeg;base64,{VIEW_B64}" alt="객석에서 바라본 B출입구 화장실 입구 전경">
        <div class="zoom-hint">🔍 탭하여 확대 보기</div>
      </div>
      <div class="view-caption">
        <div class="caption-title">👀 배재 응원석에서 정면을 바라보았을 때의 실제 시야 (파란 박스 = B출입구)</div>
        <div class="caption-text">
          맞은편 스탠드 좌측 <strong>[태양광 패널 아래 파란 박스로 표시된 B출입구 계단]</strong>으로 진입하세요. 출입구 안으로 들어가서 <strong>【오른쪽 2층】</strong>에 학생 화장실이 위치합니다.
        </div>
      </div>
    </div>

    <!-- 4. 3-Pillar Summary Cards -->
    <div class="section-title">핵심 요약 (Quick Summary)</div>
    <div class="summary-grid">
      <div class="summary-card primary">
        <div class="card-label">📍 목적지 [파란 박스]</div>
        <div class="card-value">맞은편 B출입구 2층</div>
        <div class="card-desc">응원석 정면 맞은편 스탠드 B게이트 계단</div>
      </div>
      <div class="summary-card highlight">
        <div class="card-label">☀️ 랜드마크</div>
        <div class="card-value">태양광 패널 아래 입구</div>
        <div class="card-desc">객석에서 보았을 때 태양광 패널 연결 계단</div>
      </div>
      <div class="summary-card accent">
        <div class="card-label">👉 내부 동선</div>
        <div class="card-value">진입 후 【오른쪽 2층】</div>
        <div class="card-desc">출입문 진입 직후 우측 계단으로 이동</div>
      </div>
    </div>

    <!-- 5. 4-Step Timeline Guide -->
    <div class="section-title">단계별 행동 요령 (Step-by-Step)</div>
    <div class="timeline">
      <div class="timeline-item">
        <div class="step-num">01</div>
        <div class="step-content">
          <div class="step-title">
            관객석 상단 통로로 올라가기
            <span class="step-tag">출발</span>
          </div>
          <div class="step-desc">
            배재 응원석에서 관객석 상단 통로로 안전하게 올라갑니다. <strong>하프타임 시작 직후는 혼잡</strong>하므로 쉬는 시간 5분 전 또는 경기 진행 중 미리 이용하는 것을 추천합니다.
          </div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="step-num">02</div>
        <div class="step-content">
          <div class="step-title">
            상단 통로를 따라 이동
            <span class="step-tag">도보 약 2~3분</span>
          </div>
          <div class="step-desc">
            관객석 상단 통로를 따라 오른쪽(반시계 방향)으로 돌아 맞은편 북측 스탠드로 이동합니다. <strong>경기장 필드(잔디) 및 러닝 트랙 침범은 엄격히 금지</strong>됩니다.
          </div>
        </div>
      </div>

      <div class="timeline-item active">
        <div class="step-num">03</div>
        <div class="step-content">
          <div class="step-title">
            태양광 패널 아래 [파란 박스 B출입구] 진입
            <span class="step-tag" style="background: rgba(30, 144, 255, 0.2); color: var(--pc-blue);">출입구</span>
          </div>
          <div class="step-desc">
            맞은편 스탠드 <strong>태양광 패널 지붕 아래 파란 박스로 표시된 B출입구 계단</strong>을 확인하고 내부로 진입합니다.
          </div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="step-num">04</div>
        <div class="step-content">
          <div class="step-title">
            진입 직후 【오른쪽 2층】 화장실 이용
            <span class="step-tag" style="background: rgba(39, 174, 96, 0.2); color: var(--pc-green);">화장실</span>
          </div>
          <div class="step-desc">
            출입문 안으로 들어가서 <strong>우측 계단을 통해 2층</strong>으로 올라가면 남/여 화장실이 있습니다. 1열 대기 질서를 준수해 주세요.
          </div>
        </div>
      </div>
    </div>

    <!-- 6. Safety Notice Alert -->
    <div class="alert-box">
      <div class="alert-title">⚠️ 배양전 관람 학생 안전 및 질서 수칙</div>
      <ul class="alert-list">
        <li><strong>상대 학교(양정) 응원 구역 진입 금지:</strong> 불필요한 마찰을 방지하기 위해 지정된 배재 학생 이동 동선을 엄수해 주십시오.</li>
        <li><strong>경기장 그라운드 잔디 침범 절대 금지:</strong> 원활한 경기 진행을 위해 관객석 통로로만 보행합니다.</li>
        <li><strong>화장실 이용 대기 시 1줄 서기:</strong> 혼잡 시 안전 요원(학생회 및 인솔 교사)의 안내에 적극 협조해 주십시오.</li>
        <li><strong>비상 상황 발생 시:</strong> 주변 인솔 교사 또는 진행 본부 안내 데스크로 즉시 연락 바랍니다.</li>
      </ul>
    </div>

    <!-- 7. Footer -->
    <footer class="footer">
      <p>배재학당 · 배재중학교 · 배재고등학교 학생회 & 인솔지도부</p>
      <p style="margin-top: 4px;"><strong>PaiChai Hakdang</strong> | Victory PaiChai! All Rights Reserved.</p>
    </footer>

  </div>

  <!-- Lightbox Modal -->
  <div class="modal" id="imageModal" onclick="closeModal()">
    <button class="modal-close" onclick="closeModal()">✕</button>
    <img class="modal-content" id="modalImg" src="" alt="확대 이미지">
  </div>

  <script>
    function switchTab(idx) {{
      document.getElementById('tabBtn3').classList.toggle('active', idx === 3);
      document.getElementById('tabBtn1').classList.toggle('active', idx === 1);
      document.getElementById('tabBtn2').classList.toggle('active', idx === 2);

      document.getElementById('viewCard3').style.display = (idx === 3) ? 'grid' : 'none';
      document.getElementById('viewCard1').style.display = (idx === 1) ? 'block' : 'none';
      document.getElementById('viewCard2').style.display = (idx === 2) ? 'block' : 'none';
    }}

    function openModal(imgId) {{
      const modal = document.getElementById('imageModal');
      const modalImg = document.getElementById('modalImg');
      const targetImg = document.getElementById(imgId);
      modalImg.src = targetImg.src;
      modal.classList.add('show');
    }}

    function closeModal() {{
      document.getElementById('imageModal').classList.remove('show');
    }}

    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeModal();
    }});
  </script>
</body>
</html>
'''

out_path = 'D:/Antigravity/workspace/paichai_toilet_guide/index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'index.html updated (default dual-grid): {out_path} ({os.path.getsize(out_path)//1024} KB)')
