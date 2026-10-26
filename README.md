# Thực hành Multi-Agent + Đồ thị: Tự động viết bài bán hàng

Dự án nhỏ này cho 3 "nhân viên AI" làm việc với nhau như một phòng marketing:

```
[Nghiên cứu] ──> [Viết bài] ──> [Kiểm duyệt] ──(DUYỆT)──> KẾT THÚC
                     ^               │
                     └─────(SỬA)─────┘
```

- **Nghiên cứu**: phân tích sản phẩm, khách hàng, thông điệp.
- **Viết bài**: viết bài đăng Facebook dựa trên nghiên cứu.
- **Kiểm duyệt**: chấm bài; nếu chưa đạt thì gửi góp ý để Viết bài sửa lại (tối đa 3 lần).

Đây chính là "multi-agent + graph": mỗi agent là một **node**, mũi tên là **edge**,
và dữ liệu được chuyền qua các node gọi là **state**.

## Các file trong thư mục

| File | Dùng để |
|---|---|
| `bai1_mot_agent.py` | 1 AI làm tất cả (để so sánh) |
| `bai2_do_thi_tu_viet.py` | Nhiều agent + đồ thị, tự viết bằng Python thuần, dễ đọc nhất |
| `bai3_langgraph.py` | Cùng đồ thị đó nhưng dựng bằng thư viện LangGraph |
| `llm.py` | Hàm gọi AI dùng chung (có chế độ giả lập miễn phí) |
| `caidat.bat` | Bấm đúp để cài đặt |
| `chay.bat` | Bấm đúp để chạy bài 1, 2 hoặc 3 |

## Bước 1: Cài Python (chỉ làm một lần)

1. Vào https://www.python.org/downloads/ và tải bản Python 3.12 (hoặc mới hơn).
2. Khi cài, **nhớ tick ô "Add python.exe to PATH"** ở màn hình đầu tiên.
3. Kiểm tra: mở Command Prompt (gõ `cmd` vào ô tìm kiếm Windows) và gõ `python --version`.

## Bước 2: Cài thư viện

Bấm đúp vào **`caidat.bat`**. Chờ đến khi thấy chữ `XONG!`.

## Bước 3: Chạy thử (chưa cần API key)

Bấm đúp vào **`chay.bat`**, nhập `2` rồi Enter.

Bạn sẽ thấy các agent lần lượt làm việc: Nghiên cứu → Viết → Kiểm duyệt bắt sửa → Viết lại → Duyệt.
Lúc này chương trình đang ở **chế độ GIẢ LẬP**: câu trả lời là mẫu có sẵn, không tốn tiền,
chỉ để bạn hiểu luồng chạy.

## Bước 4: Dùng AI thật

1. Vào https://console.anthropic.com, đăng ký, nạp ít tiền (vài USD là đủ học rất lâu) và tạo API key.
2. Mở file **`.env`** bằng Notepad (file này được tạo ở Bước 2), thay `dien-key-cua-ban-vao-day` bằng key của bạn, lưu lại.
3. Chạy lại `chay.bat`. Giờ mỗi agent là Claude thật, và kết quả sẽ khác nhau mỗi lần.

> Giữ bí mật API key, không gửi cho ai và không đăng lên mạng.

## Đọc code theo thứ tự này

1. **`bai1_mot_agent.py`**: rất ngắn. Chú ý: `vai_tro` (agent là ai) và `yeu_cau` (việc cần làm).
2. **`bai2_do_thi_tu_viet.py`**: đọc kỹ nhất. Mỗi hàm `agent_...` là một node.
   Hàm `buoc_tiep_theo` là edge có điều kiện. Hàm `chay_do_thi` nối mọi thứ lại.
3. **`bai3_langgraph.py`**: so sánh với bài 2. Thấy không, `add_node`, `add_edge`,
   `add_conditional_edges` thay cho vòng `while` tự viết. Chương trình còn in ra sơ đồ
   dạng Mermaid; dán vào https://mermaid.live để xem hình.

## Bài tập (làm theo thứ tự, từ dễ đến khó)

1. **Đổi sản phẩm**: sửa biến `SAN_PHAM` trong `bai2_do_thi_tu_viet.py` thành sản phẩm bạn muốn bán.
2. **Đổi tiêu chí**: trong `agent_kiem_duyet`, thêm tiêu chí như "phải có emoji", "dưới 50 chữ".
3. **Thêm agent mới**: viết `agent_dich_tieng_anh` dịch bài đã duyệt sang tiếng Anh,
   rồi chạy nó sau vòng lặp. Trong bài 3: `add_node` + sửa `ket_thuc` trỏ tới node mới thay vì `END`.
4. **Nhiều kênh song song**: cho 2 agent cùng viết, một cho Facebook, một cho TikTok, từ cùng một bản nghiên cứu.
5. **Con người duyệt cuối**: trước khi kết thúc, dùng `input("Đăng bài này? (c/k): ")` để bạn tự quyết định.
6. **Đọc nhiều sản phẩm**: đọc danh sách sản phẩm từ file Excel/CSV và chạy đồ thị cho từng sản phẩm.

## Từ bài tập đến kiếm tiền

Sau bài tập 6, bạn đã có một công cụ "nhập danh sách sản phẩm → ra bài đăng đã kiểm duyệt".
Đó là thứ các shop online (Shopee, TikTok Shop, Facebook) cần mỗi ngày:

- Làm thử miễn phí cho 1-2 shop quen, **đo thời gian tiết kiệm được**.
- Dùng con số đó để chào dịch vụ: phí cài đặt + phí hàng tháng.
- Cùng khuôn mẫu này áp dụng được cho: trả lời tin nhắn khách, viết mô tả sản phẩm,
  phân tích đánh giá của khách, soạn báo giá...

Khách hàng không mua "multi-agent", họ mua "đỡ mất 2 tiếng mỗi ngày".
