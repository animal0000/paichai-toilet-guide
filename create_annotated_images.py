"""
create_annotated_images.py
효창운동장 화장실 동선 안내 정적 가이드 이미지 생성 스크립트
- 맑은 고딕 글꼴에 미지원되는 이모지를 배제하여 글자 깨짐(□) 방지
- aerial_annotated.jpg, view_annotated.jpg 생성 및 웹 최적화 리사이즈(aerial_web.jpg, view_web.jpg)
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = 'D:/Antigravity/workspace/paichai_toilet_guide'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

font_path = 'C:/Windows/Fonts/malgunbd.ttf'
font_reg = 'C:/Windows/Fonts/malgun.ttf'

def get_font(size, bold=True):
    p = font_path if bold else font_reg
    return ImageFont.truetype(p, size)

def create_aerial_image():
    # 1. 항공뷰 가이드 이미지 생성
    raw_path = os.path.join(ASSETS_DIR, 'aerial_route.jpg')
    im_aerial = Image.open(raw_path).convert('RGBA')
    w, h = im_aerial.size

    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 배재 응원석 라벨 (하단 파란 박스 부근: x=600, y=780)
    bx1, by1, bx2, by2 = 530, 730, 680, 790
    draw.rectangle([bx1-3, by1-3, bx2+3, by2+3], outline=(26, 47, 138, 255), width=5)
    badge_w, badge_h = 240, 48
    bx_mid = (bx1 + bx2) // 2
    draw.rounded_rectangle([bx_mid - badge_w//2, by2 + 15, bx_mid + badge_w//2, by2 + 15 + badge_h], radius=12, fill=(26, 47, 138, 240), outline=(255, 255, 255, 255), width=2)
    draw.text((bx_mid, by2 + 15 + badge_h//2), '출발: 배재 응원석', font=get_font(20), fill=(255, 255, 255, 255), anchor='mm')

    # 도착 화장실 라벨 (상단 빨간 원 부근: x=630, y=370)
    rx1, ry1, rx2, ry2 = 570, 310, 680, 420
    draw.ellipse([rx1-8, ry1-8, rx2+8, ry2+8], outline=(192, 57, 43, 255), width=6)
    dbadge_w, dbadge_h = 320, 64
    rx_mid = (rx1 + rx2) // 2
    draw.rounded_rectangle([rx_mid - dbadge_w//2, ry1 - 85, rx_mid + dbadge_w//2, ry1 - 85 + dbadge_h], radius=14, fill=(192, 57, 43, 245), outline=(255, 255, 255, 255), width=3)
    draw.text((rx_mid, ry1 - 85 + 22), '도착: 맞은편 B출입구 2층', font=get_font(20), fill=(255, 255, 255, 255), anchor='mm')
    # 이모지 제거: '🚻 화장실 (진입 후 우측)' -> '화장실 (진입 후 우측)'
    draw.text((rx_mid, ry1 - 85 + 46), '화장실 (진입 후 우측)', font=get_font(16, False), fill=(255, 240, 200, 255), anchor='mm')

    # 동선 안내 태그 (관객석 상단 통로 (도보 약 2~3분))
    tag_x1, tag_y1, tag_x2, tag_y2 = 680, 560, 935, 615
    draw.rounded_rectangle([tag_x1, tag_y1, tag_x2, tag_y2], radius=10, fill=(16, 120, 50, 235), outline=(255, 255, 255, 255), width=2)
    draw.text(((tag_x1 + tag_x2)//2, (tag_y1 + tag_y2)//2), '관객석 상단 통로 (도보 약 2~3분)', font=get_font(15), fill=(255, 255, 255, 255), anchor='mm')

    # 상단 타이틀 배너
    draw.rounded_rectangle([20, 20, w-20, 75], radius=12, fill=(17, 24, 39, 230), outline=(26, 47, 138, 255), width=2)
    draw.text((w//2, 47), '2026 배양전 [효창운동장] 학생 화장실 이동 동선 조감도', font=get_font(21), fill=(255, 255, 255, 255), anchor='mm')

    final_aerial = Image.alpha_composite(im_aerial, overlay).convert('RGB')
    out_annotated = os.path.join(ASSETS_DIR, 'aerial_annotated.jpg')
    final_aerial.save(out_annotated, quality=95)
    print(f'{out_annotated} created successfully.')

    # 웹용 최적화 리사이즈 (aerial_web.jpg)
    scale = min(1.0, 1200 / max(w, h))
    im_web = final_aerial.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    out_web = os.path.join(ASSETS_DIR, 'aerial_web.jpg')
    im_web.save(out_web, format='JPEG', quality=85, optimize=True)
    print(f'{out_web} created successfully.')

def create_view_image():
    # 2. 실사 뷰 가이드 이미지 생성
    raw_path = os.path.join(ASSETS_DIR, 'view_optimized.jpg')
    im_view = Image.open(raw_path).convert('RGBA')
    vw, vh = im_view.size
    v_overlay = Image.new('RGBA', (vw, vh), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(v_overlay)

    # 태양광 패널 출입구 하이라이트 (x: 540~760, y: 440~550)
    hx1, hy1, hx2, hy2 = 540, 440, 760, 550
    v_draw.rounded_rectangle([hx1, hy1, hx2, hy2], radius=16, outline=(243, 156, 18, 255), width=6)
    v_draw.rounded_rectangle([hx1-4, hy1-4, hx2+4, hy2+4], radius=20, outline=(192, 57, 43, 200), width=3)

    # 지시 말풍선 카드 (위쪽 카드에서 아래 박스로 가리키는 화살표)
    card_w, card_h = 560, 160
    card_x = (hx1 + hx2) // 2 - card_w // 2
    card_y = hy1 - card_h - 40

    v_draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(17, 24, 39, 245), outline=(243, 156, 18, 255), width=4)
    arrow_mid = (hx1 + hx2) // 2
    v_draw.polygon([(arrow_mid - 25, card_y + card_h), (arrow_mid + 25, card_y + card_h), (arrow_mid, hy1 - 6)], fill=(243, 156, 18, 255))

    # 카드 텍스트 (이모지 📍, ☀️, 👉 제거 및 맑은 고딕 호환 텍스트)
    v_draw.text((card_x + card_w//2, card_y + 35), '맞은편 B출입구 (화장실 진입구)', font=get_font(26), fill=(255, 215, 0, 255), anchor='mm')
    v_draw.text((card_x + card_w//2, card_y + 80), '지붕 위 [태양광 패널] 아래 출입 계단', font=get_font(21), fill=(255, 255, 255, 255), anchor='mm')
    v_draw.text((card_x + card_w//2, card_y + 122), '출입문 진입 후 【 오른쪽 2층 】 화장실', font=get_font(20), fill=(100, 230, 150, 255), anchor='mm')

    # 하단 캡션 바
    v_draw.rounded_rectangle([30, vh - 110, vw - 30, vh - 30], radius=16, fill=(26, 47, 138, 240), outline=(255, 255, 255, 255), width=2)
    v_draw.text((vw//2, vh - 70), '※ 배재 응원석(객석)에서 정면으로 보이는 실제 전경', font=get_font(22), fill=(255, 255, 255, 255), anchor='mm')

    final_view = Image.alpha_composite(im_view, v_overlay).convert('RGB')
    out_annotated = os.path.join(ASSETS_DIR, 'view_annotated.jpg')
    final_view.save(out_annotated, quality=95)
    print(f'{out_annotated} created successfully.')

    # 웹용 최적화 리사이즈 (view_web.jpg)
    scale = min(1.0, 1200 / max(vw, vh))
    im_web = final_view.resize((int(vw * scale), int(vh * scale)), Image.Resampling.LANCZOS)
    out_web = os.path.join(ASSETS_DIR, 'view_web.jpg')
    im_web.save(out_web, format='JPEG', quality=85, optimize=True)
    print(f'{out_web} created successfully.')

if __name__ == '__main__':
    create_aerial_image()
    create_view_image()
    print('All annotated images generated cleanly with tofu-free text.')
