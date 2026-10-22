#!/usr/bin/env python3
"""Quy SWP ra giờ, gán người phụ trách giả định và xếp việc vào sprint theo năng lực.

Đầu vào: kết quả SWP đã hiệu chỉnh của hai lượt chấm tkm:estimate-swp — việc dev/QA/PM (plans/swp/calibrated.json)
và task BrSE review spec (plans/swp-brse/calibrated.json) — backlog YAML (thứ tự epic/issue) và plans/github-state.json.
Đầu ra: plans/project-values.json — giá trị trường Project cho từng mã backlog:
  Point = SWP đã chốt (cha = tổng con), Giờ ước lượng = SWP × hệ số (làm tròn 0,5 giờ; cha = tổng con),
  Phụ trách (việc lá) và Sprint (việc lá). Trạng thái sau sprint giả lập do lệnh khác ghi.

Xếp hai lượt:
  1. Việc dev/QA/PM theo thứ tự backlog, sprint sớm nhất còn chỗ (như trước).
  2. Task BrSE review spec (mã `…-S0`): hạn = sprint ngay trước sprint dev đầu tiên của issue (issue bắt đầu Sprint 1
     thì Sprint 1). Xếp vào sprint muộn nhất ≤ hạn còn chỗ; số BrSE tăng dần (BrSE1, BrSE2, …) tới khi mọi task kịp hạn.
  3. Task BrSE hỗ trợ UAT (mã `Exx-U01`, một task mỗi epic nghiệp vụ): sprint ngay sau sprint có việc dev/QA cuối của epic
     (tối đa Sprint 12), xếp vào BrSE đã có, lấp người đầu trước; không còn chỗ tới Sprint 12 thì dồn vào Sprint 12 và báo.
"""
import glob, json, os, sys
from collections import defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOURS_PER_SWP = {"API": 2.2, "Integration": 2.2, "Bugfix": 2.2, "UI": 1.9, "DB": 1.6, "QA": 2.0,
                 "Infra": 2.4, "Deploy": 2.4, "Migration": 2.4, "Unknown": 2.0}
BRSE_HOURS_PER_SWP = 1.3  # hệ số riêng cho task BrSE review spec (hiệu chỉnh bằng mẫu, xem estimate.md §3)
TEAM = {"BE": ["BE1", "BE2", "BE3"], "FE": ["FE1"], "QA": ["QA1", "QA2"], "INFRA": ["INFRA1"], "PM": ["PM"]}
CAPACITY = {"PM": 30}            # giờ tập trung mỗi sprint; mặc định 60 = 10 ngày × 6 giờ
DEFAULT_CAPACITY = 60
SPRINTS = 12
MAX_BRSE = 6
# Thứ tự làm theo phụ thuộc giữa epic: nền tảng → danh tính → master → nghiệp vụ → báo cáo/thông báo → phi chức năng
EPIC_ORDER = ["E01", "E02", "E04", "E03", "E05", "E06", "E07", "E08", "E09", "E10", "E12", "E11", "E13", "E14", "E15", "E16"]


def role_of(row):
    if "clarify" in row["labels"]:
        return "PM"  # issue làm rõ: PM chuẩn bị câu hỏi và chốt với KH
    return {"UI": "FE", "QA": "QA", "Infra": "INFRA", "Deploy": "INFRA"}.get(row["primaryDiscipline"], "BE")


def load_rows(state):
    """Dòng SWP đã chốt cho mọi việc lá, theo mã backlog."""
    main = {int(r["issueRef"].split("#")[1]): r for r in json.load(open(os.path.join(ROOT, "plans", "swp", "calibrated.json")))["issues"]}
    brse = {r["issueRef"].split("#")[1]: r for r in json.load(open(os.path.join(ROOT, "plans", "swp-brse", "calibrated.json")))["issues"]}
    brse.update({r["issueRef"].split("#")[1]: r for r in json.load(open(os.path.join(ROOT, "plans", "swp-uat", "calibrated.json")))["issues"]})

    def row(key):
        if key.endswith("-S0") or key.endswith("-U01"):
            return brse[key]
        rec = state.get(key)
        if rec and rec["number"] in main:
            return main[rec["number"]]
        # việc hiện thực tách từ issue lá khi thêm task BrSE: giữ nguyên SWP đã chấm cho issue cha
        return main[state[key.rsplit("-S", 1)[0]]["number"]]
    return row


