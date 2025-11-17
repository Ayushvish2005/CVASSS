import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Utility Functions
# -----------------------------
def to_gray_float(img):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img.astype(np.float32) / 255.0


def flow_to_hsv(flow):
    u = flow[..., 0]
    v = flow[..., 1]

    mag = np.sqrt(u * u + v * v)
    ang = np.arctan2(v, u)  # (-pi, pi)

    # Hue = angle
    h = (ang + np.pi) / (2 * np.pi)

    # Normalize magnitude
    m = mag / (mag.max() + 1e-6)

    hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.float32)
    hsv[..., 0] = h
    hsv[..., 1] = 1.0
    hsv[..., 2] = m

    hsv = (hsv * 255).astype(np.uint8)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return rgb


# -----------------------------
# Lucas-Kanade Optical Flow
# -----------------------------
def lucas_kanade(prev, nxt, win_size=5, eps=1e-6):
    Ix = cv2.Sobel(prev, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(prev, cv2.CV_64F, 0, 1, ksize=3)
    It = nxt - prev

    kernel = np.ones((win_size, win_size))

    Ix2 = cv2.filter2D(Ix * Ix, -1, kernel)
    Iy2 = cv2.filter2D(Iy * Iy, -1, kernel)
    Ixy = cv2.filter2D(Ix * Iy, -1, kernel)
    Ixt = cv2.filter2D(Ix * It, -1, kernel)
    Iyt = cv2.filter2D(Iy * It, -1, kernel)

    det = Ix2 * Iy2 - Ixy * Ixy
    det = det + eps

    u = (-(Iy2 * Ixt - Ixy * Iyt)) / det
    v = (-(Ix2 * Iyt - Ixy * Ixt)) / det

    flow = np.stack((u, v), axis=2)
    return flow


# -----------------------------
# Horn-Schunck Optical Flow
# -----------------------------
def horn_schunck(prev, nxt, alpha=1.0, n_iter=200):
    Ix = cv2.Sobel(prev, cv2.CV_64F, 1, 0)
    Iy = cv2.Sobel(prev, cv2.CV_64F, 0, 1)
    It = nxt - prev

    h, w = prev.shape
    u = np.zeros((h, w), np.float32)
    v = np.zeros((h, w), np.float32)

    kernel = np.array(
        [[0, 1 / 4, 0], [1 / 4, 0, 1 / 4], [0, 1 / 4, 0]], dtype=np.float32
    )

    for _ in range(n_iter):
        u_avg = cv2.filter2D(u, -1, kernel)
        v_avg = cv2.filter2D(v, -1, kernel)

        denom = alpha**2 + Ix**2 + Iy**2
        denom[denom == 0] = 1e-6

        term = (Ix * u_avg + Iy * v_avg + It) / denom

        u = u_avg - Ix * term
        v = v_avg - Iy * term

    return np.stack((u, v), axis=2)


# -----------------------------
# Matplotlib Visualization
# -----------------------------
def show_flow(img1, img2, flow):
    hsv_img = flow_to_hsv(flow)

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].set_title("Optical Flow (HSV)")
    ax[0].imshow(hsv_img)
    ax[0].axis("off")

    # quiver
    ax[1].set_title("Quiver Plot")
    ax[1].imshow(img1, cmap="gray")
    step = 15
    y, x = np.mgrid[0 : flow.shape[0] : step, 0 : flow.shape[1] : step]
    u = flow[::step, ::step, 0]
    v = -flow[::step, ::step, 1]  # invert for display

    ax[1].quiver(x, y, u, v, color="red")
    ax[1].invert_yaxis()
    ax[1].axis("off")

    plt.tight_layout()
    plt.show()


# -----------------------------
# Main Entry
# -----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", nargs=2, help="Two images: prev next")
    parser.add_argument("--method", choices=["lk", "hs"], default="lk")

    args = parser.parse_args()

    if not args.images:
        print("Please provide two images: --images img1 img2")
        return

    img1 = cv2.imread(args.images[0])
    img2 = cv2.imread(args.images[1])

    if img1 is None or img2 is None:
        print("Error: Could not load images.")
        return

    g1 = to_gray_float(img1)
    g2 = to_gray_float(img2)

    if args.method == "lk":
        flow = lucas_kanade(g1, g2, win_size=7)
    else:
        flow = horn_schunck(g1, g2, alpha=1.0, n_iter=200)

    show_flow(g1, g2, flow)


if __name__ == "__main__":
    main()
