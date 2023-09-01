import streamlit as st
import plotly.express as px
import pandas as pd



#emojis: https://www.webfx.com.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="STUDENT DASHBOARD",
                   page_icon=":bar_chart",
                   layout="wide"

)
da=pd.read_excel(
    io='BAC .xlsx',
    engine='openpyxl',
    sheet_name='ADMIS',
    skiprows=0,
    usecols='A:J',
    nrows=7297
)
da.dropna()

da.loc[(da.MOY >= 16) & (da.MOY < 18), "MENTION"] = "TB"
da.loc[(da.MOY >= 14) & (da.MOY < 16), "MENTION"] = "BIEN"
da.loc[(da.MOY >= 12) & (da.MOY < 14), "MENTION"] = "AB"
da.loc[(da.MOY >= 10) & (da.MOY < 12), "MENTION"] = "PASB"
da.loc[(da.MOY >= 8) & (da.MOY < 10), "MENTION"] = "INSF"
da.loc[(da.MOY <8), "MENTION"] = "null"

    
dt=pd.read_excel(
    io='BAC 2022.xlsx',
    engine='openpyxl',
    sheet_name='ECHOUES',
    skiprows=0,
    usecols='A:J',
    nrows=11030
)
dt.dropna()
dt.loc[(dt.MOY >= 16) & (dt.MOY < 18), "MENTION"] = "TB"
dt.loc[(dt.MOY >= 14) & (dt.MOY < 16), "MENTION"] = "BIEN"
dt.loc[(dt.MOY >= 12) & (dt.MOY < 14), "MENTION"] = "AB"
dt.loc[(dt.MOY >= 10) & (dt.MOY < 12), "MENTION"] = "PASB"
dt.loc[(dt.MOY >= 8) & (dt.MOY < 10), "MENTION"] = "INSF"
dt.loc[(dt.MOY < 8), "MENTION"] = "null"

df=pd.concat([da,dt],ignore_index=True)

#st.dataframe(df)
#st.dataframe(dt)

st.sidebar.header("Please filter here:")


DEPARTEMENTS=st.sidebar.multiselect(
    "select the DEPARTEMENTS",
    options=df['DEPARTEMENTS'].unique(),
    default=df['DEPARTEMENTS'].unique()   
)
SEXE=st.sidebar.multiselect(
    "select the SEXE",
    options=df['SEXE'].unique(),
    default=df['SEXE'].unique()  
)
MENTION=st.sidebar.multiselect(
    "select the MENTION",
    options=df['MENTION'].unique(),
    default=df['MENTION'].unique()   
)
SERIES=st.sidebar.multiselect(
    "select the SERIES",
    options=df['SERIES'].unique(),
    default=df['SERIES'].unique()   
)
ETABLISSEMENTS=st.sidebar.multiselect(
    "select the ETABLISSEMENTS",
    options=df['ETABLISSEMENTS'].unique(),
    default=df['ETABLISSEMENTS'].unique()  
)




df_selection=df.query(
    "DEPARTEMENTS==@DEPARTEMENTS & ETABLISSEMENTS==@ETABLISSEMENTS & SEXE==@SEXE & MENTION==@MENTION & SERIES==@SERIES"
)

#st.dataframe(df_selection)
#----MAINpages----
st.title(":bar_chart: BACC ")
st.markdown("##")
def Home():
    with st.expander("Tableaux"):
        showData=st.multiselect('Filter:',df_selection.columns,default=[])
        st.write(df_selection[showData])
Home()
def Main():
    #top kpi's
    total_candidats=int(df_selection["SEXE"].count())
    total_admis=int(df_selection[df_selection['MOY']>=10].value_counts().sum())
    total_echoues=int(total_candidats-total_admis)
    moyenne_general=round(da["MOY"].mean(),2)
    #star_rating=":star:"*int(round(moyenne_general,2))

    left,right,middle,up,yep=st.columns(5,gap='large')
    with left:
        st.info('Total CANDIDATS')
        st.subheader(f" {total_candidats}")
    with right:
        st.info('Total Admis')
        st.subheader(f"{total_admis}")
    with middle:
        st.info('Total Echoues')
        st.subheader(f" {total_echoues}")
    with up:
        st.info('MOY GENERAL ADMIS')
        st.subheader(f" {moyenne_general}")#{star_rating}")
    with yep:
        st.info('FIRST MOY')
        st.subheader(f"{14.75}")
Main()        
st.markdown("---")


def graph():
#TABLEAU
    cand_depar=(
        df_selection.groupby(by=["DEPARTEMENTS"]).count()[["MATRICULE"]]
    )
    fig_canddepar=px.line(
        cand_depar,
        y="MATRICULE",
        x=cand_depar.index,
        orientation="v",
        title="<b>CANDIDATS PAR DEPARTEMETS</b>",
        color_discrete_sequence=["#0083b8"]*len(cand_depar),
    )
    fig_canddepar.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=True))
    )
    
    
    cand_ETAB=(
        df_selection.groupby(by=["ETABLISSEMENTS"]).count()[["MATRICULE"]].sort_values(by="MATRICULE")
    )
    fig_candETAB=px.bar(
        cand_ETAB,
        x="MATRICULE",
        y=cand_ETAB.index,
        orientation="h",
        title="<b>CANDIDATS PAR ETABLISSEMENTS</b>",
        color_discrete_sequence=["#A73FD5"]*len(cand_ETAB),
    )
    fig_candETAB.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=True))
    )
    
    
    mention_depar=(
        df_selection.groupby(by=["MENTION"]).count()[["MATRICULE"]]
    )
    fig_mentdepar=px.bar(
        mention_depar,
        y="MATRICULE",
        x=mention_depar.index,
        orientation="v",
        title="<b>Nombre de MENTION </b>",
        color_discrete_sequence=["#21E527"]*len(mention_depar)
        #title='Nombre de Mention',values='MATRICULE',names='MATRICULE
    )
    fig_mentdepar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=True))
    )
    up,down,left=st.columns(3)
    up.plotly_chart(fig_mentdepar,use_container_width=True)
    down.plotly_chart(fig_canddepar,use_container_width=True)
    left.plotly_chart(fig_candETAB,use_container_width=True)
graph()



hide_st_style="""
            <style>
            #MainMenu{visibility:hidden;}
            footer{visibility:hidden;}
            header{visibility:hidden;}
            </style>
            """

st.markdown(hide_st_style,unsafe_allow_html=True)
