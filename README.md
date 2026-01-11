# Video Player with Keypress Tracking

A Python application that plays random videos from a folder and tracks user keypresses (1, 2, 3) during playback. Perfect for training exercises where you need to track responses at specific moments in videos.

## Features

- 🎬 Plays random videos from a specified folder
- ⌨️ Tracks keypresses (1, 2, 3) with precise timestamps during video playback
- 💾 Saves results to a JSON file, keeping each video's sessions separate
- 📊 Compares current session with previous sessions of the same video
- 🎯 Identifies matching keypresses at similar times across sessions (±0.5s time window)
- 📈 Calculates accuracy score showing consistency with previous sessions
- 🔧 Automatically creates necessary files and folders

---

## Complete Installation Guide for Beginners

### Step 0: Download the Project from GitHub

#### Option A: Download as ZIP (Easiest)

1. Go to the GitHub repository page
2. Click the green **Code** button (near the top right)
3. Click **Download ZIP**
4. Once downloaded, find the ZIP file in your Downloads folder
5. **Right-click** the ZIP file and select **Extract All...**
6. Choose where you want to extract it (e.g., `Z:\programmeerstuff\python\`)
7. Click **Extract**
8. You now have the project folder! Rename it if you want (e.g., `wizard training`)

#### Option B: Using Git Clone (If you have Git installed)

1. Open **Command Prompt** or **PowerShell**
2. Navigate to where you want the project:
   ```bash
   cd Z:\programmeerstuff\python\
   ```
3. Clone the repository:
   ```bash
   git clone <REPOSITORY_URL>
   ```
   Replace `<REPOSITORY_URL>` with the actual GitHub repository URL (looks like `https://github.com/username/repo-name.git`)
4. The project folder will be created automatically

---

### Step 1: Open VS Code

1. Open **Visual Studio Code**
2. Go to **File** → **Open Folder**
3. Navigate to and select the folder where you extracted/cloned the project (e.g., `Z:\programmeerstuff\python\wizard training`)
4. Click **Select Folder**

### Step 2: Open the Terminal in VS Code

1. In VS Code, go to the top menu: **Terminal** → **New Terminal**
2. A terminal window will appear at the bottom of VS Code
3. Make sure you're in the correct folder (you should see the path ending in `wizard training`)

### Step 3: Verify Python is Installed

In the terminal, type this command and press Enter:

```bash
python --version
```

You should see something like `Python 3.x.x`. If you get an error, try:

```bash
python3 --version
```

If `python3` works, use `python3` instead of `python` in all commands below.

### Step 4: Install Required Packages

In the terminal, run this command:

```bash
pip install -r requirements.txt
```

Wait for the installation to complete. You should see messages about downloading and installing `opencv-python`, `pygame`, and `numpy`.

#### If you get errors:

Try upgrading pip first:
```bash
python -m pip install --upgrade pip
```

Then try installing again:
```bash
pip install -r requirements.txt
```

### Step 5: Set Up Your Videos Folder

1. In the same folder as the script, create a new folder called **`videos`** (the script will also create this automatically if it doesn't exist)
2. Add your video files to this folder
   - Supported formats: `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`
   - You can add as many videos as you want

Your folder structure should look like this:
```
wizard training/
├── video_player.py
├── requirements.txt
├── README.md
├── videos/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── ...
```

### Step 6: Run the Script

In the terminal, type:

```bash
python main.py
```

And press Enter!

---

## How to Use

### During Video Playback:

1. A video window will open and start playing automatically
2. **Press the number keys** `1`, `2`, or `3` on your keyboard whenever you want to record a keypress
   - The timestamp will be saved automatically
   - Make sure the video window is focused** (click on it if needed)
3. **Press the number keys** `1`, `2`, or `3` on your keyboard whenever you want to record a keypress
   - The timestamp will be saved automatically
   - You'll see a message in the terminal confirming each keypress
4. **Press `ESC`** or close the window to quit the video early if needed
5## After the Video Ends:

1. The video window will close automatically
2. Your results are saved to `video_results.json`
3. The terminal will show:
   - Your current session results
   - Comparison with previous sessions (if any)
   - **Matching keypresses** - Shows when you pressed the same key at similar times (within ±0.5 seconds)
   - Statistics about all sessions for that video
   - **Accuracy score** - Percentage showing how consistent your current session is with previous sessions
   - **Rating** - Performance rating based on your accuracy (Excellent ≥80%, Good ≥60%, Moderate ≥40%, etc.)

### Running Again:

Just type `python video_player.py` in the terminal again! The script will:
- Pick a random video (might be the same one or a different one)
- Track new keypresses
- Add to the existing results

---

## Understanding the Results

The `video_results.json` file stores all your data:

```json
{
  "my_video.mp4": [
    {
      "session_id": "2026-01-09 15:30:45",
      "keypresses": [
        {"key": "1", "timestamp": 5.23},
        {"key": "2", "timestamp": 10.45},
        {"key": "3", "timestamp": 15.67}
      ]
    },
    {
      "session_id": "2026-01-09 16:15:22",
      "keypresses": [
        {"key": "1", "timestamp": 5.18},
        {"key": "3", "timestamp": 15.70}
      ]
    }
  ]
}
```

- Each video has its own section
- Each time you watch a video, it creates a new session
- Timestamps are in seconds from the start of the video

### Session Comparison & Accuracy

After each session, you'll see:

1. **Matching Keypresses Analysis**
   - Compares your current session with all previous sessions
   - Identifies when you pressed the same key at similar times (within ±0.5 seconds)
   - Shows the time difference for each match

2. **Overall Statistics**
   - Total matching keypresses across all session pairs
   - Breakdown by key (1, 2, or 3)

3. **Accuracy Score**
   - Percentage of your current keypresses that matched with previous sessions
   - Helps track consistency and improvement over time
   - Ratings:
     - **≥80%**: Excellent! Very consistent performance
     - **≥60%**: Good consistency across sessions
     - **≥40%**: Moderate consistency
     - **≥20%**: Low consistency - Keep practicing!
     - **<20%**: Very different from previous sessions

---

## Troubleshooting

### "No video files found" error
- Make sure you have video files in the `videos` folder
- Check that your videos have supported extensions (.mp4, .avi, etc.)

### Keypressesthe video window is focused** - click on the video window before pressing keys
- The pygame window must be the active window to detect keypresses
- You should see the window title bar highlighted when it's focusedow when pressing keys
- The terminal or VS Code window should be in focus

### "pip: command not found"
- Try using `python -m pip install -r requirements.txt` instead

### Video plays but window is too large/small
- The window size is automatically set to match the video resolution
- If it's too large for your screen, consider using smaller resolution videos

---

## Configuration (Optional)

If you want to use a different folder for videos, open `video_player.py` and find this line (near the bottom):

```python
VIDEO_FOLDER = "videos"  # Change to your folder path
```

Change `"videos"` to your preferred folder path:
- For the same directory: `VIDEO_FOLDER = "my_videos"`
- For a specific path: `VIDEO_FOLDER = "C:/Users/YourName/Videos"`

---

## Need Help?

Common issues are usually related to:
1. **Window focus** - Make sure to click on the video window before pressing keys
2. **Wrong folder** - Make sure you're in the correct directory
3. **Missing videos** - Check that video files are in the `videos` folder

If you're still stuck, check that:
- Python is properly installed: `python --version`
- Packages are installed: `pip list` (should show opencv-python and keyboard)
- You're in the right folder: `pwd` (PowerShell) or `cd` (shows current directory)
