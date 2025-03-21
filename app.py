import streamlit as st
import matplotlib.pyplot as plt
import ConvexHull as ch


# 기본 세팅
def init():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="좌표 그리기",
        page_icon="./images/logo.png")

    # 제목 설정
    st.title("Streamlit 응용 좌표그리기 예제")

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
    outline = st.radio('윤곽선 선택', ['외곽선 미표시', '외곽선 표시', '볼록 껍질'])
    visual = st.button("시각화")

    return [pointString, [outline, visual]]


# 점이 올바르게 입력되었는지 확인
def checkPoint(point: list):
    # 점 체크
    if len(point) > 0:
        temp = list(map(int, point.split()))

        # 입력 좌표 수가 짝수인지 체크
        if len(temp) % 2 == 1 or len(temp) == 0:
            st.write("좌표 개수를 짝수로 입력해주세요.")
            return [False, [], []]
        else:
            pointX = []
            pointY = []
            for i in range(len(temp)//2):
                pointX.append(temp[i*2])
                pointY.append(temp[i*2+1])

            return [True, pointX, pointY]
    else:
        st.write("좌표를 입력해주세요.")
        return [False, [], []]


def visualize(pointX, pointY, option: list):
    minX, maxX = min(pointX), max(pointX)
    minY, maxY = min(pointY), max(pointY)

    # 그래프 기본 설정
    plt.figure(figsize=(10, 10))
    plt.xlabel('X')
    plt.ylabel('Y')
    marginX = (maxX-minX) * 0.1
    marginY = (maxY-minY) * 0.1
    plt.xlim(minX - marginX, maxX + marginX)
    plt.ylim(minY - marginY, maxY + marginY)
    plt.grid(color='gray', linestyle='--', linewidth=1)

    # 옵션에 따른 좌표 출력
    if option[0] == '외곽선 미표시':
        plt.plot(pointX, pointY, marker='o', linestyle='', color='red')
    elif option[0] == '외곽선 표시':
        plt.plot(pointX, pointY, marker='o', linestyle='-', color='red')
    elif option[0] == '볼록 껍질':
        hullX, hullY = ch.ConvexHull(pointX, pointY)
        plt.plot(pointX, pointY, marker='o', linestyle='', color='red')
        plt.plot(hullX, hullY, marker='o', linestyle='-', color='blue')

    st.pyplot(plt)


def main():
    # 1. 기본 세팅
    init()

    # 2. 점 입력
    pointString, option = getOption()

    # 3. 점이 올바르게 입력되었다면 그래프 시각화
    isRight, pointX, pointY = checkPoint(pointString)
    if isRight == True:
        visualize(pointX, pointY, option)


main()


# 실행 : streamlit run app.py