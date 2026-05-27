import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="Advanced Demand Dashboard", layout="wide")

st.title("📊 Customer Demand & Fulfillment Analytics")
st.markdown("Upload the resource extract to update the metrics.")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # 2. Load Data
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip() # Clean column headers

        # --- DATA PREPARATION ---

        # Ensure dates are in datetime format for calculation
        df['Role Start Date'] = pd.to_datetime(df['Start Week'], errors='coerce')
        df['Demand Raised Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
        
        

        # Identify "Current Period" dynamically (using the latest period found in the data)
        current_period = df['Period'].max()
        
        # Filter Dataframes for specific metrics
        open_df = df[df['Role Status'].astype(str).str.lower() == 'open']
        current_period_df = df[df['Period'] == current_period]
        
        st.success(f"Analysis complete for Period: {current_period}")



        st.markdown("### 🌎 Demand Summary")
        m_col1, m_col2, m_col3 = st.columns(3)


        # --- ROW 1: PRIMARY TILES ---
        #st.markdown("### Key Metrics")
        #m_col1, m_col2, m_col3, m_col4, m_col5, m_col6, m_col7 = st.columns(7)

        with m_col1:
            # 1st Tile: Total Open Demands
            st.metric("Total Open Demands", len(open_df))

        with m_col2:
            # 2nd Tile: Count of Gaps in current period
            # Assuming 'Gap' column contains 1s and 0s
            total_gaps = current_period_df['Gap'].sum()
            st.metric(f"Gaps ({current_period})", int(total_gaps))

        with m_col3:
            # Extra Tile: Global Roles (just for context)
            global_count = open_df[open_df['Global(Y/N)'].astype(str).str.lower() == 'y']
            st.metric("Open Roles (Global=Y)", len(global_count))

        # --- ROW 2: OPERATIONAL DETAIL (4 Columns) ---
        #st.markdown("### ⚙️ Operational Status & Urgency")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)

        with m_col1:
            # 4th Tile: Open demands with OTM = No
            otm_open = open_df[open_df['OTM'].astype(str).str.lower() == 'no']
            st.metric("Open Demands (OTM is No)", len(otm_open))

        with m_col2:
            # 4th Tile: Open demands with OTM = Yes
            otm_open = open_df[open_df['OTM'].astype(str).str.lower() == 'yes']
            st.metric("Open Demands (OTM is Yes)", len(otm_open))

        

        with m_col3:
            # 3rd Tile: New demands in current period
            new_demands = current_period_df[current_period_df['New/Backfill'].astype(str).str.lower() == 'new']
            st.metric(f"New Demands ({current_period})", len(new_demands))

        
            


        with m_col4:
            # NEW METRIC: New demands with start date <= 8 weeks (56 days) from raised date
            urgent_new = current_period_df[
                (current_period_df['New/Backfill'].astype(str).str.lower() == 'new') & 
                ((current_period_df['Start Week'] - current_period_df['Created Date']).dt.days <= 56)
            ]
            st.metric("Urgent New (<=8 wks)", len(urgent_new), delta_color="inverse")


        st.markdown("---")

# --- ROW 3: NEW ENHANCEMENT (SKILL GAP ANALYSIS) ---
        st.markdown("### 🔍 Top 5 Mandatory Skill Gaps (Gap = 1)")
        
        # Filter where Gap is 1
        skill_gap_df = df[df['Gap'] == 1]
        
        if not skill_gap_df.empty:
            # Aggregate top 5 mandatory skills
            top_skills_gap = skill_gap_df['Request Key Skill'].value_counts().head(5).reset_index()
            top_skills_gap.columns = ['Mandatory Skill', 'Total Gap Count']
            
            # Display as a full-width dataframe
            st.dataframe(top_skills_gap, hide_index=True, use_container_width=True)
        else:
            st.info("No records found with a Gap of 1.")
            
        st.markdown("---")


        # --- ROW 2: TABULAR VIEW & VISUALIZATION ---
    
        
        # Calculate Top 5 Clients
        top_clients_data = open_df['Client'].value_counts().head(5).reset_index()
        top_clients_data.columns = ['Client Name', 'Open Demand Count']

 
            
        # Grouping by 'Project Status' and counting
        status_breakup = open_df['Project Status'].value_counts().reset_index()
        status_breakup.columns = ['Status Name', 'Total Count']

            # 2. Display as a clean, styled table
        #st.dataframe(status_breakup,hide_index=True,use_container_width=True)

        t_col1, t_col2 = st.columns(2)

        with t_col1:
            # Tabular View as requested
            st.markdown("### Top 5 Client Accounts (Highest Open Demand)")
            st.dataframe(top_clients_data, hide_index=True, use_container_width=True)

        #with t_col2:
            # Visual View (Optional but helpful)
            #st.bar_chart(data=top_clients_data, x='Client Name', y='Open Demand Count')

        with t_col2:
            # 1. Calculate the breakup status-wise for only OPEN roles
 
           st.markdown("### Open Demand Breakup (Project Status)")
           st.dataframe(status_breakup, hide_index=True, use_container_width=True)

        st.markdown("---")



            # 3. Optional: Add a small bar chart below the table for visual impact
            #st.bar_chart(data=status_breakup, x='Status Name', y='Total Count')




        # --- DATA EXPLORER ---
        with st.expander("View Filtered Open Demands"):
            st.dataframe(open_df)

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check if your Excel column names match the expected names exactly.")
else:
    st.info("Waiting for file upload...")
