"""Colour the black-only pose silhouettes with fabric taken from the colour cast drawing.
usage: python -I colorize.py <old_assets_dir> <new_cast.png> <out_dir>"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi

OLD, NEWCAST, OUT = sys.argv[1:]
SKIN = np.array([22, 30, 48], float)       # the dark navy used for faces/hands in the colour drawing
GOLD = np.array([214, 160, 40], float)
cast = np.array(Image.open(NEWCAST).convert('RGBA')).astype(float)

def patch(x, y, s=48):
    return cast[y - s // 2:y + s // 2, x - s // 2:x + s // 2, :3]

FAB = {'red': patch(230, 820), 'white': patch(560, 700), 'green': patch(1100, 820)}

def tile(p, h, w):
    # fabric = the patch's average colour plus a fine woven grain, no repeating pattern
    rng = np.random.default_rng(7)
    base = p.reshape(-1, 3).mean(0)
    grain = ndi.gaussian_filter(rng.normal(0, 1, (h, w)), .8)
    yy, xx = np.mgrid[0:h, 0:w]
    weave = .5 * np.sin(xx * 1.9) * np.sin(yy * 1.9)
    folds = ndi.gaussian_filter(rng.normal(0, 1, (h, w)), (h * .04, w * .012))
    folds = folds / (np.abs(folds).max() + 1e-6)
    v = 1 + .035 * grain + .02 * weave + .07 * folds
    return np.clip(base[None, None] * v[..., None], 0, 255)

def disk(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1]; return x * x + y * y <= r * r

def load_sil(img):
    a = np.array(img.convert('RGBA'))[..., 3].astype(float) / 255
    ys, xs = np.where(a > .5); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return a

def colour(alpha, fabric, kind, facing):
    """kind: 'girl' (dress, dark hair/hands/legs), 'father' (white thobe + ghutra, dark face),
    'man' (suit), 'woman' (dress + hat). facing: +1 face to the right, -1 left."""
    M = alpha > .5; h, w = M.shape
    dist = ndi.distance_transform_edt(M)
    # head = thickest point in the top 30% of the figure
    top = int(h * (.17 if kind == 'father' else .3)); d = dist.copy(); d[top:] = 0
    cy, cx = np.unravel_index(d.argmax(), d.shape); rh = d[cy, cx]
    r = max(3, int(h * .02))
    opened = ndi.binary_opening(M, structure=disk(r))
    opened = ndi.binary_propagation(opened, mask=M) & ndi.binary_opening(M, structure=disk(r))
    yy, xx = np.mgrid[0:h, 0:w]
    neck = cy + rh * 1.15
    head = ((xx - cx) ** 2 + (yy - cy) ** 2 <= (rh * 1.35) ** 2) & M
    if kind in ('man', 'woman'):
        rows = M.sum(1).astype(float); lo, hi = int(h * .1), int(h * .26)
        neck = lo + rows[lo:hi].argmin()
        head = M & (yy < neck)
    if kind == 'father':
        cloth = opened.copy()
        cloth |= head
        # thin ghutra drape behind the head belongs to the cloth too
        drape = M & ~opened & (yy < cy + rh * 7) & ((xx - cx) * facing < 0)
        cloth |= drape
        face = head & ((xx - cx) * facing > -rh * .15) & (yy > cy - rh * .45)
        cloth &= ~face
    else:
        cloth = opened & (yy > neck) & ~head
    # pointing/raised arms above the neck: keep the sleeve near the shoulder as cloth
    cloth = ndi.binary_opening(cloth, structure=disk(max(2, r // 2)))
    tex = tile(fabric, h, w)
    # soft shading: darker near edges, lighter in the middle, like the colour drawing
    shade = np.clip(.78 + .22 * np.minimum(1, dist / (rh * .9)), .7, 1.0)[..., None]
    img = np.where(cloth[..., None], tex * shade, SKIN)
    if kind in ('girl', 'father'):
        # gold trim on hems and cuffs (where cloth meets skin or ends)
        band = max(2, int(h * .012))
        edge_skin = cloth & ndi.binary_dilation(M & ~cloth, structure=disk(band))
        hem = cloth & ~ndi.binary_erosion(cloth | ~M, structure=np.ones((band * 2 + 1, 1), bool), border_value=1)
        trim = (edge_skin | hem) & (yy > neck)
        if kind == 'father':
            trim[:] = False   # plain white thobe
        img[trim] = GOLD * (.85 + .15 * np.sin(xx[trim] * .6) ** 2)[:, None]
    out = np.dstack([np.clip(img, 0, 255), alpha * 255]).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')

def sil(name, box=None):
    im = Image.open(f'{OLD}/{name}.png').convert('RGBA')
    return load_sil(im.crop(box) if box else im)

jobs = {
    'girlwalk': (sil('girlneutral'), 'red', 'girl', 1),
    'girlpoint': (sil('poses', (30, 60, 700, 980)), 'red', 'girl', 1),
    'girlfly': (sil('poses', (795, 105, 1536, 985)), 'red', 'girl', 1),
    'fatherpoint': (sil('fatherpoint'), 'white', 'father', 1),
}
for name, (a, fab, kind, facing) in jobs.items():
    colour(a, FAB[fab], kind, facing).save(f'{OUT}/{name}.png'); print('saved', name)

# The four 1930s passengers: period suits and a travelling dress.
pas = Image.open(f'{OLD}/passengers.png').convert('RGBA')
suits = [((96, 74, 52), 'man'), ((150, 120, 92), 'woman'), ((88, 92, 100), 'man'), ((60, 70, 96), 'man')]
for i, (rgb, kind) in enumerate(suits):
    a = load_sil(pas.crop((i * 384, 70, (i + 1) * 384, 945)))
    colour(a, np.full((8, 8, 3), rgb, float), kind, 1).save(f'{OUT}/p{i}.png'); print('saved p', i)
