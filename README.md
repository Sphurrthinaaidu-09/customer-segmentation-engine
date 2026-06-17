# 📊 Customer Segmentation & Marketing Intelligence System
An end-to-end Customer Analytics and Unsupervised Machine Learning application designed to partition transactional enterprise data into actionable customer personas. The system transforms raw retail invoice logs into high-value business intelligence, enabling marketing teams to proactively maximize customer lifetime value (CLTV), optimize promotional spend, and diagnose structural retention bottlenecks.
**🔗 Live Demo:** View App on Hugging Face Spaces

---

## 🚀 Project Overview
In hyper-competitive retail environments, generic marketing approaches lead to high capital inefficiency. Treating a one-time bargain hunter the same as an elite, high-margin brand champion results in wasted promotional budgets and missed revenue optimization opportunities.
This project combines **Unsupervised Machine Learning**, **RFM Behavioral Modeling**, and **Cohort Analysis** to help organizations:
 * **Programmatically segment** a massive customer universe into distinct consumer behavioral profiles.
 * **Isolate and track** elite revenue-driving accounts (**VIP Champions**).
 * **Diagnose exact operational drop-off intervals** via temporal cohort tracking.
 * **Tailor strategic**, segment-specific marketing recommendations.
 * **Deploy an interactive visual workspace** for real-time customer filtering and strategic CRM data exports.
The application functions as a complete **Marketing Intelligence Data Product** rather than a standalone clustering algorithm.

---

## 🎯 Business Problem
Most mid-market enterprises struggle to identify where their revenue is structurally concentrated and cannot catch customer churn before it solidifies.
This system helps marketing and growth executives shift from blind, uniform targeting to **precision customer relationship management (CRM)** by answering critical corporate questions:
 1. Which customer clusters command the vast majority of our revenue split matrix?
 2. Where are the critical lifecycle drop-offs occurring within newly acquired cohorts?
 3. Which historical high-value segments are slipping into the "At Risk" category and require immediate fiscal intervention?

---

## ⚙️ System Workflow

Raw Transaction Logs ──> Data Cleaning & Validation ──> RFM Feature Engineering  
                                                                 │  
                                                                 ▼  
Streamlit Dashboard <── Marketing Analytics <── K-Means <── Log + StandardScaler

---

### 📥 Step 1: Data Ingestion & Preprocessing
The ingestion engine accepts raw transactional data fields (Invoices, StockCodes, Timestamps) and executes rigorous structural transformations:
 * **Data Cleansing:** Eradicating invalid transactions, handling structural anomalies, and filtering out non-informative tracking lines.
 * **Granular Aggregation:** Grouping row-level line items by customer profiles to build a unified analytical master ledger.

---

### 🤖 Step 2: RFM Feature Engineering Pipeline
The platform programmatically engineers three critical behavioral metrics tracked per unique CustomerID:
 * **Recency (R):** Days elapsed between the customer's latest transaction date and the maximum dataset index boundary (Measures Churn Velocity).
 * **Frequency (F):** Total count of unique invoice identifiers attributed to the customer profile (Measures Engagement Density).
 * **Monetary Value (M):** Aggregate summation of structural expenditures (\text{Quantity} \times \text{UnitPrice}) (Measures Wallet Share).
> ⚠️ **Mathematical Stability:** To ensure mathematical stability for the distance-based clustering engine, the pipeline automatically applies an unbiased log transformation to correct severe right-skewness, followed by a StandardScaler normalization step.
>

---

### 📊 Step 3: Unsupervised Optimization & Clustering Engine
The pipeline utilizes advanced validation techniques to determine the ideal group boundaries:
 * **The Elbow Method:** Tracking the minimization of Within-Cluster Sum of Squares (WCSS) to pinpoint the exact geometric bend.
 * **Silhouette Analysis:** Validating structural boundary coefficients to guarantee maximum intra-cluster density with minimal cross-group bleeding.
 * **Production Run:** Training an optimized K-Means Clustering model to separate the spatial customer coordinates into 5 highly distinct enterprise personas.

---

