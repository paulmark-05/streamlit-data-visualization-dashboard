# WRICEF Data Visualizer - Main Script
# This script processes WRICEF tracker data and creates comprehensive visualizations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class WRICEFDataVisualizer:
    def __init__(self, file_path):
        """Initialize the visualizer with data file"""
        self.df = None
        self.file_path = file_path
        self.load_data()
        self.prepare_data()
    
    def load_data(self):
        """Load data from Excel file"""
        try:
            self.df = pd.read_excel(self.file_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create sample data if file not found
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        np.random.seed(42)
        n_records = 500
        
        implementations = ['Catalyst', 'Goldilocks (ANZ)', 'EWM', 'Supernova']
        wricef_types = ['W', 'R', 'I', 'C', 'E', 'F']
        complexities = ['Low', 'Medium', 'High', 'Very High']
        priorities = ['1 - High', '2 - Medium', '3 - Low']
        stages = ['06 - Dev Completed', '04 - Dev in progress', '16 - FS Review in Progress', 
                 '13 - Deferred', '15 - No Development Required']
        
        self.df = pd.DataFrame({
            'Implementation': np.random.choice(implementations, n_records),
            'WRICEF Type': np.random.choice(wricef_types, n_records),
            'Complexity': np.random.choice(complexities, n_records),
            'Priority of Delivery': np.random.choice(priorities, n_records),
            'Stage': np.random.choice(stages, n_records),
            'ABAP Effort Forecast (hrs)': np.random.uniform(10, 200, n_records),
            'ABAP Actual Effort (hrs)': np.random.uniform(10, 200, n_records),
            'PI Effort Forecast (hrs)': np.random.uniform(5, 100, n_records),
            'PI Actual Effort (hrs)': np.random.uniform(5, 100, n_records),
            'FSD Planned Del Date': pd.date_range('2022-01-01', '2024-12-31', n_records),
            'Dev Actual Delivery Date': pd.date_range('2022-01-01', '2024-12-31', n_records)
        })
        print("Sample data created for demonstration")
    
    def prepare_data(self):
        """Prepare data for analysis"""
        # Convert date columns
        date_columns = [col for col in self.df.columns if 'Date' in col]
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Fill missing effort values
        effort_cols = ['ABAP Effort Forecast (hrs)', 'ABAP Actual Effort (hrs)', 
                      'PI Effort Forecast (hrs)', 'PI Actual Effort (hrs)']
        for col in effort_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
    
    def create_dashboard_plots(self):
        """Create various dashboard plots"""
        plots = {}
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # 1. WRICEF Type Distribution
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        wricef_counts = self.df['WRICEF Type'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(wricef_counts)))
        bars = ax1.bar(wricef_counts.index, wricef_counts.values, color=colors, edgecolor='black', linewidth=1)
        ax1.set_title('WRICEF Type Distribution', fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('WRICEF Type', fontsize=12)
        ax1.set_ylabel('Count', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plots['wricef_distribution'] = fig1
        
        # 2. Implementation vs Complexity Heatmap
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        pivot_data = pd.crosstab(self.df['Implementation'], self.df['Complexity'])
        sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax2, 
                   cbar_kws={'label': 'Count'}, linewidths=0.5)
        ax2.set_title('Implementation vs Complexity Heatmap', fontsize=16, fontweight='bold', pad=20)
        ax2.set_xlabel('Complexity', fontsize=12)
        ax2.set_ylabel('Implementation', fontsize=12)
        plt.tight_layout()
        plots['complexity_heatmap'] = fig2
        
        # 3. Comprehensive Effort Analysis
        fig3, ((ax3a, ax3b), (ax3c, ax3d)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # ABAP Effort Comparison
        if 'ABAP Effort Forecast (hrs)' in self.df.columns and 'ABAP Actual Effort (hrs)' in self.df.columns:
            effort_data = self.df[['ABAP Effort Forecast (hrs)', 'ABAP Actual Effort (hrs)']].dropna()
            scatter = ax3a.scatter(effort_data['ABAP Effort Forecast (hrs)'], 
                        effort_data['ABAP Actual Effort (hrs)'], alpha=0.6, s=50, c='steelblue')
            max_val = max(effort_data['ABAP Effort Forecast (hrs)'].max(), effort_data['ABAP Actual Effort (hrs)'].max())
            ax3a.plot([0, max_val], [0, max_val], 'r--', alpha=0.8, linewidth=2, label='Perfect Estimation')
            ax3a.set_xlabel('Forecast Effort (hrs)', fontsize=12)
            ax3a.set_ylabel('Actual Effort (hrs)', fontsize=12)
            ax3a.set_title('ABAP: Forecast vs Actual Effort', fontsize=14, fontweight='bold')
            ax3a.legend()
            ax3a.grid(True, alpha=0.3)
        
        # Priority Distribution
        priority_counts = self.df['Priority of Delivery'].value_counts()
        colors_pie = plt.cm.Pastel1(np.linspace(0, 1, len(priority_counts)))
        wedges, texts, autotexts = ax3b.pie(priority_counts.values, labels=priority_counts.index, 
                                           autopct='%1.1f%%', colors=colors_pie, startangle=90)
        ax3b.set_title('Priority Distribution', fontsize=14, fontweight='bold')
        
        # Stage Progress
        stage_counts = self.df['Stage'].value_counts()
        colors_bar = plt.cm.viridis(np.linspace(0, 1, len(stage_counts)))
        bars = ax3c.barh(range(len(stage_counts)), stage_counts.values, color=colors_bar)
        ax3c.set_yticks(range(len(stage_counts)))
        ax3c.set_yticklabels([label[:30] + '...' if len(label) > 30 else label for label in stage_counts.index], fontsize=9)
        ax3c.set_title('Development Stage Distribution', fontsize=14, fontweight='bold')
        ax3c.set_xlabel('Count', fontsize=12)
        ax3c.grid(axis='x', alpha=0.3)
        
        # Complexity by Implementation
        complexity_impl = pd.crosstab(self.df['Complexity'], self.df['Implementation'])
        complexity_impl.plot(kind='bar', stacked=True, ax=ax3d, colormap='tab10')
        ax3d.set_title('Complexity by Implementation', fontsize=14, fontweight='bold')
        ax3d.set_xlabel('Complexity', fontsize=12)
        ax3d.set_ylabel('Count', fontsize=12)
        ax3d.legend(title='Implementation', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3d.tick_params(axis='x', rotation=45)
        ax3d.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plots['effort_analysis'] = fig3
        
        # 4. Time Series Analysis
        if 'FSD Planned Del Date' in self.df.columns:
            fig4, (ax4a, ax4b) = plt.subplots(2, 1, figsize=(14, 10))
            
            # Monthly delivery trend
            monthly_data = self.df.groupby(self.df['FSD Planned Del Date'].dt.to_period('M')).size()
            monthly_data.plot(kind='line', ax=ax4a, marker='o', linewidth=2, markersize=6)
            ax4a.set_title('Monthly Delivery Trend', fontsize=14, fontweight='bold')
            ax4a.set_xlabel('Month', fontsize=12)
            ax4a.set_ylabel('Number of Deliveries', fontsize=12)
            ax4a.grid(True, alpha=0.3)
            
            # Quarterly implementation breakdown
            quarterly_impl = self.df.groupby([self.df['FSD Planned Del Date'].dt.to_period('Q'), 'Implementation']).size().unstack(fill_value=0)
            quarterly_impl.plot(kind='bar', stacked=True, ax=ax4b, colormap='tab10')
            ax4b.set_title('Quarterly Implementation Breakdown', fontsize=14, fontweight='bold')
            ax4b.set_xlabel('Quarter', fontsize=12)
            ax4b.set_ylabel('Count', fontsize=12)
            ax4b.legend(title='Implementation', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax4b.tick_params(axis='x', rotation=45)
            ax4b.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plots['time_series'] = fig4
        
        return plots
    
    def create_interactive_plots(self):
        """Create interactive Plotly visualizations"""
        interactive_plots = {}
        
        # 1. Interactive Timeline
        if 'FSD Planned Del Date' in self.df.columns:
            fig_timeline = px.scatter(self.df, 
                                    x='FSD Planned Del Date', 
                                    y='Implementation',
                                    color='WRICEF Type',
                                    size='ABAP Effort Forecast (hrs)' if 'ABAP Effort Forecast (hrs)' in self.df.columns else None,
                                    hover_data=['Complexity', 'Priority of Delivery', 'Stage'],
                                    title='Interactive Project Timeline',
                                    template='plotly_white')
            fig_timeline.update_layout(height=600)
            interactive_plots['timeline'] = fig_timeline
        
        # 2. 3D Effort Analysis
        if all(col in self.df.columns for col in ['ABAP Effort Forecast (hrs)', 'ABAP Actual Effort (hrs)', 'PI Effort Forecast (hrs)']):
            fig_3d = px.scatter_3d(self.df,
                                 x='ABAP Effort Forecast (hrs)',
                                 y='ABAP Actual Effort (hrs)',
                                 z='PI Effort Forecast (hrs)',
                                 color='Implementation',
                                 symbol='WRICEF Type',
                                 title='3D Effort Analysis',
                                 template='plotly_white')
            fig_3d.update_layout(height=700)
            interactive_plots['effort_3d'] = fig_3d
        
        # 3. Sunburst Chart
        fig_sunburst = px.sunburst(self.df, 
                                 path=['Implementation', 'WRICEF Type', 'Complexity'],
                                 title='Hierarchical View: Implementation → WRICEF Type → Complexity',
                                 template='plotly_white')
        fig_sunburst.update_layout(height=600)
        interactive_plots['sunburst'] = fig_sunburst
        
        # 4. Interactive Treemap
        fig_treemap = px.treemap(self.df,
                               path=['Implementation', 'WRICEF Type'],
                               title='WRICEF Distribution Treemap',
                               template='plotly_white')
        fig_treemap.update_layout(height=600)
        interactive_plots['treemap'] = fig_treemap
        
        return interactive_plots
    
    def generate_insights(self):
        """Generate insights from the data"""
        insights = []
        
        # Basic statistics
        total_items = len(self.df)
        insights.append(f"Total WRICEF items: {total_items}")
        
        # Most common WRICEF type
        most_common_wricef = self.df['WRICEF Type'].mode()[0]
        wricef_count = self.df['WRICEF Type'].value_counts()[most_common_wricef]
        insights.append(f"Most common WRICEF type: {most_common_wricef} ({wricef_count} items, {wricef_count/total_items*100:.1f}%)")
        
        # Implementation analysis
        impl_counts = self.df['Implementation'].value_counts()
        insights.append(f"Largest implementation: {impl_counts.index[0]} ({impl_counts.iloc[0]} items, {impl_counts.iloc[0]/total_items*100:.1f}%)")
        
        # Effort analysis
        if 'ABAP Effort Forecast (hrs)' in self.df.columns:
            avg_abap_effort = self.df['ABAP Effort Forecast (hrs)'].mean()
            total_abap_effort = self.df['ABAP Effort Forecast (hrs)'].sum()
            insights.append(f"Average ABAP effort forecast: {avg_abap_effort:.1f} hours")
            insights.append(f"Total ABAP effort forecast: {total_abap_effort:.1f} hours")
        
        # Complexity analysis
        complexity_counts = self.df['Complexity'].value_counts()
        insights.append(f"Most common complexity: {complexity_counts.index[0]} ({complexity_counts.iloc[0]} items, {complexity_counts.iloc[0]/total_items*100:.1f}%)")
        
        # Priority analysis
        priority_counts = self.df['Priority of Delivery'].value_counts()
        insights.append(f"Most common priority: {priority_counts.index[0]} ({priority_counts.iloc[0]} items, {priority_counts.iloc[0]/total_items*100:.1f}%)")
        
        # Stage analysis
        stage_counts = self.df['Stage'].value_counts()
        insights.append(f"Most common stage: {stage_counts.index[0]} ({stage_counts.iloc[0]} items, {stage_counts.iloc[0]/total_items*100:.1f}%)")
        
        return insights

def main():
    """Main function to run the visualizer"""
    visualizer = WRICEFDataVisualizer('WRICEF-Tracker-dump.xlsx')
    
    # Generate static plots
    print("Generating static plots...")
    static_plots = visualizer.create_dashboard_plots()
    
    # Generate interactive plots
    print("Generating interactive plots...")
    interactive_plots = visualizer.create_interactive_plots()
    
    # Generate insights
    insights = visualizer.generate_insights()
    
    print("\n" + "="*50)
    print("KEY INSIGHTS")
    print("="*50)
    for insight in insights:
        print(f"• {insight}")
    
    # Save plots
    print("\nSaving plots...")
    for name, fig in static_plots.items():
        filename = f'{name}.png'
        fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ Saved {filename}")
    
    # Save interactive plots as HTML
    for name, fig in interactive_plots.items():
        filename = f'{name}_interactive.html'
        fig.write_html(filename)
        print(f"✅ Saved {filename}")
    
    print(f"\n✅ Analysis complete! Generated {len(static_plots)} static plots and {len(interactive_plots)} interactive plots.")
    
    # Show plots
    plt.show()
    
    return visualizer, static_plots, interactive_plots, insights

if __name__ == "__main__":
    visualizer, plots, interactive_plots, insights = main()