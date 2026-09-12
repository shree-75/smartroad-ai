import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

output_dir = r"C:\Users\srini\smartroad-ai\docs\diagrams"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E0'
plt.rcParams['axes.linewidth'] = 0.8

# Color Palette
NAVY = '#1A365D'
BLUE = '#2B6CB0'
LIGHT_BLUE = '#EBF8FF'
DARK_GRAY = '#2D3748'
LIGHT_GRAY = '#F7FAFC'
BORDER_GRAY = '#E2E8F0'
ACCENT_RED = '#C53030'
ACCENT_GREEN = '#2F855A'
ACCENT_GOLD = '#D69E2E'
ACCENT_PURPLE = '#6B46C1'

def create_fig1():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 96, "SmartRoad AI — End-to-End System Architecture", fontsize=14, fontweight='bold', color=NAVY, ha='center')
    
    # Input Layer (Boxes on Left)
    inputs = [
        ("Vision Sensors", "Camera, PERCLOS, Gaze, Pose", 82),
        ("Physiological Sensors", "HR, HRV, ECG, EDA, Temp", 62),
        ("Vehicle / IoT Sensors", "Speed, Steering, CAN Telemetry", 42),
        ("Road Context APIs", "Traffic, Weather, Road Type", 22)
    ]
    
    for title, sub, y in inputs:
        box = patches.FancyBboxPatch((3, y-6), 22, 11, boxstyle="round,pad=0.3", fc='#EDF2F7', ec=NAVY, lw=1.5)
        ax.add_patch(box)
        ax.text(14, y+1, title, fontsize=8.5, fontweight='bold', color=NAVY, ha='center')
        ax.text(14, y-3, sub, fontsize=7, color=DARK_GRAY, ha='center')
        # Arrow to Feature Extraction
        ax.annotate('', xy=(30, y), xytext=(25, y), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    # Feature Extraction Box
    box_fe = patches.FancyBboxPatch((30, 15), 16, 75, boxstyle="round,pad=0.3", fc='#EBF8FF', ec=BLUE, lw=1.5)
    ax.add_patch(box_fe)
    ax.text(38, 55, "MULTIMODAL\nFEATURE\nEXTRACTION\nENGINE\n\n- Landmark Extraction\n- Time-series Filters\n- Telemetry Derivs\n- Context Maps", 
            fontsize=8, fontweight='bold', color=NAVY, ha='center', va='center')
    
    # Arrow FE to Baseline & Modality Risk
    ax.annotate('', xy=(51, 75), xytext=(46, 75), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
    ax.annotate('', xy=(51, 35), xytext=(46, 35), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    # Driver Baseline & Threshold Engine (Top Middle)
    box_base = patches.FancyBboxPatch((51, 65), 20, 20, boxstyle="round,pad=0.3", fc='#FEFCBF', ec=ACCENT_GOLD, lw=1.5)
    ax.add_patch(box_base)
    ax.text(61, 78, "DRIVER BASELINE &\nDYNAMIC THRESHOLD", fontsize=8, fontweight='bold', color='#744210', ha='center')
    ax.text(61, 70, "Learns Individual Norms\n$T_i = f(B_i), z = (x - \\mu_i)/\\sigma_i$", fontsize=7.5, color=DARK_GRAY, ha='center')

    # Individual Modality Risk & Reliability (Bottom Middle)
    box_risk = patches.FancyBboxPatch((51, 20), 20, 30, boxstyle="round,pad=0.3", fc='#E2E8F0', ec=DARK_GRAY, lw=1.5)
    ax.add_patch(box_risk)
    ax.text(61, 44, "MODALITY RISK &\nRELIABILITY ESTIMATION", fontsize=8, fontweight='bold', color=NAVY, ha='center')
    ax.text(61, 31, "Risk: $R_v, R_p, R_{veh}$\nReliability: $w_v, w_p, w_{veh}$\nIllumination, Signal Quality", fontsize=7.5, color=DARK_GRAY, ha='center')

    # Connect Baseline to Threshold/Risk
    ax.annotate('', xy=(61, 50), xytext=(61, 65), arrowprops=dict(arrowstyle="->", color=ACCENT_GOLD, lw=1.5))

    # Arrows to Fusion
    ax.annotate('', xy=(76, 52), xytext=(71, 75), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
    ax.annotate('', xy=(76, 40), xytext=(71, 35), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    # Dynamic Fusion Box
    box_fuse = patches.FancyBboxPatch((76, 25), 21, 55, boxstyle="round,pad=0.3", fc='#C6F6D5', ec=ACCENT_GREEN, lw=1.5)
    ax.add_patch(box_fuse)
    ax.text(86.5, 68, "RELIABILITY-AWARE\nWEIGHTED FUSION\n& CONTEXT ENGINE", fontsize=8.5, fontweight='bold', color='#22543D', ha='center')
    ax.text(86.5, 52, r"$R_{fused} = \frac{\sum w_m R_m}{\sum w_m}$", fontsize=9, color=NAVY, ha='center')
    ax.text(86.5, 40, "Context Multiplier $C_{road}$\n(Traffic, Weather, Speed)", fontsize=7.5, color=DARK_GRAY, ha='center')
    ax.text(86.5, 30, "EXPLAINABLE RISK SCORE\n& ALERT DASHBOARD", fontsize=8, fontweight='bold', color=ACCENT_RED, ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig1_overall_architecture.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    
    # Left: Traditional Paradigm
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("Traditional Driver Monitoring Paradigm\n(Generic, Fixed, Isolated)", fontsize=10, fontweight='bold', color=ACCENT_RED)
    
    nodes1 = [
        ("Generic Driver Assumption", 8.5, '#FED7D7', ACCENT_RED),
        ("Universal Fixed Thresholds ($T_{fixed}$)", 6.5, '#FED7D7', ACCENT_RED),
        ("Single / Equal-Weight Modalities", 4.5, '#FED7D7', ACCENT_RED),
        ("Static Binary Output (Safe / Unsafe)", 2.5, '#FED7D7', ACCENT_RED)
    ]
    for text, y, bg, border in nodes1:
        box = patches.FancyBboxPatch((1, y-0.6), 8, 1.2, boxstyle="round,pad=0.2", fc=bg, ec=border, lw=1.2)
        ax1.add_patch(box)
        ax1.text(5, y, text, fontsize=8, fontweight='bold', color=NAVY, ha='center', va='center')
        if y > 2.5:
            ax1.annotate('', xy=(5, y-0.8), xytext=(5, y-0.6), arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.2))

    # Right: SmartRoad AI Paradigm
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title("SmartRoad AI Paradigm\n(Personalized, Multimodal, Context-Aware)", fontsize=10, fontweight='bold', color=ACCENT_GREEN)

    nodes2 = [
        ("Individual Driver Profile Learning", 8.5, '#C6F6D5', ACCENT_GREEN),
        ("Dynamic Personalized Thresholds $T_i(B_i)$", 6.5, '#C6F6D5', ACCENT_GREEN),
        ("Reliability-Aware Dynamic Fusion $w_m(t)$", 4.5, '#C6F6D5', ACCENT_GREEN),
        ("Explainable Continuous Risk + Road Context", 2.5, '#C6F6D5', ACCENT_GREEN)
    ]
    for text, y, bg, border in nodes2:
        box = patches.FancyBboxPatch((1, y-0.6), 8, 1.2, boxstyle="round,pad=0.2", fc=bg, ec=border, lw=1.2)
        ax2.add_patch(box)
        ax2.text(5, y, text, fontsize=8, fontweight='bold', color=NAVY, ha='center', va='center')
        if y > 2.5:
            ax2.annotate('', xy=(5, y-0.8), xytext=(5, y-0.6), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=1.2))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig2_research_gap.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig3():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 94, "Literature Survey Taxonomy of Driver Risk Intelligence", fontsize=12, fontweight='bold', color=NAVY, ha='center')
    
    # Root
    root = patches.FancyBboxPatch((35, 78), 30, 10, boxstyle="round,pad=0.3", fc=NAVY, ec=NAVY)
    ax.add_patch(root)
    ax.text(50, 83, "Driver Risk Monitoring Systems", fontsize=9, fontweight='bold', color='white', ha='center')
    
    categories = [
        ("Vision-Based", ["PERCLOS, Eye Closure", "Head Pose & Gaze", "Facial Landmarks"], 10),
        ("Physiological", ["Heart Rate & HRV", "EEG / EOG Signals", "Skin Conductance"], 30),
        ("Vehicle Telemetry", ["Steering Variability", "Speed & Accel.", "Lane Deviation"], 50),
        ("Context-Aware", ["Traffic Density", "Weather & Light", "Road Classification"], 70),
        ("Personalized ML", ["Individual Baselines", "Adaptive Thresholds", "Z-Score Norm."], 90)
    ]
    
    for title, subs, x in categories:
        # Arrow from root
        ax.annotate('', xy=(x, 62), xytext=(50, 78), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
        
        # Category Box
        cbox = patches.FancyBboxPatch((x-8, 52), 16, 10, boxstyle="round,pad=0.2", fc='#EBF8FF', ec=BLUE, lw=1.2)
        ax.add_patch(cbox)
        ax.text(x, 57, title, fontsize=8, fontweight='bold', color=NAVY, ha='center')
        
        # Sub items box
        sub_text = "\n".join([f"• {s}" for s in subs])
        sbox = patches.FancyBboxPatch((x-9, 15), 18, 32, boxstyle="round,pad=0.2", fc='#F7FAFC', ec=BORDER_GRAY, lw=1)
        ax.add_patch(sbox)
        ax.text(x, 31, sub_text, fontsize=7, color=DARK_GRAY, ha='center', va='center')
        
        ax.annotate('', xy=(x, 47), xytext=(x, 52), arrowprops=dict(arrowstyle="->", color=BORDER_GRAY, lw=1))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig3_literature_taxonomy.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig4():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    
    t = np.linspace(0, 50, 500)
    # Driver A: Naturally high eyelid closure baseline (0.22)
    driver_a = 0.22 + 0.04 * np.sin(t / 3) + 0.02 * np.random.randn(len(t))
    driver_a[300:380] += 0.12 # Drowsiness event
    
    # Driver B: Naturally low eyelid closure baseline (0.08)
    driver_b = 0.08 + 0.03 * np.cos(t / 4) + 0.015 * np.random.randn(len(t))
    driver_b[320:400] += 0.11 # Drowsiness event

    ax.plot(t, driver_a, label="Driver A (High Baseline Blink/Closure)", color=BLUE, lw=1.5)
    ax.plot(t, driver_b, label="Driver B (Low Baseline Eyelid Opening)", color=ACCENT_PURPLE, lw=1.5)
    
    # Fixed threshold
    ax.axhline(0.28, color=ACCENT_RED, linestyle='--', lw=1.5, label="Fixed Universal Threshold (T_fixed = 0.28)")
    
    # Personalized thresholds
    ax.axhline(0.34, color=BLUE, linestyle=':', lw=1.5, label="Driver A Personalized Threshold (T_A = 0.34)")
    ax.axhline(0.18, color=ACCENT_PURPLE, linestyle=':', lw=1.5, label="Driver B Personalized Threshold (T_B = 0.18)")

    # Annotate False Positive & False Negative
    ax.annotate('FALSE POSITIVE\nunder Fixed T', xy=(15, 0.285), xytext=(12, 0.38),
                arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.2), fontsize=7.5, fontweight='bold', color=ACCENT_RED)
    
    ax.annotate('FALSE NEGATIVE\nunder Fixed T (Driver B Drowsy)', xy=(350, 0.22), xytext=(360, 0.26),
                arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.2), fontsize=7.5, fontweight='bold', color=ACCENT_RED)

    ax.set_title("Fixed Threshold vs. Personalized Dynamic Thresholding", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_xlabel("Time (Seconds)", fontsize=9, color=DARK_GRAY)
    ax.set_ylabel("PERCLOS / Eyelid Closure Ratio", fontsize=9, color=DARK_GRAY)
    ax.legend(fontsize=7.5, loc='upper left', framealpha=0.9)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig4_threshold_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig5():
    fig, ax = plt.subplots(figsize=(9, 4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 92, "Personalized Driver Baseline Learning Pipeline", fontsize=11, fontweight='bold', color=NAVY, ha='center')
    
    steps = [
        ("Driver Profile Initialization\n(Vehicle Entry / Auth)", 8, '#EDF2F7', NAVY),
        ("Warm-up Driving Calibration\n(First 5-10 Minutes)", 28, '#EBF8FF', BLUE),
        ("Statistical Outlier Filtering\n(Remove Anomalies/Sudden Brakes)", 48, '#FEFCBF', '#744210'),
        ("Baseline Feature Matrix $(B_i)$\n[$\\mu_{PERCLOS}, \\sigma_{HRV}, \\mu_{steer}$]", 68, '#C6F6D5', ACCENT_GREEN),
        ("Adaptive Profile Update\n(Exponential Moving Avg)", 88, '#E2E8F0', DARK_GRAY)
    ]
    
    for text, x, bg, border in steps:
        box = patches.FancyBboxPatch((x-7.5, 30), 15, 40, boxstyle="round,pad=0.3", fc=bg, ec=border, lw=1.4)
        ax.add_patch(box)
        ax.text(x, 50, text, fontsize=7.5, fontweight='bold', color=NAVY, ha='center', va='center')
        if x < 88:
            ax.annotate('', xy=(x+8, 50), xytext=(x+12.5, 50), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
            
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig5_baseline_learning_pipeline.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig6():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 94, "Reliability-Aware Multimodal Fusion Architecture", fontsize=11, fontweight='bold', color=NAVY, ha='center')
    
    # Submodels
    mods = [
        ("Vision Pipeline\n($R_{vis}$)", 80, BLUE),
        ("Physio Pipeline\n($R_{phys}$)", 50, ACCENT_PURPLE),
        ("Vehicle Pipeline\n($R_{veh}$)", 20, ACCENT_GREEN)
    ]
    
    for text, y, col in mods:
        box = patches.FancyBboxPatch((5, y-8), 18, 16, boxstyle="round,pad=0.3", fc='#EBF8FF', ec=col, lw=1.4)
        ax.add_patch(box)
        ax.text(14, y, text, fontsize=8, fontweight='bold', color=NAVY, ha='center', va='center')
        
        # Arrow to Reliability Estimator
        ax.annotate('', xy=(30, y), xytext=(24, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.4))

    # Reliability Estimator Box
    box_rel = patches.FancyBboxPatch((30, 12), 22, 76, boxstyle="round,pad=0.3", fc='#FEFCBF', ec=ACCENT_GOLD, lw=1.5)
    ax.add_patch(box_rel)
    ax.text(41, 50, "RELIABILITY EVALUATION\nENGINE\n\n- Illumination Quality\n- Facial Occlusion\n- Signal Quality Index (SQI)\n- Telemetry Health\n\nOutputs: [$w_{vis}, w_{phys}, w_{veh}$]",
            fontsize=8, fontweight='bold', color='#744210', ha='center', va='center')

    # Arrow to Late Fusion
    ax.annotate('', xy=(58, 50), xytext=(53, 50), arrowprops=dict(arrowstyle="->", color=ACCENT_GOLD, lw=1.5))

    # Fusion Engine Box
    box_fuse = patches.FancyBboxPatch((58, 25), 22, 50, boxstyle="round,pad=0.3", fc='#C6F6D5', ec=ACCENT_GREEN, lw=1.5)
    ax.add_patch(box_fuse)
    ax.text(69, 50, "DYNAMIC WEIGHTED\nFUSION\n\n" + r"$R_{fused} = \frac{\sum w_m R_m}{\sum w_m}$" + "\n\nPrevents corrupted\nsensor dominance",
            fontsize=8, fontweight='bold', color='#22543D', ha='center', va='center')

    # Output Arrow
    ax.annotate('', xy=(85, 50), xytext=(81, 50), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=1.5))
    
    # Final Output Box
    box_out = patches.FancyBboxPatch((85, 35), 12, 30, boxstyle="round,pad=0.3", fc=NAVY, ec=NAVY)
    ax.add_patch(box_out)
    ax.text(91, 50, "Unified\nFused Risk\nScore", fontsize=8, fontweight='bold', color='white', ha='center', va='center')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig6_multimodal_fusion.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig7():
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 92, "Reliability Weight Computation Flow", fontsize=11, fontweight='bold', color=NAVY, ha='center')
    
    steps = [
        ("Raw Sensor Signal", 10, '#EDF2F7'),
        ("Signal Quality Index\n(SQI) & Confidence", 35, '#EBF8FF'),
        ("Environmental\nDecay Factor ($D_m$)", 60, '#FEFCBF'),
        ("Normalized Weight\n$w_m = \\frac{\\text{SQI}_m \\cdot (1-D_m)}{\\sum \\text{SQI}_k (1-D_k)}$", 85, '#C6F6D5')
    ]
    
    for text, x, bg in steps:
        box = patches.FancyBboxPatch((x-10, 25), 20, 50, boxstyle="round,pad=0.3", fc=bg, ec=NAVY, lw=1.2)
        ax.add_patch(box)
        ax.text(x, 50, text, fontsize=7.5, fontweight='bold', color=NAVY, ha='center', va='center')
        if x < 85:
            ax.annotate('', xy=(x+11, 50), xytext=(x+14, 50), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig7_reliability_weighting.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig8():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    
    distraction = np.linspace(0, 1, 100)
    
    r_empty = distraction * 40 + 10
    r_urban = distraction * 65 + 15
    r_traffic = distraction * 85 + 20
    
    ax.plot(distraction, r_empty, label="Empty Highway / Low Traffic ($C_{road} = 1.0$)", color=ACCENT_GREEN, lw=2)
    ax.plot(distraction, r_urban, label="Urban Normal Traffic ($C_{road} = 1.3$)", color=BLUE, lw=2)
    ax.plot(distraction, r_traffic, label="Dense Junction / Severe Weather ($C_{road} = 1.7$)", color=ACCENT_RED, lw=2)
    
    ax.set_title("Road-Context Risk Multiplier Integration ($C_{road}$)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_xlabel("Driver Distraction / Drowsiness Intensity", fontsize=9, color=DARK_GRAY)
    ax.set_ylabel("Contextual Overall Driver Risk Score (0-100)", fontsize=9, color=DARK_GRAY)
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig8_context_integration.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig9():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    
    categories = ['Base Normal', 'PERCLOS\nDrowsiness', 'Phone\nDistraction', 'Physio\nStress', 'Camera Low-Light\nDiscount', 'Traffic Density\nMultiplier', 'Final Risk']
    values = [15, 25, 30, 10, -8, 12, 84]
    
    colors = [BLUE, ACCENT_RED, ACCENT_RED, ACCENT_GOLD, ACCENT_GREEN, ACCENT_RED, NAVY]
    
    # Waterfall cumulative positions
    bottoms = [0, 15, 40, 70, 80, 72, 0]
    heights = [15, 25, 30, 10, -8, 12, 84]
    
    bars = ax.bar(categories, heights, bottom=bottoms, color=colors, width=0.55, edgecolor=DARK_GRAY, lw=1)
    
    for bar, val in zip(bars, values):
        y_pos = bar.get_y() + bar.get_height()/2 if val > 0 else bar.get_y() + val/2
        txt = f"+{val}%" if val > 0 and bar.get_x() > 0 and bar.get_x() < 5 else f"{val}%"
        ax.text(bar.get_x() + bar.get_width()/2, y_pos, txt, ha='center', va='center', fontsize=8, fontweight='bold', color='white' if val > 20 or val < 0 else NAVY)

    ax.set_title("Explainable Risk Score Factor Decomposition (Waterfall View)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_ylabel("Risk Contribution (%)", fontsize=9, color=DARK_GRAY)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig9_explainable_risk_score.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig10():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 96, "SmartRoad AI — 18-Step End-to-End Operational Workflow", fontsize=12, fontweight='bold', color=NAVY, ha='center')
    
    steps_col1 = [
        "1. Vehicle Entry / Auth",
        "2. Driver Profile Init",
        "3. Calibration Phase",
        "4. Baseline Feature Matrix",
        "5. Threshold Personalization",
        "6. Vision Stream (Camera)",
        "7. Physio Stream (ECG/HR)",
        "8. Vehicle Telemetry (CAN)",
        "9. Road Context Fetch"
    ]
    
    steps_col2 = [
        "10. Feature Extraction",
        "11. Modality Risk Calc",
        "12. Sensor Reliability Check",
        "13. Dynamic Modality Weight",
        "14. Weighted Multimodal Fusion",
        "15. Road Context Scaling",
        "16. Explainable Decomposition",
        "17. Real-Time Alert / HMI",
        "18. Profile Continuous Update"
    ]
    
    for i, s in enumerate(steps_col1):
        y = 86 - i*8.5
        box = patches.FancyBboxPatch((5, y-3), 38, 6.5, boxstyle="round,pad=0.2", fc='#EBF8FF', ec=BLUE, lw=1.2)
        ax.add_patch(box)
        ax.text(24, y, s, fontsize=7.5, fontweight='bold', color=NAVY, ha='center', va='center')
        
    for i, s in enumerate(steps_col2):
        y = 86 - i*8.5
        box = patches.FancyBboxPatch((57, y-3), 38, 6.5, boxstyle="round,pad=0.2", fc='#C6F6D5', ec=ACCENT_GREEN, lw=1.2)
        ax.add_patch(box)
        ax.text(76, y, s, fontsize=7.5, fontweight='bold', color='#22543D', ha='center', va='center')

    # Central Transition Arrow
    ax.annotate('', xy=(57, 50), xytext=(43, 50), arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=2.5))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig10_end_to_end_workflow.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig11():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 94, "Four-Stage Research Vision & System Evolution Progression", fontsize=11, fontweight='bold', color=NAVY, ha='center')
    
    levels = [
        ("Level 1\nFixed Camera Baseline", "Universal thresholds\nSingle vision modality", 10, '#EDF2F7', DARK_GRAY),
        ("Level 2\nPersonalized Camera", "Individual baseline $B_i$\nDynamic threshold $T_i$", 35, '#EBF8FF', BLUE),
        ("Level 3\nPersonalized Multimodal", "Vision + Physio + Vehicle\nReliability-aware fusion", 60, '#FEFCBF', '#744210'),
        ("Level 4\nMultimodal + Road Context", "Traffic + Weather integration\nExplainable Risk Intelligence", 85, '#C6F6D5', ACCENT_GREEN)
    ]
    
    for title, sub, x, bg, border in levels:
        box = patches.FancyBboxPatch((x-10, 25), 20, 50, boxstyle="round,pad=0.3", fc=bg, ec=border, lw=1.5)
        ax.add_patch(box)
        ax.text(x, 62, title, fontsize=8.5, fontweight='bold', color=NAVY, ha='center', va='center')
        ax.text(x, 40, sub, fontsize=7.5, color=DARK_GRAY, ha='center', va='center')
        if x < 85:
            ax.annotate('', xy=(x+11, 50), xytext=(x+14, 50), arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.8))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig11_four_stage_progression.png"), dpi=300, bbox_inches='tight')
    plt.close()

def create_fig12():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 94, "Four-Stage Experimental Evaluation & Ablation Protocol", fontsize=11, fontweight='bold', color=NAVY, ha='center')
    
    exp_boxes = [
        ("Exp 1: Fixed Camera", "Baseline benchmark", 8, 70, '#EDF2F7'),
        ("Exp 2: Personalized Camera", "+Personalized threshold", 8, 30, '#EBF8FF'),
        ("Exp 3: Personalized Multimodal", "+Physio/Vehicle fusion", 52, 70, '#FEFCBF'),
        ("Exp 4: Full SmartRoad AI", "+Road Context & Reliability", 52, 30, '#C6F6D5')
    ]
    
    for title, sub, x, y, bg in exp_boxes:
        box = patches.FancyBboxPatch((x, y-10), 40, 22, boxstyle="round,pad=0.3", fc=bg, ec=NAVY, lw=1.3)
        ax.add_patch(box)
        ax.text(x+20, y+3, title, fontsize=8.5, fontweight='bold', color=NAVY, ha='center')
        ax.text(x+20, y-4, sub, fontsize=7.5, color=DARK_GRAY, ha='center')

    # Arrows connecting experiments
    ax.annotate('', xy=(48, 70), xytext=(52, 70), arrowprops=dict(arrowstyle="<-", color=BLUE, lw=1.5))
    ax.annotate('', xy=(28, 45), xytext=(28, 55), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
    ax.annotate('', xy=(72, 45), xytext=(72, 55), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig12_experimental_framework.png"), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating 12 academic diagrams...")
    create_fig1()
    create_fig2()
    create_fig3()
    create_fig4()
    create_fig5()
    create_fig6()
    create_fig7()
    create_fig8()
    create_fig9()
    create_fig10()
    create_fig11()
    create_fig12()
    print("All 12 diagrams generated successfully in:", output_dir)
