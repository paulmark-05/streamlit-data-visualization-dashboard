# WRICEF Data Visualization Dashboard
# Interactive Streamlit UI for WRICEF tracker data analysis

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import io
import base64

# Configure page
st.set_page_config(
    page_title="WRICEF Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #1f77b4;
    margin: 0.5rem 0;
}
.insight-box {
    background-color: #e8f4fd;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #1f77b4;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

class StreamlitWRICEFDashboard:
    def __init__(self):
        self.df = None
        
    def load_data(self, uploaded_file=None):
        """Load data from uploaded file or create sample data"""
        if uploaded_file is not None:
            try:
                self.df = pd.read_excel(uploaded_file)
                st.success(f"✅ Data loaded successfully! Shape: {self.df.shape}")
                return True
            except Exception as e:
                st.error(f"❌ Error loading data: {e}")
                return False
        else:
            # Create sample data
            self.create_sample_data()
            st.info("📝 Using sample data for demonstration")
            return True
    
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
        process_areas = ['STS', 'RTR', 'MDM', 'PTM', 'PTP', 'LEX', 'OTC', 'EWM']
        
        # Generate realistic dates
        start_date = pd.Timestamp('2022-01-01')
        end_date = pd.Timestamp('2024-12-31')
        
        self.df = pd.DataFrame({
            'Implementation': np.random.choice(implementations, n_records),
            'Project Name': [f"Project {i+1}" for i in range(n_records)],
            'WRICEF Type': np.random.choice(wricef_types, n_records),
            'Complexity': np.random.choice(complexities, n_records),
            'Priority of Delivery': np.random.choice(priorities, n_records),
            'Stage': np.random.choice(stages, n_records),
            'Process Area': np.random.choice(process_areas, n_records),
            'ABAP Effort Forecast (hrs)': np.random.uniform(10, 200, n_records).round(1),
            'ABAP Actual Effort (hrs)': np.random.uniform(10, 200, n_records).round(1),
            'PI Effort Forecast (hrs)': np.random.uniform(5, 100, n_records).round(1),
            'PI Actual Effort (hrs)': np.random.uniform(5, 100, n_records).round(1),
            'FSD Planned Del Date': pd.to_datetime(np.random.choice(pd.date_range(start_date, end_date), n_records)),
            'Dev Actual Delivery Date': pd.to_datetime(np.random.choice(pd.date_range(start_date, end_date), n_records)),
            'Functional Owner': [f"Owner {np.random.randint(1, 20)}" for _ in range(n_records)],
            'Dev Lead': [f"Lead {np.random.randint(1, 15)}" for _ in range(n_records)]
        })
    
    def data_overview(self):
        """Display data overview"""
        st.header("📋 Data Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Total Records</h3>
                <h2 style="color: #1f77b4;">{}</h2>
            </div>
            """.format(len(self.df)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Implementations</h3>
                <h2 style="color: #ff7f0e;">{}</h2>
            </div>
            """.format(self.df['Implementation'].nunique()), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>WRICEF Types</h3>
                <h2 style="color: #2ca02c;">{}</h2>
            </div>
            """.format(self.df['WRICEF Type'].nunique()), unsafe_allow_html=True)
        
        with col4:
            total_effort = self.df['ABAP Effort Forecast (hrs)'].sum()
            st.markdown("""
            <div class="metric-card">
                <h3>Total Effort (hrs)</h3>
                <h2 style="color: #d62728;">{:.0f}</h2>
            </div>
            """.format(total_effort), unsafe_allow_html=True)
        
        # Data sample
        st.subheader("📊 Data Sample")
        st.dataframe(self.df.head(10), use_container_width=True)
    
    def create_distribution_charts(self):
        """Create distribution charts"""
        st.header("📈 Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # WRICEF Type Distribution
            fig_wricef = px.bar(
                x=self.df['WRICEF Type'].value_counts().index,
                y=self.df['WRICEF Type'].value_counts().values,
                title="WRICEF Type Distribution",
                labels={'x': 'WRICEF Type', 'y': 'Count'},
                color=self.df['WRICEF Type'].value_counts().values,
                color_continuous_scale='viridis'
            )
            fig_wricef.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_wricef, use_container_width=True)
        
        with col2:
            # Implementation Distribution
            fig_impl = px.pie(
                values=self.df['Implementation'].value_counts().values,
                names=self.df['Implementation'].value_counts().index,
                title="Implementation Distribution"
            )
            fig_impl.update_layout(height=400)
            st.plotly_chart(fig_impl, use_container_width=True)
        
        # Complexity Distribution
        st.subheader("🎯 Complexity Analysis")
        complexity_counts = self.df['Complexity'].value_counts()
        fig_complexity = px.bar(
            x=complexity_counts.index,
            y=complexity_counts.values,
            title="Complexity Distribution",
            color=complexity_counts.values,
            color_continuous_scale='reds'
        )
        fig_complexity.update_layout(height=400)
        st.plotly_chart(fig_complexity, use_container_width=True)
    
    def create_effort_analysis(self):
        """Create effort analysis charts"""
        st.header("⚡ Effort Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ABAP Effort: Forecast vs Actual
            fig_effort = px.scatter(
                self.df,
                x='ABAP Effort Forecast (hrs)',
                y='ABAP Actual Effort (hrs)',
                color='Implementation',
                size='ABAP Effort Forecast (hrs)',
                hover_data=['WRICEF Type', 'Complexity'],
                title="ABAP: Forecast vs Actual Effort"
            )
            # Add perfect estimation line
            max_effort = max(self.df['ABAP Effort Forecast (hrs)'].max(), self.df['ABAP Actual Effort (hrs)'].max())
            fig_effort.add_shape(
                type="line",
                x0=0, y0=0, x1=max_effort, y1=max_effort,
                line=dict(color="red", width=2, dash="dash"),
            )
            fig_effort.update_layout(height=500)
            st.plotly_chart(fig_effort, use_container_width=True)
        
        with col2:
            # Effort by Implementation
            effort_by_impl = self.df.groupby('Implementation')[['ABAP Effort Forecast (hrs)', 'ABAP Actual Effort (hrs)']].sum().reset_index()
            effort_melted = effort_by_impl.melt(id_vars='Implementation', 
                                              value_vars=['ABAP Effort Forecast (hrs)', 'ABAP Actual Effort (hrs)'],
                                              var_name='Effort Type', value_name='Hours')
            
            fig_effort_impl = px.bar(
                effort_melted,
                x='Implementation',
                y='Hours',
                color='Effort Type',
                title="Total Effort by Implementation",
                barmode='group'
            )
            fig_effort_impl.update_layout(height=500)
            st.plotly_chart(fig_effort_impl, use_container_width=True)
    
    def create_timeline_analysis(self):
        """Create timeline analysis"""
        st.header("📅 Timeline Analysis")
        
        # Monthly trend
        monthly_data = self.df.groupby(self.df['FSD Planned Del Date'].dt.to_period('M')).size().reset_index()
        monthly_data['FSD Planned Del Date'] = monthly_data['FSD Planned Del Date'].astype(str)
        
        fig_timeline = px.line(
            monthly_data,
            x='FSD Planned Del Date',
            y=0,
            title="Monthly Delivery Trend",
            labels={0: 'Number of Deliveries'}
        )
        fig_timeline.update_layout(height=400)
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Interactive scatter plot
        st.subheader("🎯 Interactive Project Timeline")
        fig_scatter = px.scatter(
            self.df,
            x='FSD Planned Del Date',
            y='Implementation',
            color='WRICEF Type',
            size='ABAP Effort Forecast (hrs)',
            hover_data=['Complexity', 'Priority of Delivery', 'Stage', 'Project Name'],
            title="Project Timeline with Effort Sizing"
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    def create_advanced_visualizations(self):
        """Create advanced visualizations"""
        st.header("🚀 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sunburst Chart
            fig_sunburst = px.sunburst(
                self.df,
                path=['Implementation', 'WRICEF Type', 'Complexity'],
                title="Hierarchical View: Implementation → WRICEF → Complexity"
            )
            fig_sunburst.update_layout(height=500)
            st.plotly_chart(fig_sunburst, use_container_width=True)
        
        with col2:
            # Treemap
            fig_treemap = px.treemap(
                self.df,
                path=['Implementation', 'WRICEF Type'],
                title="WRICEF Distribution Treemap"
            )
            fig_treemap.update_layout(height=500)
            st.plotly_chart(fig_treemap, use_container_width=True)
        
        # 3D Scatter Plot
        st.subheader("🌟 3D Effort Analysis")
        fig_3d = px.scatter_3d(
            self.df,
            x='ABAP Effort Forecast (hrs)',
            y='ABAP Actual Effort (hrs)',
            z='PI Effort Forecast (hrs)',
            color='Implementation',
            symbol='WRICEF Type',
            size='ABAP Effort Forecast (hrs)',
            hover_data=['Complexity', 'Priority of Delivery'],
            title="3D Effort Analysis: ABAP vs PI Effort"
        )
        fig_3d.update_layout(height=600)
        st.plotly_chart(fig_3d, use_container_width=True)
    
    def create_heatmaps(self):
        """Create correlation heatmaps"""
        st.header("🌡️ Correlation Analysis")
        
        # Create correlation matrix for numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap of Numeric Variables",
            color_continuous_scale='RdBu'
        )
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Implementation vs Complexity Heatmap
        pivot_data = pd.crosstab(self.df['Implementation'], self.df['Complexity'])
        fig_pivot = px.imshow(
            pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            text_auto=True,
            aspect="auto",
            title="Implementation vs Complexity Heatmap",
            color_continuous_scale='Viridis'
        )
        fig_pivot.update_layout(height=400)
        st.plotly_chart(fig_pivot, use_container_width=True)
    
    def generate_insights(self):
        """Generate and display insights"""
        st.header("💡 Key Insights")
        
        insights = []
        
        # Basic statistics
        total_items = len(self.df)
        insights.append(f"📊 **Total WRICEF items:** {total_items:,}")
        
        # Most common WRICEF type
        most_common_wricef = self.df['WRICEF Type'].mode()[0]
        wricef_count = self.df['WRICEF Type'].value_counts()[most_common_wricef]
        insights.append(f"🏆 **Most common WRICEF type:** {most_common_wricef} ({wricef_count:,} items, {wricef_count/total_items*100:.1f}%)")
        
        # Implementation analysis
        impl_counts = self.df['Implementation'].value_counts()
        insights.append(f"🚀 **Largest implementation:** {impl_counts.index[0]} ({impl_counts.iloc[0]:,} items, {impl_counts.iloc[0]/total_items*100:.1f}%)")
        
        # Effort analysis
        avg_abap_effort = self.df['ABAP Effort Forecast (hrs)'].mean()
        total_abap_effort = self.df['ABAP Effort Forecast (hrs)'].sum()
        insights.append(f"⚡ **Average ABAP effort forecast:** {avg_abap_effort:.1f} hours")
        insights.append(f"🔥 **Total ABAP effort forecast:** {total_abap_effort:,.1f} hours")
        
        # Complexity analysis
        complexity_counts = self.df['Complexity'].value_counts()
        insights.append(f"🎯 **Most common complexity:** {complexity_counts.index[0]} ({complexity_counts.iloc[0]:,} items, {complexity_counts.iloc[0]/total_items*100:.1f}%)")
        
        # Priority analysis
        priority_counts = self.df['Priority of Delivery'].value_counts()
        insights.append(f"⭐ **Most common priority:** {priority_counts.index[0]} ({priority_counts.iloc[0]:,} items, {priority_counts.iloc[0]/total_items*100:.1f}%)")
        
        # Effort efficiency
        effort_efficiency = (self.df['ABAP Actual Effort (hrs)'] / self.df['ABAP Effort Forecast (hrs)']).mean()
        insights.append(f"📈 **Average effort efficiency:** {effort_efficiency:.2f} (actual/forecast ratio)")
        
        # Display insights in a nice format
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                {insight}
            </div>
            """, unsafe_allow_html=True)
    
    def create_filters(self):
        """Create interactive filters"""
        st.sidebar.header("🔧 Filters")
        
        # Implementation filter
        implementations = ['All'] + list(self.df['Implementation'].unique())
        selected_impl = st.sidebar.selectbox("Select Implementation", implementations)
        
        # WRICEF Type filter
        wricef_types = ['All'] + list(self.df['WRICEF Type'].unique())
        selected_wricef = st.sidebar.selectbox("Select WRICEF Type", wricef_types)
        
        # Complexity filter
        complexities = ['All'] + list(self.df['Complexity'].unique())
        selected_complexity = st.sidebar.selectbox("Select Complexity", complexities)
        
        # Priority filter
        priorities = ['All'] + list(self.df['Priority of Delivery'].unique())
        selected_priority = st.sidebar.selectbox("Select Priority", priorities)
        
        # Date range filter
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=[self.df['FSD Planned Del Date'].min().date(), self.df['FSD Planned Del Date'].max().date()],
            min_value=self.df['FSD Planned Del Date'].min().date(),
            max_value=self.df['FSD Planned Del Date'].max().date()
        )
        
        # Apply filters
        filtered_df = self.df.copy()
        
        if selected_impl != 'All':
            filtered_df = filtered_df[filtered_df['Implementation'] == selected_impl]
        
        if selected_wricef != 'All':
            filtered_df = filtered_df[filtered_df['WRICEF Type'] == selected_wricef]
        
        if selected_complexity != 'All':
            filtered_df = filtered_df[filtered_df['Complexity'] == selected_complexity]
        
        if selected_priority != 'All':
            filtered_df = filtered_df[filtered_df['Priority of Delivery'] == selected_priority]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['FSD Planned Del Date'].dt.date >= start_date) &
                (filtered_df['FSD Planned Del Date'].dt.date <= end_date)
            ]
        
        st.sidebar.write(f"Filtered records: {len(filtered_df)}")
        
        return filtered_df

