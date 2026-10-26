"""
BÀI 3 - CÙNG Ý TƯỞNG, NHƯNG DÙNG THƯ VIỆN LANGGRAPH
====================================================
LangGraph là thư viện phổ biến để dựng hệ thống multi-agent dạng đồ thị.
So với Bài 2, bạn KHÔNG phải tự viết vòng lặp while nữa: chỉ cần khai báo
node và edge, LangGraph tự chạy, và còn vẽ được sơ đồ cho bạn.

Chạy:  python bai3_langgraph.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from llm import co_api_key
# Dùng lại đúng các agent đã viết ở Bài 2
from bai2_do_thi_tu_viet import (
    SAN_PHAM,
    agent_nghien_cuu,
    agent_viet_bai,
    agent_kiem_duyet,
    buoc_tiep_theo,
)


# 1) STATE: khai báo cái "túi dữ liệu" có những ngăn nào
class TrangThai(TypedDict):
    san_pham: str
    nghien_cuu: str
    ban_nhap: str
    gop_y: str
    duyet: bool
    so_lan_viet: int


# 2) Tạo đồ thị và thêm các NODE
do_thi = StateGraph(TrangThai)
do_thi.add_node("nghien_cuu", agent_nghien_cuu)
do_thi.add_node("viet_bai", agent_viet_bai)
do_thi.add_node("kiem_duyet", agent_kiem_duyet)

# 3) Nối các EDGE
do_thi.add_edge(START, "nghien_cuu")
do_thi.add_edge("nghien_cuu", "viet_bai")
do_thi.add_edge("viet_bai", "kiem_duyet")
do_thi.add_conditional_edges(          # rẽ nhánh sau khi kiểm duyệt
    "kiem_duyet",
    buoc_tiep_theo,
    {"viet_bai": "viet_bai", "ket_thuc": END},
)

# 4) "Biên dịch" thành ứng dụng chạy được
ung_dung = do_thi.compile()


if __name__ == "__main__":
    print("Chế độ:", "Claude thật" if co_api_key() else "GIẢ LẬP (chưa có API key)")

    # In sơ đồ (dạng Mermaid) - dán vào https://mermaid.live để xem hình
    try:
        print("\n--- SƠ ĐỒ ĐỒ THỊ (Mermaid) ---")
        print(ung_dung.get_graph().draw_mermaid())
    except Exception:
        pass

    kq = ung_dung.invoke({
        "san_pham": SAN_PHAM,
        "nghien_cuu": "",
        "ban_nhap": "",
        "gop_y": "",
        "duyet": False,
        "so_lan_viet": 0,
    })

    print("\n=== BÀI ĐĂNG CUỐI CÙNG ===\n" + kq["ban_nhap"])
    print(f"\n(Số lần viết: {kq['so_lan_viet']}, được duyệt: {kq['duyet']})")
