# =====================================================================
#  파이썬 중급 20문제 -- 정답
# =====================================================================
#  문제마다 「# [2-N]」 머리줄 아래가 그 문제의 정답입니다.
#  함수 이름·인자는 지문대로입니다. 다른 변수 이름은 한 예입니다.
#  정답을 직접 돌리면 2-10·2-11 에서 입력을 묻습니다.
#  (2-10 은 엔터만, 1111, 9876, 0000, 엔터만, 1234, 5555 를 차례로 넣으면 칸과 같습니다)
#  (2-11 은 아메리카노, 라떼, 아메리카노, 핫초코, 쿠키, 결제 를 차례로 넣으면 칸과 같습니다)
# =====================================================================

import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
# 위 두 줄은 문제 파일과 같습니다. data 폴더를 작업 폴더로 잡아 줍니다.


# [2-1] (1/20) 여러 줄 주문서 합산
memo = "아메리카노,2,4500\n라떼,1,5000\n쿠키,3,3200\n"
total = 0
count = 0
for line in memo.split("\n"):
    if line != "":
        parts = line.split(",")
        price = int(parts[2])
        amount = int(parts[1]) * price
        total = total + amount
        count = count + 1
        print(f"{parts[0]} {parts[1]}개 x {price:,}원 = {amount:,}원")
print(f"주문 {count}건 / 합계 {total:,}원")
print()


# [2-2] (2/20) 결시생이 섞인 평균
scores = ["88", "72", "", "95", "", "43"]
total = 0
taken = 0
for score in scores:
    if score != "":
        total = total + int(score)
        taken = taken + 1
everyone = len(scores)
print(f"결시까지 나눈 평균 {total / everyone:.1f}점 (분모 {everyone})")
print(f"결시를 뺀 평균 {total / taken:.1f}점 (분모 {taken})")
print(f"차이 {total / taken - total / everyone:.1f}점")
print()


# [2-3] (3/20) 평균을 함수로
class_1 = ["88", "72", "", "95", "", "43"]
class_2 = ["100", "90", "85"]
class_3 = ["", "", ""]
def average(scores):
    total = 0
    taken = 0
    for score in scores:
        if score != "":
            total = total + int(score)
            taken = taken + 1
    if taken == 0:
        return 0.0
    return total / taken

print(f"1반 평균 {average(class_1):.1f}점")
print(f"2반 평균 {average(class_2):.1f}점")
print(f"3반 평균 {average(class_3):.1f}점")
print()


# [2-4] (4/20) 가입 메일 정리와 검사
signup = [" KIM.Haneul@Example.COM ", "junseo@example.com", "   ", "jiwoo@example",
          "@example.com", "minjae@@example.com", "DAEUN@EXAMPLE.COM"]
def clean_email(raw):
    return raw.strip().lower()

def is_valid(email):
    if email.count("@") != 1:
        return False
    parts = email.split("@")
    if parts[0] == "":
        return False
    if "." in parts[1]:
        return True
    return False

def keep_valid(raw_list):
    valid = []
    for raw in raw_list:
        email = clean_email(raw)
        if is_valid(email):
            valid.append(email)
    return valid

passed = keep_valid(signup)
print(f"통과 {len(passed)}명 / 전체 {len(signup)}명")
for email in passed:
    print(email)
print()


# [2-5] (5/20) 주문 금액과 배송비
cart = [12000, 8000, 4500]
def order_total(prices, ship=3000, free_from=30000):
    goods = 0
    for price in prices:
        goods = goods + price
    if goods >= free_from:
        ship = 0
    return goods + ship

print(f"기본값 그대로: {order_total(cart):,}원")
print(f"무료 기준 20000: {order_total(cart, free_from=20000):,}원")
print(f"배송비 2500: {order_total(cart, ship=2500):,}원")
print(f"이름 없이 20000: {order_total(cart, 20000):,}원")
print()


# [2-6] (6/20) 할 일 진행률
todo_lines = ["[x] 회의실 예약", "[ ] 발표 자료 초안", "[X] 참석자 명단 확인",
              "  [ ] 간식 주문  ", "## 다음 주", "[x] 프로젝터 점검", "",
              "[ ] 안내 메일 보내기", "[ ] 교통편 확인"]
def progress(lines):
    done = 0
    total = 0
    first = "없음"
    for line in lines:
        line = line.strip()
        mark = line[:3]
        if mark == "[x]" or mark == "[X]":
            done = done + 1
            total = total + 1
        elif mark == "[ ]":
            total = total + 1
            if first == "없음":
                first = line[3:].strip()
    if total == 0:
        return 0, 0, 0.0, first
    return done, total, done / total * 100, first

