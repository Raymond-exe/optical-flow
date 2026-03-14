from lib.tools import tools
import cv2
import numpy as np

tool = tools()


scale = 0.1 # 0.01 -> 1.0, higher resolution = slower compute time
sensitivity = 4 # 1 = least sensitive, 4 = most sensitive
frameOverlay = True # set to False for just the optical flow data
interpolateFlow = False # set to True to smooth pixelated optical flow data


def create_flow_legend(radius=80):
    pad = 35
    size = (radius + pad) * 2
    center = size // 2
    legend = np.zeros((size, size, 3), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            dx, dy = x - center, y - center
            mag = np.sqrt(dx**2 + dy**2)
            if mag > radius:
                continue
            angle = np.arctan2(dy, dx)
            h = int((angle * 180 / np.pi / 2) % 180)
            v = int((mag / radius) * 255)
            legend[y, x] = [h, 255, v]

    bgr = cv2.cvtColor(legend, cv2.COLOR_HSV2BGR)
    cv2.circle(bgr, (center, center), radius, (180, 180, 180), 1)

    for deg in range(0, 360, 45):
        rad = np.deg2rad(deg)
        lx = int(center + (radius + 18) * np.cos(rad))
        ly = int(center + (radius + 18) * np.sin(rad))
        cv2.putText(bgr, f'{deg}', (lx - 10, ly + 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.32, (200, 200, 200), 1)

    return bgr


# Shows the direction/color wheel legend
legend = create_flow_legend()
lh, lw = legend.shape[:2]

cap = cv2.VideoCapture(0)
ret, prev = cap.read()
if not ret:
    raise RuntimeError('Failed to read from camera')

small_w = int(prev.shape[1] * scale)
small_h = int(prev.shape[0] * scale)
prev_gray = cv2.cvtColor(cv2.resize(prev, (small_w, small_h)), cv2.COLOR_BGR2GRAY).astype(np.float32)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_w = int(frame.shape[1] * scale)
    small_h = int(frame.shape[0] * scale)

    small = cv2.resize(frame, (small_w, small_h))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32)

    u, v = tool.optical_flow_lk(prev_gray, gray)

    magnitude, angle = cv2.cartToPolar(u.astype(np.float32), v.astype(np.float32))

    hsv = np.zeros((*u.shape, 3), dtype=np.uint8)
    hsv[..., 0] = (angle * 180 / np.pi / 2).astype(np.uint8)
    hsv[..., 1] = 255
    hsv[..., 2] = np.clip(cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX) * sensitivity, 0, 255).astype(np.uint8)

    upscaled = cv2.resize(
        cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR),
        (frame.shape[1], frame.shape[0]),
        interpolation=(cv2.INTER_LINEAR if interpolateFlow else cv2.INTER_NEAREST)
    )
    layered = cv2.max(frame, upscaled)

    if layered.shape[0] >= lh and layered.shape[1] >= lw:
        layered[-lh:, -lw:] = legend

    if (frameOverlay):
        cv2.imshow('Optical Flow Data (overlay)', layered)
    else:
        cv2.imshow('Optical Flow Data (raw)', upscaled)
    prev_gray = gray  # also make sure you're updating this each frame


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
