import os
from PIL import Image

def dump_frames():
    os.makedirs('scratch/temp_frames', exist_ok=True)
    im = Image.open('career_copilot_demo.webp')
    
    n_frames = getattr(im, 'n_frames', 1)
    print(f"Total frames: {n_frames}")
    
    interval = 40
    for i in range(0, n_frames, interval):
        im.seek(i)
        frame = im.convert('RGB')
        frame.save(f'scratch/temp_frames/frame_{i:04d}.png')
        print(f"Saved frame {i}")

if __name__ == '__main__':
    dump_frames()
