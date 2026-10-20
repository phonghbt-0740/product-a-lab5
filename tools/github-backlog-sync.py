#!/usr/bin/env python3
"""Đưa backlog YAML (plans/backlog/*.yaml) lên GitHub: nhãn, issue, quan hệ sub-issue, Project và trường.

Lệnh con (mặc định chạy thử, thêm --apply mới ghi thật):
  setup   tạo repo public, nhãn, Project public liên kết repo, trường Point / Giờ ước lượng / Phụ trách / Loại
  issues  tạo epic → issue → sub-issue, nối sub-issue, thêm vào Project, đặt trường Loại
  plan-setup  cập nhật lựa chọn Phụ trách, tạo trường Iteration "Sprint" (10 × 2 tuần từ 2026-10-05), đọc trường Status
  fields  ghi trường Project từ file JSON {key: {"Point": n, "Giờ ước lượng": n, "Phụ trách": "BE-A", ...}}

Chỉ nhắm vào OWNER/REPO cấu hình bên dưới. Trạng thái (số issue, node id, item id) lưu ở plans/github-state.json
để chạy lại không tạo trùng.
"""
import argparse, glob, json, os, subprocess, sys, time

import yaml  # PyYAML

OWNER, REPO = "phonghbt-0740", "product-a-lab5"
PROJECT_TITLE = "Product A — LAB-5 backlog"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "plans", "github-state.json")
LABEL_COLORS = {"epic": "5319e7", "screen": "0e8a16", "capability": "1d76db", "clarify": "d93f0b", "kanno": "b60205"}
SELECT_FIELDS = {
    "Loại": ["Epic", "Issue", "Sub-issue"],
    "Phụ trách": ["PM", "BE-A", "BE-B", "BE-C", "FE-A", "QA-A", "QA-B", "INFRA-A"],
}
NUMBER_FIELDS = ["Point", "Giờ ước lượng"]


def gh(args, payload=None, retries=5):
    """Gọi gh CLI; trả JSON (hoặc None). Gặp giới hạn tốc độ thì chờ rồi thử lại; lỗi khác thì dừng."""
    for attempt in range(retries):
        res = subprocess.run(["gh", *args], input=json.dumps(payload) if payload else None,
                             capture_output=True, text=True)
        out = res.stdout + res.stderr
        if res.returncode == 0 and '"errors"' not in res.stdout[:200]:
            return json.loads(res.stdout) if res.stdout.strip() else None
        low = out.lower()
        transient = any(t in low for t in ("timeout", "eof", "connection reset", "error connecting", "502", "503", "504", "bad gateway"))
        if "rate limit" in low or "abuse" in low or transient:
            wait = 15 * (attempt + 1) if transient else 60 * (attempt + 1)
            print(f"  {'lỗi mạng tạm thời' if transient else 'giới hạn tốc độ'} — chờ {wait}s", flush=True)
            time.sleep(wait)
            continue
        sys.exit(f"gh {' '.join(args[:3])} lỗi: {out.strip()[:500]}")
    sys.exit("gh: vượt số lần thử lại vì giới hạn tốc độ")


def graphql(query, **variables):
    return gh(["api", "graphql", "--input", "-"], {"query": query, "variables": variables})["data"]


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"issues": {}}


def save_state(state):
    json.dump(state, open(STATE, "w"), ensure_ascii=False, indent=1)


def load_backlog():
    epics = [yaml.safe_load(open(p)) for p in sorted(glob.glob(os.path.join(ROOT, "plans", "backlog", "E*.yaml")))]
    flat = []  # (key, title, body, labels, kind, parent_key)
    for e in epics:
        flat.append((e["key"], e["title"], e["body"], e.get("labels", []), "Epic", None))
        for i in e.get("issues", []):
            flat.append((i["key"], i["title"], i["body"], i.get("labels", []), "Issue", e["key"]))
            for s in i.get("subs", []) or []:
                flat.append((s["key"], s["title"], s["body"], s.get("labels", []), "Sub-issue", i["key"]))
    return flat


