import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def generate_dual_batter_pitch_map(excel_file_path1, excel_file_path2, batter_name1, batter_name2, match1, match2):
    """
    Generate two side-by-side cricket pitch maps for batters from same/different files/data.
    
    Parameters:
    excel_file_path1, excel_file_path2 (str): Paths to the CSV files
    batter_name1, batter_name2 (str): Names of the batter(s) to analyze
    match1, match2 (str): Match titles for each plot
    """
    try:
        # Read both CSV files
        df1 = pd.read_csv(excel_file_path1)
        df2 = pd.read_csv(excel_file_path2)
        
        # Check for required columns
        required_columns = ['bounce_x', 'bounce_y', 'batter', 'runs']
        for df in [df1, df2]:
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Files must contain 'bounce_x', 'bounce_y', 'batter', and 'runs' columns")
        
        # Filter deliveries
        all_deliveries1 = df1[df1['batter'] == batter_name1]
        all_deliveries2 = df2[df2['batter'] == batter_name2]
        
        #Second filter
        batter_deliveries1 = all_deliveries1[all_deliveries1['ball_type'] == 'Seam']
        batter_deliveries2 = all_deliveries2[all_deliveries2['ball_type'] == 'Spin']

        if batter_deliveries1.empty or batter_deliveries2.empty:
            raise ValueError(f"No deliveries found for one or both batters")
        
        # Set up figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 9), sharey=True)
        
        # Pitch dimensions
        pitch_length = 20.12
        pitch_width = 3.05
        
        # Function to draw pitch
        def draw_pitch(ax):
            ax.set_facecolor('green')
            ax.add_patch(plt.Rectangle((-pitch_width/2, 0), pitch_width, pitch_length, 
                                     facecolor='white', edgecolor='none', zorder=0))
            ax.plot([pitch_width/2, pitch_width/2], [0, pitch_length], 'k-', linewidth=1)
            ax.plot([-pitch_width/2, -pitch_width/2], [0, pitch_length], 'k-', linewidth=1)
            ax.plot([-pitch_width/2, pitch_width/2], [0, 0], 'k-', linewidth=1)
            ax.plot([-pitch_width/2, pitch_width/2], [pitch_length, pitch_length], 'k-', linewidth=1)
            ax.plot([-1.22, 1.22], [pitch_length-1.22, pitch_length-1.22], 'k-', linewidth=1)
            ax.plot([-1.22, 1.22], [1.22, 1.22], 'k-', linewidth=1)
            
            stump_width = 0.2286
            stump_positions = [-stump_width/2, 0, stump_width/2]
            for x in stump_positions:
                ax.plot([x, x], [pitch_length-0.1, pitch_length+0.1], 'k-', linewidth=2)
                ax.plot([x, x], [-0.1, 0.1], 'k-', linewidth=2)
                ax.plot([x, x], [0, pitch_length], 'k--', linewidth=1, alpha=0.5)
            
            # Wide lines (only for second version)
            if ax == ax2:
                wide_line_positions = [-0.89, 0.89]
                for x in wide_line_positions:
                    ax.plot([x, x], [0, pitch_length], 'r--', linewidth=1, alpha=0.5)
        
        # Draw pitch on both axes
        draw_pitch(ax1)
        draw_pitch(ax2)
        
        # Length classification functions
        def classify_length1(y):  # First version
            if y < 0: return 'full toss'
            elif y < 2: return 'yorker'
            elif y < 4: return 'slot'
            elif y < 6: return 'full'
            elif y < 8: return 'good'
            elif y < 10: return 'back of length'
            else: return 'short'
        
        def classify_length2(y):  # Second version
            if y < 0: return 'full toss'
            elif y < 2: return 'yorker'
            elif y < 4: return 'slot'
            elif y < 6: return 'good'
            elif y < 7: return 'back of length'
            else: return 'short'
        
        # Length colors and regions
        length_colors1 = {
            'full toss': 'grey', 'yorker': 'green', 'slot': 'cyan', 'full': 'blue',
            'good': 'purple', 'back of length': 'orange', 'short': 'red'
        }
        
        length_colors2 = {
            'full toss': 'grey', 'yorker': 'green', 'slot': 'cyan',
            'good': 'purple', 'back of length': 'orange', 'short': 'red'
        }
        
        length_regions1 = [
            ('full toss', pitch_length, pitch_length+1),
            ('yorker', pitch_length-2, pitch_length),
            ('slot', pitch_length-4, pitch_length-2),
            ('full', pitch_length-6, pitch_length-4),
            ('good', pitch_length-8, pitch_length-6),
            ('back of length', pitch_length-10, pitch_length-8),
            ('short', 0, pitch_length-10)
        ]
        
        length_regions2 = [
            ('full toss', pitch_length, pitch_length+1),
            ('yorker', pitch_length-2, pitch_length),
            ('slot', pitch_length-4, pitch_length-2),
            ('good', pitch_length-6, pitch_length-4),
            ('back of length', pitch_length-7, pitch_length-6),
            ('short', 0, pitch_length-7)
        ]
        
        outcome_colors = {
            'W': 'brown', 0: 'green', 1: 'blue', 2: 'cyan', 3: 'cyan',
            4: 'red', 6: 'magenta', 'default': 'gray'
        }
        
        # Plot deliveries
        def plot_deliveries(ax, deliveries, classify_length):
            plotted_outcomes = set()
            for index, row in deliveries.iterrows():
                outcome = 'W' if row['runs'] == -1 else row['runs']
                color = outcome_colors.get(outcome, outcome_colors['default'])
                label = str(outcome) if str(outcome) not in plotted_outcomes else ""
                plotted_outcomes.add(str(outcome))
                ax.scatter(row['bounce_y'], pitch_length-row['bounce_x'],
                          c=color, s=50, alpha=0.6, label=label)
        
        plot_deliveries(ax1, batter_deliveries1, classify_length1)
        plot_deliveries(ax2, batter_deliveries2, classify_length2)
        
        # Add length regions
        for label, y_min, y_max in length_regions1:
            ax1.axhspan(y_min, y_max, alpha=0.1, color=length_colors1[label])
            y_mid = (y_min + y_max) / 2
            ax1.text(-pitch_width/2 + 0.5, y_mid, label, 
                    ha='right', va='center', fontsize=8, rotation=0)
        
        for label, y_min, y_max in length_regions2:
            ax2.axhspan(y_min, y_max, alpha=0.1, color=length_colors2[label])
            y_mid = (y_min + y_max) / 2
            ax2.text(-pitch_width/2 + 0.5, y_mid, label, 
                    ha='right', va='center', fontsize=8, rotation=0)
        
        # Customize plots
        for ax, batter, match, deliveries in [(ax1, batter_name1, match1, batter_deliveries1),
                                            (ax2, batter_name2, match2, batter_deliveries2)]:
            ax.set_xlim(-pitch_width/2 - 0.5, pitch_width/2 + 0.5)
            ax.set_ylim(-1, pitch_length + 1)
            ax.set_title(f'{batter} vs {match} : IPL 2025 (first 3 games) \n({len(deliveries)} balls)', fontsize=10)
            ax.set_xlabel('Width (m)', fontsize=8)
            ax.legend(title='Outcome', title_fontsize=8, fontsize=6, loc='upper right')
            ax.grid(True, alpha=0.3)
            ax.text(pitch_width/2-0.1, 1.5, "@rsudharshan95",
                   ha='right', va='bottom', fontsize=8, color='red', alpha=0.7)
        
        ax1.set_ylabel('Length (meters)', fontsize=10)
        
        # Set y-ticks
        y_ticks_from_batting = np.arange(0, pitch_length + 2, 2)
        y_ticks_from_bowling = pitch_length - y_ticks_from_batting
        for ax in [ax1, ax2]:
            ax.set_yticks(y_ticks_from_bowling)
            ax.set_yticklabels([f'{tick:.0f}' for tick in y_ticks_from_batting])
        
        plt.tight_layout()
        plt.show()
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    file_path = 'SHREYAS_IYER_IPL_2025.csv'
    batter = 'SHREYAS IYER'
    match1 = 'PACE'
    match2 = 'SPIN'
    
    generate_dual_batter_pitch_map(file_path, file_path, batter, batter, match1, match2)