done, total, rate, first = progress(todo_lines)
print(f"{done}/{total} 끝 ({rate:.1f}%) 다음 할 일: {first}")
done, total, rate, first = progress(["## 메모", ""])
print(f"{done}/{total} 끝 ({rate:.1f}%) 다음 할 일: {first}")
print()


# [2-7] (7/20) 가계부 분류별 합계
ledger = [("식비", 9500), ("교통", 2800), ("식비", 12000),
          ("문화", 18000), ("교통", 1450), ("식비", 4500)]
def sum_by_kind(rows):
    totals = {}
    for kind, amount in rows:
        if kind in totals:
            totals[kind] = totals[kind] + amount
        else:
            totals[kind] = amount
    return totals

totals = sum_by_kind(ledger)
top_kind = ""
top_amount = 0
for kind in totals:
    print(f"{kind} {totals[kind]:,}원")
    if totals[kind] > top_amount:
        top_kind = kind
        top_amount = totals[kind]
print(f"가장 많이 쓴 분류: {top_kind} ({top_amount:,}원)")
print()


# [2-8] (8/20) 메뉴에 없는 주문
menu = {"아메리카노": 4500, "라떼": 5000, "쿠키": 3200}
sale = {"라떼": 500, "쿠키": 700}
order = ["아메리카노", "쿠키", "핫초코", "라떼", "아메리카노"]
def receipt(order, menu, sale):
    total = 0
    for name in order:
        if name in menu:
            off = sale.get(name, 0)
            price = menu[name] - off
            total = total + price
            print(f"{name} {price:,}원 (할인 {off:,}원)")
        else:
            print(f"{name}: 메뉴에 없음")
    return total

print(f"합계 {receipt(order, menu, sale):,}원")
print()


# [2-9] (9/20) 반찬 판매량 순위
sales = {"멸치볶음": 42, "계란말이": 57, "시금치나물": 18, "장조림": 35, "어묵볶음": 49}
def top3(sales):
    pairs = []
    for name in sales:
        pairs.append((sales[name], name))
    ranked = sorted(pairs, reverse=True)
    return ranked[:3]

rank = 1
for count, name in top3(sales):
    print(f"{rank}위 {name} {count}개")
    rank = rank + 1
print()


# [2-10] (10/20) 로그인 3회 제한
password = "9876"
def login(password):
    tries = 0
    while tries < 3:
        typed = input("비밀번호: ")
        if typed == "":
            print("빈 줄은 세지 않습니다")
        elif typed == password:
            print("로그인 성공")
            return True
        else:
            tries = tries + 1
            print(f"틀렸습니다 ({tries}/3)")
    print("계정 잠금")
    return False

print(f"결과: {login(password)}")
print(f"결과: {login(password)}")
print()


# [2-11] (11/20) 카페 장바구니
menu = {"아메리카노": 4500, "라떼": 5000, "쿠키": 3200}
def take_order(menu):
    cart = {}
    while True:
        name = input("메뉴: ")
        if name == "결제":
            break
        if name in menu:
            cart[name] = cart.get(name, 0) + 1
        else:
            print(f"{name}: 메뉴에 없음")
    return cart

cart = take_order(menu)
total = 0
for name in cart:
    amount = menu[name] * cart[name]
    total = total + amount
    print(f"{name} x{cart[name]} = {amount:,}원")
print(f"합계 {total:,}원")
print()


# [2-12] (12/20) 대출일수에 섞인 글자
raw_days = ["14", " 7 ", "열흘", "", "5일"]
def split_days(values):
    numbers = []
    others = []
    for value in values:
        value = value.strip()
        if value.isdigit():
            numbers.append(int(value))
        else:
            others.append(value)
    return numbers, others

numbers, others = split_days(raw_days)
total = 0
for day in numbers:
    total = total + day
print(f"숫자로 바꾼 것: {numbers} / 합계 {total}일")
print(f"못 바꾼 것: {others}")
print()


# [2-13] (13/20) 방문 기록 더러운 줄
def read_visits(path):
    kept = []
    bad = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            line = line.strip()
            parts = line.split(",")
            if len(parts) == 3 and parts[2].strip() != "":
                kept.append(line)
            else:
                bad.append((no, line))
    return kept, bad

kept, bad = read_visits("visits.csv")
print(f"살린 줄 {len(kept)}개 / 버린 줄 {len(bad)}개")
for item in bad:
    print(f"{item[0]}번 줄: [{item[1]}]")
print()


# [2-14] (14/20) 버린 줄을 사유와 함께 로그로
def skip_reason(line):
    if len(line.split(",")) != 3:
        return "칸 수"
    return "빈 값"

def write_skipped(path, bad):
    with open(path, "w", encoding="utf-8") as f:
        for item in bad:
            f.write(f"{item[0]}: {skip_reason(item[1])}: {item[1]}\n")

