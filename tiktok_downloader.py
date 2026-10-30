import requests
import time
import random

def download_tiktok_no_watermark(url, output_filename="tiktok_hd_video.mp4"):
    """
    Hàm tải video TikTok không logo, độ nét cao (HD) sử dụng API và giả mạo trình duyệt.
    """
    # Sử dụng API của TikWM (một dịch vụ miễn phí hỗ trợ lấy link gốc)
    api_url = "https://www.tikwm.com/api/"
    
    # Yêu cầu tải bản HD (sắc nét nhất)
    params = {
        "url": url,
        "hd": 1  
    }
    
    # Giả mạo (Fake) HTTP Headers để hệ thống tưởng đây là người dùng thật đang lướt web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.tiktok.com/"
    }

    try:
        print("⏳ Đang giả lập hành vi người dùng, vui lòng đợi...")
        # Random delay từ 2-5 giây trước khi gửi request để tránh bị đánh dấu là bot spam
        time.sleep(random.uniform(2, 5)) 
        
        print("🔍 Đang trích xuất dữ liệu video...")
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("code") == 0:
                # Ưu tiên lấy link HD (sắc nét), nếu không có thì lấy link thường không logo
                video_url = data["data"].get("hdplay") or data["data"].get("play")
                
                print(f"📥 Đã tìm thấy luồng video. Đang tiến hành tải xuống...")
                
                # Bắt đầu tải luồng video về máy
                video_response = requests.get(video_url, headers=headers, stream=True)
                
                with open(output_filename, 'wb') as file:
                    # Ghi file theo từng luồng nhỏ (chunk) để không tốn RAM
                    for chunk in video_response.iter_content(chunk_size=8192):
                        file.write(chunk)
                        
                print(f"✅ THÀNH CÔNG! Video đã được lưu tại: {output_filename}")
            else:
                print(f"❌ Thất bại: API trả về lỗi hoặc URL không hợp lệ. Lời nhắn: {data.get('msg')}")
        else:
            print(f"❌ Lỗi kết nối: Máy chủ trả về mã {response.status_code}")
            
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi không mong muốn: {e}")

# ==========================================
# CÁCH SỬ DỤNG
# ==========================================
if __name__ == "__main__":
    # Thay thế đường link dưới đây bằng link TikTok bạn muốn tải
    link_tiktok = "https://www.tiktok.com/@heosua235/video/7696494936396680455"
    ten_file_luu = "video_khong_logo_sieunet.mp4"
    
    download_tiktok_no_watermark(link_tiktok, ten_file_luu)
