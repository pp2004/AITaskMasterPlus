import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, date

def render_event_management():
    st.title("📅 Event Management System")
    st.markdown("Manage your events with full CRUD operations")
    
    # Initialize session state
    if "loading" not in st.session_state:
        st.session_state.loading = False
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if "edit_event" not in st.session_state:
        st.session_state.edit_event = None
    
    # Base API URL
    API_BASE = "http://localhost:8000"
    
    # Helper functions
    def get_events():
        try:
            response = requests.get(f"{API_BASE}/events")
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Failed to fetch events")
                return []
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
            return []
    
    def get_hosts():
        try:
            response = requests.get(f"{API_BASE}/hosts")
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Failed to fetch hosts")
                return []
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
            return []
    
    def create_event(event_data):
        try:
            response = requests.post(f"{API_BASE}/events", json=event_data)
            if response.status_code == 200:
                st.success("✅ Event created successfully!")
                return True
            else:
                st.error(f"Failed to create event: {response.text}")
                return False
        except Exception as e:
            st.error(f"Error creating event: {str(e)}")
            return False
    
    def update_event(event_id, event_data):
        try:
            response = requests.put(f"{API_BASE}/events/{event_id}", json=event_data)
            if response.status_code == 200:
                st.success("✅ Event updated successfully!")
                return True
            else:
                st.error(f"Failed to update event: {response.text}")
                return False
        except Exception as e:
            st.error(f"Error updating event: {str(e)}")
            return False
    
    def delete_event(event_id):
        try:
            response = requests.delete(f"{API_BASE}/events/{event_id}")
            if response.status_code == 200:
                st.success("✅ Event deleted successfully!")
                return True
            else:
                st.error(f"Failed to delete event: {response.text}")
                return False
        except Exception as e:
            st.error(f"Error deleting event: {str(e)}")
            return False
    
    def validate_form_data(data):
        errors = []
        if not data.get("event_title", "") or not str(data.get("event_title", "")).strip():
            errors.append("Event title is required")
        if not data.get("event_host", "") or not str(data.get("event_host", "")).strip():
            errors.append("Event host is required")
        if not data.get("event_location", "") or not str(data.get("event_location", "")).strip():
            errors.append("Event location is required")
        if not data.get("pax", "") or not str(data.get("pax", "")).strip():
            errors.append("Number of participants is required")
        try:
            int(str(data.get("pax", "0")))
        except ValueError:
            errors.append("Number of participants must be a valid number")
        return errors
    
    # Main content layout
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("➕ Create New Event", type="primary"):
            st.session_state.show_form = True
            st.session_state.edit_event = None
        
        if st.button("🔄 Refresh Events"):
            st.session_state.loading = True
            st.experimental_rerun()
    
    # Loading animation
    if st.session_state.loading:
        with st.spinner("Loading events..."):
            time.sleep(1)  # Simulate loading delay
            st.session_state.loading = False
            st.experimental_rerun()
    
    # Event creation/edit form
    if st.session_state.show_form:
        st.markdown("---")
        if st.session_state.edit_event:
            st.subheader("✏️ Edit Event")
            event = st.session_state.edit_event
        else:
            st.subheader("➕ Create New Event")
            event = {}
        
        # Get hosts for dropdown
        hosts = get_hosts()
        host_names = [host["name"] for host in hosts]
        
        with st.form("event_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                event_title = st.text_input(
                    "Event Title *", 
                    value=event.get("event_title", ""),
                    placeholder="Enter event title"
                )
                event_date = st.date_input(
                    "Event Date *",
                    value=datetime.strptime(event.get("event_date", str(date.today())), "%Y-%m-%d").date() if event.get("event_date") else date.today()
                )
                event_location = st.text_input(
                    "Event Location *",
                    value=event.get("event_location", ""),
                    placeholder="Enter event location"
                )
            
            with col2:
                selected_host = st.selectbox(
                    "Event Host *",
                    options=host_names,
                    index=host_names.index(event.get("event_host", "")) if event.get("event_host") in host_names else 0
                )
                rsvp_date = st.date_input(
                    "RSVP By *",
                    value=datetime.strptime(event.get("rsvp_by", str(date.today())), "%Y-%m-%d").date() if event.get("rsvp_by") else date.today()
                )
                pax = st.number_input(
                    "Number of Participants *",
                    min_value=1,
                    value=int(event.get("pax", 1)) if event.get("pax") else 1
                )
            
            status = st.selectbox(
                "Status",
                options=[0, 1, 2],
                format_func=lambda x: {0: "Open", 1: "Fully Booked", 2: "Completed"}[x],
                index=event.get("status", 0)
            )
            
            submitted = st.form_submit_button("💾 Save Event", type="primary")
            
            if submitted:
                form_data = {
                    "event_title": event_title,
                    "event_date": str(event_date),
                    "event_host": selected_host,
                    "event_location": event_location,
                    "rsvp_by": str(rsvp_date),
                    "pax": str(pax),
                    "status": status
                }
                
                # Validate form data
                errors = validate_form_data(form_data)
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    if st.session_state.edit_event:
                        if update_event(st.session_state.edit_event["id"], form_data):
                            st.session_state.show_form = False
                            st.session_state.edit_event = None
                            st.experimental_rerun()
                    else:
                        if create_event(form_data):
                            st.session_state.show_form = False
                            st.experimental_rerun()
        
        if st.button("❌ Cancel"):
            st.session_state.show_form = False
            st.session_state.edit_event = None
            st.experimental_rerun()
    
    # Events list
    st.markdown("---")
    st.subheader("📋 Event List")
    
    events = get_events()
    
    if not events:
        st.info("📝 No events found. Create your first event!")
    else:
        # Create DataFrame for better display
        df_data = []
        for event in events:
            status_map = {0: "🟢 Open", 1: "🟡 Fully Booked", 2: "🔴 Completed"}
            df_data.append({
                "ID": event["id"],
                "Date": event["event_date"],
                "Status": status_map.get(event["status"], "Unknown"),
                "RSVP By": event["rsvp_by"],
                "Title": event["event_title"],
                "Host": event["event_host"],
                "Location": event["event_location"],
                "Participants": event["pax"]
            })
        
        df = pd.DataFrame(df_data)
        
        # Display events table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Event actions
        st.markdown("### Event Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            event_ids = [event["id"] for event in events]
            selected_edit_id = st.selectbox("Select event to edit:", event_ids, key="edit_select")
            if st.button("✏️ Edit Event"):
                selected_event = next((e for e in events if e["id"] == selected_edit_id), None)
                if selected_event:
                    st.session_state.edit_event = selected_event
                    st.session_state.show_form = True
                    st.experimental_rerun()
        
        with col2:
            selected_delete_id = st.selectbox("Select event to delete:", event_ids, key="delete_select")
            if st.button("🗑️ Delete Event", type="secondary"):
                if delete_event(selected_delete_id):
                    st.experimental_rerun()
        
        with col3:
            st.markdown("**Quick Stats:**")
            open_events = len([e for e in events if e["status"] == 0])
            completed_events = len([e for e in events if e["status"] == 2])
            st.metric("Open Events", open_events)
            st.metric("Completed Events", completed_events)
