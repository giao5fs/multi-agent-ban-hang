"""
BÀI 2 - NHIỀU AGENT + ĐỒ THỊ (tự viết bằng Python thuần, chưa cần LangGraph)
=============================================================================
Mục tiêu: hiểu Ý TƯỞNG trước khi dùng thư viện.

Đồ thị của chúng ta:

    [Nghiên cứu] ---> [Viết bài] ---> [Kiểm duyệt] ---> (DUYỆT) ---> KẾT THÚC
                          ^                |
                          |----- (SỬA) ----|

- Mỗi ô vuông là 1 NODE (một agent với 1 vai trò riêng).
- Mỗi mũi tên là 1 EDGE (sau bước này thì đi đâu).
- "STATE" (trạng thái) là cái túi chứa dữ liệu, được chuyền qua các node.

Chạy:  python bai2_do_thi_tu_viet.py
"""

from llm import goi_ai, co_api_key

SAN_PHAM = (
    "Cà phê rang xay Đắk Lắk, gói 500g, giá 180.000đ, "
    "100% Robusta rang mộc, giao trong ngày tại TP.HCM."
)
SO_LAN_SUA_TOI_DA = 3  # chống lặp vô hạn (và chống tốn tiền)


# ---------------- CÁC NODE (mỗi hàm = 1 agent) ----------------
def agent_nghien_cuu(state: dict) -> dict:
    print("🔎 [Nghiên cứu] đang phân tích sản phẩm...")
    state["nghien_cuu"] = goi_ai(
        "Bạn là chuyên gia NGHIÊN CỨU thị trường. Trả lời ngắn gọn bằng gạch đầu dòng.",
        f"Phân tích sản phẩm sau: khách hàng mục tiêu, nỗi đau của họ, "
        f"điểm mạnh sản phẩm, thông điệp chính.\n\nSản phẩm: {state['san_pham']}",
    )
    return state


def agent_viet_bai(state: dict) -> dict:
    state["so_lan_viet"] += 1
    print(f"✍️  [Viết bài] đang viết bản nháp lần {state['so_lan_viet']}...")
    state["ban_nhap"] = goi_ai(
        "Bạn là copywriter chuyên VIẾT bài bán hàng Facebook, giọng thân thiện, dưới 80 chữ.",
        f"Sản phẩm: {state['san_pham']}\n\n"
        f"Kết quả nghiên cứu:\n{state['nghien_cuu']}\n\n"
        f"Bản nháp trước:\n{state['ban_nhap'] or '(chưa có)'}\n\n"
        f"Góp ý của người kiểm duyệt:\n{state['gop_y'] or '(chưa có)'}\n\n"
        f"Hãy viết (hoặc sửa) bài đăng. Chỉ trả về nội dung bài đăng.",
    )
    return state


def agent_kiem_duyet(state: dict) -> dict:
    print("🧐 [Kiểm duyệt] đang chấm bài...")
    ket_qua = goi_ai(
        "Bạn là trưởng phòng marketing KIỂM DUYỆT bài quảng cáo, rất khó tính. "
        "Dòng đầu tiên CHỈ ghi 'DUYỆT' hoặc 'SỬA'. Các dòng sau ghi góp ý cụ thể.",
        f"Tiêu chí: mở đầu gây tò mò, nêu lợi ích rõ ràng, có lời kêu gọi hành động, "
        f"không nói sai thông tin sản phẩm.\n\nSản phẩm: {state['san_pham']}\n\n"
        f"Bài cần chấm:\n{state['ban_nhap']}",
    )
    dong_dau = ket_qua.strip().splitlines()[0].upper()
    state["duyet"] = "DUYỆT" in dong_dau
    state["gop_y"] = ket_qua
    print("   ->", "✅ DUYỆT" if state["duyet"] else "❌ YÊU CẦU SỬA")
    return state


# ---------------- EDGE CÓ ĐIỀU KIỆN (rẽ nhánh) ----------------
def buoc_tiep_theo(state: dict) -> str:
    if state["duyet"]:
        return "ket_thuc"
    if state["so_lan_viet"] >= SO_LAN_SUA_TOI_DA:
        print("⚠️  Đã sửa quá số lần cho phép, dừng lại.")
        return "ket_thuc"
    return "viet_bai"


# ---------------- BỘ CHẠY ĐỒ THỊ ----------------
def chay_do_thi(san_pham: str) -> dict:
    state = {
        "san_pham": san_pham,
        "nghien_cuu": "",
        "ban_nhap": "",
        "gop_y": "",
        "duyet": False,
        "so_lan_viet": 0,
    }
    state = agent_nghien_cuu(state)          # Nghiên cứu -> Viết bài
    while True:
        state = agent_viet_bai(state)        # Viết bài -> Kiểm duyệt
        state = agent_kiem_duyet(state)
        if buoc_tiep_theo(state) == "ket_thuc":
            break                            # DUYỆT -> Kết thúc
        # còn lại: quay về Viết bài (vòng lặp)
    return state


if __name__ == "__main__":
    print("Chế độ:", "Claude thật" if co_api_key() else "GIẢ LẬP (chưa có API key)\n")
    kq = chay_do_thi(SAN_PHAM)
    print("\n=== NGHIÊN CỨU ===\n" + kq["nghien_cuu"])
    print("\n=== BÀI ĐĂNG CUỐI CÙNG ===\n" + kq["ban_nhap"])
    print(f"\n(Số lần viết: {kq['so_lan_viet']}, được duyệt: {kq['duyet']})")
