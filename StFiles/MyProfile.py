import streamlit as st
import base64

def show_circular_image(image_path, size=180):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <div style='display: flex; flex-direction: column; align-items: center;'>
            <img src='data:image/png;base64,{encoded}'
                 style='width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;margin-bottom: 15px;'/>
        </div>
        """,
        unsafe_allow_html=True,
    )

def myProfile():
    show_circular_image("C:/Users/mani1/OneDrive/Documents/My Resume/Manikandan Baskar.png", 180)
    st.markdown("""
    <div style="text-align:center;">
    <h2 style="margin:10px 0;">Manikandan Baskar</h2>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-start;gap:4px;">
    <p style="margin:6px 0;">
    <a href="https://github.com/mani-baskar" target="_blank"
        style="text-decoration:none;display:inline-flex;align-items:center;gap:8px;">
        <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20">
        <span style="font-size:18px;color:#333;font-weight:600;">mani-baskar</span>
    </a>
    </p>

    <p style="margin:6px 0;">
    <a href="https://linkedin.com/in/mani-baskar" target="_blank"
        style="text-decoration:none;display:inline-flex;align-items:center;gap:8px;">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20">
        <span style="font-size:18px;color:#0a66c2;font-weight:600;">mani-baskar</span>
    </a>
    </p>

    <p style="margin:6px 0;">
    <a href="mailto:mani111355@gmail.com"
        style="text-decoration:none;display:inline-flex;align-items:center;gap:8px;">
        <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="20">
        <span style="font-size:18px;color:#d44638;font-weight:600;">mani111355@gmail.com</span>
    </a>
    </p>

    <p style="margin:10px 0 5px 0;">
    Lead Software Engineer | Data Scientist in Progress<br>
    Expert in Automation, AI, and Business Intelligence<br>
    Passionate about building scalable solutions using Py
    </p>
    </div>
    <hr>
        <div style="text-align:center;">
        <p style="margin:5px 0;"><span style="font-size:15px;">&#128205; India</span></p>
        </div>
    
    """, unsafe_allow_html=True)