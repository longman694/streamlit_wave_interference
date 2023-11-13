import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.markdown("""
# Wave Interference Simulation
            
Change the variables.
""")

def update_f():
    st.session_state.f_s = st.session_state.f

def update_f_s():
    st.session_state.f = st.session_state.f_s

f = st.number_input("frequency", min_value=20, max_value=20000, value=2000, key='f', on_change=update_f)
f_s = st.slider("frequency", min_value=20, max_value=20000, value=f, key='f_s', on_change=update_f_s)

dist_l, dist_r = -100, 100
dist = 300

ampl = np.zeros([dist_r-dist_l,dist])

drivers_count = st.number_input("number of drivers", min_value=1, max_value=10, value=1, step=1)

x_positions = {}
y_positions = {}
for i in range(drivers_count):
    st.markdown(f"#### driver {i+1}")
    col1, col2 = st.columns(2)
    with col1:
        x_positions[i] = st.number_input(label=f'x position of driver {i+1}', value=0, key=f'x{i}')
    with col2:
        y_positions[i] = st.number_input(label=f'y position of driver {i+1}', value=0, key=f'y{i}')

drivers = []
for i in range(drivers_count):
    drivers.append((y_positions[i], x_positions[i]))

# drivers = [
#     # left-right offset (cm), baffle offset (cm)
#     (-15, 0),
#     (15, 0)
# ]
drivers = np.array(drivers)

def func(a,b,px,py):
    return np.sin(2*np.pi*np.sqrt((a-px)**2+(b-py)**2)*f/34300)  # cm

for driver in drivers:
    ampl += np.array([[func(i,j, driver[0], driver[1]) for j in np.arange(0,dist)] for i in np.arange(dist_l,dist_r)])

fig, ax = plt.subplots()
im = ax.imshow(ampl)
ax.set_title(f'Interferance of {len(drivers)} driver(s) at {f} Hz')
fig.colorbar(im, ax=ax, label='Interactive colorbar')
st.pyplot(fig)
