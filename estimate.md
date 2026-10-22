# Estimate — Product A (bản thật 53 màn)

## 1. Báo cáo SWP

- Báo cáo HTML của skill: [reports/swp-estimate-report.html](reports/swp-estimate-report.html)
- Cách làm ra: chạy skill `tkm:estimate-swp` ở level `medium`, không đẩy điểm sang hệ KPI (`--no-push-kpi`), chấm 316 việc lá (cha = tổng con, tổng **1590 SWP**), trung vị 5 SWP. Bước hiệu chỉnh bằng issue mẫu đã được chấp nhận (`calibrationStatus: accepted`).
- Phân bố SWP của 316 việc lá: 1 SWP: 8 · 2: 6 · 3: 57 · 4: 65 · 5: 84 · 6: 46 · 8: 30 · 9: 2 · 10: 17 · 15: 1.
- **Lệch so với quy trình chuẩn của skill:** worker chuẩn không có công cụ và nhận cả lô trong prompt, nhưng payload khoảng 430 nghìn ký tự là quá lớn để dán vào. Thay vào đó chạy 5 agent `sonnet`, mỗi agent chỉ được đọc file lô của mình và hai tài liệu quy tắc chấm của skill, rồi ghi file kết quả; không được truy cập GitHub hay mã nguồn. Lệch này đã ghi trong phần cảnh báo của báo cáo HTML.
- Lượt đầu có 19 dòng sai hợp đồng (18 dòng ngành `Unknown` đi với độ tin cậy `medium`, 1 dòng sai thứ tự chữ ký độ phức tạp); sửa một lần rồi kiểm lại, qua.

**Lượt chấm thứ hai — task BrSE review spec:** [reports/swp-estimate-report-brse.html](reports/swp-estimate-report-brse.html)

- Thêm sau khi review: mỗi issue thường có một sub-issue `[BrSE]` review và điều chỉnh spec LAB-4 (104 task, xem `task-breakdown.md` §1.5). Chấm bằng cùng skill, level `medium`, `--no-push-kpi`, nguồn là tệp tham chiếu sinh từ backlog trước khi tạo issue trên GitHub.
- Worker được dặn thêm: đây là việc review tài liệu (`workType: documentation`), ngành lấy theo tính năng có spec được review, độ phức tạp theo trạng thái spec LAB-4 (đã hiện thực < một phần < chỉ có thiết kế) và các bẫy nghiệp vụ chạm tới.
- Kết quả: **638 SWP**, trung vị 5. Phân bố: 3 SWP: 16 · 4: 8 · 5: 28 · 6: 22 · 8: 10 · 10: 19 · 16: 1. Không có dòng sai hợp đồng; hiệu chỉnh `accepted`.
- 15 issue trước đây là việc lá được tách phần việc hiện thực thành sub-issue riêng khi thêm `[BrSE]`; sub-issue tách ra giữ nguyên SWP đã chấm ở lượt đầu, không chấm lại.
- **Tổng hai lượt: 420 việc lá, 2228 SWP** (1590 việc dev/QA/PM + 638 BrSE).

## 2. Issue mẫu skill chọn để kiểm

Skill chọn 5 issue đại diện (nhỏ nhất, dưới trung vị, lớn nhất, ngoại lệ, độ tin cậy thấp nhất). Tôi duyệt từng issue một, mỗi issue hai vòng: vòng 1 chọn mức độ khó (rất dễ 1–2 · dễ 3–5 · vừa 6–12 · khó 13–25 · rất khó 26+), vòng 2 chọn điểm SWP cụ thể trong mức đó. Skill tự quy điểm đã chọn về Scope × Complexity.

