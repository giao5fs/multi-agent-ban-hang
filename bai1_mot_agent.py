"""
BÀI 1 - MỘT AGENT DUY NHẤT
==========================
Cách "truyền thống": nhờ 1 AI làm hết trong 1 lần.
Chạy:  python bai1_mot_agent.py
"""

from llm import goi_ai, co_api_key

SAN_PHAM = (
    "Cà phê rang xay Đắk Lắk, gói 500g, giá 180.000đ, "
    "100% Robusta rang mộc, giao trong ngày tại TP.HCM."
)

vai_tro = "Bạn là người VIẾT bài quảng cáo bán hàng trên Facebook, giọng thân thiện."
yeu_cau = f"Viết một bài đăng Facebook ngắn (dưới 80 chữ) bán sản phẩm sau:\n{SAN_PHAM}"

print("Chế độ:", "Claude thật" if co_api_key() else "GIẢ LẬP (chưa có API key)")
print("\n=== KẾT QUẢ CỦA 1 AGENT ===\n")
print(goi_ai(vai_tro, yeu_cau))

print(
    "\nNhận xét: không ai kiểm tra bài này. Nếu bài dở, bạn phải tự đọc và tự yêu cầu sửa.\n"
    "Bài 2 sẽ chia việc cho NHIỀU agent và để chúng tự kiểm tra lẫn nhau."
)
