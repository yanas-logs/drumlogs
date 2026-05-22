import os

class TerminalVisualizer:
    @staticmethod
    def clear_line():
        print("\r\033[K", end="")

    @staticmethod
    def render(current_step, total_steps, active_tracks):
        grid = []
        for step in range(total_steps):
            if step == current_step:
                grid.append("█")
            elif step % 4 == 0:
                grid.append("┿")
            else:
                grid.append("•")
        
        grid_str = " ".join(grid)
        tracks_str = ", ".join(active_tracks) if active_tracks else "none"
        
        print(f"\r[Step {current_step + 1:02d}/{total_steps:02d}] [{grid_str}] | Active: {tracks_str}", end="", flush=True)
