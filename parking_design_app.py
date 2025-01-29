import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import time

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
                st.write(f"🛣️ **Circulation Type:** {'Double-loaded' if span_type == 'Long Span (60\' typical)' else 'Single-loaded'}")
            
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
            
            # Create Options Button
            if st.button("Create Design Options", type="primary"):
                st.session_state.active_tab = "3D Model Options"
                st.rerun()
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Next: 3D Model Options →", key="nav_to_model", type="primary"):
                    st.session_state.active_tab = "3D Model Options"
                    st.rerun()
        
        with tab4:
            st.markdown('<div class="orange-header"><h2>3D Model Options</h2></div>', unsafe_allow_html=True)
            
            # ShapeDiver iframe embedding
            ticket = "ec17d00663f923ef03a8fc938cff333ad5101843f0b971a6068bc93faaf04b8f87a65af5e07675c2b6fb7ed75f749e8a1313cbc865a37846d39238739f0688eaea32d860f005f82ef635ed1a4526abcf87757667ac3077aa245be99b1cc1f21e5109b89138f42b-65c939a872a7798562baa8fe9487e517"
            shapediver_url = f"https://viewer.shapediver.com/v3/3.10.1/latest/index.html?ticket={ticket}"
            html_code = f'''
                <iframe 
                    width="100%" 
                    height="600" 
                    src="{shapediver_url}"
                    referrerpolicy="origin" 
                    allow="fullscreen"
                    sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
                    style="overflow: hidden; border-width: 0;">
                    <p>Your browser does not support iframes.</p>
                </iframe>
            '''
            st.components.v1.html(html_code, height=600)
            
            st.info("""
            👆 Interact with the 3D model above to:
            - Adjust building parameters
            - Visualize different configurations
            - Export design options
            """)
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Next: Cost Estimate →", key="nav_to_cost", type="primary"):
                    st.session_state.active_tab = "Cost Estimate"
                    st.rerun()

        with tab5:
            st.markdown('<div class="purple-header"><h2>Cost Estimation Calculator</h2></div>', unsafe_allow_html=True)

            # Reference Information
            st.subheader("Cost Reference Sources")
            with st.expander("📚 Reference Projects & Sources", expanded=True):
                st.markdown("""
                | Project Name | Location | Year | Cost/Space | Type |
                |--------------|----------|------|------------|------|
                | Santa Monica Place | Santa Monica, CA | 2021 | $65,000 | Underground |
                | Pike & Rose | Bethesda, MD | 2022 | $35,000 | Above Ground |
                | Legacy West | Plano, TX | 2021 | $28,000 | Above Ground |
                """)
                st.info("Note: Costs adjusted for inflation to current year")

            # Basic Parameters
            total_spaces = parking_spaces if 'parking_spaces' in locals() else 100
            num_levels = num_levels if 'num_levels' in locals() else 3

            # Detailed Cost Breakdown Sections
            st.subheader("1. Structural System")
            with st.expander("Structural Components", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("##### Material")
                    concrete_cost = st.number_input("Concrete ($/CY)", value=180.0, step=5.0, help="RSMeans 2023: $165-195/CY")
                    rebar_cost = st.number_input("Rebar ($/Ton)", value=1800.0, step=50.0, help="RSMeans 2023: $1700-1900/Ton")
                with col2:
                    st.markdown("##### Labor")
                    labor_rate = st.number_input("Labor Rate ($/Hr)", value=85.0, step=5.0, help="Union rates vary by location")
                    productivity = st.number_input("Productivity (SF/Day/Crew)", value=2000.0, step=100.0)
                with col3:
                    st.markdown("##### Equipment")
                    crane_cost = st.number_input("Crane ($/Month)", value=15000.0, step=500.0)
                    forms_cost = st.number_input("Formwork ($/SF)", value=12.0, step=0.5)

            st.subheader("2. Architectural Elements")
            with st.expander("Architectural Components", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    facade_types = {
                        "Precast Panels": 45.0,
                        "Metal Screen": 35.0,
                        "Glass Curtainwall": 85.0,
                        "Basic Concrete": 25.0
                    }
                    facade_type = st.selectbox("Facade System", list(facade_types.keys()))
                    facade_cost = st.number_input("Facade Cost ($/SF)", value=facade_types[facade_type], help="Based on RSMeans 2023")
                with col2:
                    st.markdown("##### Vertical Transportation")
                    elevator_cost = st.number_input("Elevator ($/unit)", value=175000.0, step=5000.0, help="Includes installation")
                    stair_cost = st.number_input("Stairwell ($/flight)", value=45000.0, step=1000.0)

            st.subheader("3. MEP Systems")
            with st.expander("MEP Breakdown", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### Mechanical & Plumbing")
                    ventilation_cost = st.number_input("Ventilation ($/SF)", value=12.0, step=0.5, help="Includes CO monitoring")
                    drainage_cost = st.number_input("Drainage System ($/SF)", value=8.0, step=0.5)
                with col2:
                    st.markdown("##### Electrical")
                    lighting_cost = st.number_input("Lighting ($/SF)", value=9.5, step=0.5, help="LED fixtures with controls")
                    power_cost = st.number_input("Power Distribution ($/SF)", value=7.5, step=0.5)

            st.subheader("4. Special Systems & Technology")
            with st.expander("Technology Integration", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### Parking Systems")
                    revenue_control = st.number_input("Revenue Control System ($/entry-exit)", value=35000.0, step=1000.0)
                    guidance_system = st.number_input("Parking Guidance ($/space)", value=450.0, step=50.0)
                with col2:
                    st.markdown("##### EV Charging")
                    ev_percentage = st.slider("EV Ready Spaces (%)", 5, 30, 10)
                    ev_cost = st.number_input("EV Charger Cost ($/unit)", value=7500.0, step=100.0)

            # Cost Calculations
            st.subheader("Total Cost Analysis")
            with st.expander("Cost Summary", expanded=True):
                # Calculate areas and quantities
                avg_sf_per_space = 350
                total_sf = total_spaces * avg_sf_per_space
                perimeter_sf = (total_sf/num_levels)**0.5 * 4 * num_levels  # Approximate perimeter
                num_ev_stations = int(total_spaces * ev_percentage / 100)

                # Calculate component costs
                structural_cost = (concrete_cost * total_sf * 0.15) + (rebar_cost * total_sf * 0.004)  # Approximate quantities
                facade_total = facade_cost * perimeter_sf
                mep_total = (ventilation_cost + drainage_cost + lighting_cost + power_cost) * total_sf
                systems_total = (revenue_control * 2) + (guidance_system * total_spaces) + (ev_cost * num_ev_stations)

                total_cost = structural_cost + facade_total + mep_total + systems_total
                cost_per_space = total_cost / total_spaces

                # Display metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Project Cost", f"${total_cost:,.2f}")
                    st.metric("Cost per Space", f"${cost_per_space:,.2f}")
                with col2:
                    st.metric("Cost per Square Foot", f"${(total_cost/total_sf):,.2f}")
                    st.metric("Total Area", f"{total_sf:,.0f} SF")

                # Cost breakdown chart
                cost_data = {
                    'Component': ['Structural', 'Facade', 'MEP', 'Systems'],
                    'Cost': [structural_cost, facade_total, mep_total, systems_total]
                }
                df_costs = pd.DataFrame(cost_data)
                st.bar_chart(df_costs.set_index('Component'))

                # Notes and Assumptions
                st.markdown("#### Notes & Assumptions")
                st.markdown("""
                - Costs based on Q1 2023 data
                - Labor rates vary by region (±20%)
                - Excludes land acquisition costs
                - Assumes typical soil conditions
                - Excludes soft costs (design, permits, etc.)
                - Utility connections not included
                - 20% contingency recommended
                """)

            # Export option
            st.download_button(
                label="Download Detailed Cost Estimate",
                data=df_costs.to_csv(),
                file_name="parking_structure_cost_estimate.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main() 