def cmd_setup(apply, state):
    flat = load_backlog()
    labels = sorted({label for item in flat for label in item[3]})
    print(f"Repo {OWNER}/{REPO} (public) · {len(labels)} nhãn · Project '{PROJECT_TITLE}' (public)")
    if not apply:
        return print("  chạy thử — thêm --apply để tạo")
    if subprocess.run(["gh", "repo", "view", f"{OWNER}/{REPO}"], capture_output=True).returncode != 0:
        subprocess.run(["gh", "repo", "create", f"{OWNER}/{REPO}", "--public", "--description",
                        "Product A — LAB-5: break task, GitHub Project, báo cáo tiến độ"], check=True)
    for l in labels:
        color = LABEL_COLORS.get(l, "c5def5" if l.startswith("area:") else "fbca04")
        subprocess.run(["gh", "label", "create", l, "--repo", f"{OWNER}/{REPO}", "--color", color, "--force"],
                       capture_output=True, check=True)
    if "project_id" not in state:
        owner_id = graphql("query($l:String!){user(login:$l){id}}", l=OWNER)["user"]["id"]
        repo_id = graphql("query($o:String!,$n:String!){repository(owner:$o,name:$n){id}}", o=OWNER, n=REPO)["repository"]["id"]
        p = graphql("mutation($o:ID!,$t:String!,$r:ID!){createProjectV2(input:{ownerId:$o,title:$t,repositoryId:$r})"
                    "{projectV2{id number url}}}", o=owner_id, t=PROJECT_TITLE, r=repo_id)["createProjectV2"]["projectV2"]
        graphql("mutation($p:ID!){updateProjectV2(input:{projectId:$p,public:true}){projectV2{id}}}", p=p["id"])
        state.update(project_id=p["id"], project_number=p["number"], project_url=p["url"], fields={})
    pid = state["project_id"]
    for name in NUMBER_FIELDS:
        if name not in state["fields"]:
            f = graphql("mutation($p:ID!,$n:String!){createProjectV2Field(input:{projectId:$p,dataType:NUMBER,name:$n})"
                        "{projectV2Field{... on ProjectV2Field{id}}}}", p=pid, n=name)
            state["fields"][name] = {"id": f["createProjectV2Field"]["projectV2Field"]["id"]}
    for name, options in SELECT_FIELDS.items():
        if name not in state["fields"]:
            opts = [{"name": o, "color": "GRAY", "description": ""} for o in options]
            f = graphql("mutation($p:ID!,$n:String!,$o:[ProjectV2SingleSelectFieldOptionInput!]!){createProjectV2Field("
                        "input:{projectId:$p,dataType:SINGLE_SELECT,name:$n,singleSelectOptions:$o})"
                        "{projectV2Field{... on ProjectV2SingleSelectField{id options{id name}}}}}", p=pid, n=name, o=opts)
            fld = f["createProjectV2Field"]["projectV2Field"]
            state["fields"][name] = {"id": fld["id"], "options": {o["name"]: o["id"] for o in fld["options"]}}
    save_state(state)
    print(f"  xong: {state['project_url']}")


def field_value(fld, value):
    """Giá trị ProjectV2FieldValue theo kiểu trường: lựa chọn, sprint (iteration) hoặc số."""
    if "options" in fld:
        return {"singleSelectOptionId": fld["options"][value]}
    if "iterations" in fld:
        return {"iterationId": fld["iterations"][value]}
    return {"number": float(value)}


def set_field(state, item_id, name, value):
    fld = state["fields"][name]
    val = field_value(fld, value)
    graphql("mutation($p:ID!,$i:ID!,$f:ID!,$v:ProjectV2FieldValue!){updateProjectV2ItemFieldValue("
            "input:{projectId:$p,itemId:$i,fieldId:$f,value:$v}){projectV2Item{id}}}",
            p=state["project_id"], i=item_id, f=fld["id"], v=val)


def find_project_item(state, node):
    q = graphql("query($n:ID!){node(id:$n){... on Issue{projectItems(first:10){nodes{id project{id}}}}}}", n=node)
    return next((it["id"] for it in q["node"]["projectItems"]["nodes"] if it["project"]["id"] == state["project_id"]), None)


