# 2차원 벡터의 외적값을 이용해 회전 방향 판별
def CCW(a, b, c):
    # 양수(반시계), 0(일직선), 음수(시계)
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


# Convex Hull 구하기
def convex_hull(points_X, points_Y):
    
    graph = [(points_Y[i], points_X[i]) for i in range(len(points_X))]
    
    # x좌표 오름차순으로 정렬
    graph = sorted(set(graph))

    # 아래쪽 Hull을 구함
    lower = []
    for i in graph:
        # 반시계 방향이 아닐 경우 마지막 점 제거
        while len(lower) >= 2 and CCW(lower[-2], lower[-1], i) <= 0:
            lower.pop()
        lower.append(i)
        
    # 위쪽 Hull을 구함
    upper = []
    for i in reversed(graph):
        # 반시계 방향이 아닐 경우 마지막 점 제거
        while len(upper) >= 2 and CCW(upper[-2], upper[-1], i) <= 0:
            upper.pop()
        upper.append(i)
    
    # 아래쪽 Hull과 위쪽 Hull을 중복제거하여 합치기
    result = lower[:-1] + upper[:-1]
    result_X = [result[i%len(result)][1] for i in range(len(result)+1)]
    result_Y = [result[i%len(result)][0] for i in range(len(result)+1)]
    
    return result_X, result_Y