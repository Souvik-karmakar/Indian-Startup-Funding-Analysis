import streamlit as st
import pandas as pd
import time
st.title("Startup Dashboard")
st.header("I am learning streamlit")
st.subheader("And i am loving it")
st.write("Souvik here dont fear")
st.markdown(""" My Favourite Movies
- Race 3
- Housefull
""")
#Display code in dashboard
st.code("""
def foo(input):
    return foo**2
x=foo(2)""")

st.latex('x^2+y^2+2=0')

df=pd.DataFrame({
    'name': ['Nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,12,14]
})

st.dataframe(df)

st.metric("Revenue",'Rs 3 Lacs','3%')

st.json({
    'name': ['Nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,12,14]

})
st.image("Photo.png")
st.video('Video1.mp4')
#Sidebar
st.sidebar.title('Sidebar ka title')
#Columns
col1,col2=st.columns(2)
with col1:
    st.image('Photo.png')
with col2:
    st.image('Photo.png')

#Error Message
st.error('Login Failed')

#Success Message
st.success("Login Successful")

#Progress Bar
# bar=st.progress(0)
# for i in range(1,101):
#     time.sleep(0.1)
#     bar.progress(i)

#Email
email=st.text_input("Enter email")
#Number
number=st.number_input("Enter age")
#Date input
st.date_input("Enter regis date")

# Login App
import streamlit as st
email=st.text_input("Enter Email")
password=st.text_input("Enter password")
gender=st.selectbox('select gender',['male','female','Others'])
btn=st.button('Login')
if btn:
    if email=="ksouvik98@gmail.com" and password=='1234':
        st.success("Hurrah! Login Successful")
        st.balloons()
        st.write(gender)
    else:
        st.error('Login Failed')


import streamlit as st
import pandas as pd
file=st.file_uploader('Upload a csv file')
if file is not None:
    df=pd.read_csv(file)
    st.dataframe(df.describe())