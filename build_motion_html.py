import os
import sys
import json

sys.path.append('D:/Antigravity/workspace/paichai_toilet_guide/assets')
from images_b64 import AERIAL_B64, VIEW_B64
from smooth_path_data import SMOOTH_WAYPOINTS

pts_js = [{'x': pt[0], 'y': pt[1]} for pt in SMOOTH_WAYPOINTS]
pts_json_str = json.dumps(pts_js)

html_code = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026 배양전 화장실 동선 모션그래픽 플레이어 | PaiChai</title>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --pc-navy: #1A2F8A;
      --pc-red: #C0392B;
      --pc-gold: #F39C12;
      --pc-blue: #1E90FF;
      --pc-neon: #FFE600;
      --bg: #0A0F1D;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: white;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 16px;
    }}
    .player-wrap {{
      width: 100%;
      max-width: 1000px;
      background: #131B2E;
      border: 1px solid #1E2D4A;
      border-radius: 20px;
      padding: 16px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }}
    .player-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding: 0 4px;
    }}
    .title-box h2 {{
      font-size: 18px;
      font-weight: 800;
      color: white;
    }}
    .title-box p {{
      font-size: 13px;
      color: #94A3B8;
    }}
    .canvas-container {{
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      background: #000;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}
    .controls {{
      margin-top: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .progress-bar {{
      width: 100%;
      height: 8px;
      background: #1E293B;
      border-radius: 4px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
    }}
    .progress-fill {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--pc-navy), var(--pc-neon), var(--pc-red));
      border-radius: 4px;
      transition: width 0.05s linear;
    }}
    .btn-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .play-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .control-btn {{
      background: #1E293B;
      color: white;
      border: 1px solid #334155;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      font-family: inherit;
    }}
    .control-btn:hover {{
      background: var(--pc-navy);
      border-color: var(--pc-gold);
    }}
    .time-display {{
      font-size: 14px;
      font-weight: 600;
      color: #94A3B8;
      font-variant-numeric: tabular-nums;
    }}
    .chapter-group {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .chapter-btn {{
      background: transparent;
      border: 1px solid #334155;
      color: #CBD5E1;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .chapter-btn:hover, .chapter-btn.active {{
      background: rgba(26, 47, 138, 0.4);
      border-color: var(--pc-gold);
      color: var(--pc-gold);
    }}
  </style>
</head>
<body>

  <div class="player-wrap">
    <div class="player-header">
      <div class="title-box">
        <h2>2026 배양전 학생 화장실 이용 동선 안내</h2>
        <p>효창운동장 B출입구 2층 화장실 (실시간 인터랙티브 모션그래픽)</p>
      </div>
      <a href="index.html" class="control-btn" style="text-decoration: none;">📄 안내 문서로 가기</a>
    </div>

    <div class="canvas-container" id="canvasContainer">
      <canvas id="motionCanvas" width="1920" height="1080"></canvas>
    </div>

    <div class="controls">
      <div class="progress-bar" id="progressBar" onclick="seek(event)">
        <div class="progress-fill" id="progressFill"></div>
      </div>

      <div class="btn-row">
        <div class="play-group">
          <button class="control-btn" id="playBtn" onclick="togglePlay()">▶ 재생</button>
          <span class="time-display" id="timeDisplay">00:00 / 00:18</span>
        </div>

        <div class="chapter-group">
          <button class="chapter-btn" onclick="jumpTo(0)">인트로</button>
          <button class="chapter-btn" onclick="jumpTo(3.5)">STEP 1 항공뷰</button>
          <button class="chapter-btn" onclick="jumpTo(9.0)">STEP 2 객석 실사</button>
          <button class="chapter-btn" onclick="jumpTo(14.5)">핵심 요약</button>
          <button class="control-btn" onclick="toggleFullscreen()">⛶ 전체화면</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('motionCanvas');
    const ctx = canvas.getContext('2d');
    const duration = 18.0;
    let currentTime = 0;
    let isPlaying = true;
    let lastTimestamp = null;

    const imgAerial = new Image();
    imgAerial.src = "data:image/jpeg;base64,{AERIAL_B64}";
    const imgView = new Image();
    imgView.src = "data:image/jpeg;base64,{VIEW_B64}";

    // 원본 녹색선을 100% 추적하는 171개 정밀 스무스 웨이포인트
    const WAYPOINTS = {pts_json_str};

    // 누적 거리 계산 및 정밀 보간 유틸리티
    const pathDists = [0];
    for (let i = 0; i < WAYPOINTS.length - 1; i++) {{
      const p1 = WAYPOINTS[i], p2 = WAYPOINTS[i+1];
      const d = Math.hypot(p2.x - p1.x, p2.y - p1.y);
      pathDists.push(pathDists[pathDists.length - 1] + d);
    }}
    const totalPathDist = pathDists[pathDists.length - 1];

    function getPathPosAndDir(frac) {{
      const targetD = Math.max(0, Math.min(1, frac)) * totalPathDist;
      let idx = 0;
      while (idx < pathDists.length - 1 && pathDists[idx+1] < targetD) {{
        idx++;
      }}
      if (idx >= pathDists.length - 1) {{
        const p1 = WAYPOINTS[WAYPOINTS.length - 2];
        const p2 = WAYPOINTS[WAYPOINTS.length - 1];
        const dx = p2.x - p1.x, dy = p2.y - p1.y;
        const l = Math.hypot(dx, dy) || 1;
        return {{ pos: WAYPOINTS[WAYPOINTS.length - 1], dir: {{ x: dx/l, y: dy/l }} }};
      }}
      const segD = pathDists[idx+1] - pathDists[idx];
      const f = segD > 0 ? (targetD - pathDists[idx]) / segD : 0;
      const p1 = WAYPOINTS[idx], p2 = WAYPOINTS[idx+1];
      const pos = {{ x: p1.x + (p2.x - p1.x) * f, y: p1.y + (p2.y - p1.y) * f }};
      const dx = p2.x - p1.x, dy = p2.y - p1.y;
      const l = Math.hypot(dx, dy) || 1;
      return {{ pos, dir: {{ x: dx/l, y: dy/l }} }};
    }}

    function draw(t) {{
      const w = 1920, h = 1080;
      ctx.clearRect(0, 0, w, h);

      if (t < 3.5) {{
        ctx.fillStyle = '#1A2F8A';
        ctx.fillRect(0, 0, w, h);

        ctx.strokeStyle = '#F39C12';
        ctx.lineWidth = 4;
        ctx.strokeRect(60, 60, w-120, h-120);

        ctx.fillStyle = '#C0392B';
        roundRect(ctx, w/2 - 210, 200, 420, 56, 28);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 28px Pretendard';
        ctx.textAlign = 'center';
        ctx.fillText('2026 배양전 [효창운동장]', w/2, 238);

        ctx.fillStyle = '#FFFFFF';
        ctx.font = '900 72px Pretendard';
        ctx.fillText('학생 화장실 이용 동선 안내', w/2, 360);

        ctx.fillStyle = '#0F172A';
        ctx.strokeStyle = '#F39C12';
        ctx.lineWidth = 3;
        roundRect(ctx, w/2 - 500, 470, 1000, 260, 24);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#F39C12';
        ctx.font = 'bold 36px Pretendard';
        ctx.fillText('📍 목적지: 응원석 맞은편 B출입구 2층', w/2, 535);

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 30px Pretendard';
        ctx.fillText('☀️ 랜드마크: 태양광 패널 아래 [파란 박스 계단]', w/2, 605);

        ctx.fillStyle = '#2ECC71';
        ctx.font = 'bold 30px Pretendard';
        ctx.fillText('👉 출입구 진입 후 【 오른쪽 2층 】 화장실', w/2, 670);

        ctx.fillStyle = '#CBD5E1';
        ctx.font = '26px Pretendard';
        ctx.fillText('PaiChai Middle & High School', w/2, 880);
      }}
      else if (t < 9.0) {{
        // Scene 2: 항공뷰 부드러운 동선 드로잉
        const st = t - 3.5;
        const zoom = 1.0 + (st / 5.5) * 0.12;
        const aw = imgAerial.width || 948;
        const ah = imgAerial.height || 1024;
        const cw = aw / zoom;
        const ch = ah / zoom;
        const cx = aw * (0.62 + (st / 5.5) * 0.04);
        const cy = ah * (0.55 - (st / 5.5) * 0.04);
        const sx = Math.max(0, Math.min(aw - cw, cx - cw / 2));
        const sy = Math.max(0, Math.min(ah - ch, cy - ch / 2));

        const mapW = 1180, mapH = 960;
        ctx.drawImage(imgAerial, sx, sy, cw, ch, 60, 60, mapW, mapH);

        ctx.strokeStyle = '#1A2F8A';
        ctx.lineWidth = 4;
        ctx.strokeRect(58, 58, mapW + 4, mapH + 4);

        function toScreen(gx, gy) {{
          const rx = (gx * aw - sx) / cw;
          const ry = (gy * ah - sy) / ch;
          return {{ x: 60 + rx * mapW, y: 60 + ry * mapH }};
        }}

        // 초정밀 스무스 네온 라인 드로잉 및 이동 효과 (st: 0.4s ~ 3.8s)
        const prog = Math.min(1.0, Math.max(0.0, (st - 0.4) / 3.4));
        if (prog > 0) {{
          const numPts = Math.min(WAYPOINTS.length - 1, Math.max(1, Math.floor(prog * (WAYPOINTS.length - 1))));
          
          // 1) 그림자 라인
          ctx.beginPath();
          ctx.strokeStyle = 'rgba(10, 15, 30, 0.9)';
          ctx.lineWidth = 22;
          ctx.lineCap = 'round';
          ctx.lineJoin = 'round';
          for (let i = 0; i <= numPts; i++) {{
            const pt = toScreen(WAYPOINTS[i].x, WAYPOINTS[i].y);
            if (i === 0) ctx.moveTo(pt.x, pt.y);
            else ctx.lineTo(pt.x, pt.y);
          }}
          ctx.stroke();

          // 2) 고시인성 네온 옐로우 라인
          ctx.beginPath();
          ctx.strokeStyle = '#FFE600';
          ctx.lineWidth = 14;
          ctx.lineCap = 'round';
          ctx.lineJoin = 'round';
          for (let i = 0; i <= numPts; i++) {{
            const pt = toScreen(WAYPOINTS[i].x, WAYPOINTS[i].y);
            if (i === 0) ctx.moveTo(pt.x, pt.y);
            else ctx.lineTo(pt.x, pt.y);
          }}
          ctx.stroke();

          // 3) 중심 하이라이트 코어
          ctx.beginPath();
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 4;
          ctx.lineCap = 'round';
          ctx.lineJoin = 'round';
          for (let i = 0; i <= numPts; i++) {{
            const pt = toScreen(WAYPOINTS[i].x, WAYPOINTS[i].y);
            if (i === 0) ctx.moveTo(pt.x, pt.y);
            else ctx.lineTo(pt.x, pt.y);
          }}
          ctx.stroke();

          // 4) 경로 위를 연속으로 흐르는 전진 화살표 (Flowing Chevrons)
          const numChevrons = 20;
          for (let c = 1; c <= numChevrons; c++) {{
            const cFrac = c / (numChevrons + 1);
            if (cFrac <= prog) {{
              const pData = getPathPosAndDir(cFrac);
              const cp = toScreen(pData.pos.x, pData.pos.y);
              const dx = pData.dir.x, dy = pData.dir.y;
              const nx = -dy, ny = dx;

              const flowPhase = (st * 3.2 - cFrac * 8.0) % 1.0;
              const isBright = flowPhase < 0.45;
              ctx.fillStyle = isBright ? '#FFFFFF' : '#1A2F8A';
              ctx.strokeStyle = isBright ? '#0A0F1E' : '#FFE600';
              ctx.lineWidth = 2;

              ctx.beginPath();
              ctx.moveTo(cp.x + dx * 10, cp.y + dy * 10);
              ctx.lineTo(cp.x - dx * 7 + nx * 8, cp.y - dy * 7 + ny * 8);
              ctx.lineTo(cp.x - dx * 7 - nx * 8, cp.y - dy * 7 - ny * 8);
              ctx.closePath();
              ctx.fill();
              ctx.stroke();
            }}
          }}

          // 5) 경로 완성 후 고속 에너지 펄스 주행 (st >= 3.8s)
          if (prog >= 1.0) {{
            [0.0, 0.5].forEach(offset => {{
              const pFrac = ((st - 3.8) * 0.9 + offset) % 1.0;
              const pData = getPathPosAndDir(pFrac);
              const pScr = toScreen(pData.pos.x, pData.pos.y);

              ctx.fillStyle = '#0A0F1E';
              ctx.beginPath();
              ctx.arc(pScr.x, pScr.y, 14, 0, Math.PI * 2);
              ctx.fill();

              ctx.fillStyle = '#FFFFFF';
              ctx.strokeStyle = '#FFE600';
              ctx.lineWidth = 3;
              ctx.beginPath();
              ctx.arc(pScr.x, pScr.y, 10, 0, Math.PI * 2);
              ctx.fill();
              ctx.stroke();
            }});
          }}

          // 6) 선두 유성 헤드 (Comet Head) + 펄스
          const headData = getPathPosAndDir(prog);
          const head = toScreen(headData.pos.x, headData.pos.y);

          const pulseSz = 16 + Math.floor((st * 10) % 5) * 4;
          ctx.strokeStyle = '#FFE600';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(head.x, head.y, pulseSz, 0, Math.PI * 2);
          ctx.stroke();

          ctx.fillStyle = '#FFE600';
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(head.x, head.y, 16, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#FFFFFF';
          ctx.beginPath();
          ctx.arc(head.x, head.y, 7, 0, Math.PI * 2);
          ctx.fill();

          // 7) 플로팅 가이드 뱃지
          if (prog < 0.98) {{
            const tipW = 170, tipH = 46;
            const tx = Math.max(70, Math.min(60 + mapW - tipW - 10, head.x - tipW / 2));
            const ty = Math.max(70, head.y - 68);
            ctx.fillStyle = '#1A2F8A';
            ctx.strokeStyle = '#FFE600';
            ctx.lineWidth = 3;
            roundRect(ctx, tx, ty, tipW, tipH, 10);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = '#FFFFFF';
            ctx.font = 'bold 17px Pretendard';
            ctx.textAlign = 'center';
            ctx.fillText('🚶 외곽 트랙 이동', tx + tipW / 2, ty + 28);
          }}
        }}

        // 출발 핀
        const startPt = toScreen(WAYPOINTS[0].x, WAYPOINTS[0].y);
        ctx.fillStyle = '#1A2F8A';
        ctx.beginPath();
        ctx.arc(startPt.x, startPt.y, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.fillStyle = '#1A2F8A';
        roundRect(ctx, startPt.x - 90, startPt.y + 24, 180, 36, 8);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 16px Pretendard';
        ctx.textAlign = 'center';
        ctx.fillText('출발: 배재 응원석', startPt.x, startPt.y + 48);

        // 도착 핀
        if (st > 2.0) {{
          const destPt = toScreen(WAYPOINTS[WAYPOINTS.length - 1].x, WAYPOINTS[WAYPOINTS.length - 1].y);
          const pulseR = 22 + Math.floor((st * 6) % 4) * 8;
          ctx.strokeStyle = '#C0392B';
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.arc(destPt.x, destPt.y, pulseR, 0, Math.PI * 2);
          ctx.stroke();

          ctx.fillStyle = '#C0392B';
          ctx.beginPath();
          ctx.arc(destPt.x, destPt.y, 18, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 3;
          ctx.stroke();

          roundRect(ctx, destPt.x - 125, destPt.y - 72, 250, 48, 10);
          ctx.fill();
          ctx.fillStyle = '#FFFFFF';
          ctx.font = 'bold 17px Pretendard';
          ctx.fillText('도착: B출입구 2층 화장실', destPt.x, destPt.y - 42);
        }}

        const px = 1280;
        ctx.fillStyle = '#1A2F8A';
        ctx.strokeStyle = '#F39C12';
        ctx.lineWidth = 3;
        roundRect(ctx, px, 60, w - 60 - px, 960, 24);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#F39C12';
        ctx.font = 'bold 28px Pretendard';
        ctx.textAlign = 'center';
        ctx.fillText('STEP 1', px + 290, 130);

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 38px Pretendard';
        ctx.fillText('효창운동장 전체 동선', px + 290, 180);

        const items = [
          ['① 출발', '배재 응원석 우측 계단으로 이동'],
          ['② 이동', '동측 외곽 트랙으로 이동 (도보 2~3분)'],
          ['③ 진입', '맞은편 태양광 패널 아래 B출입구 (파란 박스)'],
          ['④ 이용', '출입구 진입 후 오른쪽 2층 화장실']
        ];
        items.forEach((it, idx) => {{
          const iy = 260 + idx * 165;
          ctx.fillStyle = '#0F172A';
          roundRect(ctx, px + 30, iy, w - px - 90, 135, 16);
          ctx.fill();

          ctx.textAlign = 'left';
          ctx.fillStyle = '#F39C12';
          ctx.font = 'bold 24px Pretendard';
          ctx.fillText(it[0], px + 55, iy + 45);

          ctx.fillStyle = '#FFFFFF';
          ctx.font = '20px Pretendard';
          ctx.fillText(it[1], px + 55, iy + 90);
        }});
      }}
      else if (t < 14.5) {{
        // Scene 3: 객석 실사 뷰 - 파란 박스 위치 (cx=240, cy=580)
        const st = t - 9.0;
        const vw = imgView.width || 1080;
        const vh = imgView.height || 1440;
        const zoom = 1.0 + (st / 5.5) * 0.45;
        const cw = vw / zoom;
        const ch = vh / zoom;
        const cx = 240, cy = 580;
        const sx = Math.max(0, Math.min(vw - cw, cx - cw / 2));
        const sy = Math.max(0, Math.min(vh - ch, cy - ch / 2));

        const viewW = 1180, viewH = 960;
        ctx.drawImage(imgView, sx, sy, cw, ch, 60, 60, viewW, viewH);

        ctx.strokeStyle = '#1E90FF';
        ctx.lineWidth = 4;
        ctx.strokeRect(58, 58, viewW + 4, viewH + 4);

        function toViewScreen(gx, gy) {{
          const rx = (gx - sx) / cw;
          const ry = (gy - sy) / ch;
          return {{ x: 60 + rx * viewW, y: 60 + ry * viewH }};
        }}

        const p1 = toViewScreen(130, 450);
        const p2 = toViewScreen(350, 720);
        ctx.strokeStyle = Math.floor(st * 4) % 2 === 0 ? '#1E90FF' : '#FFFFFF';
        ctx.lineWidth = 7;
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);

        const bxMid = (p1.x + p2.x) / 2;
        ctx.fillStyle = '#1E90FF';
        roundRect(ctx, bxMid - 110, p1.y - 45, 220, 36, 8);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 18px Pretendard';
        ctx.textAlign = 'center';
        ctx.fillText('B출입구 (진입 계단)', bxMid, p1.y - 22);

        if (st > 0.6) {{
          const cardX = Math.min(p2.x + 30, 60 + viewW - 500);
          const cardY = Math.max(80, p1.y - 20);
          ctx.fillStyle = 'rgba(15, 23, 42, 0.95)';
          ctx.strokeStyle = '#1E90FF';
          ctx.lineWidth = 3;
          roundRect(ctx, cardX, cardY, 480, 160, 16);
          ctx.fill();
          ctx.stroke();

          ctx.textAlign = 'center';
          ctx.fillStyle = '#F39C12';
          ctx.font = 'bold 26px Pretendard';
          ctx.fillText('📍 B출입구 [파란 박스]', cardX + 240, cardY + 38);

          ctx.fillStyle = '#FFFFFF';
          ctx.font = 'bold 20px Pretendard';
          ctx.fillText('☀️ 태양광 패널 아래 출입 계단', cardX + 240, cardY + 78);

          ctx.fillStyle = '#2ECC71';
          ctx.font = 'bold 21px Pretendard';
          ctx.fillText('👉 진입 후 【오른쪽 2층】 화장실', cardX + 240, cardY + 120);
        }}

        const px = 1280;
        ctx.fillStyle = '#1A2F8A';
        ctx.strokeStyle = '#F39C12';
        ctx.lineWidth = 3;
        roundRect(ctx, px, 60, w - 60 - px, 960, 24);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#F39C12';
        ctx.font = 'bold 28px Pretendard';
        ctx.textAlign = 'center';
        ctx.fillText('STEP 2', px + 290, 130);

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 38px Pretendard';
        ctx.fillText('응원석 시야 실사 뷰', px + 290, 180);

        const points = [
          ['🟦 파란 박스', '스탠드 좌측 태양광 패널 아래 [B출입구 계단]'],
          ['☀️ 랜드마크', '지붕 위 태양광 패널과 연결된 출입 계단'],
          ['🚻 화장실 위치', '출입문 안쪽 [오른쪽 2층] 화장실'],
          ['💡 혼잡 방지 팁', '쉬는 시간 5분 전 미리 이용 추천']
        ];
        points.forEach((pt, idx) => {{
          const iy = 260 + idx * 165;
          ctx.fillStyle = '#0F172A';
          roundRect(ctx, px + 30, iy, w - px - 90, 135, 16);
          ctx.fill();

          ctx.textAlign = 'left';
          ctx.fillStyle = '#F39C12';
          ctx.font = 'bold 24px Pretendard';
          ctx.fillText(pt[0], px + 55, iy + 45);

          ctx.fillStyle = '#FFFFFF';
          ctx.font = '20px Pretendard';
          ctx.fillText(pt[1], px + 55, iy + 90);
        }});
      }}
      else {{
        ctx.fillStyle = '#1A2F8A';
        ctx.fillRect(0, 0, w, h);

        ctx.strokeStyle = '#F39C12';
        ctx.lineWidth = 4;
        ctx.strokeRect(60, 60, w-120, h-120);

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 52px Pretendard';
        ctx.textAlign = 'center';
        ctx.fillText('2026 배양전 학생 화장실 이용 핵심 요약', w/2, 140);

        const cardW = 540, cardH = 420;
        const gap = 40;
        const startX = (w - (cardW * 3 + gap * 2)) / 2;

        const summaries = [
          ['1️⃣ 위치 확인', '맞은편 B출입구 2층', '응원석 맞은편 [파란 박스]\nB출입구 계단으로 진입합니다', '#1E90FF'],
          ['2️⃣ 랜드마크', '태양광 패널 아래 계단', '객석에서 보았을 때\n태양광 패널 지붕 아래 입구 확인', '#F39C12'],
          ['3️⃣ 진입 후 동선', '오른쪽 2층으로 이동', '출입문 진입 직후\n반드시 우측 2층 계단 이용', '#2ECC71']
        ];

        summaries.forEach((s, i) => {{
          const cx = startX + i * (cardW + gap);
          const cy = 240;
          ctx.fillStyle = '#0F172A';
          ctx.strokeStyle = s[3];
          ctx.lineWidth = 4;
          roundRect(ctx, cx, cy, cardW, cardH, 20);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = s[3];
          ctx.font = 'bold 32px Pretendard';
          ctx.fillText(s[0], cx + cardW/2, cy + 70);

          ctx.fillStyle = '#FFFFFF';
          ctx.font = 'bold 34px Pretendard';
          ctx.fillText(s[1], cx + cardW/2, cy + 160);

          ctx.fillStyle = '#CBD5E1';
          ctx.font = '22px Pretendard';
          const lines = s[2].split('\\n');
          lines.forEach((l, lIdx) => {{
            ctx.fillText(l, cx + cardW/2, cy + 260 + lIdx * 40);
          }});
        }});

        ctx.fillStyle = '#C0392B';
        roundRect(ctx, w/2 - 450, 750, 900, 100, 16);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 30px Pretendard';
        ctx.fillText('🏆 승리의 배재! 안전하고 질서 있는 관람을 응원합니다 🏆', w/2, 810);
      }}
    }}

    function roundRect(ctx, x, y, width, height, radius) {{
      ctx.beginPath();
      ctx.moveTo(x + radius, y);
      ctx.lineTo(x + width - radius, y);
      ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
      ctx.lineTo(x + width, y + height - radius);
      ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
      ctx.lineTo(x + radius, y + height);
      ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
      ctx.lineTo(x, y + radius);
      ctx.quadraticCurveTo(x, y, x + radius, y);
      ctx.closePath();
    }}

    function animate(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const delta = (timestamp - lastTimestamp) / 1000;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += delta;
        if (currentTime >= duration) {{
          currentTime = 0;
        }}
        updateUI();
      }}

      draw(currentTime);
      requestAnimationFrame(animate);
    }}

    function updateUI() {{
      const pct = (currentTime / duration) * 100;
      document.getElementById('progressFill').style.width = pct + '%';

      const curSec = Math.floor(currentTime);
      const curStr = '00:' + (curSec < 10 ? '0' : '') + curSec;
      document.getElementById('timeDisplay').innerText = curStr + ' / 00:18';
    }}

    function togglePlay() {{
      isPlaying = !isPlaying;
      document.getElementById('playBtn').innerText = isPlaying ? '⏸ 정지' : '▶ 재생';
    }}

    function jumpTo(sec) {{
      currentTime = sec;
      updateUI();
    }}

    function seek(e) {{
      const rect = e.currentTarget.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const ratio = Math.max(0, Math.min(1, clickX / rect.width));
      currentTime = ratio * duration;
      updateUI();
    }}

    function toggleFullscreen() {{
      const el = document.getElementById('canvasContainer');
      if (!document.fullscreenElement) {{
        el.requestFullscreen().catch(err => alert(err.message));
      }} else {{
        document.exitFullscreen();
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.code === 'Space') {{
        e.preventDefault();
        togglePlay();
      }}
    }});

    requestAnimationFrame(animate);
  </script>
</body>
</html>
'''

out_path = 'D:/Antigravity/workspace/paichai_toilet_guide/motion_graphic.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_code)

print(f'motion_graphic.html updated with 171 smooth waypoints: {out_path} ({os.path.getsize(out_path)//1024} KB)')