def schedule_brse(tasks, n):
    """tasks: [(key, giờ, hạn)]. Trả {key: (sprint, người)} hoặc None nếu n người không kịp."""
    people = [f"BrSE{i + 1}" for i in range(n)]
    load, out = defaultdict(float), {}
    for key, hours, due in sorted(tasks, key=lambda t: (-t[2], t[0])):
        for s in range(due, 0, -1):  # muộn nhất còn chỗ, sát với lúc dev bắt đầu
            free = [p for p in people if load[(p, s)] + hours <= DEFAULT_CAPACITY]
            if free:
                person = free[0]  # lấp người đầu trước: BrSE thêm chỉ xuất hiện ở sprint cao điểm
                load[(person, s)] += hours
                out[key] = (s, person)
                break
        else:
            return None
    return out


def main():
    state = json.load(open(os.path.join(ROOT, "plans", "github-state.json")))["issues"]
    row_of = load_rows(state)
    epics = {e["key"]: e for e in (yaml.safe_load(open(p)) for p in glob.glob(os.path.join(ROOT, "plans", "backlog", "E*.yaml")))}
    ordered = []
    for ek in EPIC_ORDER:
        for i in epics[ek]["issues"]:
            ordered += [s["key"] for s in (i.get("subs") or [])] or [i["key"]]

    load = defaultdict(float)  # (người, sprint) → giờ đã xếp
    values = {}
    last_sprint = defaultdict(lambda: 1)   # theo vai trò: sprint chỉ đi tới, không lấp ngược việc sau vào sprint trước
    built_in = defaultdict(lambda: 1)      # theo issue cha: sprint muộn nhất của phần BE/DATA/INFRA đã xếp
    done_in = defaultdict(lambda: 1)       # theo issue cha: sprint muộn nhất của mọi phần không phải QA
    first_dev = {}                         # theo issue cha: sprint sớm nhất của việc dev/QA
    overflow = []
    for key in (k for k in ordered if not k.endswith("-S0") and not k.endswith("-U01")):
        row = row_of(key)
        hours = round(row["finalSWP"] * HOURS_PER_SWP[row["primaryDiscipline"]] * 2) / 2
        role = role_of(row)
        cap = CAPACITY.get(role, DEFAULT_CAPACITY)
        sprint, person = None, None
        parent = key.rsplit("-S", 1)[0]
        earliest = last_sprint[role]
        if role == "FE":
            earliest = max(earliest, built_in[parent])   # FE sau khi có API cùng issue
        if role == "QA":
            earliest = max(earliest, done_in[parent])    # QA sau khi mọi phần khác của issue xong
        for s in range(earliest, SPRINTS + 1):  # sprint sớm nhất còn chỗ, người nhẹ việc nhất
            free = [(load[(p, s)], p) for p in TEAM[role] if load[(p, s)] + hours <= cap]
            if free:
                sprint, person = s, min(free)[1]
                break
        if sprint is None:  # không còn chỗ: dồn vào sprint cuối và đếm để báo rủi ro
            sprint, person = SPRINTS, TEAM[role][0]
            overflow.append(key)
        load[(person, sprint)] += hours
        last_sprint[role] = sprint
        if role in ("BE", "INFRA"):
            built_in[parent] = max(built_in[parent], sprint)
        if role != "QA":
            done_in[parent] = max(done_in[parent], sprint)
        first_dev[parent] = min(first_dev.get(parent, sprint), sprint)
        values[key] = {"Point": row["finalSWP"], "Giờ ước lượng": hours, "Phụ trách": person, "Sprint": f"Sprint {sprint}"}

    # Lượt 2: task BrSE review spec, hạn là sprint trước sprint dev đầu tiên
    tasks = []
    for key in (k for k in ordered if k.endswith("-S0")):
        hours = round(row_of(key)["finalSWP"] * BRSE_HOURS_PER_SWP * 2) / 2
        tasks.append((key, hours, max(1, first_dev[key[:-3]] - 1)))
    for n in range(1, MAX_BRSE + 1):
        plan = schedule_brse(tasks, n)
        if plan:
            break
    else:
        sys.exit(f"{MAX_BRSE} BrSE vẫn không kịp hạn review")
    for key, hours, _ in tasks:
        s, person = plan[key]
        load[(person, s)] += hours
        values[key] = {"Point": row_of(key)["finalSWP"], "Giờ ước lượng": hours, "Phụ trách": person, "Sprint": f"Sprint {s}"}

    # Lượt 3: task BrSE hỗ trợ UAT, cuốn chiếu theo epic
    last_dev = defaultdict(int)
    for key, v in values.items():
        if not key.endswith("-S0"):
            last_dev[key[:3]] = max(last_dev[key[:3]], int(v["Sprint"].split()[1]))
    people = sorted({p for (p, _), h in load.items() if p.startswith("BrSE")}, key=lambda p: int(p[4:]))
    uat_overflow = []
    for key in (k for k in ordered if k.endswith("-U01")):
        hours = round(row_of(key)["finalSWP"] * BRSE_HOURS_PER_SWP * 2) / 2
        target = min(SPRINTS, last_dev[key[:3]] + 1)
        spot = next(((s, p) for s in range(target, SPRINTS + 1) for p in people if load[(p, s)] + hours <= DEFAULT_CAPACITY), None)
        if spot is None:
            spot = (SPRINTS, min(people, key=lambda p: load[(p, SPRINTS)]))
            uat_overflow.append(key)
        load[spot[::-1]] += hours
        values[key] = {"Point": row_of(key)["finalSWP"], "Giờ ước lượng": hours, "Phụ trách": spot[1], "Sprint": f"Sprint {spot[0]}"}

    # Cha (issue có sub, epic): Point và giờ = tổng con; không gán người/sprint
    for ek in EPIC_ORDER:
        epic_pt = epic_h = 0
        for i in epics[ek]["issues"]:
            subs = [s["key"] for s in (i.get("subs") or [])]
            if subs:
                pt, h = sum(values[k]["Point"] for k in subs), sum(values[k]["Giờ ước lượng"] for k in subs)
                values[i["key"]] = {"Point": pt, "Giờ ước lượng": h}
            epic_pt += values[i["key"]]["Point"]
            epic_h += values[i["key"]]["Giờ ước lượng"]
        values[ek] = {"Point": epic_pt, "Giờ ước lượng": epic_h, "Phụ trách": "PM"}

    json.dump(values, open(os.path.join(ROOT, "plans", "project-values.json"), "w"), ensure_ascii=False, indent=1)
    per_sprint = defaultdict(float)
    for (p, s), h in load.items():
        per_sprint[s] += h
    print("số BrSE:", n, "· giờ BrSE theo sprint:",
          {s: sum(h for (p, ss), h in load.items() if ss == s and p.startswith("BrSE")) for s in range(1, SPRINTS + 1)})
    print("giờ theo sprint:", {s: per_sprint[s] for s in sorted(per_sprint)})
    print("việc bị dồn vì hết chỗ:", len(overflow), overflow[:10], "· UAT dồn:", uat_overflow)
    print("tổng SWP", sum(values[e]["Point"] for e in EPIC_ORDER), "· tổng giờ", sum(values[e]["Giờ ước lượng"] for e in EPIC_ORDER))


if __name__ == "__main__":
    main()
