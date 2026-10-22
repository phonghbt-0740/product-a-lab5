# Product A — 水産物卸売市場業務支援システム (LAB-5)

- **Dự án:** Product A — 水産物卸売市場業務支援システム, hệ thống hỗ trợ nghiệp vụ chợ bán buôn thủy sản (khách hàng hư cấu).
- **Mã học viên:** PhongHBT2010
- **Đề:** Product A

## Tổng quan

Repo này là kết quả LAB-5: chia bản thật đủ 53 màn của Product A thành backlog trên GitHub Project, chấm SWP, quy ra giờ và theo dõi tiến độ một sprint giả lập.
Backlog được chia từ bản nộp LAB-4 ngày 2026-10-09 (commit `f576f42`).

| Mục | Số liệu |
|---|---|
| Nguồn break | Bộ thiết kế LAB-4 (53 màn), nộp 2026-10-09, commit `f576f42` |
| `PREMISE.md` | **Có thay đổi** so với LAB-4: 25 dòng sửa/thêm spec (S01–S25), 17 giả định bổ sung (GĐ01–GĐ17), 14 hướng đã chốt (D01–D14) |
| Epic | 16 |
| Issue | 148, trong đó 30 issue làm rõ (nhãn `clarify`) và 14 issue BrSE hỗ trợ UAT (nhãn `uat`) |
| Sub-issue | 390: 271 việc dev/QA, 104 task `[BrSE]` review spec LAB-4, 15 việc hiện thực tách ra khi thêm `[BrSE]` |
| Tổng mục trên Project | 554 (16 epic + 148 issue + 390 sub-issue) |
| Người phụ trách giả định | PM, BrSE1–BrSE4, BE1–BE3, FE1, QA1–QA2, INFRA1 |
| Estimate | 2346 SWP, 4242,5 giờ chưa buffer (chi tiết ở [`estimate.md`](estimate.md)) |
| Ràng buộc đặc thù | 完納奨励金: epic #253 và các mục gắn nhãn `kanno` (xem `task-breakdown.md` §3) |
| Sprint giả lập | Sprint 1 (Iteration "Sprint 1", 2026-10-05 → 2026-10-16) đã giả lập: cam kết 261 SWP, xong 211 SWP (81%; riêng việc dev 76/116 = 66%); chi tiết ở [`progress-report.md`](progress-report.md) |

## Link

- Repo: https://github.com/phonghbt-0740/product-a-lab5
- GitHub Project: https://github.com/users/phonghbt-0740/projects/1
  - View **Backlog** (bảng, nhóm theo sprint, có Point / Giờ ước lượng / Loại / Phụ trách): https://github.com/users/phonghbt-0740/projects/1/views/1
  - View **Board** (việc lá theo Status): https://github.com/users/phonghbt-0740/projects/1/views/2
  - View **Sprint 1** (38 việc của sprint đã giả lập: Done 30 · In Progress 6 · Todo 2): https://github.com/users/phonghbt-0740/projects/1/views/3
- Báo cáo SWP (HTML): [`reports/swp-estimate-report.html`](reports/swp-estimate-report.html) (việc dev/QA/PM) · [`reports/swp-estimate-report-brse.html`](reports/swp-estimate-report-brse.html) (task BrSE review spec) · [`reports/swp-estimate-report-uat.html`](reports/swp-estimate-report-uat.html) (task BrSE hỗ trợ UAT)
- Đã mở thử bằng cửa sổ ẩn danh: có — ngày 2026-10-20, mở repo, Project, một issue và báo cáo HTML bằng trình duyệt chưa đăng nhập GitHub (cửa sổ ẩn danh): xem được đầy đủ, không bị yêu cầu đăng nhập

## Cấu trúc repo

| File/thư mục | Nội dung |
|---|---|
| `README.md` | File này: tổng quan, link, cấu trúc repo, bảng spec → epic |
| `PREMISE.md` | Khác biệt so với LAB-4: spec sửa/thêm, giả định bổ sung, hướng đã chốt |
| `task-breakdown.md` | Nguyên tắc chia task, bảng spec → issue, hạng mục 完納奨励金, chỗ hở của spec LAB-4 |
| `estimate.md` | Cách chấm SWP, quy giờ, kết quả theo epic, so với estimate LAB-1 |
| `progress-report.md` | Báo cáo tiến độ sprint giả lập: burndown, rủi ro trễ và hành động |
| `AI-report.md` | Cách dùng AI trong LAB-5: công cụ, chỗ AI sai và cách sửa, giờ làm |
| `reports/` | Báo cáo HTML của skill SWP: lượt chấm việc dev/QA/PM, task BrSE review spec và task BrSE hỗ trợ UAT |
| `tools/` | Script tự viết: `github-backlog-sync.py` (tạo nhãn, issue, quan hệ sub-issue, Project, trường Sprint và ghi trường Point/Giờ ước lượng/Phụ trách/Sprint/Status) · `plan-sprints.py` (quy SWP ra giờ, gán người phụ trách giả định, xếp sprint, xếp task BrSE review trước sprint dev và hỗ trợ UAT sau sprint cuối của epic) · `simulate-sprint-1.py` (kịch bản Sprint 1 giả lập + burndown) · `render-docs.py` (đổi mã backlog thành số issue khi xuất tài liệu) |
| `.gitignore` | Loại các file chỉ dùng cục bộ khỏi repo công khai |

