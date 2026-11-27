# =====================================================================
#  파이썬 고급 20문제 -- 정답
# =====================================================================
#  문제마다 「# [3-N]」 머리줄 아래가 그 문제의 정답입니다.
#  함수 이름·인자·돌려줄 값 모양은 지문대로입니다. 다른 변수 이름은 한 예입니다.
#  정답을 직접 돌리면 3-11·3-12 에서 입력을 묻습니다.
#  (넣을 값은 문제 파일 3-11·3-12 「받는 것)」 의 키보드 입력 줄에 차례대로 적혀 있습니다)
# =====================================================================

import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
# 위 두 줄은 문제 파일과 같습니다. data 폴더를 작업 폴더로 잡아 줍니다.


# [3-1] (1/20) 앱 로그 오류 요약
def read_log(path):
    records = []
    broken = []
    no = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            no = no + 1
            line = line.strip()
            if line == "":
                continue
            parts = line.split("|")
            if len(parts) != 3:
                broken.append((no, line))
                continue
            records.append((parts[1].strip(), parts[2].strip()))
    return records, broken

def count_levels(records):
    counts = {}
    for level, message in records:
        counts[level] = counts.get(level, 0) + 1
    return counts

def top_message(records, level):
    counts = {}
    for rec_level, message in records:
        if rec_level == level:
            counts[message] = counts.get(message, 0) + 1
    best = ""
    best_count = 0
    for message in counts:
        if counts[message] > best_count:
            best = message
            best_count = counts[message]
    return best, best_count

records, broken = read_log("app.log")
levels = count_levels(records)
print(f"INFO {levels.get('INFO', 0)}건 / WARN {levels.get('WARN', 0)}건 / ERROR {levels.get('ERROR', 0)}건")
print(f"형식이 깨진 줄 {len(broken)}줄")
for no, line in broken:
    print(f"  {no}번 줄: {line}")
for level in ["WARN", "ERROR"]:
    message, count = top_message(records, level)
    print(f"가장 많은 {level}: {message} ({count}건)")
print()


# [3-2] (2/20) 모임 일정 메모를 CSV로
def is_date(text):
    parts = text.split("-")
    if len(parts) != 3:
        return False
    if len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2:
        return parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()
    return False

def parse_memo(path):
    rows = []
    errors = []
    no = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            no = no + 1
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            cells = line.split("/")
            if len(cells) != 4:
                errors.append((no, "칸 수", line))
                continue
            date = cells[0].strip()
            fee = cells[3].strip()
            if fee == "무료":
                fee = "0"
            if not is_date(date):
                errors.append((no, "날짜", line))
            elif not fee.isdigit():
                errors.append((no, "회비", line))
            else:
                rows.append([date, cells[1].strip(), cells[2].strip(), int(fee)])
    return rows, errors

