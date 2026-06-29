import os
from PIL import Image

def save_screenshots():
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)
    
    im = Image.open('career_copilot_demo.webp')
    
    # Map from output filename to frame number
    screenshot_map = {
        '01_landing.png': 200,
        '02_hitl.png': 760,
        '03_resume_analysis.png': 1120,
        '04_job_match.png': 1160,
        '05_interview_prep.png': 1200,
        '06_security_log.png': 1240
    }
    
    for filename, frame_num in screenshot_map.items():
        im.seek(frame_num)
        frame = im.convert('RGB')
        dest_path = os.path.join(assets_dir, filename)
        frame.save(dest_path)
        print(f"Saved {dest_path} from frame {frame_num}")

if __name__ == '__main__':
    save_screenshots()
