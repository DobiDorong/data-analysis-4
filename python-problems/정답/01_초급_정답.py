# =====================================================================
#  파이썬 초급 20문제 -- 정답
# =====================================================================
#  문제마다 「# [1-N]」 머리줄 아래가 그 문제의 정답입니다.
#  변수 이름은 한 예입니다. 출력이 칸과 같으면 이름은 달라도 됩니다.
#  정답 파일을 직접 돌리면 1-4·1-14 에서 입력을 묻습니다.
#  (1-4 는 1, 2 · 1-14 는 4500, 12000, 3000, 끝 을 차례로 넣으면 칸과 같습니다)
# =====================================================================

import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
# 위 두 줄은 문제 파일과 같습니다. data 폴더를 작업 폴더로 잡아 줍니다.


# [1-1] (1/20) 나누기 세 가지
total = 48500
people = 3
exact = total / people
each = total // people
left = total % people
print("그냥 나누기:", exact)
print("한 사람당:", each)
print("남는 금액:", left)
print()


# [1-2] (2/20) 자리 맞춘 영수증
mug_price = 8900
mug_count = 2
note_price = 3500
note_count = 3
pen_price = 900
pen_count = 5
total = mug_price * mug_count + note_price * note_count + pen_price * pen_count
print(f"머그 {mug_price:>6,} x {mug_count}개 {mug_price * mug_count:>8,}원")
print(f"노트 {note_price:>6,} x {note_count}개 {note_price * note_count:>8,}원")
print(f"볼펜 {pen_price:>6,} x {pen_count}개 {pen_price * pen_count:>8,}원")
print(f"합계 {total:>21,}원")
print()


# [1-3] (3/20) 폼에서 온 값 세 개
price_text = "4500"
box_text = "3.5"
rate_text = "0.07"
# int(box_text)   <- 돌려 보면 ValueError 가 나서 # 로 막아 두었습니다
price = int(price_text)
boxes = int(float(box_text))
rate = float(rate_text)
sales = price * boxes
fee = int(sales * rate)
print(f"상자: {box_text} -> {boxes}개")
print(f"판매 금액: {sales:,}원 / 수수료: {fee}원")
print("받을 금액: " + str(sales - fee) + "원")
print()


# [1-4] (4/20) 입력은 전부 문자열
first = input("1번 수량: ")
second = input("2번 수량: ")
print(f"그냥 더하면: {first + second}")
total = int(first) + int(second)
print(f"숫자로 더하면: {total}")
print()


# [1-5] (5/20) 가운데만 가리기
phone = "010-1234-5678"
email = "minjun@example.com"
front = phone[:4]
back = phone[8:]
print(f"전화: {front}****{back}")
print(f"메일: {email[:2]}****{email[6:]}")
print()


# [1-6] (6/20) 같은 메일인데 다르다
typed_email = "  MinJun @Example.COM "
saved_email = "minjun@example.com"
print(f"그대로: {typed_email == saved_email}")
step1 = typed_email.strip().lower()
print(f"양 끝 정리: {step1} / {step1 == saved_email}")
step2 = step1.replace(" ", "")
print(f"가운데까지: {step2} / {step2 == saved_email}")
print()


# [1-7] (7/20) 할 일 목록 고치기
todos = ["보고서 초안", "메일 회신", "회의록 정리", "비품 신청"]
print(f"3번째 할 일: {todos[2]}")
todos[1] = "메일 회신(완료)"
todos.append("출장 정산")
print(f"고친 목록: {todos}")
print(f"가나다순: {sorted(todos)}")
print()


# [1-8] (8/20) 영수증 한 줄 쪼개기
line = "  우유 ,2,2800"
parts = line.split(",")
name = parts[0].strip()
count = int(parts[1])
price = int(parts[2])
print(f"{name} {count}개 x {price:,}원 = {count * price:,}원")
print()


# [1-9] (9/20) 무료배송 기준을 딱 맞췄을 때
total = 12900 + 8900 + 8200
member = False
if total >= 30000 or member:
    fee = 0
else:
    fee = 3000
print(f"합계 {total:,}원 / 배송비 {fee:,}원")
print(f"결제 금액 {total + fee:,}원")
print()


# [1-10] (10/20) 택배 무게별 요금
weight = 10
if weight <= 5:
    print(f"{weight}kg: 3,000원")
elif weight <= 10:
    print(f"{weight}kg: 4,500원")
elif weight <= 20:
    print(f"{weight}kg: 6,000원")
else:
    print(f"{weight}kg: 접수 불가")
print()


# [1-11] (11/20) 일주일 점심값 합계
lunches = [8500, 9000, 7500, 12000, 8000, 6500, 11000]
total = 0
count = 0
for price in lunches:
    total = total + price
    count = count + 1
print(f"점심 {count}번 / 합계 {total:,}원")
print(f"하루 평균 {total / count:.1f}원")
print()


# [1-12] (12/20) 지저분한 명단 청소
raw_names = ["김민수", "", "  이서연 ", "   ", "박지훈 "]
names = []
for name in raw_names:
    name = name.strip()
    if name != "":
        names.append(name)
print(f"정리 전: {raw_names}")
print(f"정리 후: {names}")
print()


# [1-13] (13/20) 목표 금액까지 저축
saved = 10000
daily = 4000
goal = 30000
day = 0
while saved < goal:
    saved = saved + daily
    day = day + 1
print(f"{day}일 뒤 {saved:,}원")
print()


# [1-14] (14/20) 「끝」 칠 때까지 더하기
total = 0
count = 0
while True:
    text = input("금액: ")
    if text == "끝":
        break
    total = total + int(text)
    count = count + 1
print(f"영수증 {count}장 / 합계 {total:,}원")
print()


# [1-15] (15/20) 메뉴 가격표 고치기
menu = {"아메리카노": 4500, "라떼": 5000, "녹차": 4800}
print(f"라떼: {menu['라떼']:,}원")
menu["라떼"] = 5500
menu["레몬에이드"] = 6000
print(f"고친 가격표: {menu}")
print()


# [1-16] (16/20) 희망 요일 투표 세기
votes = ["화", "목", "화", "금", "목", "화", "월", "목"]
counts = {}
for day in votes:
    if day in counts:
        counts[day] = counts[day] + 1
    else:
        counts[day] = 1
for day in counts:
    print(f"{day}: {counts[day]}표")
print()


# [1-17] (17/20) 텀블러 할인 함수
def tumbler_price(price, cups):
    return (price - 300) * cups

americano = tumbler_price(4500, 2)
latte = tumbler_price(5000, 3)
print(f"아메리카노 2잔: {americano:,}원")
print(f"라떼 3잔: {latte:,}원")
print(f"합계: {americano + latte:,}원")
print()


# [1-18] (18/20) 장보기 메모 파일 읽기
num = 1
with open("shopping.txt", encoding="utf-8") as f:
    for line in f:
        print(f"{num}. {line.strip()}")
        num = num + 1
print()


# [1-19] (19/20) 간식 상자 몇 개
import math
people = 23
per_box = 6
boxes = math.ceil(people / per_box)
print(f"{boxes}상자 필요 / 남는 간식 {boxes * per_box - people}개")
print()


# [1-20] (20/20) 장보기 메모 합계 -- 종합
def line_amount(count, price):
    return count * price

total = 0
with open("shopping.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        amount = line_amount(int(parts[1]), int(parts[2]))
        total = total + amount
        print(f"{parts[0]} {amount:>6,}원")
print(f"총합계 {total:,}원")
