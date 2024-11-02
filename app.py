import streamlit as st
import matplotlib.pyplot as plt
import ConvexHull as ch


# 기본 세팅
def basic_settings():
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
    

# UI 세팅
def UserInterface():
    st.markdown("<div class='font25'>1. 좌표를 입력해주세요.", unsafe_allow_html=True)

    # 좌표 입력 필드
    point_input = st.text_area("(ex: (0, 0), (2, 3)인 경우 0 0 2 3으로 입력.)")
    
    # 옵션 선택 필드
    outline = st.radio('윤곽선 선택', ['외곽선 미표시', '외곽선 표시', '볼록 껍질'])
    visual = st.button("시각화")
    
    
    return [point_input, [outline, visual]]


# 점이 올바르게 입력되었는지 확인
def check_point(point: list):
    # 점 체크
    if len(point) > 0:
        temp = list(map(int, point.split()))
        
        # 짝수개 입력 체크
        if len(temp) % 2 == 1 or len(temp) == 0:
            st.write("좌표 개수를 짝수로 입력해주세요.")
            return [False, [], []]
        else:
            points_X = []
            points_Y = []
            for i in range(len(temp)//2):
                points_X.append(temp[i*2])
                points_Y.append(temp[i*2+1])

            return [True, points_X, points_Y]
    
    else:
        st.write("좌표를 입력해주세요.")
        return [False, [], []]


def visualize(points_X: list, points_Y: list, option: list):
    max_value = max(max(points_X), max(points_Y))
    
    plt.figure(figsize=(10, 10))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xticks(range(-1*max_value-3, max_value+3, 1))  # x축 눈금 설정
    plt.yticks(range(-1*max_value-3, max_value+3, 1))  # y축 눈금 설정
    plt.grid(color = 'gray', linestyle = '--', linewidth = 1)  # 그리드 설정
    plt.xlim(-1*max_value-3, max_value+3)  # x축 범위 설정
    plt.ylim(-1*max_value-3, max_value+3)  # y축 범위 설정
    
    # 윤곽선
    if option[0] == '외곽선 미표시':
        print("외곽선 미표시")
        plt.plot(points_X, points_Y, marker='o', linestyle='', color='red')  # 점과 선 그리기
    elif option[0] == '외곽선 표시':
        plt.plot(points_X, points_Y, marker='o', linestyle='-', color='red')  # 점과 선 그리기
    elif option[0] == '볼록 껍질':
        hull_X, hull_Y = ch.convex_hull(points_X, points_Y)
        plt.plot(points_X, points_Y, marker='o', linestyle='', color='red')  # 점과 선 그리기
        plt.plot(hull_X, hull_Y, marker='o', linestyle='-', color='blue')  # 점과 선 그리기
    
    # 그래프 표시
    st.pyplot(plt)
    
    
def main():
    # 1. 기본 세팅
    basic_settings()
    
    # 2. 점 입력
    point, option = UserInterface()
    
    # 3. 점이 올바르게 입력되었다면 그래프 시각화
    isRight, points_X, points_Y = check_point(point)
    if isRight == True:
        visualize(points_X, points_Y, option)
    


main()


# 실행 : streamlit run app.py