## Spec → epic

Cột "Spec" dùng mã hoặc file của bộ LAB-4 (tính từ gốc bộ spec LAB-4) và các dòng của `PREMISE.md`.
Bốn bẫy nghiệp vụ: **Bẫy 1** 相対取引 là luồng chính, せり là luồng phụ · **Bẫy 2** con người bắt buộc trong vòng lặp, cấm tự động hóa · **Bẫy 3** 許可 ≠ 承認, hai trục hiệu lực riêng · **Bẫy 4** bốn vai trò, hai cấp pháp lý.

| Spec (mã/file LAB-4 hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| ADR-0013, ADR-0012, ADR-0011, architecture §9; PREMISE S05, S09, S10, S25, GĐ01, GĐ07, GĐ08, GĐ11, GĐ12, D01, D02, D05, D07, D08 | #1 — Nền tảng & hạ tầng bản thật | Kiến trúc đích AWS thay prototype Vercel + Supabase. Hai issue làm rõ: RLS (#48), DR (#49) |
| SCR-001, 002, 003, 004, 005 · ADR-0011, ADR-0007 · permissions-matrix; PREMISE S12, S13, S14, S15, GĐ02, GĐ04, GĐ16, D06 | #50 — Danh tính & phân quyền nội bộ | Bẫy 2: đổi quyền do người thao tác có step-up; phân quyền vào màn là `role_permissions`, không phải 許可/承認 |
| SCR-010, 011, 012 · ADR-0004, ADR-0005; PREMISE S17, GĐ10 | #85 — Bên tham gia & hiệu lực 許可/承認 | Bẫy 3: hai trục hiệu lực tách bạch, kiểm tại thời điểm chốt; Bẫy 4: hai cấp pháp lý |
| SCR-140, 141, 142 | #103 — Dữ liệu nền (master) | Lịch chợ là nguồn cho ngày chợ mở (D12) |
| SCR-020, 021, 022, 023 · `lot_status_history` (Q-C9); PREMISE S07, GĐ08, D10 | #116 — Lô hàng & 目利き | Bẫy 2: SCR-023 là chỗ người nhập kết luận 目利き, hệ thống chỉ ghi ai, lúc nào, căn cứ gì |
| SCR-030, 031 · ADR-0006, ADR-0004, ADR-0003; PREMISE S18 | #137 — 相対取引, luồng chính | Bẫy 1: SCR-030 là màn đầu tư sâu nhất; Bẫy 3: kiểm 許可/承認 lúc chốt (BR-PERM-01) |
| SCR-040, 041, 042 · ADR-0016; PREMISE S12, GĐ06, GĐ15 | #166 — せり, luồng phụ | Bẫy 1: luồng phụ, nhỏ hơn #137; Bẫy 2: import hàng loạt phải qua người xác nhận, không tự điền |
| SCR-050, 051, 052, 053 · ADR-0015; PREMISE S07, S16, GĐ05, GĐ09 | #182 — Giao hàng (引渡し) | Truy vết giao hàng → giao dịch → ngoại lệ/紛争 |
| SCR-060, 061, 062, 063, 081 · ADR-0009, ADR-0015; PREMISE S15, GĐ09, GĐ17 | #202 — Đối chiếu, khóa ngày, thanh toán, tranh chấp | Bẫy 2: người đóng tranh chấp ≠ người mở; khóa ngày do người |
| SCR-070, 071, 072; PREMISE S19, GĐ16, D11 | #232 — Điều chỉnh sau chốt | Bẫy 2: người duyệt hai cấp, không phải rule engine; ngưỡng cấu hình có phiên bản |
| SCR-080, 107 · ADR-0008 · Q-C7, Q-C12, Q-C18; PREMISE S01, S02, GĐ14, D14 | #253 — 完納奨励金 (ràng buộc đặc thù) | **完納奨励金**: tách riêng, nhãn `kanno`; Bẫy 2: người công bố ≠ người tính |
| SCR-090, 091; PREMISE D11 | #289 — Quy tắc & biểu suất (業務規程) | Luồng nháp → trình → 決裁 dùng chung cho mọi loại quy tắc; tỷ lệ bậc thưởng thuộc #281 |
| SCR-100…112 (trừ SCR-107) · ADR-0010 · IF-ACC-01; PREMISE S06, S20, S21, GĐ13, D09 | #303 — Báo cáo & xuất dữ liệu | Cột thưởng ở SCR-110 gắn `kanno` (#320); Bẫy 1: RPT-01/11 liệt kê 相対 trước せり |
| SCR-120, 121 · FR-AUDIT-01..03; PREMISE S08, S11, S23, S24, S25, GĐ17, D04, D13 | #336 — Audit & truy vết | Lưu 7 năm, bất biến ở prod |
| SCR-130, 131, 132 · ADR-0014; PREMISE S03, S04, S05, S22, GĐ10, D01, D02, D03 | #360 — Thông báo | Hộp thư in-app, email bất đồng bộ, cảnh báo vận hành |
| NFR (hiệu năng, bảo mật, DR, trợ năng) · traceability-matrix · QAX; PREMISE GĐ05, GĐ16 | #387 — Phi chức năng & kiểm thử hồi quy | #412 có bộ kiểm bốn bẫy và E2E 完納奨励金 (#415, `kanno`) |
