import matplotlib.pyplot as plt
import streamlit as st

def show_chart(scores:dict[str,int]):

  categories = list(scores.keys())
  values = list(scores.values())

  fig , ax = plt.subplots()
  ax.bar(values,categories,color="grey")
  ax.set_xlim(0,10)
  st.pyplot(fig)


