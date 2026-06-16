import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def load_and_clean_data(file_path):
    """Loads raw transactional logs and sanitizes operational anomalies."""
    if hasattr(file_path, 'name'):
        if file_path.name.endswith('.xlsx') or file_path.name.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
    else:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
            
    # Drop rows without an identifiable customer profile
    df = df.dropna(subset=['CustomerID'])
    df['CustomerID'] = df['CustomerID'].astype(str).str.split('.').str[0]
    
    # Isolate valid non-cancelled purchase logs
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

def engineer_rfm_features(df):
    """Transforms raw transactional entries into unique Customer RFM profiles."""
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    analysis_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    rfm_df = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (analysis_date - x.max()).days,
        'InvoiceNo': 'nunique',  # Quantifies distinct orders
        'TotalAmount': 'sum'
    })
    
    rfm_df.rename(columns={'InvoiceDate': 'Recency', 
                           'InvoiceNo': 'Frequency', 
                           'TotalAmount': 'Monetary'}, inplace=True)
    
    return rfm_df[(rfm_df['Monetary'] > 0) & (rfm_df['Frequency'] > 0)]

def run_segmentation_pipeline(rfm_df, n_clusters=5):
    """Applies log normalization, scales data features, and maps clusters deterministically."""
    # Mitigate right-skewness utilizing log transformation
    rfm_log = np.log(rfm_df + 1)
    
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(rfm_log)
    
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init='auto')
    cluster_labels = kmeans.fit_predict(scaled_matrix)
    
    output_df = rfm_df.copy().reset_index()
    output_df['Raw_Cluster'] = cluster_labels
    
    # 🟢 CRITICAL ENHANCEMENT: Sort clusters deterministically by average Monetary value
    # This prevents UI flickering and randomly swapped labels across application re-runs
    monetary_means = output_df.groupby('Raw_Cluster')['Monetary'].mean().sort_values(ascending=False)
    
    # Map raw cluster IDs to ordered indices (0 = Highest Spend, 4 = Lowest Spend)
    rank_mapping = {raw: rank for rank, raw in enumerate(monetary_means.index)}
    output_df['Cluster_Rank'] = output_df['Raw_Cluster'].map(rank_mapping)
    
    # Corporate SaaS Archetype Definitions
    archetype_labels = {
        0: '👑 VIP Champions',
        1: '🟢 Loyal Customers',
        2: '🛍️ Potential Loyalists',
        3: '🕒 At Risk',
        4: '❌ Lost Customers'
    }
    
    directives_labels = {
        0: 'Enroll in premium tier VIP concierge paths, distribute exclusive early-access collections, and suppress discount offers.',
        1: 'Deploy personalized multi-product cross-sell paths and high-tier value milestone reward programs.',
        2: 'Suggest product bundling opportunities at checkout to optimize historical order frequencies.',
        3: 'Trigger high-priority automated re-engagement text/email alerts containing high-value winback coupons.',
        4: 'Isolate for automated low-cost standard holiday drip-marketing lists. Do not allocate heavy paid ad capital.'
    }
    
    output_df['Segment'] = output_df['Cluster_Rank'].map(lambda x: archetype_labels.get(x, f'Cohort {x}'))
    output_df['Directive'] = output_df['Cluster_Rank'].map(lambda x: directives_labels.get(x, 'Maintain baseline operational communication.'))
    
    # Drop intermediate processing flags before returning data frames
    output_df.drop(columns=['Raw_Cluster'], inplace=True)
    cluster_profiles = output_df.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
    
    return output_df, cluster_profiles, scaler, kmeans

def compute_optimization_metrics(rfm_df):
    """Computes spatial validation data points for system tracking visualization plots."""
    rfm_log = np.log(rfm_df + 1)
    scaled_matrix = StandardScaler().fit_transform(rfm_log)
    
    k_range = list(range(2, 8))
    wcss = []
    scores = []
    
    for k in k_range:
        km = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init='auto')
        labels = km.fit_predict(scaled_matrix)
        wcss.append(km.inertia_)
        scores.append(silhouette_score(scaled_matrix, labels))
        
    return k_range, wcss, scores

def calculate_cohort_retention(df):
    """Generates an operational corporate-grade dynamic customer retention heatmap matrix."""
    df['InvoicePeriod'] = df['InvoiceDate'].dt.to_period('M')
    df['CustomerID'] = df['CustomerID'].astype(str)
    
    # Determine the initial acquisition cohort date for each customer profile
    df['Cohort'] = df.groupby('CustomerID')['InvoiceDate'].transform('min').dt.to_period('M')
    
    cohort_group = df.groupby(['Cohort', 'InvoicePeriod']).agg({'CustomerID': 'nunique'}).reset_index()
    cohort_group['Period_Index'] = (cohort_group['InvoicePeriod'] - cohort_group['Cohort']).apply(lambda x: x.n)
    
    pivot_matrix = cohort_group.pivot_table(index='Cohort', columns='Period_Index', values='CustomerID')
    cohort_sizes = pivot_matrix.iloc[:, 0]
    
    # Derive structural percentage retention metrics across operational timelines
    retention_matrix = pivot_matrix.divide(cohort_sizes, axis=0) * 100
    retention_matrix.index = retention_matrix.index.astype(str)
    
    # Isolate a tight 6-month transaction view window to maintain UI scannability
    return retention_matrix.iloc[:6, :6].round(1)