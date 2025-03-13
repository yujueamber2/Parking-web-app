import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import time
import pandas as pd
import os

def create_shining_button():
    st.markdown("""
        <style>
        .stButton > button {
            background: linear-gradient(45deg, #ff4444, #cc0000);
            border: none;
            border-radius: 25px;
            color: white;
            padding: 20px 40px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin: 20px 0px;
            width: 100%;
            height: 80px;
            cursor: pointer;
            animation: shine 2s infinite;
        }
        .stButton > button:hover {
            background: linear-gradient(45deg, #cc0000, #ff4444);
        }
        @keyframes shine {
            0% {background-position: 200% center;}
            100% {background-position: -200% center;}
        }
        </style>
        """, unsafe_allow_html=True)
    
    if st.button("I Want a Parking Structure!", key="start_button"):
        st.session_state.show_main_app = True
        st.rerun()

def show_map(address):
    geolocator = Nominatim(user_agent="my_parking_app")
    try:
        location = geolocator.geocode(address)
        if location:
            m = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
            folium.Marker(
                [location.latitude, location.longitude],
                popup="Project Location",
                icon=folium.Icon(color="red")
            ).add_to(m)
            return m
    except:
        return None

def mock_upcodes_api(state, city):
    # Simulated response based on UpCodes structure
    return {
        "parking_codes": [
            {
                "code": "CBC 406.4",
                "title": "Motor-vehicle-related occupancies - General",
                "description": "Minimum parking space dimensions: 8'6\" × 18'0\"",
                "jurisdiction": f"{city}, {state}",
                "effective_date": "January 1, 2023"
            },
            {
                "code": "CBC 406.4.1",
                "title": "Accessible Parking",
                "description": "Accessible parking spaces: 13'0\" × 18'0\"",
                "jurisdiction": f"{city}, {state}",
                "effective_date": "January 1, 2023"
            }
        ]
    }

