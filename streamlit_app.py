
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("삼각형 판별 및 그리기 (피타고라스의 정리 활용)")

a = st.number_input("변 a의 길이", min_value=1, step=1)
b = st.number_input("변 b의 길이", min_value=1, step=1)
c = st.number_input("변 c의 길이", min_value=1, step=1)

def is_triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a

def triangle_type(a, b, c):
    sides = sorted([a, b, c])
    x, y, z = sides  # x <= y <= z
    if not is_triangle(x, y, z):
        return "삼각형이 아닙니다."
    if z**2 == x**2 + y**2:
        return "직각삼각형"
    elif z**2 < x**2 + y**2:
        return "예각삼각형"
    else:
        return "둔각삼각형"

def draw_triangle(a, b, c):
    # 삼각형의 꼭짓점 좌표 계산 (A: (0,0), B: (a,0), C: (x,y))
    # 코사인 법칙 이용
    if not is_triangle(a, b, c):
        st.warning("삼각형이 아닙니다. 그림을 그릴 수 없습니다.")
        return
    # A(0,0), B(a,0)
    # C(x, y) 계산
    # x = (a^2 + c^2 - b^2) / (2a)
    # y = sqrt(c^2 - x^2)
    try:
        x = (a**2 + c**2 - b**2) / (2*a)
        y = np.sqrt(max(c**2 - x**2, 0))
    except Exception:
        st.warning("삼각형 좌표 계산 중 오류가 발생했습니다.")
        return
    points = np.array([[0,0], [a,0], [x,y], [0,0]])
    fig, ax = plt.subplots()
    ax.plot(points[:,0], points[:,1], 'bo-')
    ax.set_aspect('equal')
    ax.set_title('삼각형 그림')
    ax.grid(True)
    # 꼭짓점 라벨
    ax.text(0, 0, 'A', fontsize=12, color='red')
    ax.text(a, 0, 'B', fontsize=12, color='red')
    ax.text(x, y, 'C', fontsize=12, color='red')
    st.pyplot(fig)

if st.button("삼각형 판별 및 그리기"):
    result = triangle_type(a, b, c)
    st.success(f"결과: {result}")
    draw_triangle(a, b, c)
