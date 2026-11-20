import io,hashlib,json
from pathlib import Path
import streamlit as st
import pandas as pd
from PIL import Image,ImageStat,ImageFilter
from agro.engine import MODEL_ID,classify,assess
from agro.advice import recommend
from agro.store import add,rows
st.set_page_config(page_title='AgroAI | Aqlli bog‘',page_icon='🌱',layout='wide',initial_sidebar_state='expanded')
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {font-family:'Manrope',sans-serif}
.stApp {background:radial-gradient(ellipse at 80% 0%,#d9f3e7 0%,transparent 45%),linear-gradient(125deg,#f6fbf7,#e7f3ed);color:#143c30}
[data-testid="stSidebar"] {background:linear-gradient(165deg,#0b4236,#145c48 60%,#0c332e)!important}
[data-testid="stSidebar"] * {color:#f2fff7!important}
[data-testid="stSidebar"] [role="radiogroup"] {gap:13px!important}
[data-testid="stSidebar"] [role="radiogroup"] label {
background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);
border-radius:17px;padding:17px 13px!important;min-height:58px;
box-shadow:0 6px 16px rgba(0,0,0,.10);
transition:transform .18s ease,background .18s ease,box-shadow .18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
transform:scale(1.045) translateX(3px);background:rgba(153,242,191,.25);
box-shadow:0 12px 23px rgba(0,0,0,.22)
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
background:#278d66!important;border-color:#9df2bc;transform:scale(1.025);
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {font-weight:800}
h1,h2,h3 {color:#104a38!important}
[data-testid="stMetricValue"] {color:#12724d!important}
.stButton>button[kind="primary"] {background:linear-gradient(90deg,#158454,#26aa73);color:white;border:0;border-radius:13px}
[data-testid="stFileUploader"] {border-radius:17px}
.hero {background:linear-gradient(110deg,#0e503e,#167a57);color:white;border-radius:24px;
padding:30px 34px;margin:12px 0 30px;box-shadow:0 16px 30px #0d563626}
.hero h1{color:white!important;font-size:2.4rem!important;margin:0 0 10px}
.hero p{color:#d7f8e5;font-size:1.05rem;margin:0}
.hero small{color:#c5e8d2;letter-spacing:2px;font-weight:700}
.stAlert {border-radius:15px}
</style>""",unsafe_allow_html=True)
st.sidebar.markdown("## 🌱 AgroAI")
st.sidebar.caption("RAQAMLI AVLOD QIZLARI • 2026")
page=st.sidebar.radio('Bo‘limni tanlang',[
 '🔬  Surat tahlili',
 '📈  Tekshiruvlar tarixi',
 '🍃  Barg kasalliklari',
 '✨  Loyiha haqida'
],label_visibility='collapsed')
st.sidebar.markdown("---")
st.sidebar.caption("Barg salomatligi • v8.4")
st.markdown("""<div class="hero"><small>AGROAI • LEAF HEALTH</small>
<h1>🌿 Tabiatni asrash — aqlli texnologiyadan boshlanadi</h1>
<p>Bargni suratga oling. AI ehtimoliy kasallik belgisini baholaydi va parvarish tavsiyasini beradi.</p></div>""",unsafe_allow_html=True)
if page.startswith('🔬'):
 st.subheader('1. Barg suratini yuklang')
 uploaded=st.file_uploader('Rasmni tanlang (JPG, PNG, WEBP)',type=['jpg','jpeg','png','webp'])
 selected='auto'
 st.caption('Faqat bargni yaqin va ravshan suratga oling. Tizim kasallik belgilarini taxmin qiladi.')
 with st.expander('🌦️ Sharoitlar (tavsiyalarni moslashtirish uchun)',expanded=False):
  weather=st.selectbox('Havo sharoiti',['Oddiy','Nam','Issiq'])
  water=st.selectbox('Sug‘orish',['Me’yorida','Ko‘p','Kam'])
  location=st.selectbox('O‘sadigan joy',['Tomorqa / dala','Issiqxona','Uyda'])
 if uploaded:
  data=uploaded.getvalue()
  if len(data)>12*1024*1024:st.error('12 MB dan kichik surat tanlang.');st.stop()
  try:
   im=Image.open(io.BytesIO(data)).convert('RGB')
   im.thumbnail((1600,1600))
  except Exception:st.error('Rasm ochilmadi.');st.stop()
  left,right=st.columns([1,1.2])
  with left:
   st.image(im,caption='Siz yuklagan surat',width='stretch')
   if min(im.size)<300:st.warning('Surat kichik. Bargni yaqinroq va ravshanroq suratga oling.')
   gray=im.convert('L').resize((256,256))
   bright=ImageStat.Stat(gray).mean[0]
   if bright<55:st.warning('Surat qorong‘i. Yorug‘roq joyda qayta suratga oling.')
   if bright>225:st.warning('Surat haddan tashqari yorug‘.')
  with right:
   st.subheader('2. Sun’iy intellekt tahlili')
   if st.button('🔍 Tahlilni boshlash',type='primary',use_container_width=True):
    try:
     with st.spinner('AI modeli suratni tahlil qilmoqda. Birinchi ishga tushishda model serverga yuklanishi mumkin...'):
      raw=classify(im)
      st.session_state['result']=(hashlib.sha256(data).hexdigest(),assess(raw,selected))
    except Exception as e:
     st.error('Modelni yuklash yoki tahlil qilishda xatolik yuz berdi.')
     st.code(str(e))
   saved=st.session_state.get('result')
   if saved and saved[0]==hashlib.sha256(data).hexdigest():
    result=saved[1]
    if result['status'] in ('unsupported','no_result'):
     st.warning('Bu surat bo‘yicha ishonchli natija yo‘q. Bargni boshqa yorug‘likda qayta suratga oling.')
    else:
     name='Barg'
     is_estimate = result['status'] == 'estimate'
     st.markdown('### 🍃 Barg tahlili natijasi')
     if is_estimate:
      st.markdown(f'**Barg holati (AI taxmini):** {result["top"]["condition"]}')
     else:
      st.warning('Kasallikni ishonchli aniqlab bo‘lmadi.')
     st.metric('Model ehtimollik bahosi',f'{result["top"]["score"]:.1%}')
     st.caption('Bu model taxmini, tasdiqlangan tashxis emas. Model faqat sog‘lom va zararlangan bargni farqlashga o‘qitilgan.')
     if is_estimate:
      st.success('Barg holati bo‘yicha dastlabki AI taxmini olindi.')
      condition=result['top']['condition'].casefold()
      if 'zararlangan' in condition:
       st.markdown('#### 🔎 Bargdagi ehtimoliy muammolar va belgilar')
       st.warning('AI zararlanish ehtimolini baholadi, ammo kasallik nomini yoki alohida belgilarni aniqlamadi. Quyidagilarni suratga qarab foydalanuvchi belgilaydi.')
       symptom_info={
        '🟤 Jigarrang yoki qora dog‘lar': ('Dog‘lanish', 'Bargda to‘q rangli dog‘lar ayrim zamburug‘li yoki bakterial muammolarda, shuningdek shikastlanishda uchrashi mumkin.', 'Bargni quruq tutishga, sug‘orishda suvni bargga emas tuproqqa yo‘naltirishga harakat qiling.'),
        '🟡 Barg sarg‘ayishi': ('Sarg‘ayish', 'Sarg‘ayish ortiqcha yoki kam sug‘orish, oziqa yetishmovchiligi va ayrim kasalliklarda kuzatilishi mumkin.', 'Tuproq namligini, drenajni va o‘simlikning yorug‘lik sharoitini tekshiring.'),
        '⚪ Oq yoki kulrang qoplama': ('Oq qoplama', 'Un yoki changga o‘xshash qoplama ayrim zamburug‘li kasalliklar bilan bog‘liq bo‘lishi mumkin.', 'Havo aylanishini yaxshilang va barglarning uzoq vaqt nam turishidan saqlaning.'),
        '🍂 Qurish yoki kuygan chetlar': ('Qurish', 'Barg chetlarining qurishi issiq, qurg‘oqchilik, tuz to‘planishi yoki boshqa stress omillari bilan bog‘liq bo‘lishi mumkin.', 'Sug‘orish me’yorini va kuchli quyosh ta’sirini tekshiring.'),
        '🌀 Barg buralishi yoki shakl o‘zgarishi': ('Shakl o‘zgarishi', 'Buralish zararkunandalar, harorat, namlik yoki ayrim kasalliklarda uchrashi mumkin.', 'Bargning ustki va pastki tomonini tekshiring, o‘zgarishlarni kuzating.'),
        '🐛 Teshiklar yoki hasharot izlari': ('Zararkunanda belgisi', 'Teshiklar va kemirilgan joylar hasharotlar yoki boshqa zararkunandalar ta’siridan paydo bo‘lishi mumkin.', 'Bargning ikki tomonini tekshiring, zararkunanda ko‘rilsa mahalliy agronomdan maslahat oling.'),
       }
       chosen=st.multiselect('Suratda o‘zingiz ko‘rgan belgilarni tanlang:',list(symptom_info),key='agro_symptoms')
       if chosen:
        for symptom in chosen:
         title,explanation,tip=symptom_info[symptom]
         with st.expander(f'🌿 {title}: mumkin bo‘lgan sabablar',expanded=True):
          st.write(explanation)
          st.write('**Tavsiya:** '+tip)
       else:
        st.info('Belgilarni tanlasangiz, har biriga mos tushuntirish va parvarish tavsiyasi chiqadi.')
       st.caption('Tanlangan belgilar foydalanuvchi kuzatuvi asosida. Ular AI tomonidan aniqlangan yoki kasallik tashxisi sifatida ko‘rsatilmaydi.')
      else:
       st.success('Model bargni sog‘lom deb baholadi. Shunga qaramay, o‘simlikni muntazam kuzatib boring.')
      st.markdown('#### 🌼 Parvarish bo‘yicha mos tavsiyalar')
      for n,item in enumerate(recommend(name,result['top']['condition'],weather,water,location),1):
       st.write(f'{n}. {item}')
     else:
      st.info('Bargni yaqinroq, tabiiy yorug‘likda, oddiy fon oldida qayta suratga oling. Model o‘qitilmagan o‘simlikni ishonchli taniy olmaydi.')
      st.markdown('#### 🌼 Umumiy parvarish')
      st.write('O‘simlikni kuzating, sug‘orish va yorug‘lik sharoitini tekshiring. Kasallik nomi tasdiqlanmaguncha maxsus ishlov bermang.')
     with st.expander('🔎 Modelning boshqa taxminlari (tashxis emas)'):
      for r in result['results']:
       st.write(f'{r["condition"]} — {r["conditional_score"]:.1%} (2 sinf orasidagi model ulushi)')
       st.progress(max(0,min(1,r['conditional_score'])))
     if st.button('💾 Natijani saqlash'):
      stored_condition = result['top']['condition'] if is_estimate else 'Aniqlanmadi (noaniq natija)'
      add(name,stored_condition,result['top']['score'],result['status'],uploaded.name)
      st.success('Natija kompyuterdagi tarixga saqlandi.')
 else:st.info('Boshlash uchun o‘simlik bargi suratini yuklang.')
elif page.startswith('📈'):
 st.subheader('📈 Tekshiruvlar tarixi')
 data=rows()
 if data:
  df=pd.DataFrame(data,columns=['Sana','Ichki toifa','Ehtimoliy belgi','Model ulushi','Holat','Fayl'])
  df=df.drop(columns=['Ichki toifa'])
  st.metric('Tekshiruvlar soni',len(df))
  st.dataframe(df,width='stretch',hide_index=True)
  st.bar_chart(df['Ehtimoliy belgi'].value_counts())
  st.download_button('⬇️ CSV hisobot',df.to_csv(index=False).encode('utf-8-sig'),'agroai_hisobot.csv','text/csv')
 else:st.info('Hali saqlangan tekshiruvlar yo‘q.')
elif page.startswith('🍃'):
 st.subheader('🍃 Barg kasalliklari va alomatlari ensiklopediyasi')
 st.caption('32 ta ma’lumot kartasi: zamburug‘li, bakterial, virusli, zararkunanda hamda parvarish va muhit ta’sirlari.')
 with open(Path(__file__).parent/'agro'/'diseases.json',encoding='utf-8') as f:
  diseases=json.load(f)
 st.info('Kasallik belgilari o‘xshash bo‘lishi mumkin. Ushbu ensiklopediya ma’lumot uchun; AI modeli bu 32 toifaning hammasini mustaqil aniqlashga o‘qitilmagan.')
 query=st.text_input('🔎 Kasallik yoki alomatni qidiring',placeholder='Masalan: zang, sarg‘ayish, oq qoplama...')
 groups=['Barchasi','Zamburug‘li','Bakterial','Virusli','Zararkunanda','Parvarish va muhit']
 group=st.selectbox('📚 Bo‘limni tanlang',groups)
 filtered=[d for d in diseases if (group=='Barchasi' or d['tur']==group) and query.casefold() in (' '.join(d.values())).casefold()]
 st.caption(f'Ko‘rsatilmoqda: {len(filtered)} ta / {len(diseases)} ta')
 if not filtered:st.warning('Bu qidiruv bo‘yicha ma’lumot topilmadi.')
 for i in range(0,len(filtered),2):
  for col,d in zip(st.columns(2,gap='large'),filtered[i:i+2]):
   with col:
    with st.container(border=True):
     st.caption('🌿 '+d['tur'])
     st.markdown('#### '+d['nom'])
     st.markdown('**🔎 Belgilari**')
     st.write(d['belgi'])
     st.markdown('**💚 Parvarish va oldini olish**')
     st.write(d['tavsiya'])
     with st.expander('Qo‘shimcha ma’lumot'):
      st.write(d['eslatma'])
 st.caption('Tasdiqlanmagan fotosuratlar yoki sun’iy chizmalar haqiqiy kasallik fotosurati sifatida ko‘rsatilmaydi.')

else:
 st.subheader('✨ AgroAI haqida')
 st.success('Raqamli avlod qizlari tanlovi uchun yaratilgan aqlli o‘simlik yordamchisi.')
 st.write('AI modeli: '+MODEL_ID)
 st.write('Model ResNet18 asosida sog‘lom va zararlangan barg uchun 2 sinfga o‘qitilgan.')
 st.write('Colab sinovida yuqori aniqlik kuzatilgan, ammo haqiqiy dala rasmlarida alohida tekshiruv zarur.')
 st.write('Model kasallik nomini aniqlamaydi; faqat sog‘lom yoki zararlangan degan taxmin beradi.')
 st.write('Yuqori ehtimollik foizi to‘g‘ri tashxis kafolati emas. Noma’lum barg yoki xira suratda model adashishi mumkin.')
 st.write('Tavsiyalar umumiy xavfsiz parvarish qoidalariga asoslangan. Ilova kimyoviy preparat yoki dozalarni avtomatik belgilamaydi.')