| Issue | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| #102 (nhỏ nhất) | S1 × C1 → **1** | Giữ S1 × C1 → **1** | Đây là một quyết định đã có sẵn phương án; phần sửa spec nằm ở issue sửa thiết kế khác. Vòng 1 tôi giữ mức "rất dễ", vòng 2 chọn thử 2 điểm (tính cả việc cập nhật spec liên quan) rồi đổi lại 1 vì việc cập nhật spec đã tính ở issue khác và "rất dễ" ở đây là mức 1 point |
| #120 (dưới trung vị) | S3 × C2 → **5** | Giữ S3 × C2 → **5** | Khoảng 8 đường đổi trạng thái, đã có mẫu test để bám theo |
| #239 (lớn nhất) | S5 × C5 → **15** | Giữ S5 × C5 → **15** | RPC nguyên tử khóa nhiều bảng, có 2 cấp duyệt, đồng thời là việc khó nhất backlog nên 15 là hợp lý |
| #7 (ngoại lệ) | S5 × C3 → **10** | Giữ S5 × C3 → **10** | Đụng nhiều file nhưng schema giữ nguyên, có bản `pg_dump` để đối chiếu |
| #335 (độ tin cậy thấp nhất) | S2 × C1 → **3** | Giữ S2 × C1 → **3** | Chủ yếu là hỏi đáp với KH, ít việc kỹ thuật |

Kết quả: **giữ nguyên cả 5**, nên không có quy tắc hiệu chỉnh nào để lan sang các issue khác (danh sách quy tắc rỗng, không có hiệu chỉnh lan truyền).

**Lượt BrSE — 5 task mẫu**, duyệt cùng cách hai vòng:

| Task | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| #444 SCR-010 (nhỏ nhất) | S2 × C1 → **3** | Giữ **3** | Một màn danh sách + hộp thoại, spec đã chạy thật ở prototype |
| #532 ops_alerts (dưới trung vị) | S3 × C2 → **5** | Giữ **5** | Spec chỉ có thiết kế, có vòng đời trạng thái và nhiều nơi phát cảnh báo |
| #540 hồi quy QAX (lớn nhất) | S8 × C3 → **16** | Giữ **16** | Soát kịch bản hồi quy nhiều luồng, chạm cả bốn bẫy và công thức thưởng |
| #423 RDS + migration (ngoại lệ) | S5 × C3 → **10** | Giữ **10** | Chuyển migration khỏi Supabase cần soát kỹ từng phụ thuộc |
| #425 lớp truy cập DB (độ tin cậy thấp nhất) | S5 × C3 → **10** | Giữ **10** | Spec còn thiếu phần chuyển lớp service, playbook cho khoảng 250 chỗ gọi |

Giữ nguyên cả 5, không có hiệu chỉnh lan truyền.

## 3. Cách quy ra giờ

**Cách chọn:** quy ước SWP → giờ theo loại việc, hiệu chỉnh bằng 10 issue mẫu được ước giờ trực tiếp.

**Vì sao chọn cách này:** (1) nhất quán — 316 việc lá dùng cùng một công thức, không việc nào "ước cảm tính" riêng; (2) giải thích được — một bảng 6 hệ số, ai đọc cũng tính lại được; (3) kiểm lại được — đổi hệ số thì chạy lại script là có số mới, không phải ước lại từng issue.

**Quy tắc cụ thể:**

- Giờ = SWP × hệ số theo `primaryDiscipline` của việc đó trong kết quả chấm, làm tròn tới **0,5 giờ**.
- Issue cha và epic = tổng giờ của con (không nhân lại).
- Giờ là **giờ tập trung của một người** cho việc đó, đã gồm unit test và code review theo định nghĩa xong chung. **Không gồm** buffer và PSM. Việc của BrSE là việc lá riêng (`[BrSE]`) có hệ số riêng ở cuối mục này.
- Việc có ngành `Unknown` (2 việc) dùng hệ số 2,0. Issue làm rõ dùng hệ số theo ngành mà skill gán, như mọi việc lá khác.

| Loại việc | Hệ số giờ/SWP |
|---|---:|
| API, Integration, Bugfix | 2,2 |
| UI | 1,9 |
| DB | 1,6 |
| QA | 2,0 |
| Infra, Deploy, Migration | 2,4 |
| Unknown | 2,0 |

**10 issue mẫu ước trực tiếp** (ước giờ theo từng việc, không dùng hệ số; đây là cơ sở hiệu chỉnh):

