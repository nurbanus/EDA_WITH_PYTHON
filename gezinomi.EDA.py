#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# In[5]:


pd.set_option("display.max_columns",None)


# In[23]:


pd.set_option("display.max_rows",None)


# In[12]:


df=pd.read_excel("C:/Users/HANDENUR/Downloads/miuul_gezinomi.xlsx")


# In[13]:


df.head(10)


# In[14]:


df.tail()


# In[15]:


df.describe().T


# In[16]:


df.isnull().values.any()


# In[17]:


df.isnull().sum()


# In[18]:


df["Price"].value_counts()


# In[19]:


#Soru 2:Kaç unique şehir vardır? Frekansları nedir? 

df["SaleCityName"].nunique()


# In[20]:


df["SaleCityName"].value_counts() #tekrar etmeyen 6 şehri  görmüş olduk 


# In[21]:


#Soru 3:Kaç unique Concept vardır?

df["ConceptName"].nunique()


# In[22]:


#Soru4: Hangi Concept’den kaçar tane satış gerçekleşmiş?(tekil) Gezinomi şirketinin yaptığı satışların fiyatlarını ve bu
#satışlara ait bilgiler içermektedir. o yüzden direkt value counts al
df["ConceptName"].value_counts()


# In[23]:


#diğer yol :groupby
df.groupby("ConceptName")["ConceptName"].value_counts()


# In[24]:


#soru5 Şehirlere göre satışlardan toplam ne kadar kazanılmış?[]
df.groupby("SaleCityName").agg({"Price": "sum"})


# In[25]:


#ya da daha basiti
df.groupby("SaleCityName")["Price"].sum()


# In[26]:


#Soru6: Concept türlerine göre göre ne kadar kazanılmış?
df["ConceptName"].value_counts() # bu bize tekil donuç verir. total istiyorum
df.groupby("ConceptName")["Price"].sum() #ya da agg ile 


# In[27]:


#Soru7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})


# In[28]:


#Soru 8: Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName").agg({"Price": "mean"})


# In[29]:


#Soru 9: Şehir-Concept kırılımında  PRICE ortalamalarınedir?
df.groupby(["ConceptName","SaleCityName"]).agg({"Price": "mean"})


# #Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
# SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
# Aralıkları ikna edici şekilde oluşturunuz.
# Örneğin: ‘0_7’, ‘7_30', ‘30_90', ‘90_max’ aralıklarını kullanabilirsiniz.
# Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullanabilirsiniz.
# 

# In[31]:


bins=[-1, 7, 30 ,90, df["SaleCheckInDayDiff"].max()]


# In[32]:


labels=["last minutes", "potential planners", "planners", "early bookers"]


# In[33]:


df["EB_score"]=pd.cut(df["SaleCheckInDayDiff"], bins ,labels=labels)


# In[34]:


df["EB_score"].head(100)


# In[35]:


#Görev 3:
#Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı
#cinsinden inceleyiniz 

df.groupby(["SaleCityName","ConceptName","EB_score"]).agg({"Price":["mean","count"]})


# In[36]:


# City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
#Elde ettiğiniz çıktıyı agg_df olarak kaydediniz

agg_df=df.groupby(["SaleCityName","ConceptName","Seasons"]).agg({"Price":"mean"}).sort_values("Price",ascending=True)


# In[37]:


agg_df


# In[38]:


#: Indekste yer alan isimleri değişken ismine çeviriniz.
#Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz


agg_df.reset_index(inplace=True)


# In[39]:


agg_df


# #Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
# • Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
# • Yeni eklenecek değişkenin adı: sales_level_based
# • Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_based değişkenini oluşturmanız gerekmektedir.

# In[44]:


for row in agg_df.values:
    print(row)


# In[53]:


agg_df["sales_level_based"]=[row[0].upper() +"_" + row[1].upper() + "_"+ row[2].upper() for row in agg_df.values]


# In[65]:


agg_df


# In[64]:


agg_df["sales_level_based"].value_counts() #tekrar eden yok. tekil


# #örev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
# • Yeni personaları PRICE’a göre 4 segmente ayırınız.
# • Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# • Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

# In[61]:


agg_df["SEGMENT"]=pd.qcut(agg_df["Price"],4 ,labels=["D","C","B","A"])


# In[63]:


agg_df.groupby(["SEGMENT"]).agg({"Price":["mean","max","sum"]})


# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
# • Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
# • Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?

# In[78]:


new_user="ANTALYA_HERŞEY DAHIL_HIGH"


# In[79]:


agg_df[agg_df["sales_level_based"] == new_user]


# In[80]:


new_user2="GIRNE_YARIM PANSIYON_LOW"


# In[81]:


agg_df[agg_df["sales_level_based"]==new_user2]


# In[ ]:





# In[ ]:




