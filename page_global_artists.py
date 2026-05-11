"""
page_global_artists.py — Studio Workload Dashboard
"""
import streamlit as st
import pandas as pd

def page_global_artists(db, nav_fn):
    """Studio-wide workload overview."""
    st.markdown('<div class="section-header">📊 Studio Workload Dashboard</div>', unsafe_allow_html=True)

    if st.button("← Back to Projects"):
        nav_fn("projects")
        return

    workload = db.get_workload_summary()

    if not workload:
        st.info("No shots assigned to artists yet.")
        return

    # Metrics
    total_shots = sum(w.get("total_shots", 0) for w in workload)
    total_wip = sum(w.get("wip", 0) for w in workload)
    total_approved = sum(w.get("approved", 0) for w in workload)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎨 Active Artists", len(workload))
    m2.metric("🎬 Total Assigned Shots", total_shots)
    m3.metric("🔵 In Progress (WIP)", total_wip)
    m4.metric("✅ Approved", total_approved)

    st.markdown("---")

    # Main Table
    df = pd.DataFrame(workload)
    df = df.rename(columns={
        "artist_name": "Artist",
        "wip": "WIP",
        "pending": "Pending",
        "review": "Review",
        "approved": "Approved",
        "retake": "Retake",
        "hold": "Hold",
        "total_shots": "Total Shots",
        "total_frames": "Total Frames",
        "tracked_seconds": "Tracked Seconds"
    })

    # Format time
    df["Tracked Hours"] = (df["Tracked Seconds"] / 3600).round(1)
    df = df.drop(columns=["Tracked Seconds"])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Artist": st.column_config.TextColumn("Artist", width="medium"),
            "WIP": st.column_config.ProgressColumn("WIP", format="%d", min_value=0),
            "Approved": st.column_config.ProgressColumn("Approved", format="%d", min_value=0),
        }
    )

    # Artist cards (optional visual)
    st.markdown("### Artist Workload Cards")
    cols = st.columns(3)
    for i, artist in enumerate(workload):
        col = cols[i % 3]
        with col:
            hours = round(artist.get("tracked_seconds", 0) / 3600, 1)
            st.markdown(f"""
            <div style="background:#16213e;border:1px solid #1e2d4a;border-radius:12px;padding:16px">
                <div style="font-size:18px;font-weight:700;color:#e94560">{artist['artist_name']}</div>
                <div style="margin:8px 0">
                    <span style="color:#4a90d9">WIP: <b>{artist.get('wip',0)}</b></span> | 
                    <span style="color:#2ECC71">Approved: <b>{artist.get('approved',0)}</b></span>
                </div>
                <div style="font-size:14px;color:#6c7a89">
                    {artist.get('total_shots',0)} shots • {hours}h tracked
                </div>
            </div>
            """, unsafe_allow_html=True)
