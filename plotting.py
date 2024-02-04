import pandas as pd
import matplotlib.pyplot as plt

def plot_interaction_profiles(csv_path, output_path):
    df = pd.read_csv(csv_path)

    base_pairs = df["Nucleotide pairs"]
    distances = df.columns[1:]  
    for pair in base_pairs:
        scores = df[df["Nucleotide pairs"] == pair].values[0][1:].astype(float)
        plt.plot(distances, scores, label=f"{pair}")

    plt.xlabel('Distance')
    plt.ylabel('Score')
    plt.legend()
    plt.title('Interaction Profiles')
    plt.savefig(output_path)
    plt.show()

if __name__ == "__main__":
    csv_path = "Final_res.csv"  
    output_path = "interaction_profiles_plot.png"  
    plot_interaction_profiles(csv_path, output_path)
