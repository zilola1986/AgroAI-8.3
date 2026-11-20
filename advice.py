"""Low-risk, condition-aware care suggestions in Uzbek."""
def recommend(plant,condition,weather,water,location):
 base=[]
 if 'Sog‘lom' in condition:
  base=['Barglarni haftasiga bir necha marta kuzatib boring.', 'Sug‘orishni tuproq namligiga moslang.', 'O‘simlik atrofida havo almashinuvini saqlang.']
 elif any(w in condition.lower() for w in ['virus','mozaika','buralish']):
  base=['Barg ostida mayda hasharotlar bor-yo‘qligini kuzating.', 'Shubhali o‘simlikni alohida kuzatib, ish asboblarini toza tuting.', 'Yangi barglarda ham belgilar paydo bo‘layotganini yozib boring.']
 elif any(w in condition.lower() for w in ['mog‘or','chir','kuyish','zang','dog‘','septorioz','eska','unshudring']):
  base=['Barglarni imkon qadar uzoq vaqt ho‘l qoldirmang.', 'O‘simliklar orasida havo aylanishini yaxshilang.', 'Zararlanish kuchayishini suratlar bilan kuzatib boring.']
 elif 'kana' in condition.lower():
  base=['Barg ostini tekshiring va mayda zararkunandalarni kuzating.', 'O‘simlikni muntazam kuzatib, yangi zararlangan barglarni qayd eting.']
 else:base=['Barglar holatini 2–3 kun davomida kuzating.','Tuproq namligi va yorug‘likni tekshiring.']
 if water=='Ko‘p':base.append('Tuproq doim nam bo‘lsa, sug‘orish oralig‘ini qayta ko‘rib chiqing.')
 if water=='Kam':base.append('Tuproq qurib qolayotgan bo‘lsa, namlikni tekshirib sug‘oring.')
 if weather=='Nam':base.append('Nam sharoitda shamollatishga alohida e’tibor bering.')
 if weather=='Issiq':base.append('Juda issiq paytda o‘simlikni qo‘shimcha stressdan asrang.')
 if location=='Uyda':base.append('Deraza yonidagi yorug‘lik va havo aylanishini tekshiring.')
 return base