| Issue | Loại | SWP | Giờ ước trực tiếp | Giờ/SWP |
|---|---|---:|---:|---:|
| #276 | API | 3 | 6 | 2,00 |
| #14 | API | 6 | 14 | 2,33 |
| #309 | UI | 3 | 5 | 1,67 |
| #209 | UI | 5 | 10 | 2,00 |
| #176 | DB | 5 | 7 | 1,40 |
| #345 | DB | 6 | 10 | 1,67 |
| #411 | QA | 4 | 8 | 2,00 |
| #296 | QA | 8 | 16 | 2,00 |
| #27 | Infra | 5 | 12 | 2,40 |
| #7 | Migration | 10 | 24 | 2,40 |

Hệ số chốt lấy trung bình hai mẫu của mỗi nhóm, làm tròn lên 0,1:

| Loại việc (`primaryDiscipline`) | Hệ số mẫu (2 điểm) | Trung bình | Hệ số chốt |
|---|---|---:|---:|
| API, Integration | 2,00, 2,33 | 2,17 | 2,2 |
| UI | 1,67, 2,00 | 1,83 | 1,9 |
| DB | 1,40, 1,67 | 1,53 | 1,6 |
| QA | 2,00, 2,00 | 2,00 | 2,0 |
| Infra, Deploy, Migration | 2,40 (Infra), 2,40 (Migration) | 2,40 | 2,4 |

Mỗi nhóm chỉ có 2 mẫu nên hệ số là xấp xỉ; Bugfix và Integration dùng chung hệ số của API, Deploy dùng chung của Infra, vì không có mẫu riêng. Mẫu đã được duyệt bởi tôi, không phải bởi một đội thật.

**Hệ số cho task BrSE review spec: 1,3 giờ/SWP**, rút từ 5 task mẫu của lượt BrSE (ước giờ trực tiếp):

| Task | SWP | Giờ ước trực tiếp | Cách tính |
|---|---:|---:|---|
| #444 | 3 | 4 | Đọc spec 1 giờ, đối chiếu PREMISE và quyết định KH 0,5 giờ, sửa spec 1,5 giờ, giải thích cho người làm 1 giờ |
| #532 | 5 | 7 | Spec chỉ có thiết kế, đối chiếu với bốn nơi phát cảnh báo |
| #540 | 16 | 19 | Khoảng 3 ngày tập trung |
| #423 | 10 | 14 | Khoảng 2,3 ngày |
| #425 | 10 | 14 | Khoảng 2,3 ngày |
| **Cộng** | **44** | **58** | 58 / 44 = 1,32 → chốt **1,3** |

Hệ số này thấp hơn của việc dev vì không có code, unit test hay code review; tôi đã duyệt hệ số trước khi áp cho 104 task.

**Áp dụng nhất quán:** `tools/plan-sprints.py` đọc kết quả SWP đã hiệu chỉnh của hai lượt chấm, nhân đúng hệ số (theo loại việc với việc dev/QA/PM, 1,3 với task BrSE) cho mọi việc lá, làm tròn, cộng lên cha và epic, ghi vào `plans/project-values.json`. Sau đó `tools/github-backlog-sync.py` ghi giá trị lên trường **Giờ ước lượng** của Project (cùng với Point). Tổng **4088,5 giờ** = 3253,5 giờ việc dev/QA/PM + 835 giờ BrSE.

## 4. Tổng theo epic

SWP và giờ lấy từ trường Point và Giờ ước lượng trên Project. "Số issue" là mọi issue của epic, gồm cả issue làm rõ; "Việc lá" là phần đã chấm SWP, gồm cả task `[BrSE]` (cộng SWP chỉ trên việc lá để không đếm trùng với cha).

