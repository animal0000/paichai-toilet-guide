import os
import sys
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.append('D:/Antigravity/workspace/paichai_toilet_guide/assets')
from smooth_path_data import SMOOTH_WAYPOINTS

# 폰트 설정
FONT_BD = 'C:/Windows/Fonts/malgunbd.ttf'
FONT_REG = 'C:/Windows/Fonts/malgun.ttf'

def get_font(size, bold=True):
    path = FONT_BD if bold else FONT_REG
    return ImageFont.truetype(path, size)

# 브랜드 및 고시인성 컬러
COLOR_NAVY = (26, 47, 138)       # PaiChai Navy #1A2F8A
COLOR_NAVY_DARK = (15, 28, 85)
COLOR_RED = (192, 57, 43)        # PaiChai Red #C0392B
COLOR_GOLD = (243, 156, 18)      # Accent Gold
COLOR_WHITE = (255, 255, 255)
COLOR_DARK = (15, 23, 42)
COLOR_GREEN = (46, 204, 113)
COLOR_DOOR_BLUE = (30, 144, 255) # 사용자 지정 출입구 파란 박스

# 고시인성 이동 동선 색상 (네온 옐로우 & 일렉트릭 골드)
COLOR_PATH_SHADOW = (10, 15, 30)      # 배경 대비용 외곽 섀도우
COLOR_PATH_NEON = (255, 230, 0)       # 눈에 확 띄는 네온 옐로우 #FFE600
COLOR_PATH_CORE = (255, 255, 235)     # 중심부 고광도 코어

# 에셋 로드
im_aerial = Image.open('D:/Antigravity/workspace/paichai_toilet_guide/assets/aerial_route.jpg').convert('RGB')
im_view = Image.open('D:/Antigravity/workspace/paichai_toilet_guide/assets/view_optimized.jpg').convert('RGB')

WAYPOINTS = SMOOTH_WAYPOINTS

# 경로 누적 거리 및 정밀 보간 유틸리티
path_dists = [0.0]
for _i in range(len(WAYPOINTS) - 1):
    _p1, _p2 = WAYPOINTS[_i], WAYPOINTS[_i+1]
    _d = ((_p2[0] - _p1[0])**2 + (_p2[1] - _p1[1])**2)**0.5
    path_dists.append(path_dists[-1] + _d)
total_path_dist = path_dists[-1]

def get_path_pos_and_dir(frac):
    target_d = max(0.0, min(1.0, frac)) * total_path_dist
    idx = 0
    while idx < len(path_dists) - 1 and path_dists[idx+1] < target_d:
        idx += 1
    if idx >= len(path_dists) - 1:
        p1 = WAYPOINTS[-2]
        p2 = WAYPOINTS[-1]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        l = (dx*dx + dy*dy)**0.5 or 1.0
        return WAYPOINTS[-1], (dx/l, dy/l)
    seg_d = path_dists[idx+1] - path_dists[idx]
    f = (target_d - path_dists[idx]) / seg_d if seg_d > 0 else 0
    p1, p2 = WAYPOINTS[idx], WAYPOINTS[idx+1]
    pos = (p1[0] + (p2[0] - p1[0])*f, p1[1] + (p2[1] - p1[1])*f)
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    l = (dx*dx + dy*dy)**0.5 or 1.0
    return pos, (dx/l, dy/l)

