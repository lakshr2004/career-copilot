import os
from PIL import Image, ImageChops, ImageStat

def find_transitions():
    frames_dir = 'scratch/temp_frames'
    files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    prev_img = None
    diffs = []
    
    for filename in files:
        img_path = os.path.join(frames_dir, filename)
        img = Image.open(img_path).convert('L')
        
        if prev_img is not None:
            diff = ImageChops.difference(img, prev_img)
            stat = ImageStat.Stat(diff)
            diffs.append((filename, stat.mean[0]))
        prev_img = img

    for filename, diff in diffs:
        print(f"Diff to {filename}: {diff:.2f}")

if __name__ == '__main__':
    find_transitions()