## 📂 Dataset
**Dataset Name:** Online Retail Transaction Ledger
 * **Total Analyzed Rows:** 12,500+ Extended Retail Records
 * **Target Analytical Profiles:** Customer-Level Behavior Matrices

---

### Original Schema Features:
| Feature Name | Description |
|---|---|
| InvoiceNo | Unique transactional order identifier |
| StockCode | Distinct inventory product code |
| Description | Textual item description |
| Quantity | Units purchased per transaction line |
| InvoiceDate | Explicit timestamp of purchase order |
| UnitPrice | Value per individual item unit |
| CustomerID | Unique customer profile tracking number |
| Country | Geographic operational location of customer account |

---

## 🔍 Exploratory Data Analysis & Segment Profiling
Through deep statistical analysis, the system successfully mapped the customer base into 5 highly distinct revenue-driving archetypes:
 * **👑 VIP Champions:** Exceptionally low recency, ultra-high purchase frequency, and commanding average ticket values (>\$600).
 * **🟢 Loyal Customers:** Highly consistent buying habits, stable transaction intervals, and strong mid-to-high ticket spending profiles.
 * **🌸 Potential Loyalists:** Recent buyers with low-to-mid frequency counts; showing highly promising baseline transaction behaviors.
 * **⚠️ At-Risk Customers:** Historically high-value or highly frequent accounts whose recency scores have drifted heavily outward (inactive for 100+ days).
 * **❌ Lost Customers:** Flatline spending tiers paired with maximum recency gaps. Inactive, low-priority accounts representing one-off promotional or bargain hunters.

---

## 📈 Model Performance & Analytical Verifications
 * **Pareto Revenue Split Verification:** The model successfully isolated the **VIP Champions (42.2%)** and **Loyal Customers (35.6%)**, visually proving that **77.8% of total gross enterprise revenue** is driven by just these two core segments.
 * **Cohort Drop-off Identification:** The retention heatmaps diagnosed a sharp drop-off across multiple monthly cohorts between Month 0 and Month 1, with return rates dropping to the 21%–27% range. This mathematically validated the necessity of deploying automated onboarding interventions for the *Potential Loyalists* segment.

---

## 💡 Strategic Marketing Recommendations
The platform converts numerical cluster identities into precise business playbooks:
 * **VIP Champions:** Deploy high-tier loyalty rewards, exclusive early product access, VIP client management pipelines, and zero-discount premium membership programs.
 * **Loyal Customers:** Optimize cross-selling frameworks, design personalized recommendation engines based on past stock categories, and reward frequent purchases.
 * **Potential Loyalists:** Launch automated trigger campaigns, limited-time welcome bundles, and interactive engagement programs to foster purchasing habits.
 * **At-Risk Customers:** Allocate high-priority win-back offers, direct "We Miss You" personalized discounts, and conduct customer satisfaction surveys.
 * **Lost Customers:** Minimize expensive manual marketing spend; automate ultra-low-cost re-engagement email loops and clearance promotional incentives.

---

## 🛠️ Technology Stack
 * **Programming Language:** Python
 * **Data Analytics & Transformations:** Pandas, NumPy, OpenPyXL
 * **Machine Learning Engine:** Scikit-Learn (KMeans, StandardScaler)
 * **Interactive & Statistical Visualization:** Plotly Express, Matplotlib, Seaborn
 * **Web Application Architecture:** Streamlit (UI Engine, Cache Management)

---