# ----------------- 가로형 (1920x1080) 렌더러 -----------------
def render_frame_landscape(t, total_time=18.0):
    w, h = 1920, 1080
    frame = Image.new('RGB', (w, h), COLOR_DARK)
    draw = ImageDraw.Draw(frame)

    if t < 3.5:
        # [SCENE 1: 인트로]
        frame.paste(Image.new('RGB', (w, h), COLOR_NAVY), (0, 0))
        draw = ImageDraw.Draw(frame)

        draw.rectangle([60, 60, w-60, h-60], outline=COLOR_GOLD, width=3)
        draw.rectangle([72, 72, w-72, h-72], outline=(255, 255, 255, 80), width=1)

        badge_w, badge_h = 420, 56
        draw.rounded_rectangle([w//2 - badge_w//2, 200, w//2 + badge_w//2, 200 + badge_h], radius=28, fill=COLOR_RED)
        draw.text((w//2, 228), '2026 배양전 [효창운동장]', font=get_font(28), fill=COLOR_WHITE, anchor='mm')

        draw.text((w//2, 360), '학생 화장실 이용 동선 안내', font=get_font(72), fill=COLOR_WHITE, anchor='mm')

        card_w, card_h = 1000, 260
        cx, cy = w//2 - card_w//2, 470
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=24, fill=(15, 23, 42), outline=COLOR_GOLD, width=3)

        draw.text((w//2, cy + 65), '📍 목적지: 응원석 맞은편 B출입구 2층', font=get_font(36), fill=COLOR_GOLD, anchor='mm')
        draw.text((w//2, cy + 135), '☀️ 랜드마크: 지붕 위 태양광 패널 아래 [파란 박스 계단]', font=get_font(30), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, cy + 200), '👉 출입구 진입 후 【 오른쪽 2층 】 화장실', font=get_font(30), fill=COLOR_GREEN, anchor='mm')

        draw.text((w//2, 880), 'PaiChai Middle & High School', font=get_font(26), fill=(200, 215, 255), anchor='mm')
        draw.text((w//2, 925), '승리의 배재! 안전하고 질서 있는 관람을 응원합니다', font=get_font(22, False), fill=(180, 195, 230), anchor='mm')

    elif t < 9.0:
        # [SCENE 2: 항공 지도 동선 - 원본 녹색선을 매끄럽게 타는 네온 옐로우 라인]
        st = t - 3.5
        zoom = 1.0 + (st / 5.5) * 0.12
        aw, ah = im_aerial.size
        cw, ch = int(aw / zoom), int(ah / zoom)
        cx = int(aw * (0.62 + (st / 5.5) * 0.04))
        cy = int(ah * (0.55 - (st / 5.5) * 0.04))
        x1 = max(0, min(aw - cw, cx - cw // 2))
        y1 = max(0, min(ah - ch, cy - ch // 2))
        crop_aerial = im_aerial.crop((x1, y1, x1 + cw, y1 + ch))

        map_w, map_h = 1180, 960
        map_resized = crop_aerial.resize((map_w, map_h), Image.Resampling.LANCZOS)
        frame.paste(map_resized, (60, 60))
        draw = ImageDraw.Draw(frame)
        draw.rectangle([58, 58, 60 + map_w + 2, 60 + map_h + 2], outline=COLOR_NAVY, width=4)

        def to_screen(gx, gy):
            rel_x = (gx * aw - x1) / cw
            rel_y = (gy * ah - y1) / ch
            return (int(60 + rel_x * map_w), int(60 + rel_y * map_h))

        # 매끄러운 궤적 드로잉 및 강력한 이동 효과
        # st: 0.4s ~ 3.8s (3.4초간 이동)
        prog = min(1.0, max(0.0, (st - 0.4) / 3.4))

        if prog > 0:
            num_pts = int(prog * (len(WAYPOINTS) - 1))
            num_pts = max(1, min(len(WAYPOINTS) - 1, num_pts))
            pts = [to_screen(*WAYPOINTS[i]) for i in range(num_pts + 1)]

            # 1) 어두운 배경 섀도우 라인 (대비 극대화)
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=COLOR_PATH_SHADOW, width=22)

            # 2) 메인 고시인성 네온 옐로우 라인
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=COLOR_PATH_NEON, width=14)

            # 3) 중심 하이라이트 코어 라인
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=COLOR_PATH_CORE, width=4)

            # 4) 경로 위를 따라 연속으로 흐르는 전진 화살표 (Flowing Chevrons)
            num_chevrons = 20
            for c_idx in range(num_chevrons):
                c_frac = (c_idx + 1) / (num_chevrons + 1)
                if c_frac <= prog:
                    pos_norm, dir_vec = get_path_pos_and_dir(c_frac)
                    cp = to_screen(*pos_norm)
                    dx, dy = dir_vec
                    nx, ny = -dy, dx # 법선 벡터

                    # 흐르는 빛의 파동 (출발 ➔ 도착 방향으로 고속 펄스 이동)
                    flow_phase = (st * 3.2 - c_frac * 8.0) % 1.0
                    is_bright = flow_phase < 0.45
                    arr_fill = (255, 255, 255) if is_bright else COLOR_NAVY
                    arr_outline = COLOR_PATH_SHADOW if is_bright else COLOR_PATH_NEON

                    tip = (cp[0] + dx * 10, cp[1] + dy * 10)
                    left = (cp[0] - dx * 7 + nx * 8, cp[1] - dy * 7 + ny * 8)
                    right = (cp[0] - dx * 7 - nx * 8, cp[1] - dy * 7 - ny * 8)
                    draw.polygon([tip, left, right], fill=arr_fill, outline=arr_outline)

            # 5) 경로 완성 후 고속 에너지 펄스 주행 (st >= 3.8s)
            if prog >= 1.0:
                for pulse_offset in [0.0, 0.5]:
                    pulse_frac = ((st - 3.8) * 0.9 + pulse_offset) % 1.0
                    p_pos, _ = get_path_pos_and_dir(pulse_frac)
                    p_scr = to_screen(*p_pos)
                    draw.ellipse([p_scr[0]-14, p_scr[1]-14, p_scr[0]+14, p_scr[1]+14], fill=COLOR_PATH_SHADOW)
                    draw.ellipse([p_scr[0]-10, p_scr[1]-10, p_scr[0]+10, p_scr[1]+10], fill=COLOR_WHITE, outline=COLOR_PATH_NEON, width=3)

            # 6) 선두 이동 유성 헤드 (Comet Head) + 펄스
            head_norm, _ = get_path_pos_and_dir(prog)
            head = to_screen(*head_norm)

            # 팽창하는 펄스 글로우 링
            pulse_sz = 16 + int((st * 10) % 5) * 4
            draw.ellipse([head[0]-pulse_sz-6, head[1]-pulse_sz-6, head[0]+pulse_sz+6, head[1]+pulse_sz+6], fill=COLOR_PATH_SHADOW)
            draw.ellipse([head[0]-pulse_sz, head[1]-pulse_sz, head[0]+pulse_sz, head[1]+pulse_sz], outline=COLOR_PATH_NEON, width=3)
            # 메인 헤드 구체
            draw.ellipse([head[0]-16, head[1]-16, head[0]+16, head[1]+16], fill=COLOR_PATH_NEON, outline=COLOR_WHITE, width=3)
            draw.ellipse([head[0]-7, head[1]-7, head[0]+7, head[1]+7], fill=COLOR_WHITE)

            # 7) 헤드를 따라다니는 이동 가이드 뱃지 (Floating Tooltip)
            if prog < 0.98:
                tip_w, tip_h = 185, 46
                tx = max(70, min(60 + map_w - tip_w - 10, head[0] - tip_w // 2))
                ty = max(70, head[1] - 68)
                draw.rounded_rectangle([tx, ty, tx + tip_w, ty + tip_h], radius=10, fill=COLOR_NAVY, outline=COLOR_PATH_NEON, width=3)
                draw.text((tx + tip_w//2, ty + tip_h//2), '🚶 관객석 상단 통로', font=get_font(17), fill=COLOR_WHITE, anchor='mm')
                draw.polygon([(head[0], head[1]-16), (head[0]-7, ty+tip_h), (head[0]+7, ty+tip_h)], fill=COLOR_PATH_NEON)

        # 출발지 핀 (배재 응원석)
        start_pt = to_screen(WAYPOINTS[0][0], WAYPOINTS[0][1])
        start_pulse = 18 + int((st * 4) % 3) * 6
        draw.ellipse([start_pt[0]-start_pulse, start_pt[1]-start_pulse, start_pt[0]+start_pulse, start_pt[1]+start_pulse], outline=COLOR_NAVY, width=2)
        draw.ellipse([start_pt[0]-18, start_pt[1]-18, start_pt[0]+18, start_pt[1]+18], fill=COLOR_NAVY, outline=COLOR_WHITE, width=3)
        draw.rounded_rectangle([start_pt[0]-90, start_pt[1]+24, start_pt[0]+90, start_pt[1]+60], radius=8, fill=COLOR_NAVY)
        draw.text((start_pt[0], start_pt[1]+42), '출발: 배재 응원석', font=get_font(16), fill=COLOR_WHITE, anchor='mm')

        # 도착지 핀 (맞은편 B출입구)
        if st > 2.0:
            dest_pt = to_screen(WAYPOINTS[-1][0], WAYPOINTS[-1][1])
            pulse_r = 22 + int((st * 6) % 4) * 8
            draw.ellipse([dest_pt[0]-pulse_r, dest_pt[1]-pulse_r, dest_pt[0]+pulse_r, dest_pt[1]+pulse_r], outline=COLOR_RED, width=4)
            draw.ellipse([dest_pt[0]-18, dest_pt[1]-18, dest_pt[0]+18, dest_pt[1]+18], fill=COLOR_RED, outline=COLOR_WHITE, width=3)
            draw.rounded_rectangle([dest_pt[0]-125, dest_pt[1]-72, dest_pt[0]+125, dest_pt[1]-24], radius=10, fill=COLOR_RED)
            draw.text((dest_pt[0], dest_pt[1]-48), '도착: B출입구 2층 화장실', font=get_font(17), fill=COLOR_WHITE, anchor='mm')

        px = 1280
        draw.rounded_rectangle([px, 60, w-60, 1020], radius=24, fill=(26, 47, 138), outline=COLOR_GOLD, width=3)
        draw.text((px + 290, 130), 'STEP 1', font=get_font(28), fill=COLOR_GOLD, anchor='mm')
        draw.text((px + 290, 180), '효창운동장 전체 동선', font=get_font(38), fill=COLOR_WHITE, anchor='mm')

        items = [
            ('① 출발', '관객석 상단 통로로 올라가기'),
            ('② 이동', '상단 통로를 따라 반시계 방향 이동 (도보 약 2~3분)'),
            ('③ 진입', '맞은편 태양광 패널 아래 B출입구 (파란 박스)'),
            ('④ 이용', '출입구 진입 후 오른쪽 2층 화장실')
        ]
        for idx, (title, desc) in enumerate(items):
            iy = 270 + idx * 165
            draw.rounded_rectangle([px + 30, iy, w - 90, iy + 135], radius=16, fill=(15, 23, 42))
            draw.text((px + 55, iy + 35), title, font=get_font(24), fill=COLOR_GOLD)
            if len(desc) > 18:
                draw.text((px + 55, iy + 72), desc[:18], font=get_font(18, False), fill=COLOR_WHITE)
                draw.text((px + 55, iy + 98), desc[18:], font=get_font(18, False), fill=COLOR_WHITE)
            else:
                draw.text((px + 55, iy + 80), desc, font=get_font(20, False), fill=COLOR_WHITE)

        draw.text((px + 290, 960), '※ 경기장 필드 잔디 진입 절대 금지', font=get_font(18), fill=(255, 120, 120), anchor='mm')

    elif t < 14.5:
        # [SCENE 3: 현장 실사 뷰 - 파란 박스 위치 (cx=240, cy=580)]
        st = t - 9.0
        vw, vh = im_view.size
        zoom = 1.0 + (st / 5.5) * 0.45
        cw, ch = int(vw / zoom), int(vh / zoom)
        cx = int(240 + (1.0 - (st / 5.5)) * 100)
        cy = int(580)
        x1 = max(0, min(vw - cw, cx - cw // 2))
        y1 = max(0, min(vh - ch, cy - ch // 2))
        crop_view = im_view.crop((x1, y1, x1 + cw, y1 + ch))

        view_w, view_h = 1180, 960
        view_resized = crop_view.resize((view_w, view_h), Image.Resampling.LANCZOS)
        frame.paste(view_resized, (60, 60))
        draw = ImageDraw.Draw(frame)
        draw.rectangle([58, 58, 60 + view_w + 2, 60 + view_h + 2], outline=COLOR_DOOR_BLUE, width=4)

        def to_view_screen(gx, gy):
            rel_x = (gx - x1) / cw
            rel_y = (gy - y1) / ch
            return (int(60 + rel_x * view_w), int(60 + rel_y * view_h))

        p1 = to_view_screen(130, 450)
        p2 = to_view_screen(350, 720)

        pulse_col = COLOR_DOOR_BLUE if int(st * 4) % 2 == 0 else (255, 255, 255)
        draw.rectangle([p1[0]-4, p1[1]-4, p2[0]+4, p2[1]+4], outline=(26, 115, 232), width=2)
        draw.rectangle([p1[0], p1[1], p2[0], p2[1]], outline=pulse_col, width=7)

        bx_mid = (p1[0] + p2[0]) // 2
        draw.rounded_rectangle([bx_mid - 120, p1[1] - 50, bx_mid + 120, p1[1] - 10], radius=10, fill=COLOR_DOOR_BLUE)
        draw.text((bx_mid, p1[1] - 30), 'B출입구 (진입 계단)', font=get_font(20), fill=COLOR_WHITE, anchor='mm')

        if st > 0.6:
            card_x = min(p2[0] + 30, 60 + view_w - 520)
            card_y = max(80, p1[1] - 20)
            card_w = 480
            card_h = 170

            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(15, 23, 42), outline=COLOR_DOOR_BLUE, width=3)
            draw.line([(card_x, card_y + 40), (p2[0] + 5, p1[1] + 40)], fill=COLOR_DOOR_BLUE, width=4)

            draw.text((card_x + card_w//2, card_y + 35), '📍 B출입구 [파란 박스]', font=get_font(26), fill=COLOR_GOLD, anchor='mm')
            draw.text((card_x + card_w//2, card_y + 78), '☀️ 태양광 패널 아래 출입 계단', font=get_font(21), fill=COLOR_WHITE, anchor='mm')
            draw.text((card_x + card_w//2, card_y + 122), '👉 진입 후 【오른쪽 2층】 화장실', font=get_font(22), fill=COLOR_GREEN, anchor='mm')

        px = 1280
        draw.rounded_rectangle([px, 60, w-60, 1020], radius=24, fill=(26, 47, 138), outline=COLOR_GOLD, width=3)
        draw.text((px + 290, 130), 'STEP 2', font=get_font(28), fill=COLOR_GOLD, anchor='mm')
        draw.text((px + 290, 180), '응원석 시야 실사 뷰', font=get_font(38), fill=COLOR_WHITE, anchor='mm')

        points = [
            ('🟦 파란 박스', '맞은편 스탠드 좌측 태양광 패널 아래 [B출입구 계단]'),
            ('☀️ 랜드마크', '지붕 위 태양광 패널과 연결된 출입 계단 확인'),
            ('🚻 화장실 위치', '출입구로 들어간 후 [오른쪽 2층] 화장실로 이동'),
            ('💡 혼잡 방지 팁', '쉬는 시간 5분 전 또는 경기 진행 중 여유 시 이용 추천')
        ]
        for idx, (title, desc) in enumerate(points):
            iy = 270 + idx * 165
            draw.rounded_rectangle([px + 30, iy, w - 90, iy + 135], radius=16, fill=(15, 23, 42))
            draw.text((px + 55, iy + 35), title, font=get_font(24), fill=COLOR_GOLD)
            if len(desc) > 18:
                draw.text((px + 55, iy + 72), desc[:18], font=get_font(18, False), fill=COLOR_WHITE)
                draw.text((px + 55, iy + 98), desc[18:], font=get_font(18, False), fill=COLOR_WHITE)
            else:
                draw.text((px + 55, iy + 80), desc, font=get_font(20, False), fill=COLOR_WHITE)

        draw.text((px + 290, 960), '※ 파란 박스로 표시된 곳이 B출입구 입구입니다', font=get_font(18), fill=(200, 220, 255), anchor='mm')

    else:
        # [SCENE 4: 최종 요약 리캡]
        frame.paste(Image.new('RGB', (w, h), COLOR_NAVY), (0, 0))
        draw = ImageDraw.Draw(frame)

        draw.rectangle([60, 60, w-60, h-60], outline=COLOR_GOLD, width=3)
        draw.text((w//2, 140), '2026 배양전 학생 화장실 이용 핵심 요약', font=get_font(52), fill=COLOR_WHITE, anchor='mm')

        card_w = 540
        card_h = 420
        gap = 40
        start_x = (w - (card_w * 3 + gap * 2)) // 2

        summary_cards = [
            ('1️⃣ 위치 확인', '맞은편 B출입구 2층', '응원석 맞은편 [파란 박스]\nB출입구 계단으로 진입합니다', COLOR_DOOR_BLUE),
            ('2️⃣ 랜드마크', '태양광 패널 아래 계단', '객석에서 보았을 때\n태양광 패널 지붕 아래 입구 확인', COLOR_GOLD),
            ('3️⃣ 진입 후 동선', '오른쪽 2층으로 이동', '출입문 진입 직후\n반드시 우측 2층으로 가세요', COLOR_GREEN)
        ]

        for i, (head, sub, desc, acc_color) in enumerate(summary_cards):
            cx = start_x + i * (card_w + gap)
            cy = 240
            draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=20, fill=(15, 23, 42), outline=acc_color, width=4)
            draw.text((cx + card_w//2, cy + 70), head, font=get_font(32), fill=acc_color, anchor='mm')
            draw.text((cx + card_w//2, cy + 160), sub, font=get_font(34), fill=COLOR_WHITE, anchor='mm')
            lines = desc.split('\n')
            for l_idx, line in enumerate(lines):
                draw.text((cx + card_w//2, cy + 260 + l_idx * 40), line, font=get_font(22, False), fill=(200, 210, 230), anchor='mm')

        draw.rounded_rectangle([w//2 - 450, 750, w//2 + 450, 850], radius=16, fill=COLOR_RED)
        draw.text((w//2, 800), '🏆 승리의 배재! 안전하고 질서 있는 관람을 응원합니다 🏆', font=get_font(30), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, 920), 'PaiChai Middle School & PaiChai High School', font=get_font(24), fill=(200, 215, 255), anchor='mm')

    return frame

# ----------------- 세로형 (1080x1920) 렌더러 -----------------
def render_frame_portrait(t, total_time=18.0):
    w, h = 1080, 1920
    frame = Image.new('RGB', (w, h), COLOR_DARK)
    draw = ImageDraw.Draw(frame)

    if t < 3.5:
        frame.paste(Image.new('RGB', (w, h), COLOR_NAVY), (0, 0))
        draw = ImageDraw.Draw(frame)

        draw.rectangle([40, 40, w-40, h-40], outline=COLOR_GOLD, width=3)

        badge_w, badge_h = 360, 52
        draw.rounded_rectangle([w//2 - badge_w//2, 380, w//2 + badge_w//2, 380 + badge_h], radius=26, fill=COLOR_RED)
        draw.text((w//2, 406), '2026 배양전 [효창운동장]', font=get_font(26), fill=COLOR_WHITE, anchor='mm')

        draw.text((w//2, 540), '학생 화장실 이용 안내', font=get_font(58), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, 620), '효창운동장 이동 동선 가이드', font=get_font(34, False), fill=COLOR_GOLD, anchor='mm')

        card_w, card_h = 920, 440
        cx, cy = w//2 - card_w//2, 740
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=24, fill=(15, 23, 42), outline=COLOR_GOLD, width=3)

        draw.text((w//2, cy + 90), '📍 목적지: 응원석 맞은편 B출입구 2층', font=get_font(34), fill=COLOR_GOLD, anchor='mm')
        draw.text((w//2, cy + 200), '☀️ 랜드마크: 태양광 패널 아래 [파란 박스]', font=get_font(30), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, cy + 310), '👉 출입구 진입 후 【 오른쪽 2층 】', font=get_font(32), fill=COLOR_GREEN, anchor='mm')

        draw.text((w//2, 1420), 'PaiChai Middle & High School', font=get_font(28), fill=(200, 215, 255), anchor='mm')
        draw.text((w//2, 1470), '승리의 배재! 안전하고 질서 있는 관람', font=get_font(24, False), fill=(180, 195, 230), anchor='mm')

    elif t < 9.0:
        st = t - 3.5
        frame.paste(Image.new('RGB', (w, h), (15, 23, 42)), (0, 0))
        draw = ImageDraw.Draw(frame)

        draw.rounded_rectangle([40, 60, w-40, 180], radius=20, fill=COLOR_NAVY, outline=COLOR_GOLD, width=2)
        draw.text((w//2, 100), 'STEP 1: 효창운동장 전체 이동 동선', font=get_font(34), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, 145), '응원석 ➔ 관객석 상단 통로를 따라 맞은편 B출입구로 이동', font=get_font(22, False), fill=COLOR_GOLD, anchor='mm')

        map_w, map_h = 1000, 1000
        zoom = 1.0 + (st / 5.5) * 0.15
        aw, ah = im_aerial.size
        cw, ch = int(aw / zoom), int(ah / zoom)
        cx = int(aw * (0.62 + (st / 5.5) * 0.04))
        cy = int(ah * (0.55 - (st / 5.5) * 0.04))
        x1 = max(0, min(aw - cw, cx - cw // 2))
        y1 = max(0, min(ah - ch, cy - ch // 2))
        crop_aerial = im_aerial.crop((x1, y1, x1 + cw, y1 + ch))
        map_resized = crop_aerial.resize((map_w, map_h), Image.Resampling.LANCZOS)
        frame.paste(map_resized, (40, 210))
        draw = ImageDraw.Draw(frame)
        draw.rectangle([38, 208, 40 + map_w + 2, 210 + map_h + 2], outline=COLOR_NAVY, width=4)

        def to_portrait_map(gx, gy):
            rel_x = (gx * aw - x1) / cw
            rel_y = (gy * ah - y1) / ch
            return (int(40 + rel_x * map_w), int(210 + rel_y * map_h))

        # 매끄러운 궤적 드로잉 및 강력한 이동 효과
        prog = min(1.0, max(0.0, (st - 0.4) / 3.4))
        if prog > 0:
            num_pts = int(prog * (len(WAYPOINTS) - 1))
            num_pts = max(1, min(len(WAYPOINTS) - 1, num_pts))
            pts = [to_portrait_map(*WAYPOINTS[i]) for i in range(num_pts + 1)]

            # 1) 어두운 배경 섀도우 라인
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=COLOR_PATH_SHADOW, width=22)

            # 2) 메인 고시인성 네온 옐로우 라인
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=COLOR_PATH_NEON, width=14)

            # 3) 중심 하이라이트 코어 라인
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=COLOR_PATH_CORE, width=4)

            # 4) 경로 위를 따라 연속으로 흐르는 전진 화살표 (Flowing Chevrons)
            num_chevrons = 18
            for c_idx in range(num_chevrons):
                c_frac = (c_idx + 1) / (num_chevrons + 1)
                if c_frac <= prog:
                    pos_norm, dir_vec = get_path_pos_and_dir(c_frac)
                    cp = to_portrait_map(*pos_norm)
                    dx, dy = dir_vec
                    nx, ny = -dy, dx

                    flow_phase = (st * 3.2 - c_frac * 8.0) % 1.0
                    is_bright = flow_phase < 0.45
                    arr_fill = (255, 255, 255) if is_bright else COLOR_NAVY
                    arr_outline = COLOR_PATH_SHADOW if is_bright else COLOR_PATH_NEON

                    tip = (cp[0] + dx * 10, cp[1] + dy * 10)
                    left = (cp[0] - dx * 7 + nx * 8, cp[1] - dy * 7 + ny * 8)
                    right = (cp[0] - dx * 7 - nx * 8, cp[1] - dy * 7 - ny * 8)
                    draw.polygon([tip, left, right], fill=arr_fill, outline=arr_outline)

            # 5) 경로 완성 후 고속 에너지 펄스 주행
            if prog >= 1.0:
                for pulse_offset in [0.0, 0.5]:
                    pulse_frac = ((st - 3.8) * 0.9 + pulse_offset) % 1.0
                    p_pos, _ = get_path_pos_and_dir(pulse_frac)
                    p_scr = to_portrait_map(*p_pos)
                    draw.ellipse([p_scr[0]-14, p_scr[1]-14, p_scr[0]+14, p_scr[1]+14], fill=COLOR_PATH_SHADOW)
                    draw.ellipse([p_scr[0]-10, p_scr[1]-10, p_scr[0]+10, p_scr[1]+10], fill=COLOR_WHITE, outline=COLOR_PATH_NEON, width=3)

            # 6) 선두 이동 유성 헤드 (Comet Head) + 펄스
            head_norm, _ = get_path_pos_and_dir(prog)
            head = to_portrait_map(*head_norm)

            pulse_sz = 16 + int((st * 10) % 5) * 4
            draw.ellipse([head[0]-pulse_sz-6, head[1]-pulse_sz-6, head[0]+pulse_sz+6, head[1]+pulse_sz+6], fill=COLOR_PATH_SHADOW)
            draw.ellipse([head[0]-pulse_sz, head[1]-pulse_sz, head[0]+pulse_sz, head[1]+pulse_sz], outline=COLOR_PATH_NEON, width=3)
            draw.ellipse([head[0]-16, head[1]-16, head[0]+16, head[1]+16], fill=COLOR_PATH_NEON, outline=COLOR_WHITE, width=3)
            draw.ellipse([head[0]-7, head[1]-7, head[0]+7, head[1]+7], fill=COLOR_WHITE)

            # 7) 플로팅 가이드 뱃지
            if prog < 0.98:
                tip_w, tip_h = 175, 44
                tx = max(50, min(40 + map_w - tip_w - 10, head[0] - tip_w // 2))
                ty = max(220, head[1] - 65)
                draw.rounded_rectangle([tx, ty, tx + tip_w, ty + tip_h], radius=10, fill=COLOR_NAVY, outline=COLOR_PATH_NEON, width=3)
                draw.text((tx + tip_w//2, ty + tip_h//2), '🚶 관객석 상단 통로', font=get_font(16), fill=COLOR_WHITE, anchor='mm')
                draw.polygon([(head[0], head[1]-16), (head[0]-6, ty+tip_h), (head[0]+6, ty+tip_h)], fill=COLOR_PATH_NEON)

        start_pt = to_portrait_map(WAYPOINTS[0][0], WAYPOINTS[0][1])
        start_pulse = 16 + int((st * 4) % 3) * 6
        draw.ellipse([start_pt[0]-start_pulse, start_pt[1]-start_pulse, start_pt[0]+start_pulse, start_pt[1]+start_pulse], outline=COLOR_NAVY, width=2)
        draw.ellipse([start_pt[0]-16, start_pt[1]-16, start_pt[0]+16, start_pt[1]+16], fill=COLOR_NAVY, outline=COLOR_WHITE, width=3)
        draw.rounded_rectangle([start_pt[0]-80, start_pt[1]+20, start_pt[0]+80, start_pt[1]+55], radius=8, fill=COLOR_NAVY)
        draw.text((start_pt[0], start_pt[1]+37), '배재 응원석', font=get_font(16), fill=COLOR_WHITE, anchor='mm')

        if st > 2.0:
            dest_pt = to_portrait_map(WAYPOINTS[-1][0], WAYPOINTS[-1][1])
            pulse_r = 20 + int((st * 6) % 4) * 8
            draw.ellipse([dest_pt[0]-pulse_r, dest_pt[1]-pulse_r, dest_pt[0]+pulse_r, dest_pt[1]+pulse_r], outline=COLOR_RED, width=4)
            draw.ellipse([dest_pt[0]-18, dest_pt[1]-18, dest_pt[0]+18, dest_pt[1]+18], fill=COLOR_RED, outline=COLOR_WHITE, width=3)
            draw.rounded_rectangle([dest_pt[0]-120, dest_pt[1]-65, dest_pt[0]+120, dest_pt[1]-20], radius=10, fill=COLOR_RED)
            draw.text((dest_pt[0], dest_pt[1]-42), 'B출입구 2층 화장실', font=get_font(18), fill=COLOR_WHITE, anchor='mm')

        draw.rounded_rectangle([40, 1240, w-40, 1850], radius=24, fill=COLOR_NAVY, outline=COLOR_GOLD, width=3)
        card_items = [
            ('① 출발', '관객석 상단 통로로 올라가기'),
            ('② 이동', '상단 통로를 따라 반시계 방향 이동 (도보 약 2~3분)'),
            ('③ 진입', '맞은편 태양광 패널 아래 B출입구 (파란 박스)'),
            ('④ 화장실', '출입문 안쪽 [오른쪽 2층] 화장실 이용')
        ]
        for idx, (t_txt, d_txt) in enumerate(card_items):
            iy = 1270 + idx * 135
            draw.rounded_rectangle([70, iy, w-70, iy + 115], radius=16, fill=(15, 23, 42))
            draw.text((100, iy + 25), t_txt, font=get_font(24), fill=COLOR_GOLD)
            draw.text((100, iy + 65), d_txt, font=get_font(21, False), fill=COLOR_WHITE)

    elif t < 14.5:
        st = t - 9.0
        frame.paste(Image.new('RGB', (w, h), (15, 23, 42)), (0, 0))
        draw = ImageDraw.Draw(frame)

        draw.rounded_rectangle([40, 60, w-40, 180], radius=20, fill=COLOR_NAVY, outline=COLOR_GOLD, width=2)
        draw.text((w//2, 100), 'STEP 2: 응원석 시야 실사 가이드', font=get_font(34), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, 145), '맞은편 [파란 박스] B출입구 계단 확인!', font=get_font(22, False), fill=COLOR_GOLD, anchor='mm')

        vw, vh = im_view.size
        zoom = 1.0 + (st / 5.5) * 0.45
        cw, ch = int(vw / zoom), int(vh / zoom)
        cx, cy = 240, 580
        x1 = max(0, min(vw - cw, cx - cw // 2))
        y1 = max(0, min(vh - ch, cy - ch // 2))
        crop_view = im_view.crop((x1, y1, x1 + cw, y1 + ch))

        view_w, view_h = 1000, 1000
        view_resized = crop_view.resize((view_w, view_h), Image.Resampling.LANCZOS)
        frame.paste(view_resized, (40, 210))
        draw = ImageDraw.Draw(frame)
        draw.rectangle([38, 208, 40 + view_w + 2, 210 + view_h + 2], outline=COLOR_DOOR_BLUE, width=4)

        def to_portrait_view(gx, gy):
            rel_x = (gx - x1) / cw
            rel_y = (gy - y1) / ch
            return (int(40 + rel_x * view_w), int(210 + rel_y * view_h))

        p1 = to_portrait_view(130, 450)
        p2 = to_portrait_view(350, 720)
        pulse_col = COLOR_DOOR_BLUE if int(st * 4) % 2 == 0 else (255, 255, 255)
        draw.rectangle([p1[0], p1[1], p2[0], p2[1]], outline=pulse_col, width=7)

        bx_mid = (p1[0] + p2[0]) // 2
        draw.rounded_rectangle([bx_mid - 110, p1[1] - 45, bx_mid + 110, p1[1] - 10], radius=8, fill=COLOR_DOOR_BLUE)
        draw.text((bx_mid, p1[1] - 27), 'B출입구 (진입 계단)', font=get_font(18), fill=COLOR_WHITE, anchor='mm')

        draw.rounded_rectangle([40, 1240, w-40, 1850], radius=24, fill=COLOR_NAVY, outline=COLOR_GOLD, width=3)
        draw.text((w//2, 1310), '📍 맞은편 B출입구 2층 화장실', font=get_font(34), fill=COLOR_GOLD, anchor='mm')
        draw.text((w//2, 1370), '☀️ 지붕 위 태양광 패널 아래 [파란 박스 계단]', font=get_font(26), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, 1430), '👉 출입문 들어가서 【오른쪽 2층】으로 이동', font=get_font(28), fill=COLOR_GREEN, anchor='mm')

        draw.rounded_rectangle([70, 1500, w-70, 1780], radius=18, fill=(15, 23, 42))
        draw.text((100, 1540), '💡 배양전 관람 꿀팁', font=get_font(24), fill=COLOR_GOLD)
        draw.text((100, 1600), '• 경기 하프타임(쉬는시간)은 매우 혼잡합니다.', font=get_font(20, False), fill=COLOR_WHITE)
        draw.text((100, 1645), '• 쉬는 시간 5분 전 또는 경기 중 이용 권장', font=get_font(20, False), fill=COLOR_WHITE)
        draw.text((100, 1690), '• 상대 학교 응원 구역 침범 금지 및 안전 준수', font=get_font(20, False), fill=COLOR_WHITE)

    else:
        frame.paste(Image.new('RGB', (w, h), COLOR_NAVY), (0, 0))
        draw = ImageDraw.Draw(frame)

        draw.rectangle([40, 40, w-40, h-40], outline=COLOR_GOLD, width=3)
        draw.text((w//2, 160), '배양전 학생 화장실 핵심 요약', font=get_font(52), fill=COLOR_WHITE, anchor='mm')

        summary_cards = [
            ('1️⃣ 위치', '맞은편 B출입구 2층', '응원석 맞은편 [파란 박스] 계단으로 진입', COLOR_DOOR_BLUE),
            ('2️⃣ 랜드마크', '태양광 패널 아래 계단', '객석에서 보았을 때 태양광 패널 지붕 아래 입구 확인', COLOR_GOLD),
            ('3️⃣ 동선', '진입 후 오른쪽 2층', '출입문 진입 직후 반드시 우측 2층 계단 이용', COLOR_GREEN)
        ]
        for i, (head, sub, desc, acc_color) in enumerate(summary_cards):
            cy = 280 + i * 360
            draw.rounded_rectangle([70, cy, w-70, cy + 310], radius=24, fill=(15, 23, 42), outline=acc_color, width=4)
            draw.text((w//2, cy + 65), head, font=get_font(34), fill=acc_color, anchor='mm')
            draw.text((w//2, cy + 145), sub, font=get_font(42), fill=COLOR_WHITE, anchor='mm')
            draw.text((w//2, cy + 225), desc, font=get_font(24, False), fill=(200, 215, 240), anchor='mm')

        draw.rounded_rectangle([w//2 - 420, 1420, w//2 + 420, 1560], radius=20, fill=COLOR_RED)
        draw.text((w//2, 1490), '🏆 승리의 배재! 안전한 관람 🏆', font=get_font(36), fill=COLOR_WHITE, anchor='mm')
        draw.text((w//2, 1660), 'PaiChai Middle School & PaiChai High School', font=get_font(26), fill=(200, 215, 255), anchor='mm')

    return frame

def render_video(out_path, mode='landscape'):
    fps = 30
    duration = 18.0
    total_frames = int(duration * fps)
    w, h = (1920, 1080) if mode == 'landscape' else (1080, 1920)

    print(f'Starting {mode} render: {total_frames} frames ({w}x{h}) -> {out_path}', flush=True)
    cmd = [
        'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{w}x{h}', '-pix_fmt', 'rgb24', '-r', str(fps),
        '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-preset', 'fast', '-crf', '20', out_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f in range(total_frames):
        t = f / fps
        frame_img = render_frame_landscape(t, duration) if mode == 'landscape' else render_frame_portrait(t, duration)
        raw_bytes = frame_img.tobytes()
        proc.stdin.write(raw_bytes)
        if f % 120 == 0:
            print(f'[{mode}] Frame {f}/{total_frames} ({t:.1f}s)', flush=True)

    proc.stdin.close()
    proc.wait()
    print(f'[{mode}] Render completed! Output: {out_path}', flush=True)

def main():
    render_video('D:/Antigravity/workspace/paichai_toilet_guide/paichai_toilet_guide.mp4', 'landscape')
    render_video('D:/Antigravity/workspace/paichai_toilet_guide/paichai_toilet_guide_mobile.mp4', 'portrait')

if __name__ == '__main__':
    main()