| Epic | Số issue | Việc lá | SWP dev/QA/PM | SWP BrSE | Tổng SWP | Tổng giờ | Ghi chú |
|---|---:|---:|---:|---:|---:|---:|---|
| #1 Nền tảng và hạ tầng bản thật (AWS, khung app, job, hàng đợi, tệp, CI/CD) | 14 | 48 | 205 | 104 | 309 | 590,5 | Nền tảng chuyển Supabase sang AWS (S09, S10, D05); 2 issue làm rõ. Đối ứng LAB-1: phần hạ tầng của NFR |
| #50 Danh tính và phân quyền nội bộ | 10 | 35 | 128 | 51 | 179 | 329,5 | Đối ứng FN-01; thêm TOTP, step-up 6 action (S12) |
| #85 Bên tham gia và hiệu lực 許可/承認 | 5 | 17 | 45 | 24 | 69 | 120 | Đối ứng FN-02 |
| #103 Master data: lịch chợ, mặt hàng, điều khoản thanh toán | 5 | 13 | 36 | 15 | 51 | 95 | Đối ứng FN-15 |
| #116 Lô hàng và đánh giá | 6 | 20 | 74 | 24 | 98 | 183 | Đối ứng FN-03 |
| #137 相対取引 | 7 | 28 | 105 | 36 | 141 | 254,5 | Đối ứng FN-04; màn được đầu tư nhất của luồng chính |
| #166 せり | 4 | 15 | 73 | 21 | 94 | 171,5 | Đối ứng FN-05; import hàng loạt là màn mới |
| #182 Giao hàng | 5 | 19 | 74 | 18 | 92 | 169,5 | Đối ứng FN-06; tệp đính kèm tách sang E01 (D08) |
| #202 Đối chiếu, chốt kỳ, tranh chấp, điều khoản thanh toán | 8 | 29 | 126 | 37 | 163 | 298 | Đối ứng FN-07; gồm tranh chấp 紛争 |
| #232 Đính chính sau chốt | 6 | 20 | 101 | 27 | 128 | 235,5 | Đối ứng FN-08; có việc khó nhất backlog (#239, 15 SWP) |
| #253 完納奨励金 | 14 | 36 | 95 | 46 | 141 | 255,5 | **Ràng buộc đặc thù 完納奨励金**, đối ứng FN-09; 4 issue làm rõ, 26/26 việc lá mang nhãn `kanno` |
| #289 Quy tắc và biểu suất | 5 | 13 | 57 | 22 | 79 | 141,5 | Đối ứng FN-10; khung chọn phiên bản dùng chung (D11) |
| #303 Báo cáo và xuất dữ liệu | 17 | 42 | 127 | 69 | 196 | 343,5 | Đối ứng FN-11; 12 báo cáo trên một khung cấu hình (RPT-07 nằm ở E11) |
| #336 Audit và truy vết | 9 | 24 | 82 | 30 | 112 | 210,5 | Đối ứng FN-12; audit ghi trong giao dịch (S24) |
| #360 Thông báo | 9 | 26 | 88 | 47 | 135 | 245,5 | Đối ứng FN-13; bốn job quét thuộc E15 (D03) |
| #387 Phi chức năng và hồi quy | 10 | 35 | 174 | 67 | 241 | 445 | Đối ứng NFR + QAX; hồi quy cuối, 3 issue làm rõ |
| **Tổng** | **134** | **420** | **1590** | **638** | **2228** | **4088,5** | 4088,5 giờ ≈ 511,1 ngày công (8 giờ/ngày); trong đó BrSE 835 giờ |

**Ràng buộc đặc thù 完納奨励金:** toàn bộ nghiệp vụ nằm ở #253 (95 SWP, 196 giờ việc dev/QA/PM; cộng 10 task BrSE thì 141 SWP, 255,5 giờ). Tính cả các mảnh gắn nhãn `kanno` ở ngoài E11 (#320, #415) thì có 29 việc lá dev/QA/PM, 114 SWP, 233,0 giờ; cộng 11 task BrSE mang nhãn `kanno` thì 40 việc lá, 166 SWP, 300,5 giờ, lọc được bằng nhãn để so với nhóm FN-09 của LAB-1. Tỷ lệ bậc vẫn là MOCK đến khi KH cấp test vector (#285).

## 5. So với estimate LAB-1

