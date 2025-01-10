import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Result_analysis:
    def __init__(self, json_path: str, figure_size: tuple = (12, 6)):
        """
        Initialize the analyzer with the path to the JSON file
        
        Parameters:
        -----------
        json_path : str
            Path to the JSON file containing simulation data
        figure_size : tuple
            Default size for matplotlib figures
        """
        self.figure_size = figure_size
        self.data = self._load_data(json_path)
        self.personalities_df = self._process_personalities()
        self.steps_df = self._process_steps()
        
    def _load_data(self, json_path: str) -> dict:
        """Load JSON data from file"""
        with open(json_path, 'r') as f:
            return json.load(f)
            
    def _process_personalities(self) -> pd.DataFrame:
        """Convert personalities dict to DataFrame"""
        personalities = pd.DataFrame.from_dict(
            self.data['results']['agent_infos']['personalities'],
            orient='index'
        )
        return personalities
        
    def _process_steps(self) -> pd.DataFrame:
        """Convert steps needed per agent to DataFrame"""
        steps = pd.DataFrame.from_dict(
            self.data['results']['agent_infos']['steps_needed_per_agent'],
            orient='index',
            columns=['steps']
        )
        return steps
        
    def plot_density_over_time(self, title: str = "Maximum Density Evolution Over Time"):
        """Plot the maximum density evolution over simulation steps"""
        plt.figure(figsize=self.figure_size)
        densities = self.data['results']['density_metrics']['max_density_across_episodes']
        plt.plot(densities, linewidth=2)
        plt.title(title)
        plt.xlabel("Simulation Step")
        plt.ylabel("Maximum Density")
        plt.grid(True)
        plt.show()
        
    def plot_personality_distributions(self, title: str = "Distribution of Personality Traits"):
        """Plot the distribution of each personality trait"""
        plt.figure(figsize=self.figure_size)
        self.personalities_df.boxplot()
        plt.title(title)
        plt.ylabel("Trait Value")
        plt.grid(True)
        plt.show()
        
    def plot_steps_distribution(self, title: str = "Distribution of Steps Needed for Evacuation"):
        """Plot the distribution of steps needed for evacuation"""
        plt.figure(figsize=self.figure_size)
        plt.hist(self.steps_df['steps'], bins=30, edgecolor='black')
        plt.title(title)
        plt.xlabel("Number of Steps")
        plt.ylabel("Count")
        plt.grid(True)
        plt.show()
        
    def plot_personality_vs_steps(self, title: str = "Correlation: Personality Traits vs Steps Needed"):
        """Plot correlation between personality traits and steps needed"""
        merged_df = pd.merge(
            self.personalities_df,
            self.steps_df,
            left_index=True,
            right_index=True
        )
        
        corr_matrix = merged_df.corr()
        
        plt.figure(figsize=self.figure_size)
        im = plt.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        plt.colorbar(im)
        
        # Add correlation values as text
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                text = plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                              ha='center', va='center')
                
        plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
        plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
        plt.title(title)
        plt.tight_layout()
        plt.show()
        
    def plot_trait_influence(self, title: str = "Average Steps Needed by Dominant Trait"):
        """Plot average steps needed for agents with highest values in each trait"""
        merged_df = pd.merge(
            self.personalities_df,
            self.steps_df,
            left_index=True,
            right_index=True
        )
        
        # For each trait, get the average steps for top 10% agents
        results = {}
        for trait in ['O', 'C', 'E', 'A', 'N']:
            threshold = merged_df[trait].quantile(0.9)
            avg_steps = merged_df[merged_df[trait] >= threshold]['steps'].mean()
            results[trait] = avg_steps
            
        plt.figure(figsize=self.figure_size)
        bars = plt.bar(results.keys(), results.values())
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
            
        plt.title(title)
        plt.xlabel("Personality Trait")
        plt.ylabel("Average Steps (Top 10% in trait)")
        plt.grid(True)
        plt.show()
        
    def plot_evacuation_timeline(self, title: str = "Evacuation Timeline"):
        """Plot the cumulative percentage of evacuated agents over time"""
        max_steps = self.steps_df['steps'].max()
        evacuated = np.zeros(max_steps + 1)
        
        for steps in self.steps_df['steps']:
            evacuated[steps:] += 1
            
        evacuated_pct = (evacuated / len(self.steps_df)) * 100
        
        plt.figure(figsize=self.figure_size)
        plt.plot(evacuated_pct, linewidth=2)
        plt.title(title)
        plt.xlabel("Simulation Step")
        plt.ylabel("Percentage of Evacuated Agents")
        plt.grid(True)
        plt.show()
        
    def plot_all(self):
        """Generate all available plots with default titles"""
        self.plot_density_over_time()
        self.plot_personality_distributions()
        self.plot_steps_distribution()
        self.plot_personality_vs_steps()
        self.plot_trait_influence()
        self.plot_evacuation_timeline()

if __name__ == "__main__":
    analyzer = Result_analysis("results/simulation_metrics_20241224_1204.json")
    
    # Generate all plots at once
    analyzer.plot_all()
    
    # Or generate individual plots with custom titles
    if 0:
        analyzer.plot_density_over_time("Custom Density Plot Title")
        analyzer.plot_personality_distributions("Custom Personality Distribution Title")