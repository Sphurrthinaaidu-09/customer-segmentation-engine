import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from sklearn.cluster import KMeans
import engine as pipe

# --- PREMIUM SAAS STYLING INJECTION ---
st.set_page_config(page_title="Core Segment Terminal", layout="wide", page_icon="🔮")

st.markdown("""
    <style>
    :root {
        --bg-dark: #090A0F;
        --card-white: #FFFFFF;
        --brand-purple: #7C4DFF;
        --brand-blue: #00E5FF;
    }
    .stApp {
        background-color: #0B0C10;
        color: #F0F2F5;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #00E5FF !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: #A0A5B5 !important;
    }
    .hero-container {
        background: linear-gradient(135deg, #120C36 0%, #05162E 100%);
        padding: 40px;
        border-radius: 16px;
        border-left: 5px solid #7C4DFF;
        margin-bottom: 30px;
    }
    .recommendation-card {
        background-color: #171A21;
        padding: 25px;
        border-radius: 12px;
        border-top: 4px solid #00E5FF;
        margin-bottom: 20px;
    }
    .schema-pill {
        background-color: #1E222B;
        padding: 4px 10px;
        border-radius: 4px;
        border: 1px solid #313B4D;
        font-family: monospace;
        color: #00E5FF;
        margin-right: 5px;
        display: inline-block;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# --- APPLICATION STATE INITIALIZATION ---
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.raw_df = None
    st.session_state.final_df = None
    st.session_state.cluster_stats = None
    st.session_state.wcss = None
    st.session_state.retention_matrix = None

# --- SIDEBAR CONTROL TERMINAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#00E5FF;'>🔮 Segment OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A0A5B5; font-size:12px;'>Enterprise Marketing Intelligence Hub</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_page = option_menu(
        menu_title="Control Terminal",
        options=[
            "Executive Overview", "Upload Center", "Segmentation Engine", 
            "3D Customer Universe", "Segment Explorer", "Customer Simulator", 
            "Marketing Intelligence", "Cohort Retention", "Strategic Recommendations", "Export Center"
        ],
        icons=[
            "speedometer2", "cloud-upload", "cpu", 
            "globe", "search", "person-bounding-box", 
            "bar-chart-line", "calendar-range", "lightbulb", "download"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#090A0F"},
            "icon": {"color": "#00E5FF", "font-size": "15px"}, 
            "nav-link": {"font-size": "13px", "text-align": "left", "margin":"5px", "color":"#F0F2F5"},
            "nav-link-selected": {"background-color": "#7C4DFF", "font-weight": "500"},
        }
    )

# --- GLOBAL HELPER FOR DATA GUARD ---
def check_data_presence():
    if not st.session_state.data_loaded:
        st.warning("⚠️ No enterprise dataset active in context memory. Please visit the **Upload Center** to load your transactional records first.")
        st.stop()

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if selected_page == "Executive Overview":
    st.markdown("""
        <div class='hero-container'>
            <h1 style='color:#FFFFFF; margin:0; font-size:38px;'>🛍️ Customer Segmentation &<br>Marketing Intelligence System</h1>
            <p style='color:#00E5FF; font-size:16px; margin-top:10px; margin-bottom:0;'>
                Understand your customers. Predict buying behavior. Drive structural retention.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    check_data_presence()
    final_df = st.session_state.final_df
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers Tracked", f"{final_df['CustomerID'].nunique():,}")
    c2.metric("Total Revenue Portfolio", f"${final_df['Monetary'].sum():,.2f}")
    c3.metric("Segments Under Management", f"{final_df['Segment'].nunique()}")
    c4.metric("Operational Status", "Synced & Active")
    
    st.markdown("---")
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("📈 Overall Customer Base Health Index")
        slipping_ratio = len(final_df[final_df['Segment'].str.contains('Slipping|At Risk|Lost', case=False)]) / len(final_df)
        health_score = round((1 - slipping_ratio) * 100)
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#7C4DFF"},
                'bar': {'color': "#00E5FF"},
                'bgcolor': "#1A1D20",
                'steps': [
                    {'range': [0, 50], 'color': '#FF5252'},
                    {'range': [50, 75], 'color': '#FF9100'},
                    {'range': [75, 100], 'color': '#00E676'}
                ],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_right:
        st.subheader("🍩 Portfolio Segment Share")
        counts = final_df['Segment'].value_counts()
        fig_donut = px.pie(names=counts.index, values=counts.values, hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold)
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280)
        st.plotly_chart(fig_donut, use_container_width=True)

