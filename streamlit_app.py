
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

st.title("삼각형 판별 및 그리기 (피타고라스의 정리 활용)")

a = st.number_input("변 a의 길이", min_value=1, step=1)
b = st.number_input("변 b의 길이", min_value=1, step=1)
c = st.number_input("변 c의 길이", min_value=1, step=1)


def triangle_inequality_explanation(a, b, c):
    reasons = []
    if a + b <= c:
        reasons.append(f"a + b = {a} + {b} = {a+b} ≤ c = {c}")
    if a + c <= b:
        reasons.append(f"a + c = {a} + {c} = {a+c} ≤ b = {b}")
    if b + c <= a:
        reasons.append(f"b + c = {b} + {c} = {b+c} ≤ a = {a}")
    return reasons

def is_triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a


def triangle_type_and_explanation(a, b, c):
    sides = sorted([a, b, c])
    x, y, z = sides  # x <= y <= z
    explanation = ""
    if not is_triangle(x, y, z):
        reasons = triangle_inequality_explanation(a, b, c)
        explanation += "삼각형이 아닙니다.\n"
        if reasons:
            explanation += "삼각형이 되려면 각 변의 합이 다른 한 변보다 커야 합니다.\n"
            for r in reasons:
                explanation += f"- {r}\n"
        else:
            explanation += "입력값에 오류가 있습니다.\n"
        return "삼각형이 아닙니다.", explanation
    # 피타고라스의 정리 풀이
    explanation += f"가장 긴 변: {z}, 나머지 두 변: {x}, {y}\n"
    explanation += f"{z}² {'=' if z**2 == x**2 + y**2 else ('<' if z**2 < x**2 + y**2 else '>')} {x}² + {y}² = {x**2} + {y**2} = {x**2 + y**2}\n"
    if z**2 == x**2 + y**2:
        explanation += "→ 피타고라스의 정리에 의해 직각삼각형입니다."
        return "직각삼각형", explanation
    elif z**2 < x**2 + y**2:
        explanation += "→ 가장 긴 변의 제곱이 나머지 두 변의 제곱의 합보다 작으므로 예각삼각형입니다."
        return "예각삼각형", explanation
    else:
        explanation += "→ 가장 긴 변의 제곱이 나머지 두 변의 제곱의 합보다 크므로 둔각삼각형입니다."
        return "둔각삼각형", explanation

    # 삼각형의 꼭짓점 좌표 계산 (A: (0,0), B: (a,0), C: (x,y))
    # 코사인 법칙 이용
    if not is_triangle(a, b, c):
        st.warning("삼각형이 아닙니다. 그림을 그릴 수 없습니다.")
        return
    # 한글 폰트 설정
    font_path = "fonts/NanumGothic-Regular.ttf"
    fontprop = fm.FontProperties(fname=font_path)
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
    ax.set_title('삼각형 그림', fontproperties=fontprop)
    ax.grid(True)
    # 꼭짓점 라벨
    ax.text(0, 0, 'A', fontsize=12, color='red', fontproperties=fontprop)
    ax.text(a, 0, 'B', fontsize=12, color='red', fontproperties=fontprop)
    ax.text(x, y, 'C', fontsize=12, color='red', fontproperties=fontprop)
    st.pyplot(fig)


if st.button("삼각형 판별 및 그리기"):
    result, explanation = triangle_type_and_explanation(a, b, c)
    st.success(f"결과: {result}")
    st.info(f"풀이:\n{explanation}")
    draw_triangle(a, b, c)
