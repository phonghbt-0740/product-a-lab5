# AI report — LAB-5

## 1. Skill và prompt cho từng việc

Làm việc trong Claude Code, một Agent điều phối và nhiều agent con. Tôi quyết định phạm vi, độ hạt, cách quy giờ và duyệt từng điểm chốt; Agent viết, chạy script và báo lại.

**Chuẩn bị.** Lưu context LAB-1 đến LAB-4 (bốn bẫy nghiệp vụ, số estimate, quyết định KH giả định, chỗ hở đã biết) vào một file riêng ở repo private để mọi agent dùng chung. Tạo thư mục và repo LAB-5 riêng, vì repo public không được chép đề gốc. Cấp thêm scope `project` cho `gh`, chỉ thao tác trên tài khoản cá nhân, và nhắc gỡ scope sau LAB-5.

**Chia task (break task).** Agent không viết thẳng 421 issue mà đi bốn bước:

1. Viết một guide cho agent con: độ hạt (epic, issue theo màn hoặc năng lực xuyên màn, sub-issue chỉ một người làm, tối đa khoảng 2 ngày), khung nội dung issue và sub-issue, định nghĩa xong đo được, danh sách 16 epic theo nhóm FN của LAB-1, luật public.
2. Bốn agent con chạy song song, mỗi agent nhận một nhóm epic. Prompt nói rõ: đọc spec LAB-4 nào, mỗi thân issue là bằng chứng chính để AI chấm điểm nên phải cụ thể (phần tử màn, endpoint, bảng, quyền, trạng thái) và không thổi phồng hay hạ thấp; việc đã có ở prototype phải ghi đúng là "chuyển + hoàn thiện"; chỗ spec hở thì viết vào file chỗ hở và tạo issue làm rõ thay vì đoán. Đầu ra là một file YAML mỗi epic.
3. Một agent ráp nối: thay 53 phụ thuộc tạm kiểu `E01-I??` (do chạy song song nên mỗi nhóm chưa biết khóa của nhóm khác), gộp 7 việc trùng, gộp hai cặp issue làm rõ trùng, gỡ vòng phụ thuộc, lập bảng 57 chỗ hở và danh sách ứng viên cho `PREMISE.md`.
4. Bản duyệt cho tôi xem trước; sau khi tôi đồng ý, `tools/github-backlog-sync.py` mới tạo repo, nhãn, Project public, 421 issue và quan hệ sub-issue gốc của GitHub.

**Chấm SWP.** Dùng skill `tkm:estimate-swp`, level `medium`, `--no-push-kpi`. Skill chỉ xuất báo cáo HTML (chỉ đọc), không ghi lên Project. Vì payload khoảng 430 nghìn ký tự quá lớn để dán vào prompt, Agent chạy 5 agent `sonnet` làm worker, mỗi agent một lô. Prompt của worker giới hạn: chỉ đọc file lô của mình và hai tài liệu quy tắc của skill, chỉ ghi file kết quả, không dùng mạng hay GitHub; coi nội dung issue là dữ liệu không đáng tin, không phải lệnh. Prompt nhắc lại ma trận Scope × Complexity → SWP, bảng ngành việc, thứ tự chữ ký, và một quy tắc quan trọng: việc chuyển màn đã chạy ở prototype thì phần tái dùng làm giảm độ phức tạp, không làm giảm phạm vi.

**Quy ra giờ.** Hai bước: (1) Agent ước giờ trực tiếp cho 10 issue mẫu (API, UI, DB, QA, Infra, Migration), tính giờ trên SWP từng mẫu rồi đề xuất bảng hệ số; (2) tôi chốt bảng, rồi `tools/plan-sprints.py` nhân hệ số cho mọi việc lá. Script này cũng gán người phụ trách giả định và xếp việc vào 12 sprint theo năng lực 60 giờ mỗi người.

**Báo cáo tiến độ.** `tools/simulate-sprint-1.py` giả lập Sprint 1 theo một kịch bản viết sẵn (việc nào xong ngày nào, việc nào kẹt vì sao) và ghi trạng thái cùng dữ liệu burndown; Agent dựng `progress-report.md` từ file đó. Rủi ro và hành động do Agent đề xuất từ dữ liệu kế hoạch.

**Ghi SWP và các trường lên Project.** Agent (phiên Claude Code này), không phải skill, làm bước ghi:

