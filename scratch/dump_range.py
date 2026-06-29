import os
from PIL import Image

def dump_range():
    os.makedirs('scratch/temp_frames', exist_ok=True)
    im = Image.open('career_copilot_demo.webp')
    
    for i in range(1120, 1201, 10):
        im.seek(i)
        frame = im.convert('RGB')
        frame.save(f'scratch/temp_frames/frame_{i:04d}.png')
        print(f"Saved frame {i}")

if __name__ == '__main__':
    dump_range()
