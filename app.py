from flask import Flask, render_template, request, jsonify, Response
import requests
import time
import random
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch', methods=['POST'])
def fetch_video():
    """Trích xuất thông tin video từ TikTok URL"""
    data = request.json
    tiktok_url = data.get('url', '')
    
    if not tiktok_url:
        return jsonify({"success": False, "message": "Vui lòng nhập link TikTok!"})
    
    api_url = "https://www.tikwm.com/api/"
    params = {"url": tiktok_url, "hd": 1}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.tiktok.com/"
    }
    
    try:
        time.sleep(random.uniform(1, 2))
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                video_data = result["data"]
                video_url = video_data.get("hdplay") or video_data.get("play")
                cover = video_data.get("cover", "")
                title = video_data.get("title", "Video TikTok")
                author = video_data.get("author", {})
                author_name = author.get("nickname", "Unknown")
                author_avatar = author.get("avatar", "")
                duration = video_data.get("duration", 0)
                play_count = video_data.get("play_count", 0)
                digg_count = video_data.get("digg_count", 0)
                comment_count = video_data.get("comment_count", 0)
                share_count = video_data.get("share_count", 0)
                music_title = video_data.get("music_info", {}).get("title", "")
                music_author = video_data.get("music_info", {}).get("author", "")
                
                return jsonify({
                    "success": True,
                    "video_url": video_url,
                    "cover": cover,
                    "title": title,
                    "author_name": author_name,
                    "author_avatar": author_avatar,
                    "duration": duration,
                    "play_count": play_count,
                    "digg_count": digg_count,
                    "comment_count": comment_count,
                    "share_count": share_count,
                    "music_title": music_title,
                    "music_author": music_author
                })
            else:
                return jsonify({"success": False, "message": f"Không thể xử lý link này: {result.get('msg', 'URL không hợp lệ')}"})
        else:
            return jsonify({"success": False, "message": f"Lỗi kết nối: mã {response.status_code}"})
    except requests.exceptions.Timeout:
        return jsonify({"success": False, "message": "Hết thời gian chờ. Vui lòng thử lại!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi: {str(e)}"})

@app.route('/api/download')
def download_video():
    """Proxy tải video để tránh CORS"""
    video_url = request.args.get('url', '')
    if not video_url:
        return jsonify({"error": "Missing URL"}), 400
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.tiktok.com/"
    }
    
    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=30)
        
        def generate():
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk
        
        return Response(
            generate(),
            content_type='video/mp4',
            headers={
                'Content-Disposition': 'attachment; filename="tiktok_video_no_watermark.mp4"',
                'Content-Length': r.headers.get('Content-Length', '')
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
