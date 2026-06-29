import os
from PIL import Image, ImageChops

def check_for_mobile():
    im = Image.open('career_copilot_demo.webp')
    n_frames = getattr(im, 'n_frames', 1)
    
    # We will sample a few pixels at x=400, y=500 (which is in the dashboard on desktop,
    # but on mobile might be different) or we can inspect if there's a frame where the left column disappears.
    # In desktop layout, frame 0 has a sidebar on the left (x: 0 to 360) and main content on the right.
    # Let's count how many frames have a layout change by comparing each frame to frame 0.
    # We can check the difference at the column split region.
    
    mobile_frames = []
    for i in range(n_frames):
        im.seek(i)
        # Let's check if the layout is stacked. If stacked, the sidebar at the top (x=50, y=800) would be white or different.
        # Let's print out if any frame is very different in layout.
        # Actually, let's just dump a frame list and inspect some indicators, or look at the frames.
        # Let's check if the frame width/height changes, or if there's a frame where the background at the top-right changes.
        pass

    # A simpler way: let's inspect the webp frames using a script that computes average color of the left sidebar vs right content.
    # If the left sidebar is hidden/stacked, the left and right regions will look very similar.
    for i in range(0, n_frames, 20):
        im.seek(i)
        left_region = im.crop((50, 400, 150, 600)).convert('L')
        right_region = im.crop((500, 400, 600, 600)).convert('L')
        
        # average color
        l_mean = sum(left_region.getdata()) / (100 * 200)
        r_mean = sum(right_region.getdata()) / (100 * 200)
        diff = abs(l_mean - r_mean)
        print(f"Frame {i:04d}: left={l_mean:.1f}, right={r_mean:.1f}, diff={diff:.1f}")

if __name__ == '__main__':
    check_for_mobile()