- **LAB-1:** MD của bảng task **trước buffer 30%**: 627 MD (gồm FN-14 51 MD, DOC 75 MD, Design UI/UX 56 MD, QA chạy test 134 MD). Sau buffer, đội 968 + BrSE 290 + PSM 87 = **1345 MD** (kịch bản AI 20% + responsive 15%).
- **LAB-5:** MD = giờ / 8 (8 giờ một ngày công), chưa buffer, chưa PSM, **chỉ tính việc dev/QA/PM** để so cùng đáy với bảng task LAB-1: 3253,5 / 8 = **406,7 MD**. Task BrSE review spec (835 giờ ≈ 104,4 MD) so riêng ở mục "BrSE" bên dưới.
- Nên so 627 với 406,7. Con số 1345 MD là sau buffer và gánh BrSE/PSM, không cùng đáy với bảng task.
- **LAB-5 sau chặn mức giảm 30% theo epic:** **453,5 MD** (3628,1 giờ). Cộng task BrSE (104,4 MD) thì estimate chốt là **557,9 MD** (4463,1 giờ). Cách tính chặn ở mục "Chặn mức giảm tối đa 30% theo epic" bên dưới. Bảng so sánh ngay sau đây giữ số gốc (SWP × hệ số) để thấy lệch thật trước khi chặn.

