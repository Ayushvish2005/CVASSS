

# 🌀 Optical Flow Estimation: Lucas–Kanade & Horn–Schunck

This Python project implements and visualizes two classical **optical flow algorithms from first principles**:

* **Lucas–Kanade (LK)** — A *local* optical flow method using least-squares in small windows.
* **Horn–Schunck (HS)** — A *global* optical flow method using energy minimization with smoothness constraints.

Both methods operate on two consecutive image frames and produce two types of visualizations:

* **HSV color-encoded optical flow**
* **Quiver (vector) plots**

### Using The Lucas–Kanade Method

![alt text](lk.png)


### Using The Horn–Schunck Method

![alt text](hs.png)


---

## 📘 Algorithms Implemented

---

### **1. Lucas–Kanade (Local Method)**

A local optical flow method assuming constant motion inside a neighborhood (e.g., a (7 \times 7) window).

#### **Key Idea**

Solve the optical flow constraint equation:

[
I_x u + I_y v + I_t = 0
]

over all pixels in the window using **least squares**.

#### **Pros**

* Simple and computationally fast
* Works well on textured regions and corners
* Robust to noise within the window

#### **Cons**

* Fails on flat, texture-less regions (aperture problem)
* Sensitive to large motion unless pyramids are used

---

### **2. Horn–Schunck (Global Method)**

A dense optical flow method that computes a smooth motion vector ((u, v)) for every pixel.

#### **Key Idea**

Minimize a global energy functional:

[
E = \iint \left( (I_x u + I_y v + I_t)^2 + \alpha^2 (|\nabla u|^2 + |\nabla v|^2) \right) dx,dy
]

#### **Pros**

* Produces a globally smooth and dense flow field
* Works well in texture-less areas

#### **Cons**

* Can oversmooth sharp motion boundaries
* Higher computational cost due to iterative updates

---

## 🧠 Core Mathematical Concepts

Optical flow relies on the **Brightness Constancy** assumption:

[
I(x, y, t) \approx I(x + dx, y + dy, t + dt)
]

Using a first-order Taylor expansion, we obtain the **Optical Flow Constraint Equation**:

[
I_x u + I_y v + I_t = 0
]

This is *one equation with two unknowns*, so additional assumptions are required.

---

### **Lucas–Kanade: Least-Squares Solution**

LK assumes ((u, v)) are constant inside an (N \times N) window, giving an overdetermined system:

[
A
\begin{bmatrix}
u \
v
\end{bmatrix} = -b
]

Where:

[
A =
\begin{bmatrix}
I_{x_1} & I_{y_1} \
I_{x_2} & I_{y_2} \
\vdots & \vdots
\end{bmatrix},
\quad
b =
\begin{bmatrix}
I_{t_1}  \
I_{t_2}  \
\vdots
\end{bmatrix}
]

Solution:

[
\begin{bmatrix}
u \
v
\end{bmatrix}
=============

-(A^T A)^{-1} (A^T b)
]

This is exactly what the `lucas_kanade()` function computes.

---

### **Horn–Schunck: Global Energy Minimization**

The HS method minimizes:

[
E = (I_x u + I_y v + I_t)^2 + \alpha^2 (|\nabla u|^2 + |\nabla v|^2)
]

Using calculus of variations, we obtain the iterative update equations:

[
u^{k+1} = \bar u^k - I_x \frac{I_x \bar u^k + I_y \bar v^k + I_t}{\alpha^2 + I_x^2 + I_y^2}
]

[
v^{k+1} = \bar v^k - I_y \frac{I_x \bar u^k + I_y \bar v^k + I_t}{\alpha^2 + I_x^2 + I_y^2}
]

Where (\bar u), (\bar v) are neighborhood averages (smoothed using a 4-connected kernel).

This is precisely what `horn_schunck()` implements.

---

## 📦 Requirements

Install dependencies:

```bash
pip install opencv-python numpy matplotlib
```

Required libraries:

* **OpenCV (cv2)** — for gradients and image loading
* **NumPy** — numerical operations
* **Matplotlib** — visualizations

---

## 🚀 How to Run

The script requires two sequential frames as input.

### **Syntax**

```bash
python3 main.py --images <image1_path> <image2_path> [--method <lk|hs>]
```

### **Arguments**

| Argument   | Description                                                   |
| ---------- | ------------------------------------------------------------- |
| `--images` | **(Required)** Path to the two input images (frame1, frame2). |
| `--method` | Which algorithm to run: `lk` (default) or `hs`.               |

---

## 📝 Examples

### **Lucas–Kanade (Default)**

```bash
python3 main.py --images frame10.png frame11.png
```

OR explicitly:

```bash
python3 main.py --images frame10.png frame11.png --method lk
```

### **Horn–Schunck**

```bash
python3 main.py --images frame10.png frame11.png --method hs
```

---

## 📊 Output Visualizations

On execution, a Matplotlib window appears with two plots:

### **1. Optical Flow (HSV)**

* **Hue (color):** Motion direction
* **Value (brightness):** Motion magnitude
* **Black:** No motion

### **2. Quiver Plot**

* Arrows represent motion direction
* Arrow length represents magnitude
* Overlaid on grayscale frame

### Example Output (Lucas–Kanade)

*(Insert your provided image here if desired)*

---

## 📁 Project Structure

```
.
├── main.py               # Main script: Lucas-Kanade + Horn-Schunck
├── frame10.png           # Example input frame (optional)
├── frame11.png           # Example input frame (optional)
└── README.md             # Documentation
```

---

## 🎓 Use Cases

* Computer Vision lab assignments
* Motion estimation in videos
* Object tracking
* Visual odometry
* Video stabilization
* Learning classical optical flow

---
