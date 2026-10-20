#!/usr/bin/env python3
"""Giả lập kết quả Sprint 1 (2026-10-05 → 2026-10-16) như một sprint đã chạy thật.

Kịch bản giả lập (ghi lại để tái lập và để báo cáo tiến độ trích dẫn):
- Xong: các việc nền E01 không phụ thuộc quyết định của KH; KH trả lời câu hỏi DR (E01-C02).
- Đang làm, chuyển sprint sau: E01-C01 (KH chưa trả lời chiến lược RLS) → chặn E01-I03-S1/S2;
  E01-I02-S2 (chuyển migration khó hơn dự kiến ở quyền EXECUTE của RPC); E01-I01-S2 (chờ AWS duyệt hạn mức).
- Chưa bắt đầu: E01-I03-S3 (test phân quyền chờ RLS), E02-C01 (PM dồn sức cho E01-C01).
Ngày xong của từng việc dùng để vẽ burndown theo ngày làm việc (1..10).

Đầu ra: thêm trường Status vào plans/project-values.json (lá trong Sprint 1 theo kịch bản, lá khác Todo,
cha suy từ con) và ghi plans/sprint-1-simulation.json (danh sách đóng issue + burndown).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONE_ON_DAY = {  # mã backlog → ngày làm việc hoàn thành trong sprint
    "E01-I01-S1": 3, "E01-I04-S1": 4, "E01-C02": 4, "E01-I02-S1": 5, "E01-I04-S2": 6, "E01-I11-S1": 6,
    "E01-I04-S3": 7, "E01-I07-S1": 7, "E01-I06-S2": 8, "E01-I05-S1": 9, "E01-I10-S2": 9, "E01-I08-S2": 10,
}
IN_PROGRESS = {"E01-C01", "E01-I03-S1", "E01-I03-S2", "E01-I02-S2", "E01-I01-S2"}
NOT_STARTED = {"E01-I03-S3", "E02-C01"}
WORKING_DAYS = 10


def main():
    path = os.path.join(ROOT, "plans", "project-values.json")
    values = json.load(open(path))
    sprint1 = {k for k, v in values.items() if v.get("Sprint") == "Sprint 1"}
    scripted = set(DONE_ON_DAY) | IN_PROGRESS | NOT_STARTED
    if sprint1 != scripted:  # kịch bản phải phủ đúng các việc đã cam kết trong Sprint 1
        raise SystemExit(f"Kịch bản lệch kế hoạch: thiếu {sorted(sprint1 - scripted)}, thừa {sorted(scripted - sprint1)}")

    for k, v in values.items():
        if "Sprint" in v:  # việc lá
            v["Status"] = "Done" if k in DONE_ON_DAY else "In Progress" if k in IN_PROGRESS else "Todo"
    # Cha: Done khi mọi con Done; In Progress khi có con đã bắt đầu; còn lại Todo
    children = {}
    for k in values:
        parent = k.rsplit("-S", 1)[0] if "-S" in k else (k.split("-")[0] if "-" in k else None)
        if parent and parent != k:
            children.setdefault(parent, []).append(k)
    for parent in sorted((p for p in values if "Sprint" not in values[p]), key=lambda p: -p.count("-")):
        states = [values[c]["Status"] for c in children.get(parent, [])]
        values[parent]["Status"] = ("Done" if states and all(s == "Done" for s in states)
                                    else "In Progress" if any(s != "Todo" for s in states) else "Todo")
    json.dump(values, open(path, "w"), ensure_ascii=False, indent=1)

    committed = sum(values[k]["Point"] for k in sprint1)
    remaining, burndown = committed, []
    for day in range(0, WORKING_DAYS + 1):
        remaining -= sum(values[k]["Point"] for k, d in DONE_ON_DAY.items() if d == day)
        burndown.append({"day": day, "ideal": round(committed * (1 - day / WORKING_DAYS), 1), "actual": remaining})
    out = {"committedSWP": committed, "doneSWP": committed - remaining, "burndown": burndown,
           "close": sorted(DONE_ON_DAY), "inProgress": sorted(IN_PROGRESS), "notStarted": sorted(NOT_STARTED)}
    json.dump(out, open(os.path.join(ROOT, "plans", "sprint-1-simulation.json"), "w"), ensure_ascii=False, indent=1)
    print(f"Sprint 1: cam kết {committed} SWP, xong {committed - remaining} SWP, còn {remaining} SWP")


if __name__ == "__main__":
    main()