| Phần (chức năng/epic) | LAB-1 (MD) | LAB-5 (MD) | Chênh | Vì sao |
|---|---:|---:|---:|---|
| FN-01 Danh tính và phân quyền nội bộ (#50) | 36 | 32,8 | -3,2 | Prototype đã có đăng nhập và phân quyền (3 màn "đã hiện thực"), nhưng bản thật thêm TOTP, step-up 6 action, khóa tài khoản và phiên bằng Redis (S12, GĐ02, GĐ04, D06) nên chỉ thấp hơn một chút |
| FN-02 Bên tham gia và hiệu lực 許可/承認 (#85) | 42 | 11,1 | -30,9 | 3/4 mục LAB-4 ở E03 đã hiện thực ở LAB-3 nên tính là chuyển + hoàn thiện (nhãn `lab4:da-hien-thuc`); LAB-1 còn gánh QA chạy test thủ công và thiết kế trong từng nhóm, LAB-5 tách ra E16. Thêm `registered_on` cho bên ngoài (S17) rất nhỏ |
| FN-03 Lô hàng và đánh giá (#116) | 53 | 18,9 | -34,1 | 4/5 mục E05 đã hiện thực; đường ghi `delivered_complete` để ở issue làm rõ (#136, D10); kiểm thử thủ công của LAB-1 chỉ còn E2E và sub-issue [QA] |
| FN-04 相対取引 (#137) | 36 | 25,9 | -10,1 | 5 màn đã hiện thực nên nhẹ hơn LAB-1; vẫn là epic nghiệp vụ nặng nhất của luồng chính (bẫy 相対取引, SCR-030). Có sửa trần số liệu dùng chung client/server (S18), dùng lại helper ngày chợ (D12) |
| FN-05 せり (#166) | 20 | 18,0 | -2,0 | SCR-042 import hàng loạt là màn mới (hiện thực mới, không tái dùng), step-up 6 action (S12), chính sách lô tồn đọng (GĐ06, GĐ15) nên gần bằng LAB-1 |
| FN-06 Giao hàng (#182) | 40 | 18,2 | -21,8 | 2 đã hiện thực + 2 một phần; phần chứng từ đính kèm (nén ảnh, quét mã độc, lưu ở kho S3 của AWS, S07) do #28 làm một lần cho mọi màn (D08), nên E08 nhẹ hơn; khi so cần cộng cả phần tệp bên E01 |
| FN-07 Đối chiếu và chốt kỳ (#202) | 26 | 31,2 | +5,2 | Cao hơn LAB-1: gồm tranh chấp 紛争 (SCR-062, ADR-0015) làm mới theo LAB-4 với quyền `dispute:*` (S15, D06), giả định cờ và bản ghi tranh chấp (GĐ09), tính ngày chợ mở (D12), chứng từ (S07) |
| FN-08 Đính chính sau chốt (#232) | 17 | 25,0 | +8,0 | Cao hơn LAB-1: RPC nguyên tử khóa nhiều bảng + 2 cấp duyệt (#239), đổi ngưỡng từ ≥ sang > (S19), khung ngưỡng dùng phiên bản quy tắc (D11), tài khoản thử thứ hai (GĐ16) |
| FN-09 完納奨励金 (#253) | 23 | 24,5 | +1,5 | Gần bằng LAB-1 dù 10/14 issue là thiết kế mới: run lưu bất biến thay cho tính khi đọc (S01, S02), nháp lỗi thời (GĐ14), ràng buộc đặc thù tách riêng (D14). Công thức vẫn MOCK chờ #285 |
| FN-10 Quy tắc và biểu suất (#289) | 15 | 14,1 | -0,9 | Gần bằng LAB-1; khung chọn phiên bản dùng chung cho cả 完納奨励金 và ngưỡng điều chỉnh (D11), điền `rule_version_id` theo epic chủ (D13, GĐ17) |
| FN-11 Báo cáo và xuất dữ liệu (#303) | 46 | 31,6 | -14,4 | Thấp hơn LAB-1: 12 báo cáo chạy trên một khung cấu hình (ADR-0010) và RPT-07 nằm ở E11. Bù lại thêm CSV phía server dạng stream (S06, D09) và xuất kế toán qua SFTP có IP cố định (GĐ12, GĐ13) |
| FN-12 Audit và truy vết (#336) | 17 | 21,4 | +4,4 | Cao hơn LAB-1: audit ghi trong giao dịch (S24), bất biến ở prod (S25), danh mục action chuẩn (S23), che dữ liệu một chủ (D04), snapshot cột epic khác (GĐ17); FT-143 chia hai phía, nửa còn lại ở #28 (D08) |
| FN-13 Thông báo (#360) | 14 | 23,0 | +9,0 | Cao hơn LAB-1: 9/9 issue là thiết kế mới; bốn job quét và `enqueue_notification` thuộc E15 (D03), bộ gửi SES, `ops_alerts` (D07, GĐ10), `maskEmail` (S08), API xem trước tác động (S22). Worker và hàng đợi nằm ở E01 (D01, D02, S05) |
| FN-15 Master data (#103) | 13 | 9,4 | -3,6 | Thấp hơn LAB-1: 4/4 mục đã hiện thực; thêm helper ngày chợ dùng chung (D12) |
| NFR + QAX (QA hồi quy) (#1 + #387) | 103 | 101,5 | -1,5 | Gần bằng LAB-1 nhưng cơ cấu khác: E01 gánh chuyển nền tảng Supabase sang AWS (S09, S10, D05, GĐ01, GĐ03, GĐ08), E16 chỉ còn hồi quy E2E, kiểm hiệu năng, bảo mật, tablet (GĐ05); QA chạy test thủ công diện rộng của LAB-1 (134 MD trong 627) không còn |
| FN-14 Chuyển đổi và sẵn sàng vận hành (không có) | 51 | 0,0 | -51,0 | Loại khỏi backlog: là hoạt động dự án (migration dữ liệu, cutover, UAT, đào tạo, hỗ trợ), không phải phần mềm. Xem dòng "FN-14 dịch vụ dự án" ở `task-breakdown.md` §2 |
| DOC thiết kế + tài liệu bàn giao (không có) | 75 | 0,0 | -75,0 | Loại khỏi backlog: thiết kế đã làm ở LAB-4; bản thật chỉ cập nhật tài liệu API trong DoD chung. Xem dòng "Tài liệu thiết kế (LAB-4) và tài liệu bàn giao" ở `task-breakdown.md` §2 |
| **Cộng so được (bỏ FN-14 và DOC)** | **501** | **406,7** | **-94,3** | Hai bên cùng chưa buffer, cùng chưa BrSE/PSM, cùng là việc phần mềm |
| **Tổng** | **627** | **406,7** | **-220,3** | LAB-5 = 3253,5 giờ / 8 |
| **Cộng so được, sau chặn 30%** | **501** | **453,5** | **-47,5** | Bốn epic giảm quá 30% được nâng lên đúng 70% LAB-1 (xem mục dưới) |

**Vì sao 627 MD (trước buffer) lệch xa 1345 MD (sau buffer, BrSE, PSM):** hai con số không cùng đáy. 1345 gồm đội 968 + BrSE 290 + PSM 87, tức đã cộng buffer 30% và hai vai trò quản lý/cầu nối; 627 chỉ là nhân lực làm task. Cộng thêm hạng mục LAB-5 không có (FN-14 51 + DOC 75 = 126 MD) thì phần so được của LAB-1 là 501 MD, còn LAB-5 là 406,7 MD, thấp hơn khoảng 94 MD.

**Phần thấp hơn chủ yếu vì:**

- LAB-5 tái dùng prototype cho 33 màn đã hiện thực; những màn đó tính là chuyển và hoàn thiện, không tính làm mới.
- LAB-1 nhét QA chạy test thủ công (134 MD) vào bảng task; LAB-5 chỉ còn E2E, hồi quy tự động và sub-issue [QA] (594 giờ, khoảng 74 MD).

**Phần cao hơn chủ yếu vì:** LAB-5 làm đủ 53 màn trong khi LAB-1 chỉ estimate 40/53 màn; việc chuyển nền tảng Supabase sang AWS (S09, S10, D05, GĐ01, GĐ03, GĐ08), 30 issue làm rõ (79 SWP), và các màn thiết kế mới/một phần mà LAB-1 không tính hoặc tính mỏng (tranh chấp, thông báo, audit, điều chỉnh: S01, S19, S24, D01–D03).

### Chặn mức giảm tối đa 30% theo epic

**Quy tắc (người dùng chốt khi review):** epic nào có MD LAB-5 thấp hơn LAB-1 quá 30% thì nâng MD LAB-5 lên bằng **70% của LAB-1**, tức chỉ cho giảm tối đa 30%. Epic giảm ít hơn 30% hoặc cao hơn LAB-1 giữ nguyên. Không áp cho FN-14 và DOC vì hai phần này không có epic ở LAB-5 (đã loại khỏi backlog, lý do ở bảng trên).

**Vì sao chặn:** để phòng rủi ro hiểu sai yêu cầu. Một epic giảm quá nhiều so với LAB-1 có thể là dấu hiệu LAB-5 đã hiểu thiếu hoặc hiểu sai bài toán, chứ chưa chắc là việc thật sự nhẹ hơn. Vì vậy mức giảm tối đa được giới hạn đúng bằng tỷ lệ buffer 30% đã đưa ra từ giai đoạn estimate LAB-1.

| Epic | LAB-1 (MD) | LAB-5 gốc (MD) | Mức giảm | Sàn 70% (MD) | LAB-5 sau chặn (MD) | Giờ sau chặn | Giờ thêm |
|---|---:|---:|---:|---:|---:|---:|---:|
| #85 Bên tham gia và 許可/承認 | 42 | 11,1 | -73,7% | 29,4 | **29,4** | 235,2 | +146,7 |
| #116 Lô hàng và đánh giá | 53 | 18,9 | -64,3% | 37,1 | **37,1** | 296,8 | +145,3 |
| #182 Giao hàng | 40 | 18,2 | -54,4% | 28,0 | **28,0** | 224,0 | +78,0 |
| #303 Báo cáo và xuất dữ liệu | 46 | 31,6 | -31,2% | 32,2 | **32,2** | 257,6 | +4,6 |
| **Cộng 4 epic** | **181** | **79,9** | | | **126,7** | **1013,6** | **+374,6** |

Các epic gần ngưỡng nhưng không bị chặn: #137 相対取引 -28,1%, #103 Master data -27,4%.

**Kết quả:** tổng LAB-5 từ 3253,5 giờ (406,7 MD) lên **3628,1 giờ (453,5 MD)**, thêm 374,6 giờ (46,8 MD). Phần so được với LAB-1: 501 MD so với 453,5 MD, thấp hơn 47,5 MD (-9,5%).

**Phạm vi áp dụng:** khoản chặn là **dự phòng ở cấp epic**, chỉ nằm trong tài liệu estimate này. SWP, trường "Giờ ước lượng" trên từng issue và kế hoạch 12 sprint **không đổi** (giữ nguyên theo quyết định không kéo dài kế hoạch). Khi chia khoản thêm về vai trò, giờ của từng vai trò trong epic bị chặn được nhân cùng một hệ số (giờ sau chặn / giờ gốc của epic đó).

### BrSE

| | LAB-1 | LAB-5 |
|---|---:|---:|
| BrSE trước buffer | ≈ 223,1 MD (290 / 1,3) | 104,4 MD (835 giờ, 104 task `[BrSE]`) |
| BrSE sau buffer 30% | 290 MD | 135,7 MD |

LAB-5 thấp hơn vì task `[BrSE]` chỉ là review và điều chỉnh spec LAB-4 trước khi dev, một lần cho mỗi issue. BrSE của LAB-1 gánh cả việc cầu nối suốt dự án: họp với KH, dịch tài liệu và câu hỏi, trả lời Q&A, hỗ trợ UAT. Các việc đó không nằm trong backlog LAB-5 (một phần do PM làm qua 30 issue làm rõ). Chặn mức giảm 30% không áp cho BrSE vì bảng task LAB-1 không có dòng BrSE để so theo epic.

### Effort theo vai trò, sau chặn 30% và sau buffer 30%

Buffer 30% là tỷ lệ đã chốt ở bảng task LAB-1. Buffer chỉ cộng ở cấp tổng hợp để so với LAB-1: trường "Giờ ước lượng" trên từng issue và kế hoạch 12 sprint vẫn dùng giờ **gốc, chưa chặn, chưa buffer** (quyết định giữ nguyên kế hoạch, không kéo dài thêm sprint). Vai trò lấy theo trường "Phụ trách" của việc lá (BE1–BE3, FE1, QA1–QA2, INFRA1, PM, BrSE1–BrSE4); BE gồm cả việc DATA/migration. Chặn 30% chỉ áp cho việc dev/QA/PM, không áp cho BrSE. Giờ từng dòng làm tròn 0,1 nên tổng các dòng có thể lệch 0,1 so với dòng Tổng.

| Vai trò | Việc lá | SWP | Giờ gốc | Giờ sau chặn 30% | Giờ sau chặn + buffer 30% | MD sau chặn + buffer (8h) | Tỷ lệ |
|---|---:|---:|---:|---:|---:|---:|---:|
| BE | 145 | 792 | 1636,0 | 1850,7 | 2405,9 | 300,7 | 41,5% |
| FE | 69 | 296 | 556,5 | 669,3 | 870,0 | 108,8 | 15,0% |
| QA | 50 | 297 | 594,0 | 629,1 | 817,8 | 102,2 | 14,1% |
| INFRA | 22 | 126 | 302,5 | 302,8 | 393,6 | 49,2 | 6,8% |
| PM (issue làm rõ) | 30 | 79 | 164,5 | 176,3 | 229,2 | 28,7 | 4,0% |
| BrSE (review spec) | 104 | 638 | 835,0 | 835,0 | 1085,5 | 135,7 | 18,7% |
| **Tổng** | **420** | **2228** | **4088,5** | **4463,1** | **5802,0** | **725,3** | 100% |

- BE + FE + QA sau chặn và buffer: 4093,7 giờ ≈ 511,7 MD.
- Cùng buffer 30%, phần so được của LAB-1 là 501 × 1,3 = 651,3 MD, LAB-5 (không tính BrSE) là 589,6 MD (thấp hơn khoảng 62 MD, cùng lý do ở trên).
- Đã gồm task BrSE review spec; chưa gồm PSM và phần BrSE ngoài review spec (LAB-1: BrSE 290 + PSM 87 MD sau buffer).
