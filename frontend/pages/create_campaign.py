import streamlit as st
from services.api import (generate_research,generate_campaign,regenerate_campaign,save_campaign)
import requests
if "marketing_request" not in st.session_state:
    st.session_state.marketing_request = None

if "research" not in st.session_state:
    st.session_state.research = None

if "campaign" not in st.session_state:
    st.session_state.campaign = None
st.title("✨ Create Marketing Campaign")

st.subheader("Campaign Details")

product = st.text_input(
    "Product",
    placeholder="e.g. Wireless Headphones",
)

audience = st.text_input(
    "Target Audience",
    placeholder="e.g. College Students",
)

platform = st.selectbox(
    "Platform",
    [
        "Facebook",
        "Instagram",
        "LinkedIn",
    ],
)

generate_research_button = st.button(
    "🔍 Generate Research",
    use_container_width=True,
)

if generate_research_button:

    request ={
        "product":product,
        "audience":audience,
        "platform":platform
    }
    try:
        research = generate_research(request)

        st.session_state.marketing_request = request
        st.session_state.research = research
        st.session_state.campaign = None
        st.success("Market research generated successfully.")

    except requests.HTTPError as e:
        st.error(f"Error: {e}")

    except Exception as e:
        st.error(str(e))

if st.session_state.research is not None:

    research = st.session_state.research

    st.divider()

    st.header("📊 Market Research")

    with st.expander("🔍 SEO Keywords",expanded=True):

        for keyword in research["seo_keywords"]:
            st.write(f"• {keyword}")

    with st.expander("🏢 Competitors",expanded=True):

        for competitor in research["competitors"]:
            st.write(f"• {competitor}")

    with st.expander("👥 Audience Insights",expanded=True):

        for insight in research["audience_insights"]:
            st.write(f"• {insight}")

    with st.expander("💡 Marketing Suggestions",expanded=True):

        for suggestion in research["marketing_suggestions"]:
            st.write(f"• {suggestion}")

if st.session_state.research is not None:
    st.divider()

    generate_campaign_button = st.button(
        "✨ Generate Campaign",
        use_container_width=True,
    )

    if generate_campaign_button:

        request = {
            "marketing_request": st.session_state.marketing_request,
            "research": st.session_state.research,
        }

        try:

            campaign = generate_campaign(request)

            st.session_state.campaign = campaign

            st.success(
                "Campaign generated successfully."
            )

        except requests.HTTPError as e:

            st.error(str(e))

        except Exception as e:

            st.error(str(e))

    if st.session_state.campaign is not None:

        campaign = st.session_state.campaign

        st.divider()

        st.header("🎯 Campaign")

        st.subheader("Campaign Title")
        st.write(campaign["title"])

        st.subheader("Tagline")
        st.write(campaign["tagline"])

        st.subheader("Call To Action")
        st.write(campaign["cta"])

        st.subheader("Hashtags")
        st.write(" ".join(campaign["hashtags"]))

if st.session_state.campaign is not None:
    st.divider()

    st.header("💬 Improve Campaign")

    feedback = st.text_area(
        "Feedback",
        placeholder="Example: Make it more premium and target young professionals.",
    )

    regenerate_button = st.button(
        "🔄 Regenerate Campaign",
        use_container_width=True,
    )
    if regenerate_button:

        request = {
            "marketing_request": st.session_state.marketing_request,
            "research": st.session_state.research,
            "previous_campaign": st.session_state.campaign,
            "feedback": feedback,
        }

        try:

            campaign = regenerate_campaign(request)

            st.session_state.campaign = campaign

            st.success(
                "Campaign regenerated successfully."
            )
            st.rerun()

        except requests.HTTPError as e:

            st.error(str(e))

        except Exception as e:

            st.error(str(e))

st.divider()

save_campaign_button = st.button(
    "💾 Save Campaign",
    use_container_width=True,
)

if save_campaign_button:

    request = {
        "marketing_request": st.session_state.marketing_request,
        "campaign": st.session_state.campaign,
    }

    try:

        campaign = save_campaign(request)

        st.success(
            "Campaign saved successfully."
        )

    except requests.HTTPError as e:

        st.error(str(e))

    except Exception as e:

        st.error(str(e))