def write_schedule(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("날짜,모임,장소,회비\n")
        for row in rows:
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")

def write_errors(path, errors):
    with open(path, "w", encoding="utf-8") as f:
        for no, reason, line in errors:
            f.write(f"{no}: {reason}: {line}\n")

rows, errors = parse_memo("schedule_memo.txt")
write_schedule("schedule.csv", rows)
write_errors("schedule_errors.txt", errors)
monthly = {}
for row in rows:
    month = row[0][:7]
    monthly[month] = monthly.get(month, 0) + row[3]
print(f"일정 {len(rows)}건 / 오류 {len(errors)}건")
for month in monthly:
    print(f"{month} 회비 {monthly[month]:,}원")
for path in ["schedule.csv", "schedule_errors.txt"]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            print(line.strip())
print()


# [3-3] (3/20) 회원 명단 정제
def clean_email(text):
    return text.strip().lower()

def read_members(path):
    kept = []
    bad = []
    seen = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            line = line.strip()
            if no == 1 or line == "":
                continue
            cells = line.split(",")
            if len(cells) != 4:
                bad.append((no, "칸 수", line))
                continue
            email = clean_email(cells[1])
            if "@" not in email:
                bad.append((no, "메일", line))
                continue
            try:
                point = int(cells[3])
            except ValueError:
                bad.append((no, "포인트", line))
                continue
            if email in seen:
                bad.append((no, "중복", line))
                continue
            seen.append(email)
            city = cells[2].strip()
            if city == "":
                city = "미정"
            kept.append([cells[0].strip(), email, city, point])
    return kept, bad

def write_members(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("이름,메일,도시,포인트\n")
        for row in rows:
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")

kept, bad = read_members("members.csv")
write_members("members_clean.csv", kept)
print(f"살린 회원 {len(kept)}명 / 버린 줄 {len(bad)}줄")
for no, reason, line in bad:
    print(f"  {no}: {reason}: {line}")
with open("members_clean.csv", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-4] (4/20) 전화번호 표준화
samples = ["031-123-4567", "+82 10-2345-6789", "(010) 3456 7890", "010-123-456"]
def format_phone(text):
    digits = ""
    for ch in text:
        if ch.isdigit():
            digits = digits + ch
    if len(digits) == 12 and digits[:2] == "82":
        digits = "0" + digits[2:]
    if len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return ""

def fix_contacts(src, dst):
    rows = []
    problems = []
    no = 0
    with open(src, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            cells = line.strip().split(",")
            if no == 1 or len(cells) != 3:
                continue
            name = cells[0].strip()
            phone = format_phone(cells[1])
            group = cells[2].strip()
            if group == "":
                group = "미지정"
            if phone == "":
                problems.append((name, cells[1].strip()))
            else:
                rows.append(f"{name},{phone},{group}")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("이름,전화,그룹\n")
        for row in rows:
            f.write(row + "\n")
    return len(rows), problems

for text in samples:
    phone = format_phone(text)
    if phone == "":
        phone = "확인 필요"
    print(f"{text} -> {phone}")
count, problems = fix_contacts("contacts.csv", "contacts_fixed.csv")
print(f"저장 {count}명 / 확인 필요 {len(problems)}명")
for name, raw in problems:
    print(f"  {name}: [{raw}]")
with open("contacts_fixed.csv", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-5] (5/20) 할 일 JSON 불러와 고쳐 저장
import json
done_ids = [2, 4, 7]
new_titles = ["관리비 영수증 정리", " 우유 사기 ", "세탁소 들르기"]
def next_id(todos):
    biggest = 0
    for todo in todos:
        if todo["id"] > biggest:
            biggest = todo["id"]
    return biggest + 1

def mark_done(todos, ids):
    missing = []
    for todo_id in ids:
        found = False
        for todo in todos:
            if todo["id"] == todo_id:
                todo["done"] = True
                found = True
        if not found:
            missing.append(todo_id)
    return missing

def add_todos(todos, titles):
    skipped = []
    for title in titles:
        title = title.strip()
        exists = False
        for todo in todos:
            if todo["title"] == title:
                exists = True
        if exists:
            skipped.append(title)
        else:
            todos.append({"id": next_id(todos), "title": title, "done": False})
    return skipped

with open("todos.json", encoding="utf-8") as f:
    todos = json.load(f)
missing = mark_done(todos, done_ids)
skipped = add_todos(todos, new_titles)
with open("todos_after.json", "w", encoding="utf-8") as f:
    json.dump(todos, f, ensure_ascii=False, indent=2)
print(f"없는 번호: {missing}")
print(f"이미 있는 제목: {skipped}")
with open("todos_after.json", encoding="utf-8") as f:
    saved = json.load(f)
for todo in saved:
    mark = " "
    if todo["done"]:
        mark = "v"
    print(f"[{mark}] {todo['id']} {todo['title']}")
no = 0
with open("todos_after.json", encoding="utf-8") as f:
    for line in f:
        no = no + 1
        if no > 5:
            break
        print(line.replace("\n", ""))
print()


# [3-6] (6/20) 가게 설정 파일 로더
DEFAULTS = {"store_name": "우리 가게", "open_hour": 9, "close_hour": 21,
            "delivery_fee": 3000, "free_delivery_min": 20000, "notice": "없음"}
NUMBER_KEYS = ["open_hour", "close_hour", "delivery_fee", "free_delivery_min"]

def split_setting(line):
    parts = line.split("=")
    return parts[0].strip(), parts[1].strip()

def load_config(path, defaults, number_keys):
    config = defaults.copy()
    warnings = []
    no = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            no = no + 1
            line = line.strip()
            if line == "" or line[:1] == "#":
                continue
            if "=" not in line:
                warnings.append(f"{no}번 줄: = 없음 [{line}]")
                continue
            key, value = split_setting(line)
            if key in number_keys:
                if value.isdigit():
                    value = int(value)
                else:
                    warnings.append(f"{no}번 줄: {key} 숫자 아님 [{value}] -> 기본값 {defaults[key]}")
                    continue
            config[key] = value
    return config, warnings

config, warnings = load_config("store.cfg", DEFAULTS, NUMBER_KEYS)
for key in config:
    print(f"{key} = {config[key]}")
print(f"경고 {len(warnings)}건")
for warning in warnings:
    print(warning)
hours = config["close_hour"] - config["open_hour"]
print(f"영업 {hours}시간 ({config['open_hour']}시 ~ {config['close_hour']}시)")
print(f"DEFAULTS 그대로: open_hour = {DEFAULTS['open_hour']}")
print()


# [3-7] (7/20) 일자별 파일 한 번에 합치기
def csv_names(folder):
    names = []
    for name in sorted(os.listdir(folder)):
        if name.endswith(".csv"):
            names.append(name)
    return names

def read_rows(path):
    rows = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            line = line.strip()
            if no > 1 and line != "":
                rows.append(line)
    return rows

def merge_daily(folder, out_path):
    counts = {}
    total = 0
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("날짜,품목,수량,금액\n")
        for name in csv_names(folder):
            date = name.replace(".csv", "")
            rows = read_rows(folder + "/" + name)
            counts[name] = len(rows)
            for row in rows:
                out.write(f"{date},{row}\n")
                total = total + int(row.split(",")[2])
    return counts, total

counts, total = merge_daily("daily", "daily_all.csv")
merged = 0
for name in counts:
    print(f"{name} {counts[name]}줄")
    merged = merged + counts[name]
print(f"합친 줄 {merged}개 / 매출 합계 {total:,}원 -> daily_all.csv")
with open("daily_all.csv", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-8] (8/20) 연체 보고서
WORD_DAYS = {"열흘": 10, "보름": 15}

def to_days(text):
    text = text.strip()
    if text.isdigit():
        return int(text)
    return WORD_DAYS.get(text, -1)

def overdue_days(days, renewals):
    late = days - (14 + renewals * 7)
    if late > 0:
        return late
    return 0

def sum_overdue(path):
    totals = {}
    count = 0
    unknown = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            line = line.strip()
            if no == 1 or line == "":
                continue
            parts = line.split(",")
            if len(parts) != 4 or to_days(parts[2]) == -1:
                unknown.append(no)
                continue
            late = overdue_days(to_days(parts[2]), int(parts[3]))
            if late > 0:
                email = parts[1].strip().lower()
                totals[email] = totals.get(email, 0) + late
                count = count + 1
    return totals, count, unknown

def write_report(path, totals, count, unknown):
    pairs = []
    for email in totals:
        pairs.append((totals[email], email))
    rank = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"연체 {count}건 / 회원 {len(totals)}명 / 확인 필요 줄 {unknown}\n")
        for pair in sorted(pairs, reverse=True):
            rank = rank + 1
            f.write(f"{rank}위 {pair[0]:>2}일 {pair[0] * 100:>5,}원  {pair[1]}\n")
    return rank + 1

totals, count, unknown = sum_overdue("loans_nov.csv")
written = write_report("overdue_report.txt", totals, count, unknown)
print(f"{written}줄 썼습니다 -> overdue_report.txt")
with open("overdue_report.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-9] (9/20) 열람실 날짜별 방문 요약
def time_text(minutes):
    if minutes < 60:
        return f"{minutes}분"
    return f"{minutes // 60}시간 {minutes % 60}분"

def load_visits(path):
    visits = []
    dropped = 0
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            parts = line.strip().split(",")
            if len(parts) == 3 and parts[2].strip().isdigit():
                visits.append((parts[0].strip(), parts[1].strip().lower(), int(parts[2])))
            else:
                dropped = dropped + 1
    return visits, dropped

def by_date(visits):
    counts = {}
    minutes = {}
    seen = []
    dupes = 0
    for date, email, stay in visits:
        if (date, email) in seen:
            dupes = dupes + 1
            continue
        seen.append((date, email))
        counts[date] = counts.get(date, 0) + 1
        minutes[date] = minutes.get(date, 0) + stay
    return counts, minutes, dupes

visits, dropped = load_visits("visits.csv")
counts, minutes, dupes = by_date(visits)
people = 0
total = 0
for date in counts:
    print(f"{date}  {counts[date]}명  {time_text(minutes[date])}")
    people = people + counts[date]
    total = total + minutes[date]
print(f"합계 {people}명  {time_text(total)}")
print(f"뺀 줄 {dropped}줄 / 겹친 기록 {dupes}줄")
print()


# [3-10] (10/20) 게시판 페이지 나누기
import math

def load_posts(path):
    notice = ""
    posts = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) != 4:
                continue
            if parts[3] == "공지":
                notice = parts[2]
            elif parts[3] == "공개":
                posts.append((parts[1], int(parts[0]), parts[2]))
    return notice, sorted(posts, reverse=True)

def page_count(posts, size):
    return math.ceil(len(posts) / size)

def show_page(notice, posts, page, size):
    total = page_count(posts, size)
    if page < 1 or page > total:
        print(f"[{page}쪽] 없는 쪽입니다 (전체 {total}쪽)")
    else:
        print(f"[{page}/{total}쪽] 글 {len(posts)}개")
        print(f"  [공지] {notice}")
        start = (page - 1) * size
        for date, no, title in posts[start:start + size]:
            print(f"  {no:>3}  {date}  {title}")

notice, posts = load_posts("posts.txt")
for page in [1, 3, 4, 0]:
    show_page(notice, posts, page, 4)
print()


# [3-11] (11/20) 가입 입력 검증기
def load_emails(path):
    emails = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            parts = line.split(",")
            if no > 1 and len(parts) >= 2:
                emails.append(parts[1].strip().lower())
    return emails

def ask_email(emails):
    while True:
        email = input("메일: ").strip().lower()
        if "@" not in email:
            print("  다시 입력: 메일 모양이 아닙니다")
        elif email in emails:
            print("  다시 입력: 이미 가입한 메일입니다")
        else:
            return email

def ask_point():
    while True:
        text = input("포인트: ")
        try:
            point = int(text)
        except ValueError:
            print("  다시 입력: 포인트는 숫자로 적어 주세요")
            continue
        if point < 0:
            print("  다시 입력: 포인트는 0 이상이어야 합니다")
        else:
            return point

def save_members(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("이름,메일,포인트\n")
        for row in rows:
            f.write(row + "\n")

emails = load_emails("members.csv")
rows = []
while True:
    name = input("이름(빈 줄이면 끝): ").strip()
    if name == "":
        break
    email = ask_email(emails)
    point = ask_point()
    emails.append(email)
    rows.append(f"{name},{email},{point}")
save_members("new_members.csv", rows)
print(f"새 회원 {len(rows)}명 -> new_members.csv")
with open("new_members.csv", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-12] (12/20) 재고 출고 콘솔
def load_stock(path):
    stock = {}
    safety = {}
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            parts = line.strip().split(",")
            if no == 1 or len(parts) != 3:
                continue
            stock[parts[0]] = int(parts[1])
            safety[parts[0]] = int(parts[2])
    return stock, safety

def ship(stock, safety, item, text):
    try:
        count = int(text)
    except ValueError:
        count = 0
    if count < 1:
        return f"수량은 1 이상의 정수로: {text.strip()}"
    if count > stock[item]:
        return f"재고 부족: {item} 남은 {stock[item]}개"
    stock[item] = stock[item] - count
    message = f"출고: {item} {count}개, 남은 {stock[item]}개"
    if stock[item] < safety[item]:
        message = message + f" (안전재고 {safety[item]}개 미만)"
    return message

def save_stock(path, stock, safety):
    with open(path, "w", encoding="utf-8") as f:
        f.write("품목,재고,안전재고\n")
        for item in stock:
            f.write(f"{item},{stock[item]},{safety[item]}\n")

stock, safety = load_stock("stock.csv")
while True:
    item = input("품목: ").strip()
    if item == "끝":
        break
    if item not in stock:
        print(f"  없는 품목입니다: {item}")
        continue
    print("  " + ship(stock, safety, item, input("수량: ")))
save_stock("stock_after.csv", stock, safety)
print("stock_after.csv 에 저장했습니다")
with open("stock_after.csv", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-13] (13/20) 사진 파일 이름 정리 계획
def find_date(name):
    digits = ""
    for ch in name:
        if ch.isdigit():
            digits = digits + ch
    return digits[:4] + "-" + digits[4:6] + "-" + digits[6:8]

def new_name(old, plan):
    ext = old.split(".")[-1].lower()
    date = find_date(old)
    name = f"{date}.{ext}"
    number = 1
    while name in plan:
        number = number + 1
        name = f"{date}_{number}.{ext}"
    return name

def make_plan(path):
    plan = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            old = line.strip()
            if old != "":
                new = new_name(old, plan)
                plan[new] = old
    return plan

plan = make_plan("photo_list.txt")
with open("rename_plan.txt", "w", encoding="utf-8") as f:
    for new in plan:
        f.write(f"{plan[new]} -> {new}\n")
print(f"계획 {len(plan)}건 -> rename_plan.txt")
with open("rename_plan.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-14] (14/20) 반납 안내문 채우기
def load_names(path):
    names = {}
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            parts = line.strip().split(",")
            if no > 1 and len(parts) == 4:
                names[parts[1].strip().lower()] = parts[0].strip()
    return names

def fill(template, name, book):
    return template.replace("{이름}", name).replace("{도서}", book)

def make_notices(template, names, path):
    notices = []
    seen = []
    unknown = 0
    dupes = 0
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            parts = line.strip().split(",")
            if no == 1 or len(parts) != 4:
                continue
            book = parts[0].strip()
            email = parts[1].strip().lower()
            if (book, email) in seen:
                dupes = dupes + 1
                continue
            seen.append((book, email))
            if email in names:
                notices.append(fill(template, names[email], book))
            else:
                notices.append(fill(template, "회원", book))
                unknown = unknown + 1
    return notices, unknown, dupes

with open("notice_template.txt", encoding="utf-8") as f:
    template = f.read().strip()
names = load_names("members.csv")
notices, unknown, dupes = make_notices(template, names, "loans_nov.csv")
with open("notices.txt", "w", encoding="utf-8") as f:
    for notice in notices:
        f.write(notice + "\n")
print(f"안내문 {len(notices)}통 -> notices.txt (명단에 없는 메일 {unknown}통 · 겹친 줄 {dupes}줄)")
with open("notices.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-15] (15/20) 택배 묶음 배송 박스 배정
def load_parcels(path, limit):
    groups = {}
    problems = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            parts = line.strip().split(",")
            if no == 1 or len(parts) != 3:
                continue
            name = parts[0].strip()
            item = parts[1].strip()
            if parts[2].strip() == "":
                problems.append(f"{name} {item} (무게 빈칸)")
                continue
            weight = float(parts[2])
            if weight > limit:
                problems.append(f"{name} {item} {weight:.1f}kg (한도 넘음)")
                continue
            if name not in groups:
                groups[name] = []
            groups[name].append((item, weight))
    return groups, problems

def pack(parcels, limit):
    boxes = []
    total = 0
    names = ""
    for item, weight in parcels:
        if total + weight > limit:
            boxes.append((total, names))
            total = 0
            names = ""
        if names == "":
            names = item
        else:
            names = names + ", " + item
        total = total + weight
    boxes.append((total, names))
    return boxes

def write_plan(path, groups, problems, limit):
    with open(path, "w", encoding="utf-8") as f:
        for name in groups:
            boxes = pack(groups[name], limit)
            no = 0
            for total, names in boxes:
                no = no + 1
                f.write(f"{name} 박스 {no}/{len(boxes)} {total:.1f}kg: {names}\n")
        for problem in problems:
            f.write(f"확인 필요: {problem}\n")

groups, problems = load_parcels("parcels.csv", 20)
write_plan("box_plan.txt", groups, problems, 20)
print(f"수령인 {len(groups)}명 / 확인 필요 {len(problems)}건 -> box_plan.txt")
with open("box_plan.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
print()


# [3-16] (16/20) 출결 요약과 수료 판정
def count_status(cells):
    counts = {"출석": 0, "지각": 0, "결석": 0}
    typos = []
    for cell in cells:
        cell = cell.strip()
        if cell in counts:
            counts[cell] = counts[cell] + 1
        else:
            typos.append(cell)
    return counts, typos

def judge(counts):
    days = counts["출석"] + counts["지각"] + counts["결석"]
    if days == 0:
        return 0.0, "판정 불가"
    absent = counts["결석"] + counts["지각"] // 3
    rate = (days - absent) / days * 100
    if rate >= 80:
        return rate, "수료"
    return rate, "미수료"

def read_attendance(path):
    people = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            cells = line.strip().split(",")
            people.append((cells[0].strip(), cells[1:]))
    return people

result = {"수료": 0, "미수료": 0, "판정 불가": 0}
for name, cells in read_attendance("attendance.csv"):
    counts, typos = count_status(cells)
    rate, verdict = judge(counts)
    status = f"출석 {counts['출석']} 지각 {counts['지각']} 결석 {counts['결석']}"
    if verdict == "판정 불가":
        print(f"{name}  {status}  판정 불가")
    else:
        print(f"{name}  {status}  출석률 {rate:.1f}% {verdict}")
    for typo in typos:
        print(f"  확인 필요: '{typo}' (계산에서 뺌)")
    result[verdict] = result[verdict] + 1
print(f"수료 {result['수료']}명 / 미수료 {result['미수료']}명 / 판정 불가 {result['판정 불가']}명")
print()


# [3-17] (17/20) 삼킨 예외에서 범인 찾기
def broken_total(path):
    total = 0
    counted = 0
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            try:
                cells = line.strip().split(",")
                total = total + int(cells[3])
                counted = counted + 1
            except:
                continue
    return total, counted

total, counted = broken_total("wordbook.csv")
print(f"고치기 전: 합계 {total}회 / 센 줄 {counted}줄")

# 범인: 맞힌횟수는 셋째 칸(cells[2])인데 cells[3] 을 읽었다. 칸이 3개인 줄마다
#       IndexError 가 났고 except: 가 전부 삼켰다. 4칸인 escalate 줄만 더해져 합계 1.
#       except ValueError: 로 좁히면 「IndexError: list index out of range」 로 멈춘다.
def fixed_total(path):
    total = 0
    counted = 0
    dropped = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            if no == 1:
                continue
            cells = line.strip().split(",")
            if len(cells) != 3:
                dropped.append((no, f"칸 {len(cells)}개"))
                continue
            try:
                total = total + int(cells[2])
                counted = counted + 1
            except ValueError:
                dropped.append((no, f"숫자 아님 '{cells[2].strip()}'"))
    return total, counted, dropped

total, counted, dropped = fixed_total("wordbook.csv")
print(f"고친 뒤: 합계 {total}회 / 센 줄 {counted}줄 / 버린 줄 {len(dropped)}줄")
for no, reason in dropped:
    print(f"  {no}번 줄: {reason}")
print()


# [3-18] (18/20) 할인 이벤트 설정 검증
required = ["code", "name", "rate", "start", "end"]
import datetime
import json

def to_date(text):
    parts = text.split("-")
    return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))

def check_promo(promo, base_day):
    for key in required:
        if key not in promo:
            return f"필수 키 없음 ({key})"
    if promo["rate"] < 1 or promo["rate"] > 50:
        return f"할인율 범위 밖 ({promo['rate']})"
    start = to_date(promo["start"])
    end = to_date(promo["end"])
    if start > end:
        return "기간 거꾸로"
    if base_day < start:
        return "시작 전"
    if base_day > end:
        return "이미 끝남"
    return ""

def filter_promos(promos, base_day):
    passed = []
    failed = []
    no = 0
    for promo in promos:
        no = no + 1
        reason = check_promo(promo, base_day)
        if reason == "":
            passed.append(promo)
        else:
            failed.append((no, promo.get("code", "(코드 없음)"), reason))
    return passed, failed

with open("promo_config.json", encoding="utf-8") as f:
    promos = json.load(f)
passed, failed = filter_promos(promos, datetime.date(2026, 5, 1))
for no, code, reason in failed:
    print(f"{no}번 {code}: {reason}")
with open("valid_promos.json", "w", encoding="utf-8") as f:
    json.dump(passed, f, ensure_ascii=False, indent=2)
print(f"통과 {len(passed)}개 / 탈락 {len(failed)}개 -> valid_promos.json")
with open("valid_promos.json", encoding="utf-8") as f:
    for promo in json.load(f):
        print(f"{promo['code']}  {promo['rate']}%  {promo['start']} ~ {promo['end']}  {promo['name']}")
print()


# [3-19] (19/20) 가계부와 카드 내역 대조
import csv

def read_amounts(path):
    amounts = {}
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            no = no + 1
            if no == 1 or len(row) != 3:
                continue
            key = (row[0].strip(), row[1].strip())
            amounts[key] = int(row[2].replace(",", ""))
    return amounts

def compare(ledger, card):
    lines = []
    counts = {"일치": 0, "불일치": 0, "가계부에만": 0, "카드에만": 0}
    for key in ledger:
        if key not in card:
            kind = "가계부에만"
            lines.append(f"가계부에만: {key[0]} {key[1]} {ledger[key]:,}원")
        elif ledger[key] == card[key]:
            kind = "일치"
            lines.append(f"일치: {key[0]} {key[1]} {ledger[key]:,}원")
        else:
            kind = "불일치"
            lines.append(f"불일치: {key[0]} {key[1]} 가계부 {ledger[key]:,}원 / 카드 {card[key]:,}원")
        counts[kind] = counts[kind] + 1
    for key in card:
        if key not in ledger:
            lines.append(f"카드에만: {key[0]} {key[1]} {card[key]:,}원")
            counts["카드에만"] = counts["카드에만"] + 1
    return lines, counts

lines, counts = compare(read_amounts("ledger.csv"), read_amounts("card_bill.csv"))
for line in lines:
    print(line)
summary = f"일치 {counts['일치']}건 / 불일치 {counts['불일치']}건"
print(f"{summary} / 가계부에만 {counts['가계부에만']}건 / 카드에만 {counts['카드에만']}건")
print()


# [3-20] (20/20) 도서관 운영 보고서 -- 마지막 관문
def read_rows(path, size):
    rows = []
    no = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            no = no + 1
            cells = line.split(",")
            if no == 1 or len(cells) != size:
                continue
            row = []
            for cell in cells:
                row.append(cell.strip())
            row[1] = row[1].lower()
            rows.append(row)
    return rows

def member_names(rows):
    names = {}
    for row in rows:
        if "@" in row[1] and row[1] not in names:
            names[row[1]] = row[0]
    return names

def build_report(names, loans, visits):
    books = {}
    seen = []
    outside = []
    for row in loans:
        if (row[1], row[0]) in seen:
            continue
        seen.append((row[1], row[0]))
        if row[1] in names:
            books[row[1]] = books.get(row[1], 0) + 1
        else:
            outside.append(f"- {row[0]} ({row[1]})")
    minutes = {}
    other = 0
    for row in visits:
        if row[2].isdigit():
            if row[1] in names:
                minutes[row[1]] = minutes.get(row[1], 0) + int(row[2])
            else:
                other = other + 1
    lines = [f"도서관 운영 보고서 (회원 {len(names)}명)"]
    for email in names:
        lines.append(f"{names[email]}: 대출 {books.get(email, 0)}권, 열람실 {minutes.get(email, 0)}분")
    lines.append(f"겹친 대출 기록 {len(loans) - len(seen)}건은 한 번만 셌습니다")
    lines.append(f"명단에 없는 대출 {len(outside)}건")
    for line in outside:
        lines.append(line)
    lines.append(f"명단에 없는 방문 {other}건")
    return lines

names = member_names(read_rows("members.csv", 4))
lines = build_report(names, read_rows("loans.csv", 4), read_rows("visits.csv", 3))
with open("library_report.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
print(f"{len(lines)}줄 썼습니다 -> library_report.txt")
with open("library_report.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
