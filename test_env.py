import sys
print("Python Environment Check")
print(f"Version: {sys.version}")
print(f"Executable: {sys.executable}")
try:
    import streamlit
    print("Streamlit is installed")
except ImportError:
    print("Streamlit is NOT installed")