def main():
    """Main Streamlit application"""
    # Header
    st.markdown('<h1 class="main-header">📊 WRICEF Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize dashboard
    dashboard = StreamlitWRICEFDashboard()
    
    # File upload
    st.sidebar.header("📁 Data Input")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your WRICEF Excel file",
        type=['xlsx', 'xls'],
        help="Upload your WRICEF tracker Excel file to analyze your data"
    )
    
    # Load data
    if dashboard.load_data(uploaded_file):
        # Apply filters
        dashboard.df = dashboard.create_filters()
        
        # Navigation
        st.sidebar.header("🧭 Navigation")
        page = st.sidebar.selectbox(
            "Select Analysis Page",
            ["Data Overview", "Distribution Analysis", "Effort Analysis", 
             "Timeline Analysis", "Advanced Analytics", "Correlation Analysis", "Key Insights"]
        )
        
        # Display selected page
        if page == "Data Overview":
            dashboard.data_overview()
        elif page == "Distribution Analysis":
            dashboard.create_distribution_charts()
        elif page == "Effort Analysis":
            dashboard.create_effort_analysis()
        elif page == "Timeline Analysis":
            dashboard.create_timeline_analysis()
        elif page == "Advanced Analytics":
            dashboard.create_advanced_visualizations()
        elif page == "Correlation Analysis":
            dashboard.create_heatmaps()
        elif page == "Key Insights":
            dashboard.generate_insights()
        
        # Footer
        st.markdown("---")
        st.markdown("**📈 WRICEF Analytics Dashboard** | Built with Streamlit & Plotly")

if __name__ == "__main__":
    main()