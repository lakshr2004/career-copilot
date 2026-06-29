import json
import os

log_path = r"C:\Users\Laksh\.gemini\antigravity-ide\brain\11c4f2b9-07c6-4994-82a2-f5b48be1678a\.system_generated\logs\transcript_full.jsonl"
app_path = r"c:\Users\Laksh\Desktop\career-copilot\src\App.jsx"

if not os.path.exists(log_path):
    print("Log path does not exist")
    exit(1)

# We want to reconstruct lines 1 to 855.
# Let's map line number -> content
reconstructed_file = {}

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get("type") == "VIEW_FILE" and "Total Lines: 855" in data.get("content", ""):
                content = data["content"]
                lines = content.split("\n")
                for l in lines:
                    if ": " in l:
                        parts = l.split(": ", 1)
                        if parts[0].strip().isdigit():
                            line_num = int(parts[0].strip())
                            line_content = parts[1]
                            reconstructed_file[line_num] = line_content
        except Exception as e:
            pass

# Check if we have all lines from 1 to 855
missing_lines = []
for i in range(1, 856):
    if i not in reconstructed_file:
        missing_lines.append(i)

if missing_lines:
    print(f"Error: Missing lines: {missing_lines}")
else:
    print("All 855 lines successfully recovered!")
    # Stitch and write
    file_content = ""
    for i in range(1, 856):
        file_content += reconstructed_file[i] + "\n"
    
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"Original App.jsx restored successfully! Size: {len(file_content)} chars")
