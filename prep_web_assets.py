import base64
from PIL import Image

def optimize_and_encode(in_path, out_path, max_dim=1200, q=82):
    im = Image.open(in_path)
    w, h = im.size
    scale = min(1.0, max_dim / max(w, h))
    if scale < 1.0:
        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    im.save(out_path, format='JPEG', quality=q, optimize=True)
    with open(out_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    print(f'{out_path} size: {len(b64)*3//4//1024} KB')
    return b64

b1 = optimize_and_encode('D:/Antigravity/workspace/paichai_toilet_guide/assets/aerial_annotated.jpg', 'D:/Antigravity/workspace/paichai_toilet_guide/assets/aerial_web.jpg')
b2 = optimize_and_encode('D:/Antigravity/workspace/paichai_toilet_guide/assets/view_annotated.jpg', 'D:/Antigravity/workspace/paichai_toilet_guide/assets/view_web.jpg')

with open('D:/Antigravity/workspace/paichai_toilet_guide/assets/images_b64.py', 'w', encoding='utf-8') as f:
    f.write(f'AERIAL_B64 = "{b1}"\nVIEW_B64 = "{b2}"\n')
print('Base64 generated')
