"""
llm.py - Hàm dùng chung để "gọi AI".

- Nếu bạn đã điền ANTHROPIC_API_KEY vào file .env  -> gọi Claude thật.
- Nếu chưa có key                                  -> chạy CHẾ ĐỘ GIẢ LẬP
  (trả lời mẫu có sẵn) để bạn vẫn thấy được luồng chạy của các agent.
"""

import os
import sys

# Giúp cửa sổ dòng lệnh Windows hiển thị đúng tiếng Việt
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Đọc file .env (nếu đã cài thư viện python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL = os.getenv("MODEL", "claude-sonnet-5-5")


def co_api_key() -> bool:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    return bool(key) and not key.startswith("dien-key")


def goi_ai(vai_tro: str, yeu_cau: str) -> str:
    """
    vai_tro : mô tả agent là ai, làm gì (system prompt)
    yeu_cau : nội dung cụ thể cần làm lần này
    Trả về  : câu trả lời của AI (dạng chữ)
    """
    if not co_api_key():
        return _tra_loi_gia_lap(vai_tro, yeu_cau)

    import anthropic

    client = anthropic.Anthropic()  # tự đọc ANTHROPIC_API_KEY
    try:
        tin_nhan = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            system=vai_tro,
            messages=[{"role": "user", "content": yeu_cau}],
        )
    except anthropic.AuthenticationError as e:
        _dung_lai(
            "API key KHÔNG HỢP LỆ (lỗi 401).",
            "- Key đúng phải bắt đầu bằng 'sk-ant-api03-'. Tạo key tại "
            "https://console.anthropic.com/settings/keys\n"
            "- Mở file .env, dán lại key, không có dấu cách hay dấu ngoặc kép.",
            e,
        )
    except anthropic.PermissionDeniedError as e:
        _dung_lai("Key không có quyền dùng model này (lỗi 403).",
                  "- Kiểm tra tài khoản/workspace của key trên console.anthropic.com.", e)
    except anthropic.NotFoundError as e:
        _dung_lai(f"Không tìm thấy model '{MODEL}' (lỗi 404).",
                  "- Sửa dòng MODEL trong file .env, ví dụ: MODEL=claude-sonnet-5-5", e)
    except anthropic.RateLimitError as e:
        _dung_lai("Gửi quá nhiều yêu cầu (lỗi 429).", "- Chờ 1 phút rồi chạy lại.", e)
    except anthropic.BadRequestError as e:
        goi_y = "- Đọc thông báo gốc bên dưới."
        if "credit" in str(e).lower():
            goi_y = ("- Tài khoản HẾT TIỀN. Nạp thêm tại "
                     "https://console.anthropic.com/settings/billing")
        _dung_lai("Yêu cầu bị từ chối (lỗi 400).", goi_y, e)
    except anthropic.APIConnectionError as e:
        _dung_lai("Không kết nối được tới Claude.",
                  "- Kiểm tra mạng Internet, VPN, tường lửa hoặc proxy công ty.", e)
    # Câu trả lời có thể gồm nhiều khối (ví dụ khối "suy nghĩ" + khối chữ).
    # Chỉ lấy các khối chữ (type == "text") và ghép lại.
    return "".join(
        khoi.text for khoi in tin_nhan.content if getattr(khoi, "type", "") == "text"
    ).strip()


def _dung_lai(van_de: str, cach_sua: str, loi: Exception):
    print("\n❌ LỖI KHI GỌI CLAUDE:", van_de)
    print("👉 Cách sửa:\n" + cach_sua)
    print("\n(Thông báo gốc:", str(loi)[:300] + ")")
    sys.exit(1)


# ---------------------------------------------------------------------------
# CHẾ ĐỘ GIẢ LẬP: không tốn tiền, không cần mạng. Chỉ để học luồng chạy.
# ---------------------------------------------------------------------------
def _tra_loi_gia_lap(vai_tro: str, yeu_cau: str) -> str:
    v = vai_tro.upper()

    if "NGHIÊN CỨU" in v:
        return (
            "- Khách hàng mục tiêu: dân văn phòng 25-40 tuổi, thích cà phê nguyên chất.\n"
            "- Nỗi đau: cà phê ngoài hàng hay pha tạp, không rõ nguồn gốc.\n"
            "- Điểm mạnh: 100% Robusta Đắk Lắk, rang mộc, giao nhanh.\n"
            "- Gợi ý thông điệp: 'Cà phê thật - vị đậm thật - nguồn gốc rõ ràng'."
        )

    if "VIẾT" in v:
        if "GÓP Ý" in yeu_cau.upper() and "(chưa có)" not in yeu_cau:
            return (
                "[BẢN ĐÃ SỬA] ☕ Sáng nay bạn uống cà phê thật hay cà phê 'pha'?\n"
                "Cà phê rang mộc Đắk Lắk - 100% Robusta, không tẩm, không pha.\n"
                "Gói 500g chỉ 180.000đ, giao trong ngày tại TP.HCM.\n"
                "👉 Inbox ngay để nhận ưu đãi giảm 10% cho đơn đầu tiên!"
            )
        return (
            "Cà phê rang xay Đắk Lắk rất ngon, gói 500g giá 180.000đ. "
            "Mua ngay nhé."
        )

    if "KIỂM DUYỆT" in v:
        if "[BẢN ĐÃ SỬA]" in yeu_cau:
            return "DUYỆT\nBài viết có mở đầu cuốn hút, nêu rõ lợi ích và có lời kêu gọi hành động."
        return (
            "SỬA\n"
            "- Mở đầu nhạt, chưa gây tò mò.\n"
            "- Chưa nêu điểm khác biệt (nguyên chất, rang mộc).\n"
            "- Thiếu lời kêu gọi hành động cụ thể và ưu đãi."
        )

    return "(giả lập) Đây là câu trả lời mẫu."
