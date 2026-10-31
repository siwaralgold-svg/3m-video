import sys, json, numpy as np, cv2
from scipy import ndimage
src, outdir, name = sys.argv[1], sys.argv[2], sys.argv[3]
img = cv2.imread(src)  # BGR
img = cv2.resize(img, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[..., 0] * 100 / 255
# brown silhouettes are dark (L~30); ground/plants/wood are L>60
alpha = np.clip((58 - L) / (58 - 38), 0, 1)
hard = alpha > 0.5
# components on slightly dilated hard mask
lbl, n = ndimage.label(ndimage.binary_dilation(hard, iterations=2))
brown = np.median(img[alpha > 0.95], axis=0) if (alpha > 0.95).any() else np.array([44, 61, 91])
pieces = []
for i in range(1, n + 1):
    m = lbl == i
    area = int(m.sum())
    if area < 400: continue
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    pad = 4
    y0, x0 = max(0, y0 - pad), max(0, x0 - pad); y1, x1 = min(1920, y1 + pad), min(1080, x1 + pad)
    a = (alpha * ndimage.binary_dilation(m, iterations=3))[y0:y1, x0:x1]
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    rgba[..., :3] = brown
    rgba[..., 3] = (a * 255).astype(np.uint8)
    fn = f"{name}_p{len(pieces)}.png"
    cv2.imwrite(f"{outdir}/{fn}", rgba)
    pieces.append(dict(file=fn, x=int(x0), y=int(y0), w=int(x1 - x0), h=int(y1 - y0), area=area))
# plate: inpaint all brown
mask = (ndimage.binary_dilation(alpha > 0.05, iterations=4)).astype(np.uint8) * 255
plate = img.copy().astype(np.float32)
hm = mask > 0
for y in range(1920):
    row = hm[y]
    if not row.any(): continue
    x = 0
    while x < 1080:
        if row[x]:
            x0 = x
            while x < 1080 and row[x]: x += 1
            x1 = x
            lc = plate[y, x0 - 1].copy() if x0 > 0 else None
            rc = plate[y, x1].copy() if x1 < 1080 else None
            if lc is None: lc = rc
            if rc is None: rc = lc
            t = (np.arange(x0, x1) - x0 + 1) / (x1 - x0 + 1)
            plate[y, x0:x1] = lc[None] * (1 - t[:, None]) + rc[None] * t[:, None]
        else:
            x += 1
fill = cv2.GaussianBlur(plate, (1, 9), 0)
plate[hm] = fill[hm]
plate = np.clip(plate, 0, 255).astype(np.uint8)
cv2.imwrite(f"{outdir}/{name}_plate.jpg", plate, [cv2.IMWRITE_JPEG_QUALITY, 92])
print(json.dumps(dict(name=name, brown=[int(c) for c in brown[::-1]], pieces=sorted(pieces, key=lambda p: -p['area']))))
