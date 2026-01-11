import cv2
import json
import os
import random
import time
from datetime import datetime
from pathlib import Path
import pygame
import numpy as np

class VideoPlayer:
    def __init__(self, video_folder, results_file="video_results.json"):
        self.video_folder = video_folder
        self.results_file = results_file
        self.keypresses = []
        self.video_start_time = None
        self.is_playing = False
        self.current_video = None
        
        # Initialize pygame
        pygame.init()
        
        # Create results file if it doesn't exist
        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w') as f:
                json.dump({}, f, indent=2)
    
    def get_random_video(self):
        """Get a random video file from the folder."""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(Path(self.video_folder).glob(f'*{ext}'))
        
        if not video_files:
            raise FileNotFoundError(f"No video files found in {self.video_folder}")
        
        return str(random.choice(video_files))
    
    def record_keypress(self, key):
        """Record the keypress with timestamp."""
        if self.video_start_time:
            timestamp = time.time() - self.video_start_time
            self.keypresses.append({
                "key": key,
                "timestamp": round(timestamp, 2)
            })
            print(f"Key '{key}' pressed at {timestamp:.2f}s")
    
    def play_video(self, video_path):
        """Play the video and track keypresses."""
        self.current_video = os.path.basename(video_path)
        self.keypresses = []
        self.is_playing = True
        self.video_start_time = time.time()
        
        # Open video with OpenCV
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            self.is_playing = False
            return
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30  # Default FPS if unable to detect
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create pygame window
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f'Video Player - {self.current_video}')
        clock = pygame.time.Clock()
        
        print(f"\nPlaying: {self.current_video}")
        print("Press 1, 2, or 3 during playback to record keypresses")
        print("Press ESC or close window to quit early")
        print("Make sure the video window is focused!\n")
        
        # Last pressed key time for debouncing
        last_key_time = {'1': 0, '2': 0, '3': 0}
        debounce_delay = 0.3  # seconds
        
        while self.is_playing:
            # Handle pygame events
            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nVideo stopped by user")
                    self.is_playing = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("\nVideo stopped by user")
                        self.is_playing = False
                        break
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        if current_time - last_key_time['1'] > debounce_delay:
                            self.record_keypress('1')
                            last_key_time['1'] = current_time
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        if current_time - last_key_time['2'] > debounce_delay:
                            self.record_keypress('2')
                            last_key_time['2'] = current_time
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        if current_time - last_key_time['3'] > debounce_delay:
                            self.record_keypress('3')
                            last_key_time['3'] = current_time
            
            if not self.is_playing:
                break
            
            # Read frame from video
            ret, frame = cap.read()
            
            if not ret:
                # End of video
                break
            
            # Convert from BGR (OpenCV) to RGB (Pygame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Rotate frame (OpenCV and Pygame have different coordinate systems)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            
            # Display frame
            screen.blit(frame, (0, 0))
            pygame.display.flip()
            
            # Control playback speed
            clock.tick(fps)
        
        self.is_playing = False
        cap.release()
        pygame.quit()
    
    def save_results(self):
        """Save the current session results to JSON file."""
        # Load existing results
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        # Create session data
        session_data = {
            "session_id": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keypresses": self.keypresses
        }
        
        # Add to results
        if self.current_video not in results:
            results[self.current_video] = []
        
        results[self.current_video].append(session_data)
        
        # Save back to file
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to {self.results_file}")
    
    def compare_with_previous(self):
        """Compare current session with previous sessions of the same video."""
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        if self.current_video not in results:
            print("\nNo previous sessions found for this video.")
            return
        
        sessions = results[self.current_video]
        
        if len(sessions) <= 1:
            print("\nThis is the first session for this video. No comparison available.")
            return
        
        print(f"\n{'='*60}")
        print(f"COMPARISON: {self.current_video}")
        print(f"{'='*60}")
        
        # Current session (last one)
        current = sessions[-1]
        print(f"\nCurrent session ({current['session_id']}):")
        print(f"  Total keypresses: {len(current['keypresses'])}")
        if current['keypresses']:
            for kp in current['keypresses']:
                print(f"    Key {kp['key']} at {kp['timestamp']}s")
        else:
            print("    No keypresses recorded")
        
        # Previous sessions
        print(f"\nPrevious sessions ({len(sessions) - 1}):")
        for i, session in enumerate(sessions[:-1], 1):
            print(f"\n  Session {i} ({session['session_id']}):")
            print(f"    Total keypresses: {len(session['keypresses'])}")
            if session['keypresses']:
                for kp in session['keypresses']:
                    print(f"      Key {kp['key']} at {kp['timestamp']}s")
            else:
                print("      No keypresses recorded")
        
        # Statistical comparison
        print(f"\n{'='*60}")
        print("STATISTICS:")
        all_sessions = sessions
        avg_keypresses = sum(len(s['keypresses']) for s in all_sessions) / len(all_sessions)
        print(f"  Average keypresses per session: {avg_keypresses:.2f}")
        
        # Count key frequencies
        key_counts = {'1': 0, '2': 0, '3': 0}
        for session in all_sessions:
            for kp in session['keypresses']:
                key_counts[kp['key']] = key_counts.get(kp['key'], 0) + 1
        
        print(f"  Total key frequencies across all sessions:")
        for key, count in sorted(key_counts.items()):
            print(f"    Key {key}: {count} times")
        
        # Compare same key presses at similar times across sessions
        print(f"\n{'='*60}")
        print("MATCHING KEYPRESSES (Same key at similar time):")
        print("(Time window: ±0.5 seconds)")
        print(f"{'='*60}")
        
        time_window = 0.5  # seconds - consider keypresses within this window as "same time"
        matches_found = False
        
        # Compare current session with each previous session
        for i, prev_session in enumerate(sessions[:-1], 1):
            print(f"\nComparing current session with Session {i}:")
            session_matches = []
            
            for curr_kp in current['keypresses']:
                for prev_kp in prev_session['keypresses']:
                    # Check if same key pressed at similar time
                    if (curr_kp['key'] == prev_kp['key'] and 
                        abs(curr_kp['timestamp'] - prev_kp['timestamp']) <= time_window):
                        time_diff = curr_kp['timestamp'] - prev_kp['timestamp']
                        session_matches.append({
                            'key': curr_kp['key'],
                            'current_time': curr_kp['timestamp'],
                            'previous_time': prev_kp['timestamp'],
                            'time_diff': time_diff
                        })
                        matches_found = True
            
            if session_matches:
                print(f"  Found {len(session_matches)} matching keypresses:")
                for match in session_matches:
                    print(f"    Key '{match['key']}' - Current: {match['current_time']:.2f}s, "
                          f"Previous: {match['previous_time']:.2f}s "
                          f"(diff: {match['time_diff']:+.2f}s)")
            else:
                print(f"  No matching keypresses found")
        
        # Overall matching statistics
        print(f"\n{'='*60}")
        print("OVERALL MATCHING STATISTICS:")
        
        # Count total matches across all session pairs
        total_comparisons = 0
        total_matches = 0
        key_match_counts = {'1': 0, '2': 0, '3': 0}
        
        for i in range(len(sessions)):
            for j in range(i + 1, len(sessions)):
                total_comparisons += 1
                for kp1 in sessions[i]['keypresses']:
                    for kp2 in sessions[j]['keypresses']:
                        if (kp1['key'] == kp2['key'] and 
                            abs(kp1['timestamp'] - kp2['timestamp']) <= time_window):
                            total_matches += 1
                            key_match_counts[kp1['key']] += 1
        
        print(f"  Total session pairs compared: {total_comparisons}")
        print(f"  Total matching keypresses across all pairs: {total_matches}")
        print(f"  Matching keypresses by key:")
        for key in sorted(key_match_counts.keys()):
            print(f"    Key '{key}': {key_match_counts[key]} matches")
        
        if not matches_found:
            print("\n  No matching keypresses found at similar times.")
        
        # Calculate accuracy score
        print(f"\n{'='*60}")
        print("ACCURACY SCORE:")
        print(f"{'='*60}")
        
        # Calculate accuracy based on current session vs previous sessions
        if len(current['keypresses']) == 0:
            print("  Cannot calculate accuracy: no keypresses in current session")
        else:
            # Count how many current keypresses have matches in previous sessions
            matched_current = set()
            total_previous_sessions = len(sessions) - 1
            
            for curr_idx, curr_kp in enumerate(current['keypresses']):
                for prev_session in sessions[:-1]:
                    for prev_kp in prev_session['keypresses']:
                        if (curr_kp['key'] == prev_kp['key'] and 
                            abs(curr_kp['timestamp'] - prev_kp['timestamp']) <= time_window):
                            matched_current.add(curr_idx)
                            break
            
            accuracy = (len(matched_current) / len(current['keypresses'])) * 100
            
            print(f"  Current session keypresses: {len(current['keypresses'])}")
            print(f"  Matched with previous sessions: {len(matched_current)}")
            print(f"  Accuracy: {accuracy:.1f}%")
            
            # Additional context
            if accuracy >= 80:
                print(f"  Rating: Excellent! Very consistent performance.")
            elif accuracy >= 60:
                print(f"  Rating: Good consistency across sessions.")
            elif accuracy >= 40:
                print(f"  Rating: Moderate consistency.")
            elif accuracy >= 20:
                print(f"  Rating: Low consistency. Keep practicing!")
            else:
                print(f"  Rating: Very different from previous sessions.")
        
        print(f"{'='*60}\n")
    
    def run(self):
        """Main method to run the video player."""
        try:
            # Get random video
            video_path = self.get_random_video()
            
            # Play video
            self.play_video(video_path)
            
            # Save results
            self.save_results()
            
            # Compare with previous sessions
            self.compare_with_previous()
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.is_playing = False


if __name__ == "__main__":
    # Configure your video folder path here
    VIDEO_FOLDER = "videos"  # Change this to your video folder path
    
    # Check if folder exists
    if not os.path.exists(VIDEO_FOLDER):
        print(f"Creating video folder: {VIDEO_FOLDER}")
        os.makedirs(VIDEO_FOLDER)
        print(f"Please add video files to the '{VIDEO_FOLDER}' folder and run again.")
    else:
        player = VideoPlayer(VIDEO_FOLDER)
        player.run()