def ensure_project_item(state, node):
    """Trả item id của issue trong Project; thêm nếu chưa có.
    GitHub tự đưa sub-issue vào Project của issue cha nhưng có độ trễ, nên gặp lỗi trùng thì chờ rồi đọc lại."""
    for _ in range(6):
        found = find_project_item(state, node)
        if found:
            return found
        res = subprocess.run(["gh", "api", "graphql", "--input", "-"], capture_output=True, text=True,
                             input=json.dumps({"query": "mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:"
                                               "{projectId:$p,contentId:$c}){item{id}}}",
                                               "variables": {"p": state["project_id"], "c": node}}))
        data = json.loads(res.stdout or "{}")
        if (data.get("data") or {}).get("addProjectV2ItemById"):
            return data["data"]["addProjectV2ItemById"]["item"]["id"]
        time.sleep(2)  # đã có sẵn (tự thêm) hoặc lỗi tạm — đọc lại
    sys.exit(f"Không lấy được item Project cho {node}")


def reconcile(state):
    """Ghi lại các issue đã tạo trên GitHub nhưng chưa có trong file trạng thái (nhận diện qua dấu Mã backlog)."""
    issues = gh(["issue", "list", "-R", f"{OWNER}/{REPO}", "--state", "all", "--limit", "1000",
                 "--json", "number,id,body"]) or []
    flat = {f[0]: f for f in load_backlog()}
    for it in issues:
        key = next((k for k in [l.split("`")[1] for l in it["body"].splitlines() if "Mã backlog: `" in l]), None)
        if key and key not in state["issues"] and key in flat:
            rec = {"number": it["number"], "node": it["id"], "kind": flat[key][4], "parent": flat[key][5]}
            rec["item"] = ensure_project_item(state, rec["node"])
            set_field(state, rec["item"], "Loại", rec["kind"])
            state["issues"][key] = rec
            print(f"  khớp lại #{it['number']} {key}")
    save_state(state)


def cmd_issues(apply, state):
    if apply:
        reconcile(state)
    flat = load_backlog()
    todo = [f for f in flat if f[0] not in state["issues"]]
    print(f"{len(flat)} mục trong backlog · {len(todo)} chưa tạo")
    if not apply:
        return print("  chạy thử — thêm --apply để tạo")
    for key, title, body, labels, kind, parent in todo:
        r = gh(["api", f"repos/{OWNER}/{REPO}/issues", "--method", "POST", "--input", "-"],
               {"title": title, "body": f"{body}\n\n<sub>Mã backlog: `{key}`</sub>", "labels": labels})
        rec = {"number": r["number"], "node": r["node_id"], "kind": kind, "parent": parent}
        if parent:
            graphql("mutation($a:ID!,$b:ID!){addSubIssue(input:{issueId:$a,subIssueId:$b}){issue{id}}}",
                    a=state["issues"][parent]["node"], b=rec["node"])
        rec["item"] = ensure_project_item(state, rec["node"])
        state["issues"][key] = rec
        set_field(state, rec["item"], "Loại", kind)
        save_state(state)  # lưu sau mỗi issue để chạy lại an toàn
        print(f"  #{rec['number']} {key} {kind}", flush=True)
        time.sleep(1.5)  # giữ dưới giới hạn tạo nội dung của GitHub


def cmd_fields(apply, state, path):
    values = json.load(open(path))
    print(f"{len(values)} mục sẽ được ghi trường từ {os.path.basename(path)}")
    for key, fields in list(values.items())[:5]:
        print(f"  {key}: {fields}")
    if not apply:
        return print("  chạy thử — thêm --apply để ghi")
    progress_path = os.path.join(ROOT, "plans", "fields-progress.json")
    done = set(json.load(open(progress_path))) if os.path.exists(progress_path) else set()
    pending = [(k, f, f"{k}:{json.dumps(f, sort_keys=True, ensure_ascii=False)}") for k, f in values.items()]
    pending = [p for p in pending if p[2] not in done]  # bỏ mục đã ghi đúng giá trị ở lần chạy trước
    print(f"  còn {len(pending)} mục", flush=True)
    for start in range(0, len(pending), 3):  # 3 mục × ≤5 trường ≈ 15 lệnh ghi một request (30 lệnh thì GitHub hay timeout)
        chunk = pending[start:start + 3]
        parts, variables = [], {"p": state["project_id"]}
        for key, fields, _ in chunk:
            for name, value in fields.items():
                n = len(parts)
                fld = state["fields"][name]
                variables[f"i{n}"], variables[f"f{n}"] = state["issues"][key]["item"], fld["id"]
                variables[f"v{n}"] = field_value(fld, value)
                parts.append(f"m{n}:updateProjectV2ItemFieldValue(input:{{projectId:$p,itemId:$i{n},fieldId:$f{n},value:$v{n}}})"
                             "{projectV2Item{id}}")
        decl = ",".join(["$p:ID!"] + [f"$i{n}:ID!,$f{n}:ID!,$v{n}:ProjectV2FieldValue!" for n in range(len(parts))])
        gh(["api", "graphql", "--input", "-"], {"query": f"mutation({decl}){{{' '.join(parts)}}}", "variables": variables})
        done.update(stamp for _, _, stamp in chunk)
        json.dump(sorted(done), open(progress_path, "w"), ensure_ascii=False)
        print(f"  {chunk[-1][0]} ({start + len(chunk)}/{len(pending)})", flush=True)
    print("  xong")


