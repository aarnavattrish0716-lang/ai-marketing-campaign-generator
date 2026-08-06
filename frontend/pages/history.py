import streamlit as st
import streamlit as st
import requests

from services.api import (
    get_campaigns,
    delete_campaign,
    update_campaign,
)

if "editing_campaign" not in st.session_state:
    st.session_state.editing_campaign = None

st.title("📜 Campaign History")

try:

    campaigns = get_campaigns()

except requests.HTTPError as e:

    st.error(str(e))

    st.stop()

except Exception as e:

    st.error(str(e))

    st.stop()

if not campaigns:

    st.info(
        "No campaigns found."
    )

    st.stop()

for campaign in campaigns:

    with st.container(border=True):

        st.subheader(campaign["title"])

        st.write(
            f"**Product:** {campaign['product']}"
        )

        st.write(
            f"**Audience:** {campaign['audience']}"
        )

        st.write(
            f"**Platform:** {campaign['platform']}"
        )

        st.write(
            f"**Tagline:** {campaign['tagline']}"
        )

        st.write(
            f"**CTA:** {campaign['cta']}"
        )

        st.write(
            f"**Hashtags:** {campaign['hashtags']}"
        )

        col1, col2 = st.columns(2)

        with col1:
            delete_button = st.button(
                "🗑️ Delete",
                key=f"delete_{campaign['id']}",
                use_container_width=True,
            )

        with col2:
            update_button = st.button(
                "🔄 Update",
                key=f"update_{campaign['id']}",
                use_container_width=True,
            )

        if delete_button:

            try:

                delete_campaign(campaign["id"])

                st.success(
                    "Campaign deleted successfully."
                )

                st.rerun()

            except requests.HTTPError as e:

                st.error(str(e))

            except Exception as e:

                st.error(str(e))

        if update_button:
            st.session_state.editing_campaign = campaign["id"]
            st.rerun()

        if st.session_state.editing_campaign == campaign["id"]:
            title = st.text_input(
                "Title",
                value=campaign["title"],
                key=f"title_{campaign['id']}",
            )

            tagline = st.text_area(
                "Tagline",
                value=campaign["tagline"],
                key=f"tagline_{campaign['id']}",
            )

            cta = st.text_input(
                "CTA",
                value=campaign["cta"],
                key=f"cta_{campaign['id']}",
            )

            hashtags = st.text_input(
                "Hashtags",
                value=campaign["hashtags"],
                key=f"hashtags_{campaign['id']}",
            )

            col1, col2 = st.columns(2)
            with col1:

                save_changes = st.button(
                    "💾 Save Changes",
                    key=f"save_{campaign['id']}",
                    use_container_width=True,
                )
            with col2:

                cancel = st.button(
                    "❌ Cancel",
                    key=f"cancel_{campaign['id']}",
                    use_container_width=True,
                )

            if cancel:
                st.session_state.editing_campaign = None
                st.rerun()

            if save_changes:

                request = {
                    "title": title,
                    "tagline": tagline,
                    "cta": cta,
                    "hashtags": [
                        tag.strip()
                        for tag in hashtags.split(",")
                    ],
                }

                try:

                    update_campaign(
                        campaign["id"],
                        request,
                    )

                    st.success(
                        "Campaign updated successfully."
                    )

                    st.session_state.editing_campaign = None

                    st.rerun()

                except requests.HTTPError as e:

                    st.error(str(e))

                except Exception as e:

                    st.error(str(e))