def main():
    # Add custom CSS for Apple-style UI
    st.markdown("""
        <style>
        /* Global Styles */
        .stApp {
            background-color: #f5f5f7;
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(145deg, #007AFF, #0063CC);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Header Styles */
        .yellow-header {
            background: linear-gradient(145deg, #FFD70080, #FFC00080);  /* 80 = 50% opacity */
            padding: 12px 16px;  /* Smaller padding */
            border-radius: 10px;
            margin: 8px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .yellow-header h2 {
            font-size: 1.2rem;  /* Smaller font size */
            margin: 0;
        }
        
        .blue-header {
            background: linear-gradient(145deg, #007AFF80, #0063CC80);
            padding: 12px 16px;
            border-radius: 10px;
            margin: 8px 0;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .blue-header h2 {
            font-size: 1.2rem;
            margin: 0;
        }
        
        .green-header {
            background: linear-gradient(145deg, #34C75980, #2EAD5080);
            padding: 12px 16px;
            border-radius: 10px;
            margin: 8px 0;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .green-header h2 {
            font-size: 1.2rem;
            margin: 0;
        }
        
        .orange-header {
            background: linear-gradient(145deg, #FF950080, #FF800080);
            padding: 12px 16px;
            border-radius: 10px;
            margin: 8px 0;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .orange-header h2 {
            font-size: 1.2rem;
            margin: 0;
        }
        
        .purple-header {
            background: linear-gradient(145deg, #AF52DE80, #9F40CE80);
            padding: 12px 16px;
            border-radius: 10px;
            margin: 8px 0;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .purple-header h2 {
            font-size: 1.2rem;
            margin: 0;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #E5E5EA;
            padding: 8px 12px;
        }
        .stNumberInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #E5E5EA;
            padding: 8px 12px;
        }
        
        /* Selectbox */
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 1px solid #E5E5EA;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #E5E5EA;
            padding: 10px 15px;
        }
        .streamlit-expanderContent {
            background-color: white;
            border-radius: 0 0 8px 8px;
            border: 1px solid #E5E5EA;
            border-top: none;
            padding: 15px;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            background-color: white;
            padding: 10px 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Charts */
        [data-testid="stArrowVegaLiteChart"] {
            background-color: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: white;
            padding: 8px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 14px;
            min-width: auto;
            color: #1E1E1E;
        }
        
        /* Tab Colors */
        .stTabs [data-baseweb="tab"]:nth-child(1) {
            background: linear-gradient(145deg, #FFD700, #FFC000);
        }
        .stTabs [data-baseweb="tab"]:nth-child(2) {
            background: linear-gradient(145deg, #007AFF, #0063CC);
            color: white;
        }
        .stTabs [data-baseweb="tab"]:nth-child(3) {
            background: linear-gradient(145deg, #34C759, #2EAD50);
            color: white;
        }
        .stTabs [data-baseweb="tab"]:nth-child(4) {
            background: linear-gradient(145deg, #FF9500, #FF8000);
            color: white;
        }
        .stTabs [data-baseweb="tab"]:nth-child(5) {
            background: linear-gradient(145deg, #AF52DE, #9F40CE);
            color: white;
        }
        
        /* Active tab highlight */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }
        
        /* Info boxes */
        .stAlert {
            background-color: white;
            border-radius: 12px;
            border: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1, h2, h3 {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 600;
        }
        
        p {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
        }
        
        /* Welcome page button */
        .shine-button {
            background: linear-gradient(145deg, #007AFF, #0063CC);
            border: none;
            border-radius: 12px;
            color: white;
            padding: 20px 40px;
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            margin: 20px 0;
            width: 100%;
            box-shadow: 0 4px 12px rgba(0,122,255,0.3);
            transition: all 0.3s ease;
        }
        .shine-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,122,255,0.4);
        }
        
        /* Navigation button style */
        .nav-button {
            width: 100%;
            height: 40px;
            font-size: 14px;
            margin: 10px 0;
            background: linear-gradient(145deg, #007AFF, #0063CC);
            color: white;
            border: none;
            border-radius: 6px;
            transition: all 0.3s ease;
        }
        .nav-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .cost-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section-header {
            background: linear-gradient(145deg, #AF52DE80, #9F40CE80);
            padding: 10px 20px;
            border-radius: 8px;
            color: white;
            margin: 10px 0;
        }
        .result-box {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'show_main_app' not in st.session_state:
        st.session_state.show_main_app = False

    if not st.session_state.show_main_app:
        st.title("Welcome to Parking Structure Design Tool")
        st.markdown("### Transform Your Space into an Efficient Parking Solution")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            create_shining_button()
    
    else:
        st.title("WPM Parking Structure Design Tool")
        
        # Update tab selection based on session state
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = "Project Criteria from Client"

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Project Criteria from Client", 
            "Building Codes", 
            "Conceptual Design",
            "3D Model Options",
            "Cost Estimate"
        ])

        # Set the active tab based on session state
        if st.session_state.active_tab == "Building Codes":
            tab2.active = True
        elif st.session_state.active_tab == "Conceptual Design":
            tab3.active = True
        elif st.session_state.active_tab == "3D Model Options":
            tab4.active = True
        elif st.session_state.active_tab == "Cost Estimate":
            tab5.active = True
        
        with tab1:
            st.markdown('<div class="yellow-header"><h2>Project Information</h2></div>', unsafe_allow_html=True)
            
            user_type = st.selectbox(
                "Select User Type",
                ["Architect", "Engineer", "Developer", "Contractor", "Other"]
            )
            
            st.subheader("Project Requirements")
            parking_spaces = st.number_input("Number of Parking Spaces Needed", min_value=1, value=100)
            
            st.subheader("Site Information")
            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("State", ["California", "New York", "Texas", "Florida"])
            with col2:
                city = st.text_input("City")
            
            address = st.text_input("Project Address")
            if address:
                map_obj = show_map(f"{address}, {city}, {state}")
                if map_obj:
                    folium_static(map_obj)
                
            st.subheader("Budget Information")
            budget = st.number_input("Project Budget ($)", min_value=0, value=1000000, step=100000)
            cost_per_space = st.number_input("Estimated Cost per Space ($)", min_value=0, value=25000)
            
            st.markdown("---")  # Add a separator
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Next: Building Codes →", key="nav_to_codes", type="primary"):
                    st.session_state.active_tab = "Building Codes"
                    st.rerun()
        
        with tab2:
            st.markdown('<div class="blue-header"><h2>Applicable Building Codes</h2></div>', unsafe_allow_html=True)
            st.markdown(f"### {state} Building Codes - 2022 Edition")
            st.markdown("*Showing relevant parking structure requirements*")
            
            codes = mock_upcodes_api(state, city)
            for code in codes["parking_codes"]:
                with st.expander(f"{code['code']} - {code['title']}", expanded=True):
                    st.markdown(f"**Description:** {code['description']}")
                    st.markdown(f"**Jurisdiction:** {code['jurisdiction']}")
                    st.markdown(f"**Effective Date:** {code['effective_date']}")
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Next: Conceptual Design →", key="nav_to_design", type="primary"):
                    st.session_state.active_tab = "Conceptual Design"
                    st.rerun()
        
        with tab3:
            st.markdown('<div class="green-header"><h2>Conceptual Design Parameters</h2></div>', unsafe_allow_html=True)
            
            # Site Parameters
            st.subheader("Site Dimensions")
            col1, col2 = st.columns(2)
            with col1:
                site_length = st.number_input("Site Length (ft)", min_value=0.0, value=200.0)
            with col2:
                site_width = st.number_input("Site Width (ft)", min_value=0.0, value=150.0)
            
            # Structural System
            st.subheader("Structural Configuration")
            span_type = st.radio(
                "Select Span Configuration",
                ["Long Span (60' typical)", "Short Span (30' typical)"]
            )
            
            # Building Height Parameters
            st.subheader("Building Height Configuration")
            num_levels = st.number_input("Number of Levels", min_value=1, max_value=10, value=3)
            first_floor_height = st.number_input("First Floor Height (ft)", min_value=8.0, value=12.0)
            typical_floor_height = st.number_input("Typical Floor Height (ft)", min_value=8.0, value=10.0)
            
            # Ramp Configuration
            num_ramps = st.number_input("Number of Ramps", min_value=1, max_value=4, value=1)
            
            # Design Criteria Analysis
            st.subheader("Interpreting the Design Criteria")
            with st.expander("Design Analysis", expanded=True):
                total_height = first_floor_height + (num_levels - 1) * typical_floor_height
                total_area = site_length * site_width * num_levels
                approx_spaces = total_area / 350  # Rough estimate of area per parking space
                
                st.write(f"🏗️ **Total Building Height:** {total_height:.1f} ft")
                st.write(f"📏 **Total Floor Area:** {total_area:,.0f} sq ft")
                st.write(f"🚗 **Estimated Capacity:** {approx_spaces:.0f} spaces")
                span_type_long = 'Long Span (60\' typical)'
                st.write(f"🛣️ **Circulation Type:** {'Double-loaded' if span_type == span_type_long else 'Single-loaded'}")
            
            # Code Requirements Summary
            st.subheader("Evaluating Code Requirements")
            with st.expander("Code Analysis Summary", expanded=True):
                st.write("🎯 **Key Code Requirements:**")
                st.write("- Minimum clear height: 7'-0\"")
                st.write("- Standard stall size: 8'-6\" × 18'-0\"")
                st.write("- Minimum drive aisle: 24'-0\"")
                st.write("- Maximum ramp slope: 1:8")
                if num_levels > 1:
                    st.write("- Required fire separation between levels")
                    st.write("- Mechanical ventilation required")
            
            # Add button to generate CSV
            if st.button("Generate Design Parameters CSV", key="gen_csv", type="primary"):
                try:
                    # Create dictionary of design parameters
                    design_params = {
                        'site_length': [site_length],
                        'site_width': [site_width],
                        'span_type': [span_type],
                        'num_levels': [num_levels],
                        'first_floor_height': [first_floor_height],
                        'typical_floor_height': [typical_floor_height],
                        'num_ramps': [num_ramps],
                        'total_height': [total_height],
                        'total_area': [total_area],
                        'approx_spaces': [approx_spaces]
                    }
                    
                    # Convert dictionary to DataFrame
                    df = pd.DataFrame(design_params)
                    
                    # Save to CSV
                    csv_filename = "design_parameters.csv"
                    df.to_csv(csv_filename, index=False)
                    
                    # Show success message with download button
                    st.success(f"Design parameters saved to {csv_filename}")
                    
                    # Create download button
                    with open(csv_filename, 'rb') as file:
                        st.download_button(
                            label="Download Parameters CSV",
                            data=file,
                            file_name=csv_filename,
                            mime='text/csv',
                            key="download_csv"
                        )
                except Exception as e:
                    st.error(f"Error generating CSV: {str(e)}")
            
            # Navigation button
            if st.button("Next: 3D Model Options →", key="nav_to_model", type="primary"):
                st.session_state.active_tab = "3D Model Options"
                st.rerun()
        
        with tab4:
            st.markdown('<div class="orange-header"><h2>3D Model Options</h2></div>', unsafe_allow_html=True)
            
            # Add custom CSS for parameter styling
            st.markdown("""
                <style>
                .param-container {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #e9ecef;
                    margin: 10px 0;
                }
                .param-header {
                    color: #6c757d;
                    font-size: 0.9em;
                    font-weight: 600;
                    margin-bottom: 10px;
                }
                .param-value {
                    color: #212529;
                    font-size: 0.85em;
                    font-family: monospace;
                }
                .metric-container {
                    font-size: 0.85em;
                }
                .metric-container .st-emotion-cache-1xarl3l {
                    font-size: 0.9em;
                }
                .metric-container .st-emotion-cache-183lzff {
                    font-size: 0.8em;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Option 1: Load from local file
            st.markdown("#### Option 1: Load Local Design Parameters")
            try:
                if st.button("Load Latest Design Parameters", key="load_local", type="primary"):
                    if os.path.exists("design_parameters.csv"):
                        df = pd.read_csv("design_parameters.csv")
                        st.success("Local design parameters loaded successfully!")
                        with st.expander("View Local Parameters", expanded=True):
                            # Fancy parameter details section
                            st.markdown('<div class="param-container">', unsafe_allow_html=True)
                            st.markdown('<p class="param-header">📊 Parameter Details</p>', unsafe_allow_html=True)
                            
                            # Create a styled dataframe
                            styled_df = df.style.format({
                                'site_length': '{:.1f}',
                                'site_width': '{:.1f}',
                                'total_height': '{:.1f}',
                                'total_area': '{:,.0f}',
                                'approx_spaces': '{:.0f}'
                            }).set_properties(**{
                                'font-size': '0.85em',
                                'font-family': 'monospace'
                            })
                            
                            st.dataframe(styled_df, height=120)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Key Parameters Summary with smaller text
                            st.markdown('<div class="param-container">', unsafe_allow_html=True)
                            st.markdown('<p class="param-header">🎯 Key Parameters Summary</p>', unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('<p class="param-header">📏 Dimensions</p>', unsafe_allow_html=True)
                                with st.container():
                                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                                    st.metric("Site Length", f"{df['site_length'].iloc[0]:.1f} ft")
                                    st.metric("Site Width", f"{df['site_width'].iloc[0]:.1f} ft")
                                    st.metric("Number of Levels", f"{df['num_levels'].iloc[0]}")
                                    st.markdown('</div>', unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown('<p class="param-header">📊 Calculations</p>', unsafe_allow_html=True)
                                with st.container():
                                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                                    st.metric("Total Height", f"{df['total_height'].iloc[0]:.1f} ft")
                                    st.metric("Total Area", f"{df['total_area'].iloc[0]:,.0f} sq ft")
                                    st.metric("Approx. Spaces", f"{df['approx_spaces'].iloc[0]:.0f}")
                                    st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Store parameters in session state
                        for column in df.columns:
                            st.session_state[f'param_{column}'] = df[column].iloc[0]
                    else:
                        st.warning("No local design parameters file found. Please generate parameters in the Conceptual Design tab first.")
            except Exception as e:
                st.error(f"Error loading local file: {str(e)}")
            
            # Option 2: Upload file (use the same styling)
            st.markdown("#### Option 2: Upload Parameters File")
            uploaded_file = st.file_uploader("Upload design parameters CSV", type=['csv'], key="csv_upload")
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    
                    st.success("Design parameters loaded successfully!")
                    with st.expander("View Uploaded Parameters", expanded=True):
                        # Use the same fancy styling as above
                        st.markdown('<div class="param-container">', unsafe_allow_html=True)
                        st.markdown('<p class="param-header">📊 Parameter Details</p>', unsafe_allow_html=True)
                        
                        styled_df = df.style.format({
                            'site_length': '{:.1f}',
                            'site_width': '{:.1f}',
                            'total_height': '{:.1f}',
                            'total_area': '{:,.0f}',
                            'approx_spaces': '{:.0f}'
                        }).set_properties(**{
                            'font-size': '0.85em',
                            'font-family': 'monospace'
                        })
                        
                        st.dataframe(styled_df, height=120)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Key Parameters Summary
                        st.markdown('<div class="param-container">', unsafe_allow_html=True)
                        st.markdown('<p class="param-header">🎯 Key Parameters Summary</p>', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('<p class="param-header">📏 Dimensions</p>', unsafe_allow_html=True)
                            with st.container():
                                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                                st.metric("Site Length", f"{df['site_length'].iloc[0]:.1f} ft")
                                st.metric("Site Width", f"{df['site_width'].iloc[0]:.1f} ft")
                                st.metric("Number of Levels", f"{df['num_levels'].iloc[0]}")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<p class="param-header">📊 Calculations</p>', unsafe_allow_html=True)
                            with st.container():
                                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                                st.metric("Total Height", f"{df['total_height'].iloc[0]:.1f} ft")
                                st.metric("Total Area", f"{df['total_area'].iloc[0]:,.0f} sq ft")
                                st.metric("Approx. Spaces", f"{df['approx_spaces'].iloc[0]:.0f}")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Store parameters in session state
                    for column in df.columns:
                        st.session_state[f'param_{column}'] = df[column].iloc[0]
                
                except Exception as e:
                    st.error(f"Error loading CSV file: {str(e)}")

            # ShapeDiver viewer implementation following official documentation
            #ticket = "ec17d00663f923ef03a8fc938cff333ad5101843f0b971a6068bc93faaf04b8f87a65af5e07675c2b6fb7ed75f749e8a1313cbc865a37846d39238739f0688eaea32d860f005f82ef635ed1a4526abcf87757667ac3077aa245be99b1cc1f21e5109b89138f42b-65c939a872a7798562baa8fe9487e517"
            #model_view_url = "https://sdr7euc1.eu-central-1.shapediver.com"
 
            
            iframe_src = "https://appbuilder.shapediver.com/v1/main/latest/?slug=parking-structure-generator-v-1-0-21"
            #st.components.v1.html(html_content, height=620)

            st.components.v1.html(
                f'''
                <div style="position: relative; width: 100%; padding-bottom: 56.25%;">
                    <iframe src="{iframe_src}" style="position: absolute; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
                </div>
                '''
            )



            # Add helpful instructions below the viewer
            st.info("""
            👆 Use the 3D model viewer above to:
            - Rotate and zoom the model using your mouse
            - Adjust parameters using the control panel
            - View different design configurations
            - Analyze spatial relationships
            """)
            
            # Navigation buttons
            st.markdown("---")
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Next: Cost Estimate →", key="nav_to_cost", type="primary"):
                    st.session_state.active_tab = "Cost Estimate"
                    st.rerun()

        with tab5:
            # Main container with custom padding
            st.markdown("""
                <style>
                .cost-container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
                .section-header {
                    background: linear-gradient(145deg, #AF52DE80, #9F40CE80);
                    padding: 10px 20px;
                    border-radius: 8px;
                    color: white;
                    margin: 10px 0;
                }
                .result-box {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #e9ecef;
                    margin: 10px 0;
                }
                </style>
            """, unsafe_allow_html=True)

            # Project Data Section
            st.markdown('<div class="section-header"><h3>Project Data</h3></div>', unsafe_allow_html=True)
            
            with st.container():
                # Building Parameters
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### 🏗️ Building Configuration")
                    total_levels = st.selectbox("Total Levels:", range(1, 11), 2)
                    below_grade = st.selectbox("Levels Below Grade:", ["None"] + list(range(1, total_levels + 1)))
                    total_stalls = st.number_input("Number of Parking Stalls:", min_value=100, value=500)
                    efficiency = st.number_input("Efficiency (SF/Stall):", min_value=300, value=320,
                                               help="Typical range: 300-400 SF per stall")
                
                with col2:
                    st.markdown("##### 🔧 Structural Systems")
                    structural_system = st.selectbox("Structural System:", ["Long Span", "Short Span"])
                    lateral_system = st.selectbox("Lateral System:", ["Shear Walls", "Moment Frame", "Dual System"])
                    foundation_type = st.selectbox("Foundation Type:", ["Shallow Foundation", "Deep Foundation"])
                    facade_finish = st.slider("Facade Quality (1-10):", 1, 10, 5,
                                            help="1=Basic, 5=Standard, 10=Premium")

            # Quick Summary Box
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            quick_stats_col1, quick_stats_col2, quick_stats_col3 = st.columns(3)
            with quick_stats_col1:
                st.metric("Total Area", f"{total_stalls * efficiency:,} SF")
            with quick_stats_col2:
                st.metric("Levels", f"{total_levels} ({below_grade if below_grade != 'None' else '0'} below)")
            with quick_stats_col3:
                st.metric("Stalls per Level", f"{total_stalls // total_levels:,}")
            st.markdown('</div>', unsafe_allow_html=True)

            # Cost Calculation Section
            st.markdown('<div class="section-header"><h3>Cost Calculations</h3></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("##### 💰 Additional Cost Factors (Optional)")
                
                # Optional cost factors with checkboxes
                include_misc = st.checkbox("Include Misc. Project Cost", value=True,
                                        help="Site work, utilities, etc.")
                if include_misc:
                    misc_cost_percent = st.number_input("Misc. Project Cost (%):", value=5.0, format="%.1f")
                else:
                    misc_cost_percent = 0.0

                include_gc = st.checkbox("Include GC + OH&P + Insurance", value=True,
                                      help="General Conditions, Overhead & Profit, Insurance")
                if include_gc:
                    gc_oh_percent = st.number_input("GC + OH&P + Insurance (%):", value=15.0, format="%.1f")
                else:
                    gc_oh_percent = 0.0

                include_contingency = st.checkbox("Include Design Contingency", value=True,
                                               help="Allowance for unknown design elements")
                if include_contingency:
                    contingency_percent = st.number_input("Design Contingency (%):", value=10.0, format="%.1f")
                else:
                    contingency_percent = 0.0

                include_escalation = st.checkbox("Include Escalation", value=True,
                                              help="Future cost increases")
                if include_escalation:
                    escalation_percent = st.number_input("Escalation (%):", value=6.0, format="%.1f")
                else:
                    escalation_percent = 0.0
            
            with col2:
                st.markdown("##### 🏗️ Market Conditions (Optional)")
                include_market = st.checkbox("Include Market Adjustment", value=False,
                                          help="Apply market condition multiplier to final cost")
                if include_market:
                    market_condition = st.selectbox(
                        "Current Market:",
                        ["Aggressive", "Normal", "Impacted"],
                        help="Affects final cost based on number of bidders"
                    )

            def calculate_base_construction_cost():
                # Base cost factors
                base_cost_per_sf = {
                    "Long Span": {
                        "Above Grade": 95.0,  # Base cost for long span above grade
                        "Below Grade": 125.0  # Base cost for long span below grade
                    },
                    "Short Span": {
                        "Above Grade": 85.0,  # Base cost for short span above grade
                        "Below Grade": 115.0  # Base cost for long span below grade
                    }
                }

                # Structural system multipliers
                lateral_system_multiplier = {
                    "Shear Walls": 1.0,
                    "Moment Frame": 1.15,
                    "Dual System": 1.25
                }

                # Foundation multipliers
                foundation_multiplier = {
                    "Shallow Foundation": 1.0,
                    "Deep Foundation": 1.35
                }

                # Facade multipliers (1-10 scale)
                facade_multiplier = 1.0 + (facade_finish - 5) * 0.05  # 5% adjustment per level from baseline of 5

                # Calculate above and below grade areas
                below_grade_levels = 0 if below_grade == "None" else int(below_grade)
                above_grade_levels = total_levels - below_grade_levels
                
                area_per_level = total_area / total_levels
                above_grade_area = area_per_level * above_grade_levels
                below_grade_area = area_per_level * below_grade_levels

                # Calculate base cost
                if below_grade_levels > 0:
                    below_cost = below_grade_area * base_cost_per_sf[structural_system]["Below Grade"]
                    above_cost = above_grade_area * base_cost_per_sf[structural_system]["Above Grade"]
                    base_cost = below_cost + above_cost
                else:
                    base_cost = total_area * base_cost_per_sf[structural_system]["Above Grade"]

                # Apply multipliers
                adjusted_cost = (base_cost * 
                               lateral_system_multiplier[lateral_system] * 
                               foundation_multiplier[foundation_type] * 
                               facade_multiplier)

                return adjusted_cost

            def calculate_total_cost():
                base_cost = calculate_base_construction_cost()
                
                # Initialize additional costs
                misc_cost = base_cost * (misc_cost_percent / 100) if include_misc else 0
                gc_oh_cost = base_cost * (gc_oh_percent / 100) if include_gc else 0
                contingency_cost = base_cost * (contingency_percent / 100) if include_contingency else 0
                escalation_cost = base_cost * (escalation_percent / 100) if include_escalation else 0

                # Calculate subtotal
                subtotal = base_cost + misc_cost + gc_oh_cost + contingency_cost + escalation_cost

                # Apply market condition if selected
                if include_market:
                    market_multiplier = {
                        "Aggressive": 0.95,
                        "Normal": 1.0,
                        "Impacted": 1.15
                    }
                    total = subtotal * market_multiplier[market_condition]
                else:
                    total = subtotal

                return {
                    "base_cost": base_cost,
                    "misc_cost": misc_cost,
                    "gc_oh_cost": gc_oh_cost,
                    "contingency_cost": contingency_cost,
                    "escalation_cost": escalation_cost,
                    "total_cost": total,
                    "market_adjusted": include_market,
                    "included_factors": {
                        "misc": include_misc,
                        "gc": include_gc,
                        "contingency": include_contingency,
                        "escalation": include_escalation
                    }
                }

            # Calculate Button
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                calculate_button = st.button("📊 Calculate Costs", type="primary", use_container_width=True)

            if calculate_button:
                costs = calculate_total_cost()
                
                # Results Display
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                # Cost Breakdown
                st.markdown("#### 📊 Cost Breakdown")
                cost_cols = st.columns(3)
                with cost_cols[0]:
                    st.metric("Base Construction", f"${costs['base_cost']:,.0f}")
                    if costs['included_factors']['misc']:
                        st.metric("Misc. Project", f"${costs['misc_cost']:,.0f}")
                with cost_cols[1]:
                    if costs['included_factors']['gc']:
                        st.metric("GC + OH&P", f"${costs['gc_oh_cost']:,.0f}")
                    if costs['included_factors']['contingency']:
                        st.metric("Contingency", f"${costs['contingency_cost']:,.0f}")
                with cost_cols[2]:
                    if costs['included_factors']['escalation']:
                        st.metric("Escalation", f"${costs['escalation_cost']:,.0f}")
                    if costs['market_adjusted']:
                        st.info(f"Market Condition ({market_condition}) Applied")
                
                # Summary of included/excluded factors
                st.markdown("#### 📋 Included Cost Factors:")
                included_factors = []
                if costs['included_factors']['misc']: included_factors.append("Misc. Project Cost")
                if costs['included_factors']['gc']: included_factors.append("GC + OH&P")
                if costs['included_factors']['contingency']: included_factors.append("Design Contingency")
                if costs['included_factors']['escalation']: included_factors.append("Escalation")
                if costs['market_adjusted']: included_factors.append(f"Market Adjustment ({market_condition})")
                
                if included_factors:
                    st.write(" • " + "\n • ".join(included_factors))
                else:
                    st.write("Base construction cost only (no additional factors included)")
                
                # Final Metrics
                st.markdown("---")
                final_cols = st.columns(3)
                with final_cols[0]:
                    st.metric("Total Cost", f"${costs['total_cost']:,.0f}")
                with final_cols[1]:
                    st.metric("Cost/SF", f"${costs['total_cost']/total_area:,.2f}")
                with final_cols[2]:
                    st.metric("Cost/Stall", f"${costs['total_cost']/total_stalls:,.0f}")
                
                if not costs['market_adjusted']:
                    st.info("💡 Market conditions not included in this calculation. Enable 'Include Market Adjustment' for market-adjusted costs.")
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Information Expanders
            st.markdown("### 📚 Reference & Help")
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("📝 Detailed Cost Calculation Methods"):
                    st.markdown("""
                    ### Base Cost Calculation Process
                    
                    1. **Area Calculations**
                       - Total Area = Number of Stalls × Efficiency
                       - Area per Level = Total Area ÷ Number of Levels
                       - Above/Below Grade Areas calculated separately
                    
                    2. **Base Cost Determination**
                       - Long Span Above Grade: $95/SF
                       - Long Span Below Grade: $125/SF
                       - Short Span Above Grade: $85/SF
                       - Short Span Below Grade: $115/SF
                    
                    3. **Structural System Adjustments**
                       - Long Span: Better efficiency but higher cost
                       - Short Span: More columns but lower cost
                       - Below Grade: +30-40% premium for waterproofing & excavation
                    
                    4. **System Multipliers Applied**
                       - Lateral System:
                         * Shear Walls: Base cost (1.0×)
                         * Moment Frame: +15% premium (1.15×)
                         * Dual System: +25% premium (1.25×)
                       
                       - Foundation Type:
                         * Shallow Foundation: Base cost (1.0×)
                         * Deep Foundation: +35% premium (1.35×)
                    
                    5. **Facade Quality Adjustment**
                       - Base level is 5 (standard quality)
                       - Each point above/below 5: ±5% cost adjustment
                       - Example: Level 8 = +15% premium (3 points × 5%)
                    
                    6. **Additional Costs**
                       - Misc. Project Costs: % of base cost
                       - GC + OH&P: % of base cost
                       - Design Contingency: % of base cost
                       - Escalation: % of base cost
                    
                    7. **Market Adjustment**
                       - Final multiplier based on market conditions
                    """)
            
            with col2:
                with st.expander("ℹ️ Detailed Cost Factors Reference"):
                    st.markdown("""
                    ### System Cost Impacts
                    
                    **Structural Systems:**
                    - **Long Span**
                      * Pros: Better circulation, fewer columns
                      * Cons: Higher structural cost
                      * Typical efficiency: 300-340 SF/stall
                    
                    - **Short Span**
                      * Pros: Lower structural cost
                      * Cons: More columns, reduced flexibility
                      * Typical efficiency: 330-390 SF/stall
                    
                    **Below Grade Construction:**
                    - Waterproofing: +15-20%
                    - Excavation: +10-15%
                    - Shoring: +5-10%
                    
                    **Lateral System Selection:**
                    - **Shear Walls**
                      * Most economical
                      * Good for seismic regions
                      * May impact circulation
                    
                    - **Moment Frame**
                      * Better openness
                      * Higher steel content
                      * Premium: +15%
                    
                    - **Dual System**
                      * Best seismic performance
                      * Most expensive option
                      * Premium: +25%
                    
                    **Foundation Impact:**
                    - **Shallow Foundation**
                      * Standard spread footings
                      * Good soil conditions
                      * Base cost option
                    
                    - **Deep Foundation**
                      * Piles or caissons
                      * Poor soil conditions
                      * Premium: +35%
                    
                    **Market Condition Factors:**
                    - **Aggressive:** -5%
                      * Many bidders (6+)
                      * High competition
                    - **Normal:** Base cost
                      * 3-5 bidders
                      * Typical market
                    - **Impacted:** +15%
                      * Limited bidders (1-2)
                      * Difficult conditions
                    """)

                with st.expander("🎯 Calculator Usage Example"):
                    st.markdown("""
                    ### Example Project Calculation
                    
                    **Sample Project Scenario:**
                    - 500-car garage
                    - 4 levels (1 below grade)
                    - Long span structure
                    - Located in urban area
                    
                    **Step-by-Step Input:**
                    1. **Project Data:**
                       - Total Levels: 4
                       - Below Grade: 1
                       - Parking Stalls: 500
                       - Efficiency: 330 SF/stall
                    
                    2. **Structural Choices:**
                       - Long Span system
                       - Shear Walls for lateral
                       - Deep Foundation (urban site)
                       - Facade Quality: 7 (above average)
                    
                    3. **Cost Factors:**
                       - Misc. Project: 5%
                       - GC + OH&P: 15%
                       - Contingency: 10%
                       - Escalation: 6%
                       - Normal market conditions
                    
                    **Expected Results:**
                    - Total Area: 165,000 SF
                    - Base Cost: ~$17.5M
                    - Final Cost: ~$23.8M
                    - Cost per Space: ~$47,600
                    
                    **Key Considerations:**
                    - Below grade level increases cost
                    - Urban location affects logistics
                    - Premium facade adds quality
                    - Normal market provides stable pricing
                    
                    This example shows how different factors combine to influence the final cost estimate.
                    """)

if __name__ == "__main__":
    main() 