from ConvexHull import CCW as CCW
import functools


def dist(A, B):
    return (A[0] - B[0])**2 + (A[1] - B[1])**2


def sortCCW(points):
    if len(points) <= 2:
        return sorted(points)

    # 제일 하단에 있는 점을 pivot으로 설정
    pivot = min(points, key= lambda x: (x[1], x[0]))

    # pivot을 리스트에서 분리
    others = [p for p in points if p != pivot]

    def cmp(A, B):
        res = CCW(pivot, A, B)
        # 반시계 방향이면 A가 우선
        if res > 0:
            return -1
        # 시계 방향이면 B가 우선
        elif res < 0:
            return 1
        # 일직선이라면 가까운 순서대로 정렬
        if dist(pivot, A) < dist(pivot, B):
            return -1
        return 1

    # 정렬 수행
    others.sort(key=functools.cmp_to_key(cmp))

    return [pivot] + others