# --- PAGE 2: UPLOAD CENTER ---
elif selected_page == "Upload Center":
    st.subheader("📁 Enterprise Data Ingestion Gateway")
    st.markdown("Upload transactional files here to feed data directly through your custom segmentation backend pipeline.")
    
    # Custom interactive schema info block below the label
    st.markdown("""
    <div style="background-color: #11141A; padding: 15px; border-radius: 8px; border-left: 3px solid #00E5FF; margin-bottom: 20px;">
        <span style="color: #A0A5B5; font-size: 14px; display: block; margin-bottom: 8px;"><b>⚙️ Required File Schema footprint:</b></span>
        <span class="schema-pill">InvoiceNo</span>
        <span class="schema-pill">StockCode</span>
        <span class="schema-pill">Description</span>
        <span class="schema-pill">Quantity</span>
        <span class="schema-pill">InvoiceDate</span>
        <span class="schema-pill">UnitPrice</span>
        <span class="schema-pill">CustomerID</span>
        <span class="schema-pill">Country</span>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload transactional retail logs (CSV or XLSX)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        with st.spinner("Processing calculations across optimization steps..."):
            try:
                raw_df = pipe.load_and_clean_data(uploaded_file)
                rfm_table = pipe.engineer_rfm_features(raw_df)
                final_df, stats, scaler, kmeans = pipe.run_segmentation_pipeline(rfm_table)
                
                wcss_list = []
                features_matrix = rfm_table[['Recency', 'Frequency', 'Monetary']].copy()
                for k in range(2, 8):
                    km = KMeans(n_clusters=k, random_state=42, n_init=10)
                    km.fit(features_matrix)
                    wcss_list.append(km.inertia_)
                
                retention_matrix = pipe.calculate_cohort_retention(raw_df)
                
                st.session_state.raw_df = raw_df
                st.session_state.final_df = final_df
                st.session_state.cluster_stats = stats
                st.session_state.wcss = wcss_list
                st.session_state.retention_matrix = retention_matrix
                st.session_state.data_loaded = True
                
                st.success("🎉 Analytics Pipeline Complete! All segments and retention tracking maps updated instantly.")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Unique Customer IDs Profiled", f"{final_df['CustomerID'].nunique():,}")
                m2.metric("Total Ledger Rows Processed", f"{raw_df.shape[0]:,}")
                m3.metric("Aggregated Gross Spend Pipeline", f"${final_df['Monetary'].sum():,.2f}")
                
            except Exception as e:
                st.error(f"Ingestion pipeline dropped out: {e}")

# --- PAGE 3: SEGMENTATION ENGINE ---
elif selected_page == "Segmentation Engine":
    st.subheader("🧠 Math & Clustering Engine Optimization Metrics")
    check_data_presence()
    
    c1, c2 = st.columns(2)
    c1.metric("Calculated Clusters (K)", f"{st.session_state.final_df['Segment'].nunique()}")
    c2.metric("Variance Explained Trend Status", "Optimal")
    
    st.markdown("---")
    k_space = list(range(2, 8))
    
    graph_l, graph_r = st.columns(2)
    with graph_l:
        st.markdown("**Real Within-Cluster Sum of Squares (Elbow curve)**")
        fig_elbow = px.line(x=k_space, y=st.session_state.wcss, markers=True, labels={'x':'Number of Clusters (K)', 'y':'WCSS'}, title="Calculated Elbow Method Dataset Curve")
        fig_elbow.add_vline(x=st.session_state.final_df['Segment'].nunique(), line_dash="dash", line_color="#00E5FF")
        st.plotly_chart(fig_elbow, use_container_width=True)
        
    with graph_r:
        st.markdown("**Feature Profile Box Plot Overviews**")
        fig_box = px.box(st.session_state.final_df, x='Segment', y='Monetary', log_y=True, title="Monetary Distribution Scale Across Extracted Clusters", color='Segment')
        st.plotly_chart(fig_box, use_container_width=True)

# --- PAGE 4: 3D CUSTOMER UNIVERSE ---
elif selected_page == "3D Customer Universe":
    st.subheader("🌌 Multi-Dimensional Spatial Cluster View")
    check_data_presence()
    
    fig_3d = px.scatter_3d(
        st.session_state.final_df, x='Recency', y='Frequency', z='Monetary',
        color='Segment', log_y=True, log_z=True,
        hover_data=['CustomerID'],
        color_discrete_sequence=px.colors.qualitative.Bold,
        opacity=0.7
    )
    fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='#0B0C10', height=650)
    st.plotly_chart(fig_3d, use_container_width=True)

# --- PAGE 5: SEGMENT EXPLORER ---
elif selected_page == "Segment Explorer":
    st.subheader("👥 Live Cohort Profile Character Evaluation Panel")
    check_data_presence()
    
    final_df = st.session_state.final_df
    segment_choices = final_df['Segment'].unique().tolist()
    selected_seg = st.selectbox("Select Target Cluster to Investigate:", segment_choices)
    
    seg_data = final_df[final_df['Segment'] == selected_seg]
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Segment Population Size", f"{len(seg_data):,} accounts")
    sc2.metric("Mean Spend Value", f"${seg_data['Monetary'].mean():,.2f}")
    sc3.metric("Mean Order Frequency", f"{round(seg_data['Frequency'].mean(), 1)} orders")
    sc4.metric("Mean Recency Delta", f"{round(seg_data['Recency'].mean(), 1)} days ago")
    
    st.markdown("---")
    st.subheader("📋 Dynamic Segment Account Profiles Ledger")
    st.dataframe(seg_data[['CustomerID', 'Recency', 'Frequency', 'Monetary']].reset_index(drop=True), use_container_width=True)

# --- PAGE 6: CUSTOMER SIMULATOR ---
elif selected_page == "Customer Simulator":
    st.subheader("🤖 Algorithmic Segment Prediction Sandbox")
    check_data_presence()
    
    st.markdown("Enter custom performance attributes below to dynamically determine what segment group a user lands in.")
    
    sim_r = st.number_input("Recency (Days since last interaction)", min_value=0, max_value=365, value=15)
    sim_f = st.number_input("Frequency (Total lifetime checks completed)", min_value=1, max_value=1000, value=5)
    sim_m = st.number_input("Monetary Value (Gross total spend amount, $)", min_value=1.0, max_value=250000.0, value=250.0)
    
    if st.button("Run Vector Classification Assessment"):
        avg_monetary = st.session_state.final_df['Monetary'].median()
        avg_freq = st.session_state.final_df['Frequency'].median()
        
        if sim_r <= 15 and sim_f > (avg_freq * 3) and sim_m > (avg_monetary * 3):
            pred = "VIP Champions"
            action = "Channel straight into premium preview tiers. Do not apply discount cuts."
        elif sim_r > 90:
            pred = "At Risk"
            action = "Trigger automated high-value return vouchers to prevent permanent expiration drops."
        elif sim_f >= avg_freq and sim_m >= avg_monetary:
            pred = "Loyal Customers"
            action = "Target with multi-product cross-sell groupings directly inside browser recommendation spaces."
        else:
            pred = "Potential Loyalists"
            action = "Deliver low-barrier coupon models to stabilize structural checkouts."
            
        st.markdown("### 🎯 Classification Results Matrix")
        c_res1, c_res2 = st.columns(2)
        c_res1.metric("Assigned Target Classification Category", pred)
        c_res2.metric("Engine Direct Pipeline Status", "Computed Match")
        st.info(f"**Prescriptive Playbook Workflow Directive:** {action}")

# --- PAGE 7: MARKETING INTELLIGENCE DASHBOARD ---
elif selected_page == "Marketing Intelligence":
    st.subheader("📈 Revenue Performance & Aggregations Dashboard")
    check_data_presence()
    
    final_df = st.session_state.final_df
    rev_summary = final_df.groupby('Segment')['Monetary'].agg(['sum', 'mean', 'count']).reset_index()
    
    dl1, dl2 = st.columns(2)
    with dl1:
        fig_bar1 = px.bar(rev_summary, x='Segment', y='sum', title="Aggregated Gross Revenue Yield per Cluster Type", color='Segment', color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_bar1, use_container_width=True)
    with dl2:
        fig_pie1 = px.pie(rev_summary, names='Segment', values='sum', title="Enterprise True Revenue Split Matrix Contribution", hole=0.3, color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_pie1, use_container_width=True)
        
    dl3, dl4 = st.columns(2)
    with dl3:
        fig_hbar = px.bar(rev_summary, x='mean', y='Segment', orientation='h', title="Mean Ticket Value Array across Groups", color='Segment', color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_hbar, use_container_width=True)
    with dl4:
        fig_bar2 = px.bar(rev_summary, x='Segment', y='count', title="Account Profiles Density Distribution Spread", color='Segment', color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_bar2, use_container_width=True)

# --- PAGE 8: COHORT RETENTION ANALYTICS ---
elif selected_page == "Cohort Retention":
    st.subheader("📊 Dynamic Time-Series Transaction Retention Analytics Grid")
    check_data_presence()
    
    st.markdown("Tracking recurring transactional volume across dynamic consumer lifecycle acquisition boundaries.")
    matrix = st.session_state.retention_matrix

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0B0C10')
    ax.set_facecolor('#0B0C10')
    
    sns.heatmap(
        matrix, 
        annot=True, 
        fmt=".1f" if matrix.max().max() <= 100 else ".0f", 
        cmap="YlGnBu", 
        linewidths=.5, 
        ax=ax,
        cbar_kws={'label': 'Retention Scale Index'}
    )
    
    ax.set_title("True Transaction Ledger Cohort Performance Heatmap", color='#F0F2F5', fontsize=12, pad=15)
    ax.set_xlabel("Lifecycle Retention Month Index Sequence", color='#F0F2F5', fontsize=10)
    ax.set_ylabel("Acquisition Month Stamp Group", color='#F0F2F5', fontsize=10)
    ax.tick_params(colors='#F0F2F5', labelsize=9)
    st.pyplot(fig)

# --- PAGE 9: STRATEGIC RECOMMENDATIONS ---
elif selected_page == "Strategic Recommendations":
    st.subheader("💡 Automated Marketing Playbook & Growth Vectors")
    check_data_presence()
    
    final_df = st.session_state.final_df
    total_rev = final_df['Monetary'].sum()
    
    st.markdown("Data-driven growth playbooks generated automatically based on your active segment distribution profiles.")
    st.markdown("---")
    
    # Unified exact-match blueprint map for your 5 segments
    playbooks = {
        "VIP Champions": {
            "icon": "👑",
            "desc": "Your highest-value core accounts. They trust your platform completely and carry your premium revenue metrics.",
            "action": "Channel directly into a premium 'Insiders Club'. Provide dedicated VIP perks, early product drops, and non-discount rewards to maintain high margin gains.",
            "kpi": "Maximize customer lifetime retention and premium advocate brand value."
        },
        "Loyal Customers": {
            "icon": "⚪",
            "desc": "Predictable mainstay accounts with steady repeat checkouts. They represent your reliable, recurring volume base.",
            "action": "Deploy 'Frequently Bought Together' category bundles and tier-based milestone rewards to keep them highly engaged.",
            "kpi": "Increase average items per basket checkout value."
        },
        "Potential Loyalists": {
            "icon": "🛍️",
            "desc": "Recent shoppers with low purchase history but immediate momentum. They are ripe for habitual cultivation.",
            "action": "Trigger automated post-purchase welcome paths, product guides, or low-barrier second-order vouchers to establish a routine.",
            "kpi": "Convert single-transaction trend users into habitual core buyers."
        },
        "At Risk": {
            "icon": "🟡",
            "desc": "Previously frequent buyers who haven't generated a single invoice row in a long tracking period. High churn warning indicator.",
            "action": "Launch personalized 'We Miss You' outreach triggers with high-incentive retention offers to capture attention before full dropout.",
            "kpi": "Disrupt churn migration paths and salvage baseline volume records."
        },
        "Lost Customers": {
            "icon": "❌",
            "desc": "Completely dormant buyer profiles with minimal historical spend footprints. High acquisition friction to reactivate.",
            "action": "Isolate away from regular paid ads. Limit outreach to automated warehouse clearance emails. ",
            "kpi": "Minimize marketing overhead waste on non-responsive cold targets."
        }
    }
    
    for seg_name, content in playbooks.items():
        seg_subset = final_df[final_df['Segment'].str.contains(seg_name.split()[0], case=False, na=False)]
        
        if not seg_subset.empty:
            seg_rev = seg_subset['Monetary'].sum()
            seg_pct = (seg_rev / total_rev) * 100
            count = len(seg_subset)
            
            st.markdown(f"""
                <div class="recommendation-card">
                    <h3 style="color:#00E5FF; margin-top:0;">{content['icon']} {seg_name} <span style="font-size:14px; color:#A0A5B5; float:right;">{count:,} accounts</span></h3>
                    <p style="color:#F0F2F5; font-size:14px;"><strong>Segment Character:</strong> {content['desc']}</p>
                    <p style="color:#7C4DFF; font-size:15px; margin-bottom:5px;"><strong>🎯 Growth Action Vector:</strong></p>
                    <p style="color:#FFFFFF; background-color:#1E222B; padding:12px; border-radius:6px; border-left:3px solid #7C4DFF;">{content['action']}</p>
                    <div style="margin-top:15px; font-size:13px; color:#A0A5B5;">
                        <strong>Financial Impact:</strong> Responsible for <b>${seg_rev:,.2f}</b> ({seg_pct:.1f}% of total portfolio) | <strong>Primary Target Metric:</strong> <u>{content['kpi']}</u>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- PAGE 10: EXPORT CENTER ---
elif selected_page == "Export Center":
    st.subheader("📥 Campaign Target File Extraction Panel")
    check_data_presence()
    
    final_df = st.session_state.final_df
    st.markdown("Filter and export highly specific consumer cohorts directly into tailored audience targeting lists.")
    
    selected_export_segment = st.selectbox("Select Target Cluster to Isolate for Campaign Delivery:", final_df['Segment'].unique().tolist())
    filtered_export_df = final_df[final_df['Segment'] == selected_export_segment]
    
    csv_data = filtered_export_df[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Segment']].to_csv(index=False).encode('utf-8')
    
    st.markdown("---")
    st.subheader("📥 Production-Ready Campaign File Delivery")
    
    st.download_button(
        label=f"Download clean {selected_export_segment} Target Audience List (CSV)",
        data=csv_data,
        file_name=f"{selected_export_segment.lower().replace(' ', '_')}_campaign_list.csv",
        mime='text/csv'
    )