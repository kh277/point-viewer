import streamlit as st
import matplotlib.pyplot as plt
from ConvexHull import ConvexHull
from CCWsort import sortCCW

INF = 1000000000000


# 기본 세팅
def init():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="좌표 그리기",
        page_icon="./images/logo.png")

    # 제목 설정
    st.title("다각형 시각화 툴")

    # 기본 CSS 문법 설정
    st.markdown("""
    <style>
        .gap15 { margin-bottom: 15px; }
        .gap30 { margin-bottom: 30px; }
        .gap60 { margin-bottom: 60px; }
        .font25 { font-size: 25px;
            color: blue; }
        .font15 { font-size: 15px; }
    </style>
    """, unsafe_allow_html=True)


# 좌표 및 처리 옵션 반환
def getOption():
    st.markdown("<div class='font25'>1. 좌표를 입력해주세요.", unsafe_allow_html=True)

    # 좌표 입력 필드
    pointString = st.text_area("(ex: (0, 0), (2, 3)인 경우 0 0 2 3으로 입력.)")

    # 옵션 선택 필드
    outline = st.radio('', ['점 표시', '외곽선 표시 (입력 순서대로)', '외곽선 표시 (반시계 방향 정렬)', '외곽선 표시 (+볼록 껍질)'])
    visual = st.button("시각화")

    return [pointString, [outline, visual]]


# 점이 올바르게 입력되었는지 확인
def checkPoint(point):
    # 점 체크
    if len(point) > 0:
        temp = list(map(float, point.split()))

        # 입력 좌표 수가 짝수인지 체크
        if len(temp) % 2 == 1 or len(temp) == 0:
            st.write("짝수 개의 좌표를 입력해주세요.")
            return []
        else:
            points = []
            for i in range(len(temp)//2):
                points.append((temp[i<<1], temp[i<<1 | 1]))
            return points
    else:
        st.write("좌표를 입력해주세요.")
        return []


def visualize(points, option):
    # 좌표 전처리
    hull = ConvexHull(points)
    sortedCCW = sortCCW(points)
    points.append(points[0])
    hull.append(hull[0])
    sortedCCW.append(sortedCCW[0])

    minX, maxX = INF, -INF
    minY, maxY = INF, -INF
    for x, y in points:
        minX = min(minX, x)
        maxX = max(maxX, x)
        minY = min(minY, y)
        maxY = max(maxY, y)

    # 그래프 기본 설정
    marginX = (maxX-minX) * 0.1
    marginY = (maxY-minY) * 0.1
    plt.figure(figsize=(10, 10))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(minX - marginX, maxX + marginX)
    plt.ylim(minY - marginY, maxY + marginY)
    plt.grid(color='gray', linestyle='--', linewidth=1)

    # 옵션에 따른 그래프 출력
    targetPoints = points
    lineStyle = '-'
    hullStyle = ''
    if option[0] == '점 표시':
        lineStyle = ''
    elif option[0] == '외곽선 표시 (입력 순서대로)':
        pass
    elif option[0] == '외곽선 표시 (반시계 방향 정렬)':
        targetPoints = sortedCCW
    elif option[0] == '외곽선 표시 (+볼록 껍질)':
        targetPoints = sortedCCW
        hullStyle = '-'

    # 외곽선 표시
    plt.plot(*zip(*targetPoints), marker='', linestyle=lineStyle, color='black', linewidth=3)

    # 볼록 껍질 표시
    plt.plot(*zip(*hull), linestyle=hullStyle, color='red', linewidth=1.5)

    # 점 표시
    plt.plot(*zip(*points), marker='o', linestyle='', color='black')

    st.pyplot(plt)


def main():
    # 1. 기본 세팅
    init()

    # 2. 점 입력
    pointString, option = getOption()

    # 3. 점이 올바르게 입력되었다면 그래프 시각화
    points = checkPoint(pointString)
    if len(points) > 0:
        visualize(points, option)


main()


# 실행 : streamlit run app.py