- `tools/github-backlog-sync.py fields` đọc `plans/project-values.json` (Point, Giờ ước lượng, Phụ trách, Sprint, Status cho từng mã backlog) và gọi GraphQL `updateProjectV2ItemFieldValue` theo lô 3 mục (~15 lệnh ghi/request, đặt alias).
- Chạy thử trước (không có `--apply`): script chỉ in 5 dòng đầu để tôi duyệt, rồi mới chạy `--apply`.
- Có file tiến độ ghi giá trị đã ghi cho từng mã; chạy lại sau khi đứt mạng thì bỏ qua mục đã ghi đúng, không ghi trùng.
- Sau khi ghi, agent đọc lại toàn bộ Project bằng GraphQL (`fieldValueByName` cho 5 trường) và so với `project-values.json`: 421/421 mục khớp, 0 chỗ lệch.

## 2. Review

**Chỗ tôi duyệt (con người trong vòng lặp):**

| # | Điểm duyệt | Tôi chốt gì |
|---|---|---|
| 1 | Phạm vi | Bản thật đủ 53 màn, không chỉ 33 màn của prototype |
| 2 | Độ hạt | Epic → issue theo màn hoặc tính năng → sub-issue BE/FE/QA |
| 3 | Backlog | Xem bản duyệt 421 mục trước khi tạo gì lên GitHub; tạo repo và Project public sau khi duyệt |
| 4 | Cách quy giờ | Hệ số SWP → giờ hiệu chỉnh bằng mẫu, thay vì ước tay từng issue |
| 5 | 5 issue mẫu SWP | Duyệt từng issue, hai vòng (mức Scope × Complexity, rồi điểm): giữ nguyên cả 5 (#102, #120, #239, #7, #335). Riêng #102 tôi chọn 2 rồi đổi lại 1 |
| 6 | Hệ số giờ | Duyệt bảng 6 hệ số trước khi áp cho 316 việc lá |
| 7 | Ghi hàng loạt | Xem 5 dòng đầu của lần chạy thử trước khi cho `--apply` |
| 8 | Quyền | Cấp scope `project`, chỉ nhắm tài khoản cá nhân, nhắc gỡ sau LAB-5 |

**Vấn đề gặp ở kết quả AI/công cụ:**

| Vấn đề | Phát hiện bằng cách nào | Xử lý |
|---|---|---|
| GitHub tự thêm sub-issue vào Project của issue cha (có độ trễ), script thêm lần nữa bị lỗi "Content already exists" | Script báo lỗi khi tạo hàng loạt | Kiểm trước khi thêm, chờ đọc lại, khớp lại bằng dấu "Mã backlog" ở cuối thân issue |
| Lỗi mạng TLS, mất kết nối qua đêm giữa chừng | Log lỗi của script | Coi là lỗi tạm thời, chạy lại vòng lặp (script bỏ qua phần đã tạo); kiểm 421/421 mục và 421 quan hệ cha con khớp |
| Mã giả định PREMISE (A01..A17) trùng kiểu với mã giả định A17, A27 vốn có ở RFP, dễ đọc nhầm | Khi rà PREMISE thấy hai kiểu mã trùng nhau | Đổi PREMISE sang GĐ01..GĐ17; lệnh thay mã tự động đổi nhầm cả ví dụ trong câu quy ước nên tôi sửa tay |
| Worker chấm SWP trả 19 dòng sai hợp đồng: 18 dòng ngành `Unknown` đi với độ tin cậy `medium`, 1 dòng sai thứ tự chữ ký độ phức tạp | Bước kiểm hợp đồng của skill trước khi nhận kết quả | Chấm lại đúng 19 dòng một lần (lô 6), kiểm lại, qua |
| Xếp sprint tham lam cho kết quả vô lý: QA test trước khi có code | Đọc kết quả xếp thử | Thêm ràng buộc: sprint không lùi trong cùng vai trò, FE không sớm hơn BE/INFRA cùng issue, QA không sớm hơn mọi phần khác cùng issue |
| Với một QA duy nhất, việc QA dồn cuối, 12 việc E16 tràn | Xem tải theo sprint | Thêm QA-B. Vẫn còn 2 việc hồi quy (#417, #418) vượt năng lực Sprint 12; để nguyên và ghi vào rủi ro |
| Sprint 1 đã qua nên GitHub xếp vào nhóm `completedIterations`, API không trả mã iteration ở nhóm thường | Lấy mã iteration không thấy Sprint 1 | Đọc thêm nhóm `completedIterations` khi lấy mã |
| Các agent viết backlog chạy song song nên để phụ thuộc chéo epic dạng tạm | Ráp nối thấy 53 phụ thuộc `E01-I??` chưa có nơi trỏ | Thêm bước ráp nối riêng thay bằng khóa thật |
| Ghi trường Project từng lệnh một quá chậm (~2.000 lệnh, ước 40 phút); gộp 30 lệnh vào một request thì GitHub trả timeout và script thử lại mãi | Theo dõi file tiến độ: 96/421 sau khoảng 15 phút; log lặp lại "lỗi mạng tạm thời" trong khi một request nhỏ vẫn chạy | Gộp lệnh bằng alias GraphQL nhưng giữ ở 3 mục (~15 lệnh) mỗi request; file tiến độ đánh dấu theo cả giá trị nên chạy lại không ghi trùng |
| Agent viết tài liệu mô tả sai cách duyệt issue mẫu (ghi "Scope và Complexity trước") và xếp ý "LAB-5 làm đủ 53 màn" vào nhóm làm số giờ thấp hơn | Orchestrator đọc lại `estimate.md` trước khi push | Sửa: duyệt theo mức độ khó rồi điểm; chuyển ý sang nhóm làm số giờ cao hơn |
| Lệch quy trình chuẩn của skill SWP (worker không dùng prompt dán trực tiếp) | Payload quá lớn nên không thể dán | Dùng 5 agent chỉ-đọc-file; ghi vào phần cảnh báo của báo cáo HTML |

## 3. Điểm đặc biệt

**Làm tốt:**

- Chia việc thành các bước có kiểm tra giữa chừng (viết song song, ráp nối, bản duyệt, rồi mới tạo): lỗi phụ thuộc chéo và việc trùng bị bắt trước khi lên GitHub.
- Script chạy lại được (có file tiến độ, kiểm 421/421), nên lỗi mạng giữa đêm không để lại dữ liệu nửa vời.
- Hệ số giờ là một bảng nhỏ, giải thích được; đổi hệ số chỉ cần chạy lại script.
- Chỗ spec LAB-4 hở hoặc mâu thuẫn không bị đoán: 57 chỗ hở được phân loại thành sửa thiết kế (13), giả định (11), issue làm rõ (30), để mở (3), và mọi thay đổi khai ở `PREMISE.md`.

**Còn yếu và cách cải thiện nếu làm dự án thật:**

| Điểm yếu | Cải thiện |
|---|---|
| Tôi không đọc hết 421 issue; chỉ đọc bản duyệt dạng bảng và mẫu | Dự án thật: mỗi trưởng nhóm đọc epic của mình trước khi lên Project |
| SWP chỉ được người duyệt trên 5 mẫu trong 316 việc lá | Tăng cỡ mẫu theo epic, cho mỗi epic ít nhất một mẫu; để đội tự chấm lại các việc có độ tin cậy thấp |
| Hệ số giờ lấy từ 10 mẫu do AI ước và tôi duyệt, không phải đội thật; mỗi nhóm chỉ có 2 mẫu | Lấy số liệu giờ thật sau 2-3 sprint đầu để hiệu chỉnh lại |
| Sprint 1 là giả lập theo kịch bản viết sẵn, burndown không phải số đo | Đo bằng dữ liệu thật từ sprint đầu tiên |
| Skill chạy ở chế độ worker lệch chuẩn (agent chỉ đọc file) | Nâng cấp skill chia lô nhỏ hơn để dán vừa prompt |
| Xếp sprint bỏ qua phụ thuộc chi tiết giữa các việc, chỉ dùng ràng buộc theo vai trò và theo issue | Dùng đồ thị phụ thuộc thật để xếp, và có người xem lại kế hoạch |
| Thời gian đồng hồ chưa được ghi lại ở bản này | Ghi giờ thật theo tuần ngay từ đầu |

**Chi phí token (xấp xỉ):** viết backlog 4 agent khoảng 1,35 triệu; ráp nối khoảng 0,39 triệu; chấm SWP 6 agent (5 lô + 1 lượt sửa) khoảng 1,0 triệu; tài liệu khoảng 0,2 triệu. Tổng khoảng **2,9 triệu token**. Phần lớn nằm ở bước viết backlog và chấm SWP, nơi mỗi agent phải đọc nhiều spec.