SPRINT_START, SPRINT_DAYS, SPRINT_COUNT = "2026-10-05", 14, 12


def cmd_plan_setup(apply, state):
    print(f"Phụ trách = {SELECT_FIELDS['Phụ trách']} · Sprint 1..{SPRINT_COUNT} từ {SPRINT_START}, {SPRINT_DAYS} ngày")
    if not apply:
        return print("  chạy thử — thêm --apply để ghi")
    pid, fields = state["project_id"], state["fields"]
    opts = [{"name": o, "color": "GRAY", "description": ""} for o in SELECT_FIELDS["Phụ trách"]]
    f = graphql("mutation($f:ID!,$o:[ProjectV2SingleSelectFieldOptionInput!]){updateProjectV2Field(input:{fieldId:$f,"
                "singleSelectOptions:$o}){projectV2Field{... on ProjectV2SingleSelectField{id options{id name}}}}}",
                f=fields["Phụ trách"]["id"], o=opts)["updateProjectV2Field"]["projectV2Field"]
    fields["Phụ trách"]["options"] = {o["name"]: o["id"] for o in f["options"]}
    if "Sprint" not in fields:
        from datetime import date, timedelta
        start = date.fromisoformat(SPRINT_START)
        its = [{"title": f"Sprint {i + 1}", "startDate": str(start + timedelta(days=SPRINT_DAYS * i)), "duration": SPRINT_DAYS}
               for i in range(SPRINT_COUNT)]
        f = graphql("mutation($p:ID!,$c:ProjectV2IterationFieldConfigurationInput!){createProjectV2Field(input:{projectId:$p,"
                    "dataType:ITERATION,name:\"Sprint\",iterationConfiguration:$c}){projectV2Field{... on ProjectV2IterationField"
                    "{id configuration{iterations{id title} completedIterations{id title}}}}}}",
                    p=pid, c={"startDate": SPRINT_START, "duration": SPRINT_DAYS, "iterations": its})
        fld = f["createProjectV2Field"]["projectV2Field"]
        cfg = fld["configuration"]  # sprint đã qua nằm ở completedIterations
        fields["Sprint"] = {"id": fld["id"], "iterations": {i["title"]: i["id"] for i in cfg["iterations"] + cfg["completedIterations"]}}
    q = graphql("query($p:ID!){node(id:$p){... on ProjectV2{field(name:\"Status\"){... on ProjectV2SingleSelectField"
                "{id options{id name}}}}}}", p=pid)["node"]["field"]
    fields["Status"] = {"id": q["id"], "options": {o["name"]: o["id"] for o in q["options"]}}
    save_state(state)
    print(f"  xong: Phụ trách {list(fields['Phụ trách']['options'])} · Sprint {list(fields['Sprint']['iterations'])} · Status {list(fields['Status']['options'])}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["setup", "issues", "plan-setup", "fields"])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--values", help="file JSON cho lệnh fields")
    a = ap.parse_args()
    st = load_state()
    {"setup": lambda: cmd_setup(a.apply, st), "issues": lambda: cmd_issues(a.apply, st),
     "plan-setup": lambda: cmd_plan_setup(a.apply, st), "fields": lambda: cmd_fields(a.apply, st, a.values)}[a.command]()