## 📸 Streamlit Application Interface Walkthrough
<details>
<summary> 1. Executive Hub Control Terminal (Click to Expand)</summary>
<p align="center">
<img src="<img width="1763" height="844" alt="Screenshot_17-6-2026_0451_localhost" src="https://github.com/user-attachments/assets/6b1e1cb1-77ac-46ee-a985-ecde1fd2b13a" />
" alt="Executive Hub Control Terminal" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 2. Enterprise Data Ingestion Gateway (Click to Expand)</summary>
<p align="center">
<img src="1000251843.jpg" alt="Enterprise Data Ingestion Gateway" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 3. Math & Clustering Engine Optimization Metrics (Click to Expand)</summary>
<p align="center">
<img src="1000251844.jpg" alt="Clustering Engine Optimization Metrics" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 4. Multi-Dimensional Spatial Cluster View (Click to Expand)</summary>
<p align="center">
<img src="1000251845.jpg" alt="Multi-Dimensional Spatial Cluster View" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 5. Live Cohort Profile Character Explorer (Click to Expand)</summary>
<p align="center">
<img src="1000251846.jpg" alt="Live Cohort Profile Character Explorer" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 6. Algorithmic Segment Prediction Sandbox (Click to Expand)</summary>
<p align="center">
<img src="1000251848.jpg" alt="Algorithmic Segment Prediction Sandbox" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 7. Revenue Performance & Aggregations Dashboard (Click to Expand)</summary>
<p align="center">
<img src="1000251849.jpg" alt="Revenue Performance Dashboard" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 8. True Transaction Ledger Cohort Performance Heatmap (Click to Expand)</summary>
<p align="center">
<img src="1000251850.jpg" alt="Cohort Performance Heatmap" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 9. Automated Marketing Playbook & Growth Vectors (Click to Expand)</summary>
<p align="center">
<img src="1000251851.jpg" alt="Automated Marketing Playbook" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>
<details>
<summary> 10. Campaign Target File Extraction Panel (Click to Expand)</summary>
<p align="center">
<img src="1000251852.jpg" alt="Campaign Target File Extraction Panel" width="85%" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>
</details>

---

## 📂 Project Structure

Customer_Segmentation_System/  
├── data/  
│   └── Online_Retail.xlsx                 # Input transactional dataset log repository  
├── engine.py                              # Ingestion, RFM pipeline, and scaling models  
├── app.py                                 # Core Streamlit app UI frontend  
├── requirements.txt                       # Python environment execution dependencies  
└── README.md                              # Comprehensive project documentation

---

## 🎓 Skills Demonstrated
Through this project, I gained and applied practical experience in:
 * **Unsupervised Machine Learning:** Structuring distance-based clustering algorithms and verifying geometric bounds using multi-metric mathematical checks (WCSS and Elbow curves).
 * **Feature Pipeline Engineering:** Constructing automated ETL workflows to safely clean transactional logs, isolate custom metrics (R, F, M), and stabilize high-skew variance via log scalers.
 * **Cohort Analysis:** Building temporal transaction matrices to visualize retention drops across complex chronological lifecycles.
 * **Data Visualization Design:** Developing multi-dimensional plots, including logarithmic box plots and interactive 3D scatter clouds, to cleanly communicate complex statistical relationships.
 * **Business & Revenue Intelligence:** Linking abstract machine learning clusters directly to financial KPIs (Gross Revenue Yield, Account Profile Density) to drive corporate strategy.
 * **Full-Stack Application Deployment:** Packaging a raw machine learning pipeline into a responsive, production-ready analytics software hub for corporate administrators.

---

## 🔮 Future Enhancements
 * **BG/NBD Modeling Integration:** Incorporating Beta-Geometric/Negative Binomial Distribution frameworks to calculate explicit individual Customer Lifetime Value (CLTV) projections.
 * **BERTopic Persona Discovery:** Applying natural language processing (NLP) to product descriptions within clusters to unlock contextual sub-persona categories.
 * **Predictive Churn Triggers:** Training a supervised classification model on top of the cluster states to forecast individual customer attrition risks before they stop purchasing.
 * **Automated Marketing API Hooks:** Building microservice endpoints to dynamically push filtered high-risk or VIP CSV customer data directly into enterprise CRM tools like HubSpot or Salesforce.

---

## 👨‍💻 Author
**Sphurrthi Naidu** *B.Tech Student in Artificial Intelligence and Data Science | Aspiring Data & Business Analyst* * **GitHub:** Sphurrthinaaidu-09
 * **LinkedIn:** [Your LinkedIn Profile Link Here] *(Optional: update this line!)*
⭐ *If you found this marketing intelligence framework valuable, consider giving this repository a star!*
```text
#MachineLearning #CustomerSegmentation #RFMAnalysis #CohortAnalysis #Streamlit #DataScience #DataAnalytics #BusinessIntelligence #PredictiveAnalytics #KMeans

```
