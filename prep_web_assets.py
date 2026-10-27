import base64
import os

ASSETS = 'D:/Antigravity/workspace/paichai_toilet_guide/assets'

def get_b64(fname):
    p = os.path.join(ASSETS, fname)
    with open(p, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

a_b64 = get_b64('aerial_web.jpg')
v_b64 = get_b64('view_web.jpg')
n_b64 = get_b64('aerial_annotated_neon.jpg')
p_b64 = get_b64('poster_motion.jpg')

out_py = os.path.join(ASSETS, 'images_b64.py')
with open(out_py, 'w', encoding='utf-8') as f:
    f.write(f'AERIAL_B64 = "{a_b64}"\n')
    f.write(f'VIEW_B64 = "{v_b64}"\n')
    f.write(f'AERIAL_NEON_B64 = "{n_b64}"\n')
    f.write(f'POSTER_B64 = "{p_b64}"\n')

print(f'{out_py} generated successfully with all 4 base64 images.')
