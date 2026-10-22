# Task breakdown — Product A (bản thật 53 màn)

Tài liệu này giải thích cách backlog LAB-5 được chia: nguyên tắc (§1), mỗi spec LAB-4 đi vào issue nào (§2),
các hạng mục 完納奨励金 tách riêng (§3) và chỗ hở/mâu thuẫn của spec LAB-4 phát hiện khi chia (§4).
Mã `#<số>` là issue trên Project (khóa backlog `Exx-Inn...` ghi ở cuối mỗi issue); `S##/GĐ##/D##` trỏ tới dòng trong `PREMISE.md`. Mã `A##` trong nội dung (ví dụ A27, A29) là giả định đã có từ LAB-1/LAB-4, không phải dòng của PREMISE.

## 1. Nguyên tắc chia task

### 1.1. Ba cấp và khi nào dừng chia

| Cấp | Là gì | Ghi chú |
|---|---|---|
| Epic | Một nhóm chức năng, khớp nhóm FN của estimate LAB-1 để so sánh | 16 epic. Không chấm SWP trực tiếp |
| Issue | Một màn hình, hoặc một năng lực xuyên màn (engine, pipeline, hạ tầng) | Là container: có sub-issue `[BrSE]` và các sub-issue việc làm. Chỉ issue làm rõ là việc lá |
| Sub-issue | Một phần việc giao được cho **một** người | Tối đa khoảng 2 ngày công. Mỗi issue thường có một sub-issue `[BrSE]` review spec (mục 1.5) |

- **Dừng chia** khi phần việc thỏa cả bốn: một người làm, một kỷ luật, không quá khoảng 2 ngày công, có checklist "Định nghĩa xong" đo được.
- **Tách sub-issue** khi issue có từ hai kỷ luật trở lên (ví dụ API + giao diện) hoặc ước vượt khoảng 2 ngày. Issue nhỏ một kỷ luật không tách theo kỷ luật (ví dụ các báo cáo RPT cấu hình trên khung chung); từ khi thêm task BrSE, phần việc của chúng nằm ở một sub-issue "Hiện thực" duy nhất (mục 1.5).
- Không chia máy móc: `[QA]` chỉ có khi luồng nghiệp vụ đáng kiểm riêng (E2E, kiểm thử tích hợp); unit test của logic mới nằm trong DoD của việc `[BE]`/`[FE]`.
- Màn đã hiện thực ở LAB-3 (nhãn `lab4:da-hien-thuc`) tính là chuyển + hoàn thiện theo spec, không tính như làm mới; màn thiết kế mới (`lab4:thiet-ke`) tính đủ.
- Chỗ spec hở hoặc mâu thuẫn mà chưa quyết được thì không đoán trong issue làm việc: tạo **issue làm rõ** (mục 1.3).

### 1.2. Định nghĩa xong (DoD)

**DoD chung**, áp cho mọi việc, issue không chép lại:

- Code review xong.
- Unit test cho logic mới qua.
- Đúng spec LAB-4 (phần tử E##, validation, quyền hiển thị).
- Không hard-code dữ liệu nghiệp vụ.
- Audit ghi đúng sự kiện nếu là thao tác ghi.
- Tài liệu API cập nhật.

**DoD riêng** nằm trong thân từng issue, mục "Định nghĩa xong": checklist đo được cho phần riêng của việc đó (ví dụ "một hàm tính, grep không thấy công thức thứ hai", "chạy hai request đồng thời, chỉ một thành công").
Khung thân issue: Mục tiêu · Phạm vi · Trạng thái ở LAB-4 · Nguồn · Định nghĩa xong · Phụ thuộc. Sub-issue: Việc cần làm (3–8 gạch đầu dòng) · Định nghĩa xong · Tham chiếu.

### 1.3. Dùng epic → issue → sub-issue trên Project

- Quan hệ cha–con dùng **sub-issue gốc của GitHub** ở cả hai tầng: epic → issue, issue → sub-issue. Project hiện trường **Loại** (Epic / Issue / Sub-issue) để lọc.
- Trường khác trên Project: Status, Iteration, Phụ trách (người giả định theo vai trò), **Point** (SWP đã review), **Giờ ước lượng**.
- **SWP của epic = tổng con**: chấm ở sub-issue và issue lá; issue cha cộng từ sub-issue; epic cộng từ issue. Epic không chấm riêng.
- **Issue làm rõ** (30 cái): khóa dạng `Exx-Cnn`, nhãn `clarify`, tiêu đề `[Làm rõ]`, không có sub-issue. Mỗi cái nêu câu hỏi, các phương án, đề xuất, và issue nào bị chặn hoặc đổi estimate theo câu trả lời.
- Nhãn: `epic` · `screen` · `capability` · `clarify` · `disc:be|fe|qa|infra|data|brse` · `uat` · `lab4:da-hien-thuc|mot-phan|thiet-ke` · `kanno` (完納奨励金) · `area:<tên ngắn epic>`.

### 1.4. Đặt khóa và tiêu đề

| Loại | Khóa | Tiêu đề |
|---|---|---|
| Epic | `Exx` | `[Epic] …` |
| Issue | `Exx-Inn` | màn: bắt đầu bằng mã `SCR-xxx`; năng lực xuyên màn: tên năng lực |
| Sub-issue | `Exx-Inn-Sn` | bắt đầu bằng `[BE]`, `[FE]`, `[QA]`, `[INFRA]` hoặc `[DATA]` |
| Sub-issue BrSE | `Exx-Inn-S0` | `[BrSE] Review và điều chỉnh spec LAB-4: <tên issue cha>` |
| Issue hỗ trợ UAT | `Exx-U01` | `[BrSE] Hỗ trợ UAT: <tên epic>` |
| Issue làm rõ | `Exx-Cnn` | `[Làm rõ] …` |

Khóa nằm ở dòng cuối thân issue ("Mã backlog"). Hai cặp issue làm rõ trùng nội dung đã gộp thành một, khóa bị gộp không dùng lại nên dãy `Cnn` có chỗ trống.

### 1.5. Task BrSE review và điều chỉnh spec

Spec đã làm xong ở LAB-4, nhưng trước khi dev bắt đầu một issue vẫn phải có người đọc lại spec đó với PREMISE (S##, GĐ##, D##) và quyết định KH, chỉnh theo kiến trúc đích, chốt "Định nghĩa xong" với người làm. Việc này giao cho BrSE:

- **Phạm vi:** mỗi issue thường (104 issue, trừ 30 issue làm rõ) có đúng một sub-issue `[BrSE]`, khóa `Exx-Inn-S0`, nhãn `disc:brse`, mang lại nhãn `lab4:*`, `area:*` và `kanno` của issue cha.
- **Thời điểm:** ở sprint ngay trước sprint có việc dev đầu tiên của issue; issue có dev bắt đầu ngay Sprint 1 thì review ở đầu Sprint 1.
- **Không thay issue làm rõ:** câu hỏi mới phát sinh khi review chuyển cho PM; BrSE không tự quyết thay KH.
- **15 issue trước đây là việc lá** (một kỷ luật, không có sub-issue): khi thêm `[BrSE]` thì phần việc hiện thực được tách thành một sub-issue riêng `Exx-Inn-S1` (tiêu đề `[BE]/[FE]/[QA]/[DATA] Hiện thực: …`), giữ nguyên SWP đã chấm cho issue trước khi tách.

**Hỗ trợ UAT:** mỗi epic nghiệp vụ (E02–E15) có thêm một issue `[BrSE] Hỗ trợ UAT` (khóa `Exx-U01`, nhãn `uat` và `disc:brse`, là việc lá nằm thẳng dưới epic): soạn kịch bản UAT tiếng Nhật cho các màn và năng lực của epic, hướng dẫn KH, tiếp nhận, dịch và phân loại phản hồi thành issue cho đội, xác nhận sau khi sửa, ghi biên bản. KH là người chạy UAT và quyết định đạt hay không. UAT cuốn chiếu: làm ở sprint ngay sau sprint có việc dev/QA cuối của epic (tối đa Sprint 12). E01 và E16 không có issue này vì KH không UAT trực tiếp.

## 2. Spec → issue

Mỗi dòng là một đơn vị spec LAB-4 (đường dẫn tương đối từ gốc bộ spec LAB-4, ghi dạng chữ, không liên kết). Cột cuối ghi phần **chưa thành issue** và lý do; "Sửa: S##" là chỗ backlog đã sửa spec theo `PREMISE.md` §1; "chờ issue làm rõ" là điểm chưa quyết, đang là issue làm rõ; "—" là phủ trọn.
Tổng cộng 53 màn đều có issue (không màn nào bị bỏ). Số sub-issue trong cột thứ ba đã gồm sub-issue `[BrSE]` của issue đó.

| Spec | Epic | Issue/sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| `specs/06-screens/screen-specs/scr-001-login.md` | #50 | #56 (+4 sub-issue) | Màn phụ TOTP, đặt mật khẩu qua link, quên mật khẩu chưa có spec: chờ #83 |
| `specs/06-screens/screen-specs/scr-002-internal-accounts.md` | #50 | #67 (+4 sub-issue) | Tạo tài khoản bên ngoài (EXT-PARTY) chưa có nguồn: để mở (G12). Sửa: S13 |
| `specs/06-screens/screen-specs/scr-003-account-permissions.md` | #50 | #71 (+6 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-004-home.md` | #50 | #64 (+3 sub-issue) | Sửa: S14 |
| `specs/06-screens/screen-specs/scr-005-step-up.md` | #50 | #60 (+4 sub-issue) | Sửa: S12 |
| `specs/06-screens/screen-specs/scr-010-parties.md` | #85 | #89 (+3 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-011-party-profile.md` | #85 | #92 (+7 sub-issue) | Sửa: S17 |
| `specs/06-screens/screen-specs/scr-012-expiry-alerts.md` | #85 | #99 (+3 sub-issue) | Job quét hết hiệu lực do #369 làm, không nằm trong issue màn |
| `specs/06-screens/screen-specs/scr-020-lot-intake.md` | #116 | #121 (+4 sub-issue) | Sửa: S07 |
| `specs/06-screens/screen-specs/scr-021-lots-by-day.md` | #116 | #125 (+3 sub-issue) | Đường ghi `delivered_complete` chờ #136 |
| `specs/06-screens/screen-specs/scr-022-lot-detail.md` | #116 | #128 (+4 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-023-assessment.md` | #116 | #132 (+4 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-030-aitai-desk.md` | #137 | #149 (+8 sub-issue) | Có cần step-up/maker ≠ checker khi chốt 相対 chờ #165. Sửa: S18 |
| `specs/06-screens/screen-specs/scr-031-trade-detail.md` | #137 | #157 (+6 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-040-seri-result-entry.md` | #166 | #167 (+4 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-041-seri-result-search.md` | #166 | #171 (+4 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-042-seri-bulk-import.md` | #166 | #175 (+6 sub-issue) | Tùy chọn trong LAB-4 nhưng vẫn làm; lô tồn đọng chờ #181. Sửa: S12 |
| `specs/06-screens/screen-specs/scr-050-delivery-board.md` | #182 | #183 (+3 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-051-delivery-record.md` | #182 | #186 (+7 sub-issue) | Sửa: S07 |
| `specs/06-screens/screen-specs/scr-052-delivery-exceptions.md` | #182 | #193 (+5 sub-issue) | Nhánh phụ kiểm quyền trong sơ đồ ngoại lệ chờ #201. Sửa: S07 |
| `specs/06-screens/screen-specs/scr-053-delivery-detail.md` | #182 | #198 (+3 sub-issue) | Sửa: S16 |
| `specs/06-screens/screen-specs/scr-060-day-reconciliation.md` | #202 | #203 (+3 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-061-day-lock.md` | #202 | #206 (+5 sub-issue) | Blocker `undelivered` giữ nhãn MOCK đến khi KH xác nhận (G28) |
| `specs/06-screens/screen-specs/scr-062-disputes.md` | #202 | #218 (+8 sub-issue) | Mốc SLA khi lịch chợ chưa đủ ngày chờ #231. Sửa: S07, S15 |
| `specs/06-screens/screen-specs/scr-063-payment-status.md` | #202 | #211 (+4 sub-issue) | Thời điểm tạo dòng `payments` chờ #230 |
| `specs/06-screens/screen-specs/scr-070-correction-request.md` | #232 | #233 (+5 sub-issue) | Điều chỉnh thấp hơn số đã giao chờ #252. Sửa: S07, S19 |
| `specs/06-screens/screen-specs/scr-071-correction-approval.md` | #232 | #238 (+5 sub-issue) | Sửa: S19 |
| `specs/06-screens/screen-specs/scr-072-correction-approval-threshold.md` | #232 | #243 (+5 sub-issue) | Mốc chụp ngưỡng khi đổi giữa chừng chờ #251 |
| `specs/06-screens/screen-specs/scr-080-kanno-incentive-results.md` | #253 | #270 (+5 sub-issue) | Tỷ lệ bậc là MOCK đến khi có test vector (#285); chi tiền/ghi sổ kế toán ngoài phạm vi |
| `specs/06-screens/screen-specs/scr-081-payment-terms-due-dates.md` | #202 | #215 (+3 sub-issue) | Thời điểm snapshot điều khoản chờ #230 |
| `specs/06-screens/screen-specs/scr-090-rule-versions.md` | #289 | #290 (+3 sub-issue) | Hiển thị một hay mọi loại quy tắc chờ #301 |
| `specs/06-screens/screen-specs/scr-091-rule-version-edit.md` | #289 | #293 (+4 sub-issue) | Trần 4 lần đổi quy tắc/năm chờ #302 |
| `specs/06-screens/screen-specs/scr-100-report-hub.md` | #303 | #309 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | Sửa: S06, S20 |
| `specs/06-screens/screen-specs/scr-101-rpt-01-daily-trades.md` | #303 | #310 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-102-rpt-02-lot-trade-history.md` | #303 | #311 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-103-rpt-03-party-validity.md` | #303 | #312 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | Cột còn là đề xuất (thiếu `valid_from`): #335 |
| `specs/06-screens/screen-specs/scr-104-rpt-04-delivery-backlog.md` | #303 | #313 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-105-rpt-05-day-reconciliation.md` | #303 | #314 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | Cột còn là đề xuất (thiếu ngoại lệ mở theo bên mua): #335 |
| `specs/06-screens/screen-specs/scr-106-rpt-06-accounting-export.md` | #303 | #315 (+3 sub-issue) | Đặc tả IF-ACC-01 (cột tệp, ACK, SFTP hay REST) chờ #334. Sửa: S21 |
| `specs/06-screens/screen-specs/scr-107-rpt-07-kanno-results.md` | #253 | #275 (+3 sub-issue) | Cột chưa tách delta theo kỳ gốc: #335. Sửa: S02 |
| `specs/06-screens/screen-specs/scr-108-rpt-08-post-lock-log.md` | #303 | #318 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-109-rpt-09-dispute-sla.md` | #303 | #319 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-110-rpt-10-monthly-by-party.md` | #303 | #320 (+3 sub-issue) | Cột thưởng chỉ hiện khi có quyền (kanno), xem mục 3 |
| `specs/06-screens/screen-specs/scr-111-rpt-11-monthly-by-trade-kind.md` | #303 | #323 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-112-rpt-12-rule-changes.md` | #303 | #324 (+2 sub-issue: [BrSE] và việc hiện thực tách ra) | — |
| `specs/06-screens/screen-specs/scr-120-audit-search.md` | #336 | #347 (+3 sub-issue) | Sửa: S23 |
| `specs/06-screens/screen-specs/scr-121-audit-detail.md` | #336 | #350 (+3 sub-issue) | Tra theo `id` trên bảng phân vùng chờ #357 |
| `specs/06-screens/screen-specs/scr-130-notification-inbox.md` | #360 | #374 (+3 sub-issue) | Email người nhận ngoài chờ #385 |
| `specs/06-screens/screen-specs/scr-131-notification-settings.md` | #360 | #377 (+3 sub-issue) | Mức độ `delivery_backlog` chờ #386. Sửa: S22 |
| `specs/06-screens/screen-specs/scr-132-notification-log.md` | #360 | #380 (+3 sub-issue) | Sửa: S03 |
| `specs/06-screens/screen-specs/scr-140-market-calendar.md` | #103 | #104 (+4 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-141-items.md` | #103 | #108 (+3 sub-issue) | — |
| `specs/06-screens/screen-specs/scr-142-payment-terms.md` | #103 | #111 (+3 sub-issue) | Ai được ghi điều khoản chờ #115 |
| `specs/04-adr/ADR-0001-vercel-supabase-thay-fargate-rds.md` | #1 | #5 | Quyết định cho prototype (Vercel + Supabase), không có việc dựng lại; bản thật theo ADR-0013 |
| `specs/04-adr/ADR-0002-supabase-auth-rls-chi-doc-ghi-qua-api-withroute.md` | #1 | #9, #51 | Phần RLS sau khi bỏ Supabase Auth chờ #48 |
| `specs/04-adr/ADR-0003-rpc-nguyen-tu-va-thu-tu-khoa.md` | #137 | #145, #206, #248 | — |
| `specs/04-adr/ADR-0004-kyoka-shonin-hai-truc-hieu-luc-br-perm-01.md` | #85 | #86, #141 | — |
| `specs/04-adr/ADR-0005-bon-vai-tro-hai-cap-phap-ly-bang-party-types.md` | #85 | #86 | — |
| `specs/04-adr/ADR-0006-aitai-torihiki-la-luong-chinh-seri-la-phu.md` | #137 | #149, #167 | — |
| `specs/04-adr/ADR-0007-con-nguoi-trong-vong-lap.md` | #116 | #132, #218, #293 | Là nguyên tắc xuyên epic, thể hiện trong DoD từng màn, không có issue riêng |
| `specs/04-adr/ADR-0008-rule-versions-gyomu-kitei-kanno-shoreikin.md` | #253 | #254, #290 | Phần "tính khi đọc, không lưu" thay bằng run lưu bất biến (S01); công thức MOCK giữ đến #285 |
| `specs/04-adr/ADR-0009-khoa-ngay-va-dieu-chinh-sau-khoa.md` | #202 | #206, #248 | — |
| `specs/04-adr/ADR-0010-mot-component-bao-cao-cau-hinh-duoc.md` | #303 | #304 | Phần dựng CSV ở trình duyệt sửa theo S06 |
| `specs/04-adr/ADR-0011-step-up-auth-cho-thao-tac-nhay-cam.md` | #50 | #60 | Sửa: S12; step-up ở E06/E09/E10/E12 nằm trong DoD từng màn |
| `specs/04-adr/ADR-0012-seed-ngay-tuong-doi-va-demo-reset.md` | #1 | #37, #345 | Sửa: S25 |
| `specs/04-adr/ADR-0013-kien-truc-dich-ban-that-53-man.md` | #1 | #2…#45 | Sửa: S09, S10; chiến lược RLS và DR chờ #48, #49 |
| `specs/04-adr/ADR-0014-thong-bao-hop-thu-in-app-kenh-bat-dong-bo-thu-lai-log.md` | #360 | #361…#369, #25 | Sửa: S05, S08 |
| `specs/04-adr/ADR-0015-tranh-chap-quy-trinh-nguoi-lien-ket-ngoai-le-va-dieu-chinh.md` | #202 | #218, #193 | — |
| `specs/04-adr/ADR-0016-import-hang-loat-seri-validate-preview-confirm.md` | #166 | #175 | Lô tồn đọng chờ #181 |
| `specs/01-overview/system-overview.md`, `glossary.md` | — | — | Tài liệu nền và thuật ngữ, dùng ở mọi epic; không phải việc phải làm |
| `specs/02-requirements/feature-list.md` (87 feature) | mọi epic | mỗi FT gắn vào issue màn/năng lực | FT-160, 164–167 và FT-900..903 không thành issue (xem cuối bảng); FT-053 sửa theo S16 |
| `specs/02-requirements/screen-list.md`, `screen-list-planned.md` | mọi epic | 53 dòng ở trên | — |
| `specs/02-requirements/customer-decisions.md` (Q-C1..Q-C30) | mọi epic | nằm trong DoD của issue liên quan | Là quyết định KH giả định, không thành issue; điểm chưa chốt thành issue làm rõ (mục 4) |
| `specs/02-requirements/permissions-matrix.md` | #50 | #77, #393 | Sửa: S15 |
| `specs/03-architecture/architecture.md` §1–8 (kiến trúc prototype) | — | — | Mô tả prototype Vercel + Supabase, chỉ làm tham chiếu khi chuyển; không dựng lại |
| `specs/03-architecture/architecture.md` §9.1–9.8 (kiến trúc đích) | #1 | #2…#45, #369, #175, #342, #325 | §9.8 "việc cần quyết" thành #48, #49, #334; sửa: S04, S05, S08, S23 |
| `specs/03-architecture/system-flow.md` | #387 | #412 | Sơ đồ luồng, dùng làm kịch bản hồi quy; không có việc riêng |
| `specs/05-data/data-model.md`, `db-object-catalog.md` | #1 | #5, #9 | Bảng gắn vào issue sở hữu; migration viết lại theo S10 |
| `specs/05-data/data-model-part-a-identity-lots.md` | #50 | #51, #86, #117 | — |
| `specs/05-data/data-model-part-b-trades-settlement.md` | #137 | #138, #211 | — |
| `specs/05-data/data-model-part-c-planned.md` (16 bảng đề xuất, migration p12–p18) | #1 | [DATA] của từng epic: #72, #339, #218, #361, #175, #258, #298, #311, #319, #323, #324 | Sửa: S11 (tách p12 theo epic) |
| `specs/05-data/api-planned.md` | mọi epic | endpoint nằm trong sub-issue [BE] của issue sở hữu | Sửa: S22 |
| `specs/06-screens/screen-flow.md`, `specs/07-wireframes/` (53 màn + bảng luồng) | — | — | Đầu vào cho sub-issue [FE], không có việc riêng |
| `specs/08-traceability/traceability-matrix.md` | #387 | #412 | Dùng làm đầu vào bộ hồi quy; không có việc riêng |
| `specs/09-verification/` (4 checklist đối chiếu RFP) | — | — | Bằng chứng đối chiếu của LAB-4, không phải việc làm |
| `specs/README.md`, `PREMISE.md`, `AI-report.md`, `_templates/` | — | — | Tài liệu nộp và mẫu của LAB-4 |
| FN-14 dịch vụ dự án: FT-160, FT-164–FT-167 (migration dữ liệu, cutover, UAT, đào tạo, hỗ trợ vận hành) | — | chỉ phần BrSE hỗ trợ UAT: 14 issue `Exx-U01` | Là hoạt động dự án, không phải phần mềm hay dữ liệu; LAB-1 estimate riêng (51 MD / 94 SP trước buffer). Riêng việc BrSE hỗ trợ UAT đã thành issue (mục 1.5); KH chạy UAT, migration dữ liệu, cutover, đào tạo, hỗ trợ vận hành vẫn ngoài backlog |
| 4 option FT-900..903 (遠隔取引, cổng 買出人, phân tích, gợi ý chất lượng bằng AI) | — | không có | Ngoài baseline (LAB-1 tính riêng 224 MD); option gợi ý chất lượng còn chạm bẫy "con người trong vòng lặp" nên không đưa vào |
| Tài liệu thiết kế (LAB-4) và tài liệu bàn giao (LAB-1 nhóm DOC) | — | không có | Đã làm xong ở LAB-4; bản thật chỉ cập nhật tài liệu API trong DoD chung |

## 3. Hạng mục chịu ràng buộc đặc thù (完納奨励金)

完納奨励金 (thưởng thanh toán đúng hạn) có công thức, vòng đời kết quả và người chịu trách nhiệm riêng, nên toàn bộ nằm ở #253 và mọi mục liên quan mang nhãn `kanno`.
Ngoài #253 chỉ có hai mảnh có điều kiện và một mục hồi quy (dòng cuối bảng), đều gắn `kanno` và phụ thuộc #253. Task `[BrSE]` review spec của các issue này cũng mang nhãn `kanno`. Có thể lọc nhãn này để so với estimate LAB-1 nhóm FN-09.

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Epic tổng | #253 | Gom toàn bộ nghiệp vụ thưởng để đo riêng |
| Cơ sở tính đủ điều kiện (A27): tổng chưa thuế phần đã giao đủ, đã tất toán, trả đúng hạn, nhân 110/100, nhân tỷ lệ bậc, làm tròn xuống JPY | #254, #255, #256; làm rõ #286 (nghĩa "đã tất toán", "quá hạn"), #287 (khoản chưa đến hạn) | Công thức riêng; một hàm duy nhất, tiền tính bằng số nguyên; hai chỗ nghĩa còn mở làm đổi số tiền |
| Phiên bản biểu suất theo ngày nghiệp vụ của từng giao dịch (Q-C7) | #254 (nhóm theo phiên bản), #281, #282 | Đổi biểu suất giữa tháng thì một bên có nhiều nhóm; chọn sai phiên bản là lệch tiền. Khung chọn phiên bản chung nằm ở #297, không mang nhãn `kanno` |
| Đối tượng được hưởng (Q-C18): mọi bên mua, 卸売業者 không có dòng | #255 | Lọc theo loại bên; gắn với bẫy bốn vai trò hai cấp pháp lý |
| Run → công bố, người công bố ≠ người tính (Q-C12, `publisher_is_computer`) | #257, #258, #259, #260, #261, #262, #263, #264, #265, #284; làm rõ #288 | Bẫy "con người trong vòng lặp": hệ thống tính, người có quyền công bố; run đã công bố bất biến (ràng buộc ở DB); job cuối kỳ chỉ tạo nháp, không tự công bố |
| Chênh lệch kỳ sau (FR-INC-03) | #266, #267, #268, #269 | Kỳ đã công bố giữ nguyên; điều chỉnh sau chốt thành dòng chênh lệch ở run tháng kế, gắn mã điều chỉnh |
| Test vector chưa có (Phụ lục C) | #278, #279, #280, #285, #415 | Tỷ lệ bậc còn MOCK đến khi KH cấp số; cần khung kiểm thử theo dữ liệu và hồi quy riêng (#415 chạy lại cả chuỗi tính, công bố, chênh lệch, RPT-07) |
| RPT-07 (SCR-107) | #275, #276, #277 | RPT-07 đặt ở #253, không ở #303, vì là kết quả thưởng đã công bố kèm chênh lệch |
| Cột thưởng có điều kiện ở RPT-10 (SCR-110) | #320, #321, #322 | Chỉ người có quyền xem thưởng mới thấy cột (Q-C22); phụ thuộc run của #253 |
| Tỷ lệ bậc ở SCR-090/091 | #281, #282, #283 | Nghiệp vụ biểu suất thưởng; luồng nháp → trình → 決裁 dùng chung ở #289 |
| Màn kết quả (SCR-080) | #270, #271, #272, #273, #274 | Màn riêng cho Tính / Công bố / Bỏ nháp; nhãn MOCK cho tỷ lệ bậc |

## 4. Chỗ hở / mâu thuẫn của spec LAB-4 phát hiện khi break

57 dòng, mã `G01..G57` là mã dùng ở `PREMISE.md`. Cột cuối đúng một trong bốn dạng: đã sửa thiết kế → PREMISE S##; giả định → PREMISE GĐ##; tạo issue làm rõ; để mở kèm lý do.
Tổng: 13 sửa thiết kế, 11 giả định, 30 chuyển thành issue làm rõ, 3 để mở. Năm dòng giả định của PREMISE không đứng ở cột "Xử lý" vì chỉ là điều tạm trong lúc chờ làm rõ hoặc bổ sung cho dòng khác: GĐ03 (G02), GĐ06 (G22), GĐ11 (G20), GĐ12 (G45); GĐ01 là giả định công cụ, không gắn G nào.

| # | Spec | Chỗ hở/mâu thuẫn | Xử lý |
|---|---|---|---|
| G01 | ADR-0013 ("dùng lại `lib/domain`, `withRoute`, hợp đồng API") vs mã prototype | ADR coi lớp service là dùng lại được, nhưng service gọi supabase-js ở khoảng 250 chỗ (~67 file); phải chuyển sang kết nối Postgres trực tiếp. Chi phí này không có trong ADR. | đã sửa thiết kế → PREMISE S09 |
| G02 | ADR-0013 · architecture §9.8 · ADR-0002 · K7 (3 lớp quyền báo cáo) | Chiến lược RLS đọc sau khi bỏ Supabase Auth còn mở (biến phiên `app.user_id` hay bỏ RLS đọc). Nhiều spec dựa vào RLS (view `my_*`, `is_internal()`, lớp thứ ba của K7 cho báo cáo) nên đổi hướng làm đổi cả cách cách ly bên ngoài. | tạo issue làm rõ #48 |
| G03 | ADR-0013 ("giữ nguyên migration") · migration p02–p11 · data-model-part-c §5 (`p12_accounts_audit_columns`) | (1) `app_users.id` tham chiếu `auth.users`, policy dùng `auth.uid()`, grant cho `authenticated/anon/service_role`, `insert into storage.buckets` — không chạy được trên Postgres thường, ADR không nêu việc viết lại. (2) Một migration `p12` gộp cột `app_users` (E02) và `audit_logs` (E14); hai epic cùng đụng một file khi làm song song. | đã sửa thiết kế → PREMISE S10, S11 |
| G04 | architecture §9.2/§9.3 · ADR-0014 quyết định 3 · FR-NOTIFY-02 | Một chỗ vẽ "poll mỗi phút", chỗ khác "EventBridge → RunTask mỗi phút", ADR-0014 viết "ECS scheduled task mỗi phút". Khởi động Fargate mỗi phút khó bảo đảm Critical ≤ 5 phút và tốn chi phí. | đã sửa thiết kế → PREMISE S05 |
| G05 | architecture §9.1/§9.4 (bảng 12 job, Redis, `attachment_cold_archive`) | Giờ chạy job ghi "đề xuất, chưa đo"; không có bảng `job_runs` trong data model; job chuyển lạnh trùng lifecycle rule của S3; Redis ghi "idempotency + phiên" nhưng không có spec idempotency-key và chưa nói "phiên" là gì khi dùng token Cognito. | giả định → PREMISE GĐ02, GĐ07 |
| G06 | A20 · ADR-0013 · NFR-AVL-03 · SEC-IAM | Region primary/backup/DR và mức DR (pilot light hay warm standby) chưa chốt; Cognito theo region, không sao chép cross-region, nên cách khôi phục đăng nhập ở DR (mật khẩu/TOTP không xuất được) chưa có. | tạo issue làm rõ #49 |
| G07 | SCR-001 · NFR-SEC-01 | Spec chỉ có form email + mật khẩu; thiếu màn đăng ký/nhập TOTP, đặt mật khẩu từ link, quên mật khẩu (SCR-002/003 lại nói "đặt qua link"), trong khi MFA bắt buộc cho quản trị và người duyệt. | tạo issue làm rõ #83 |
| G08 | SCR-005 §4 · ADR-0011 · data-model-part-c §7 | Step-up còn là nhập lại mật khẩu, cookie không thu hồi phía server (ADR ghi nợ); SCR-005 liệt kê 4 action nhưng data model C có thêm `account:permission_change` và `seri:import_confirm` (6 action). | đã sửa thiết kế → PREMISE S12 |
| G09 | NFR-SEC-01 / SEC-IAM-02 · A22 | MFA cho bên ngoài chưa chốt; "đăng xuất bắt buộc khi chuyển ca" không có màn hay cơ chế. | tạo issue làm rõ #84 |
| G10 | SCR-001 §4 · GĐ21–GĐ22 · NFR-SEC-03 | Khóa 5 lần/15 phút và idle 30/15 phút mới chỉ hiển thị; Cognito không cấu hình đúng 5/15 phút và hạn làm mới theo cả pool, không theo vai trò; "15 phút cho admin/người duyệt" chưa nói áp ra sao khi một tài khoản giữ nhiều vai trò. | giả định → PREMISE GĐ04 |
| G11 | SCR-002 §6 (E05, E08) · data-model-part-c §6.1 | Email nằm ở `auth.users` và tìm theo "email một phần"; Cognito không hỗ trợ tìm chứa và đọc Admin API từng dòng chậm, bị giới hạn tốc độ. | đã sửa thiết kế → PREMISE S13 |
| G12 | SCR-002/003 · Q-C1 | Q-C1 chỉ nói mời tài khoản nội bộ; cách tạo tài khoản bên ngoài (EXT-PARTY) chưa có nguồn. | để mở: chưa có nguồn cách cấp tài khoản bên ngoài; không làm ở LAB-5, ghi vào tài liệu mock khi làm SCR-002 và hỏi KH khi có kênh cấp tài khoản |
| G13 | SCR-004 §8 · SCR-062 §11 + permissions-matrix §8.3 · SCR-011 §13 · SCR-030 §6 · feature-list FT-053 · SCR-100 §3/§11/§12 | (1) SCR-004: widget 有効期限 vẫn MOCK, liên kết tiêu đề đổi sang SCR-012 và nhóm `notify` chưa có trong registry. (2) SCR-062 còn ghi "mở bằng `dispute:write` hoặc `dispute:open`" trong khi bảng tên chung chốt `dispute:open`; permissions-matrix §8.3 ghi SETTLEMENT-MGR là "W" nhưng §8.2 chỉ cho `dispute:resolve`. (3) SCR-011: bên ngoài cấp 2 không nhận `registered_on` nên panel 登録のみ trống. (4) SCR-030: regex client (99.999.999 kg / 9 chữ số giá) lớn hơn trần zod server (10.000.000 kg / 100.000.000 ¥/kg). (5) feature-list ghi FT-053 "Làm thật", "SCR-053 không dựng" trong khi mục ánh xạ và spec màn coi SCR-053 là màn riêng, "Hiện thực một phần". (6) SCR-100 mô tả theo prototype (7 tile mở, 5 mờ, chuỗi "7/5" cứng; thiếu `report:monthly`, RPT-10/11/12) trong khi bản thật mở đủ 12. | đã sửa thiết kế → PREMISE S14, S15, S16, S17, S18, S20 |
| G14 | Q-C30 · SCR-072 · SCR-062 | Thử maker ≠ checker (SCR-072) và `publisher_is_computer` cần SETTLEMENT-MGR thứ hai; môi trường LAB-3 chỉ có `admin` giữ cả SETTLEMENT-MGR lẫn RULE-ADMIN (Q-C30 cho LAB-3 "không thêm"). | giả định → PREMISE GĐ16 |
| G15 | SCR-030 §12 (BR-PERM-01) vs SCR-012 §12 · Q-C29 | SCR-030 xét hiệu lực lúc chốt theo ngày JST thực; SCR-012 và Q-C29 tính "đang chặn giao dịch" theo 業務日 hiện tại. Hai ngày lệch khi ngày làm việc trước chưa khóa qua nửa đêm. | tạo issue làm rõ #102 |
| G16 | SCR-030 §4 Interaction Notes | 相対 không step-up và một người lập/trình/chốt (MOCK FT-031); chưa có tiêu chí để quyết giữ hay đổi cho bản thật. | tạo issue làm rõ #165 |
| G17 | SCR-142 §12 · FT-172 | FT-172 liệt kê RULE-ADMIN là tác nhân, code chỉ cho SYS-ADMIN `master:write`; spec đánh dấu [UNVERIFIED]. | tạo issue làm rõ #115 |
| G18 | SCR-021 §12 (FT-024) · SCR-051 §12 · lot-transitions | Trạng thái lô `delivered_complete` có trong máy trạng thái và được `cancel_trade` kiểm tra nhưng không luồng nào ghi nó; thiếu một nửa bất biến `lot_status_history`. Hai nhóm viết backlog cùng phát hiện, nay gộp một issue. | tạo issue làm rõ #136 |
| G19 | data-model-part-c §4.8 (`lot_status_history`) · SCR-140 §1 · SCR-030/031/040 (RPC chốt/ghi) | (1) `lot_status_history`: không nói backfill cho lô đã có và chỉ phủ trạng thái, không phủ lịch sử số lượng (vẫn đọc từ audit ở SCR-022). (2) SCR-140 nói lịch là mốc "để tạo 業務日" nhưng việc sinh `gyomu_days` kế tiếp nằm ở SCR-061. (3) Prototype cấp EXECUTE cho `service_role` của Supabase; RDS không có vai trò này và spec chưa mô tả vai trò DB thay thế. | giả định → PREMISE GĐ08 |
| G20 | SCR-020 §13 (GĐ29) · SCR-051/052/053 (chứng từ) · FT-143 | Chứng từ 4 MB, chỉ JPEG/PNG/PDF, chưa quét mã độc, chưa nén (prototype) khác đích ≤ 10 MB + quét + Glacier 3 năm; spec chỉ mô tả hiện trạng. FT-143 lại trải hai chỗ (nén ảnh + quét ở hạ tầng tệp, audit metadata ở nhóm audit) nên nếu chỉ tính E14 thì thiếu hẳn phần chính. | đã sửa thiết kế → PREMISE S07 |
| G21 | SCR-041 §3/§12 (FR-SERI-03 "lịch sử sửa") | RFP/spec nói "lịch sử sửa" nhưng không có thao tác sửa tại chỗ (sửa = hủy rồi nhập lại hoặc điều chỉnh sau chốt); bản thật có cần sửa tại chỗ trong ngày chưa khóa không. | giả định → PREMISE GĐ15 |
| G22 | SCR-042 §1, §4 (vòng đời lô nhập) | Lô `validated` bỏ dở "mở lại được tới khi bị hủy/dọn" nhưng chưa nêu chính sách dọn; chưa có lối nạp lại riêng dòng `failed` sau `partially_applied`; một người vừa nạp vừa xác nhận. | tạo issue làm rõ #181 |
| G23 | SCR-012 §12/§13 · architecture §9.4 · ADR-0014 §Hệ quả · part C §2.4 · part C §4.7 · Q-C14 | (1) Người nhận nội bộ ở mốc 30/14/7 ngoài "admin" chưa nêu (GĐ35, Q-C15); cột C10 "đã thông báo" còn [ĐỀ XUẤT]. (2) Job/producer không gán epic: `party_expiry_scan` đọc view của SCR-012, `dispute_opened` thuộc quy trình tranh chấp, `export_failed` thuộc xuất kế toán. (3) `ops_alerts.source` có `health`, `security_event` nhưng chưa có bên sinh (NFR-OPS-01 có bốn nhóm giám sát). (4) Hộp thư xóa sau 13 tháng (Q-C14) trái nguyên tắc không xóa cứng (§2.4). | giả định → PREMISE GĐ10 |
| G24 | SCR-052 §12 (FIG-014) | Nhánh phụ "kiểm tra quyền / quyền hết hiệu lực" của sơ đồ ngoại lệ không được RFP giải thích; chưa rõ "quyền" là quyền màn hay 許可/承認 của bên mua. | tạo issue làm rõ #201 |
| G25 | SCR-052 §E34 · SCR-062 · ADR-0015 · SCR-053 §E21–E24 | (1) Cờ `delivery_exceptions.dispute` và bảng `disputes` cùng mô tả một sự thật; dữ liệu cũ có ngoại lệ cờ bật nhưng chưa có bản ghi; DELIVERY mở 紛争 trước khi xác nhận nên lệch thời điểm; tick 紛争 lúc xác nhận đụng ràng buộc một tranh chấp mở mỗi ngoại lệ (409). (2) SCR-053: dòng đối chiếu là mỗi (ngày, bên mua), không theo lần giao; dòng `payments` có thể chưa tồn tại nên dễ hiểu nhầm là số của riêng lần giao. | giả định → PREMISE GĐ09 |
| G26 | SCR-062 §4.1 · api-planned §6.6 | `sla_due_at` khóa lúc mở theo 5 ngày chợ mở nhưng chưa nói khi `market_calendar` chưa phủ đủ ngày tương lai (SCR-081 có mã `calendar_short`, SCR-062 thì không). | tạo issue làm rõ #231 |
| G27 | SCR-063/081 §13 (Q-C11) vs `payment-queries.ts` | Q-C11 chụp điều khoản "khi `payments` được tạo", nhưng prototype tạo dòng lười (upsert khi mở danh sách) và seed; không có đường tạo khi chốt giao dịch nên snapshot phản ánh lúc mở màn. | tạo issue làm rõ #230 |
| G28 | SCR-061/SCR-060 (BR-CLOSE-01) · SCR-060/061 §11 · SCR-091 §11 · SCR-072 §11 · Q-C12 · SCR-090/091 (`submit_rule_version`) | (1) Blocker `undelivered` do người dùng chọn ở LAB-3, KH chưa xác nhận. (2) Đánh dấu đối chiếu và khóa ngày chỉ SETTLEMENT; SETTLEMENT-MGR không tự khóa nên khi tổ vắng không ai thay. (3) Biểu suất do SETTLEMENT (`rule:approve`), ngưỡng điều chỉnh do SETTLEMENT-MGR (`correction:approve_high`), công bố 完納奨励金 do SETTLEMENT-MGR: ba chỗ ba cấp; RPC nộp phiên bản cứng `rule:approve`. | để mở: (1) giữ nhãn MOCK đến khi KH xác nhận, E2E đặt cờ bật/tắt kiểm `undelivered`; (2) đúng theo spec (tách người làm / người quyết), ghi rủi ro vận hành; (3) khung #297 đổi quyền theo loại mà không sửa mã, hỏi KH thật khi có |
| G29 | SCR-070 §6 (E10, E12) | Điều chỉnh số lượng không kiểm lũy kế đã giao nên "đã giao" có thể vượt số lượng giao dịch; chưa nêu xử lý khi giao dịch có 紛争 mở mà yêu cầu không gắn tranh chấp. | tạo issue làm rõ #252 |
| G30 | SCR-072 §12 "Không hồi tố" · data-model-part-c §5 | Chưa nêu mốc chụp `threshold_version_id` cho bản nháp, `needs_info`, `approved_l1` khi ngưỡng đổi giữa chừng. | tạo issue làm rõ #251 |
| G31 | SCR-070/071 · Q-C21 | Code LAB-3 dùng `≥` ngưỡng để cần cấp 2, Q-C21 chốt `>` ("vượt ngưỡng"); spec đã ghi "thay đổi đề xuất". | đã sửa thiết kế → PREMISE S19 |
| G32 | SCR-090 · SCR-072 | SCR-090 mô tả riêng biểu suất 完納奨励金, SCR-072 có bảng phiên bản ngưỡng riêng; không nói SCR-090 liệt kê một hay mọi loại khi `rule_versions` có hai loại. | tạo issue làm rõ #301 |
| G33 | FT-094 · SCR-091 §13 · SCR-090 §12 vs SCR-072 §6/§12 (GOV-RULE-01) | Danh sách tính năng và phần mock nói "không có trần 4 lần đổi mỗi năm"; SCR-072 lại đề xuất cảnh báo từ lần thứ 4. | tạo issue làm rõ #302 |
| G34 | SCR-051 §10 · PREMISE §1 · NFR-COMP ("tablet cho 11/40 màn") | PREMISE nói wireframe có bản tablet nhưng spec §10 chỉ mô tả flex-wrap; LAB-4 không liệt kê 11 màn hiện trường/bên ngoài cần tablet. | giả định → PREMISE GĐ05 |
| G35 | SCR-050 (Q-C25) · SCR-080 App B4 · SCR-010 §4/§13 · SCR-042 §13 · SCR-031 §3 E13 · SCR-110 §3.3 · SCR-112 §3.3 · SCR-062 E47 | (1) Ngưỡng quá hạn đọc từ `app_settings` ở SCR-050 nhưng part C chuyển vào `notification_rules.threshold`. (2) Job cuối kỳ thưởng "tùy chọn, có thể bỏ (YAGNI)" nhưng bảng job liệt kê như job thật. (3) Ô tìm SCR-010 gọi API mỗi ký tự, cắt 500 bên; dòng mock "contact" lệch bảng E09. (4) Dòng mock SCR-042 ghi "chưa có import". (5) Link "事後修正を申請" ở SCR-031 hiện cho người không có `correction:request` (403). (6) SCR-110 mặc định tháng trước có thể chưa có run thưởng (cột `—`). (7) RPT-12 chỉ có một loại quy tắc trước migration p17. (8) `source_type = other` của 紛争 không có đường tạo. | để mở: lệch tài liệu hoặc thứ tự phụ thuộc, không đổi phạm vi; xử lý trong DoD của issue liên quan (hàm cấu hình duy nhất, #284 làm sau cùng, debounce ở FE, cập nhật tài liệu mock, thông báo không quyền thân thiện, ghi điều kiện phụ thuộc), không tạo issue riêng |
| G36 | SCR-080 §12 · `compute-kanno-shoreikin.ts` · A27 · FR-INC-01 | Một khoản quá hạn làm cả bên mua nhận 0 (code) trong khi câu chữ FR-INC-01 có thể chỉ loại khoản đó; "đã tất toán" chỉ là `paid_on` do người nhập; tỷ lệ đúng hạn theo số khoản hay giá trị chưa nêu. | tạo issue làm rõ #286 |
| G37 | SCR-080 §4/§12 | Khoản chưa đến hạn lúc tính vừa không đúng hạn vừa không quá hạn (không vào cơ sở nhưng vào mẫu số); khoản trả đúng hạn nhưng nhập `paid_on` sau khi công bố không có đường vào kỳ sau (delta chỉ sinh từ điều chỉnh). | tạo issue làm rõ #287 |
| G38 | SCR-080 §6 (D2) · api-planned §6.8 | Công bố thưởng không step-up trong khi mọi quyết định tương tự (khóa ngày, 決裁 điều chỉnh, 決裁 biểu suất) đều có; tổng bên mua có thể âm (delta âm) mà nghĩa nghiệp vụ chưa có. | tạo issue làm rõ #288 |
| G39 | Test vector Phụ lục C (Q-C7) · A27 · #412 | KH chưa cấp số; tỷ lệ bậc và tiêu chí bậc vẫn MOCK; INC-EDGE-01..03 chỉ có tên ca nên hồi quy tiền thưởng chỉ dựa tỷ lệ giả. | tạo issue làm rõ #285 |
| G40 | ADR-0008 (Accepted) · SCR-107 §13 vs Q-C12 · SCR-080 · part C §4.6 | (1) ADR-0008 ghi "tính khi đọc, không lưu" và coi run lưu là phương án bị loại; Q-C12 và part C §4.6 yêu cầu run lưu bất biến. (2) SCR-107 §13: RPT-07 giữ vai trò xem trước, tính mỗi lần đọc, không tách delta; bối cảnh LAB-1→4 §3/§5 lại coi "RPT-07 chưa có dòng chênh lệch kỳ sau" là việc cần làm. | đã sửa thiết kế → PREMISE S01, S02 |
| G41 | SCR-080 §4 Branches · part C §4.6 | `audit_high_water` / `is_stale` chỉ viện "mẫu `daily_reconciliations`" mà không liệt kê sự kiện nào làm nháp lỗi thời (thanh toán mới? điều chỉnh đã ghi sổ? sửa hạn thanh toán?). | giả định → PREMISE GĐ14 |
| G42 | SCR-100 K3/K5 · ADR-0010 · NFR-PERF-01 | Khung báo cáo dùng trần 5.000 dòng và dựng CSV ở trình duyệt, không phân trang; NFR-PERF-01 đòi tra cứu 7 năm p95 ≤ 2 s, spec chỉ ghi "stream/job nền khi vượt trần" mà không thiết kế. | đã sửa thiết kế → PREMISE S06 |
| G43 | SCR-106 §3.3/§13 | Khi không lọc, tổng gồm cả batch `failed` và batch thay thế cùng ngày nên đếm trùng. | đã sửa thiết kế → PREMISE S21 |
| G44 | SCR-106 §4/§11 | Bản thật gửi tự động bằng job; spec chỉ có nút mô phỏng gửi/ACK/lỗi. Không rõ ai gửi lại sau 3 lần tự động và có cần step-up không (`generate`/`simulate` hiện không step-up). | giả định → PREMISE GĐ13 |
| G45 | IF-ACC-01 (A17/A19) · architecture §9.8 | Cột tệp, phương thức (SFTP/REST), mẫu ACK, thư mục, thời hạn chờ ACK đều là giả định. | tạo issue làm rõ #334 |
| G46 | FT-100 `daily_report_batch` · A18 | Chỉ ghi "xong trước 11:00 JST", không nói đầu ra (tệp? bản chụp?) hay thời gian lưu; cột của 12 báo cáo là đề xuất (RPT-03 thiếu `valid_from`, RPT-05 thiếu ngoại lệ mở theo bên mua, RPT-07 không tách delta theo kỳ gốc). | tạo issue làm rõ #335 |
| G47 | SCR-132 §6 (E07) vs Q-C27 · architecture §9.4 vs Q-C28 · SCR-131 §4 (Q-C26) vs api-planned §6.11 · architecture §9.3 vs ADR-0014 5b | (1) SCR-132 cho khoảng ngày xem tối đa 93 ngày, Q-C27 chốt 92. (2) §9.4 ghi `dispute_sla_scan` mỗi giờ, Q-C28 chốt 08:00 JST. (3) Hộp xác nhận SCR-131 cần "số bên bị ảnh hưởng" nhưng không có API xem trước. (4) §9.3 viện `redact-email.ts` để che email, ADR-0014 5b nói hàm đó chỉ trả `{domain, hash}` và cần `maskEmail` mới. | đã sửa thiết kế → PREMISE S03, S04, S08, S22 |
| G48 | ADR-0014 · SCR-131 §3.1 · A28 (`delivery_backlog`) | Sự kiện mặc định 緊急 không hạ mức, không tắt (422), nhưng A28 chỉ Critical khi sắp khóa ngày còn lại High; `severity` một giá trị trên rule không biểu diễn được. | tạo issue làm rõ #386 |
| G49 | SCR-130 §11 · ADR-0014 · APPI | Tài khoản bên ngoài cấp 1 vào SCR-130 nhưng "link về hồ sơ của mình" chưa có màn đích (SCR-012 nội bộ); email người nhận ngoài lấy từ đâu khi xác thực sang Cognito; chính sách nội dung email chứa dữ liệu bên. | tạo issue làm rõ #385 |
| G50 | FR-AUDIT-01 · prototype `writeAudit` · SCR-120 §3 (E06) · ADR-0012 (bất biến audit) | (1) `writeAudit` chạy sau nghiệp vụ và không ném lỗi nên mất dòng audit nếu DB trục trặc giữa hai lệnh; audit nằm hai nơi (SQL trong RPC, TS ở khoảng 47 chỗ). (2) Danh mục nhóm action lấy từ `split_part(action, '.', 1)` nhưng chưa có danh mục action chuẩn. (3) Prototype cố ý không có trigger bất biến vì `reset-demo` TRUNCATE mọi bảng; đích cần bất biến ở prod nhưng staging vẫn cần reset. | đã sửa thiết kế → PREMISE S23, S24, S25 |
| G51 | SCR-120/121 · part C §5 | `audit_logs` phân vùng theo tháng nhưng route SCR-121 dùng `[id]` đơn; khóa chính phân vùng phải gồm `at`, dò theo `id` trong ~84 phân vùng chậm. | tạo issue làm rõ #357 |
| G52 | SCR-121 E22 · Q-C11 · FR-AUDIT-03 | Snapshot điều khoản thanh toán nằm trên `payments` (migration của E09) và `rule_version_id` chỉ điền ở `incentive.*`/`correction.*` (epic khác) nhưng SCR-121 (E14) hiển thị; chưa có issue chỉ rõ bên nào thêm cột/điền giá trị. | giả định → PREMISE GĐ17 |
| G53 | B.7 · NFR-X-09 · NFR-X-07 | Xóa vật lý audit sau 7 năm "phải có phê duyệt" nhưng không nói ai; yêu cầu xóa dữ liệu cá nhân (APPI) mâu thuẫn với audit bất biến. | tạo issue làm rõ #358 |
| G54 | api-planned §6.10 (danh sách khóa che) | Danh sách khóa cần che trong `before/after` còn `[CẦN KH XÁC NHẬN]`. | tạo issue làm rõ #359 |
| G55 | NFR-AVL-02 · NFR-X-01 · A30 | Hàng đợi offline cho thao tác hiện trường: LAB-4 ghi "Thiết kế — chưa hiện thực, ngoài phạm vi" nhưng bản thầu cam kết cơ chế và hòa giải. | tạo issue làm rõ #419 |
| G56 | NFR-X-07 (log truy cập dữ liệu cá nhân) | Chưa liệt kê màn/API nào phải ghi log truy cập dữ liệu cá nhân. | tạo issue làm rõ #420 |
| G57 | NFR-X-06 (in A4 qua driver chuẩn) | Không màn nào mô tả mẫu in; chưa biết in chứng từ nào tại hiện trường. | tạo issue làm rõ #421 |
