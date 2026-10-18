import os
import streamlit as st
from phonesleuth.phone import analyze_number
from phonesleuth.osint import build_search_links
from phonesleuth.storage import Store
from phonesleuth.export import export_csv, export_json
from phonesleuth.privacy import mask_number

st.set_page_config(page_title="PhoneSleuth Pro", page_icon="📱", layout="wide")
st.title("📱 PhoneSleuth Pro")
st.caption("Legal mobile-number metadata, public OSINT links, scam reports, and forensic case records")
st.warning("Use only for lawful, authorized investigations. This app does not trace live locations, identify private subscribers, or access private accounts.")
store = Store(os.environ.get("PHONESLEUTH_DB", "data/phonesleuth.db"))
tabs = st.tabs(["Number Analyzer", "Public OSINT", "Scam Reports", "Cases & Audit", "Exports"])

with tabs[0]:
    st.subheader("Number metadata")
    with st.form("number_form"):
        number = st.text_input("Phone number", placeholder="+923001234567")
        region = st.text_input("Default region (optional)", value="PK", max_chars=2)
        submit = st.form_submit_button("Analyze")
    if submit:
        try:
            result = analyze_number(number, region.strip().upper() or None)
            st.json(result)
            st.caption("Carrier and region fields are numbering-plan metadata, not proof of current subscriber or carrier.")
        except ValueError as e:
            st.error(str(e))

with tabs[1]:
    st.subheader("Public search links")
    query = st.text_input("Search query (use only information you are authorized to search)", placeholder='"publicly published number"')
    if st.button("Build search links"):
        try:
            for item in build_search_links(query):
                st.markdown(f"- [{item['engine']}]({item['url']}) — {item['note']}")
        except ValueError as e:
            st.error(str(e))

with tabs[2]:
    st.subheader("Record a suspected scam report")
    cases = store.list_cases()
    case_options = {"No case": None} | {f"{c['case_id']} — {c['title']}": c["case_id"] for c in cases}
    with st.form("report_form"):
        phone = st.text_input("Phone number (will be masked)")
        category = st.selectbox("Category", ["Spam", "Suspected fraud", "Harassment", "Phishing", "Other"])
        description = st.text_area("Observed behavior / evidence (avoid unnecessary personal data)")
        source_url = st.text_input("Public source URL (optional)")
        incident_date = st.text_input("Incident date (optional, e.g. 2026-10-18)")
        selected_case = st.selectbox("Attach to case", list(case_options.keys()))
        consent = st.checkbox("I am authorized to record this information and will treat the allegation as unverified.")
        saved = st.form_submit_button("Save report")
    if saved:
        if not consent:
            st.error("Confirm authorization before saving.")
        else:
            try:
                rid = store.add_report(mask_number(phone), category, description, source_url,
                                       incident_date, case_options[selected_case])
                st.success(f"Saved as {rid}; status: unverified.")
            except ValueError as e:
                st.error(str(e))
    reports = store.list_reports()
    if reports:
        st.dataframe(reports, use_container_width=True, hide_index=True)
        for r in reports:
            with st.expander(f"{r['report_id']} — {r['masked_number']} — {r['status']}"):
                new_status = st.selectbox("Status", ["unverified","reviewing","substantiated","dismissed"], key="status_"+r["report_id"])
                if st.button("Update status", key="update_"+r["report_id"]):
                    store.update_status(r["report_id"], new_status); st.rerun()

with tabs[3]:
    st.subheader("Forensic case management")
    with st.form("case_form"):
        title = st.text_input("Case title")
        purpose = st.text_input("Purpose / incident reference")
        auth = st.text_area("Authorization basis (e.g. consent, internal ticket, lawful authority)")
        create = st.form_submit_button("Create case")
    if create:
        try:
            st.success("Created case " + store.create_case(title, purpose, auth))
        except ValueError as e:
            st.error(str(e))
    cases = store.list_cases()
    st.dataframe(cases, use_container_width=True, hide_index=True)
    with st.expander("Audit log"):
        st.dataframe(store.list_audit(), use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Export stored records")
    reports = store.list_reports()
    cases = store.list_cases()
    audit = store.list_audit()
    which = st.selectbox("Dataset", ["Reports", "Cases", "Audit log"])
    data = {"Reports": reports, "Cases": cases, "Audit log": audit}[which]
    st.write(f"{len(data)} record(s)")
    if st.button("Prepare JSON and CSV exports"):
        os.makedirs("exports", exist_ok=True)
        export_json(data, f"exports/{which.lower().replace(' ', '_')}.json")
        export_csv(data, f"exports/{which.lower().replace(' ', '_')}.csv")
        st.success("Exports written to the local exports/ folder.")
    if data:
        st.download_button("Download JSON", export_json(data, f"/tmp/phonesleuth_{which}.json").read_bytes(),
                           file_name=f"{which.lower().replace(' ', '_')}.json", mime="application/json")
        st.download_button("Download CSV", export_csv(data, f"/tmp/phonesleuth_{which}.csv").read_bytes(),
                           file_name=f"{which.lower().replace(' ', '_')}.csv", mime="text/csv")