kept, bad = read_visits("visits.csv")
write_skipped("visits_skipped.txt", bad)
print(f"{len(bad)}줄 썼습니다 -> visits_skipped.txt")
with open("visits_skipped.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [2-15] (15/20) 단어장 중복 걸러내기
def clean_wordbook(src, dst):
    words = {}
    no = 0
    with open(src, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            parts = line.strip().split(",")
            word = parts[0].strip().lower()
            if len(parts) != 3 or word in words:
                continue
            words[word] = f"{word},{parts[1].strip()},{parts[2].strip()}"
    with open(dst, "w", encoding="utf-8") as f:
        f.write("영어,뜻,맞힌횟수\n")
        for word in words:
            f.write(words[word] + "\n")
    return len(words), no - 1 - len(words)

kept, dropped = clean_wordbook("wordbook.csv", "wordbook_clean.csv")
print(f"남긴 단어 {kept}개 / 버린 줄 {dropped}개")
with open("wordbook_clean.csv", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [2-16] (16/20) 없는 파일은 다음 후보로
contact_files = ["contacts_today.csv", "contacts.csv", "contacts_old.csv"]
word_files = ["words_a.csv", "words_b.csv"]
def read_first(paths):
    for path in paths:
        if os.path.exists(path):
            count = 0
            with open(path, encoding="utf-8-sig") as f:
                for line in f:
                    count = count + 1
            return path, count
        print(f"{path} 없음 -> 다음 후보")
    return "", 0

path, count = read_first(contact_files)
print(f"쓴 파일 '{path}' / {count}줄")
path, count = read_first(word_files)
print(f"쓴 파일 '{path}' / {count}줄")
print()


# [2-17] (17/20) 택배 도착 예정일
import datetime
ship_days = [1, 2, 3, 6]
day_names = ["월", "화", "수", "목", "금", "토", "일"]
def arrival(order_date, days):
    arrive = order_date + datetime.timedelta(days=days)
    if arrive.weekday() == 5:
        arrive = arrive + datetime.timedelta(days=2)
    elif arrive.weekday() == 6:
        arrive = arrive + datetime.timedelta(days=1)
    return arrive

order_date = datetime.date(2026, 11, 26)
print(f"주문일 {order_date} ({day_names[order_date.weekday()]})")
for days in ship_days:
    arrive = arrival(order_date, days)
    print(f"배송 {days}일 -> {arrive} ({day_names[arrive.weekday()]})")
print()


# [2-18] (18/20) 메뉴별 매출 정산 표
menu_sales = {"아메리카노": 144000, "라떼": 85000, "쿠키": 38400, "케이크": 52000}
def print_report(sales):
    total = 0
    for name in sales:
        total = total + sales[name]
    print(f"{'매출':>7}{'비중':>5}  메뉴")
    print("-" * 28)
    for name in sales:
        share = sales[name] / total * 100
        print(f"{sales[name]:>9,}{share:>6.1f}%  {name}")
    print("-" * 28)
    print(f"{total:>9,}{100:>6.1f}%  합계")

print_report(menu_sales)
print()


# [2-19] (19/20) 어제 명단 오늘 명단
yesterday = ["김민수", "이서연", "박지훈", "정하늘"]
today = [" 이서연", "박지훈 ", "최유진", "이서연", "한도윤", "최유진 "]
def clean_names(names):
    result = []
    for name in names:
        name = name.strip()
        if name not in result:
            result.append(name)
    return result

def only_in(a, b):
    result = []
    for name in a:
        if name not in b:
            result.append(name)
    return result

old = clean_names(yesterday)
new = clean_names(today)
print(f"어제: {old}")
print(f"오늘: {new}")
print(f"새로 온 사람: {only_in(new, old)}")
print(f"빠진 사람: {only_in(old, new)}")
print()


# [2-20] (20/20) 대출 기록 집계 -- 종합
def read_loans(path):
    counts = {}
    days = {}
    dropped = 0
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            parts = line.strip().split(",")
            if len(parts) == 4 and parts[2].strip().isdigit():
                book = parts[0].strip()
                counts[book] = counts.get(book, 0) + 1
                days[book] = days.get(book, 0) + int(parts[2])
            else:
                dropped = dropped + 1
    return counts, days, dropped

def write_report(path, counts, days):
    with open(path, "w", encoding="utf-8") as f:
        f.write("도서별 대출 횟수와 총 일수\n")
        for book in counts:
            f.write(f"{counts[book]}회 {days[book]:>3}일  {book}\n")

counts, days, dropped = read_loans("loans.csv")
write_report("loans_report.txt", counts, days)
print(f"도서 {len(counts)}종 / 버린 줄 {dropped}줄")
with open("loans_report.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
