# AgroAI v7.0 — Tanlov versiyasi

Bu ZIP ichida Colab’da o‘qitilgan `AgroAI_v7_model.pth` modeli ham bor. Oldingi v6 dizayni, tarix va 32 kartalik barg kasalliklari ensiklopediyasi saqlangan.

## Windows 10/11
1. Python 3.11 (64-bit) o‘rnating va PATH ga qo‘shing.
2. ZIP ni to‘liq oching (ZIP ichida turib START.bat ni ishga tushirmang).
3. Internetga ulangan holda `START.bat` ni ikki marta bosing. Birinchi safar kutubxonalar o‘rnatiladi; keyingi safar modelni ishlatish uchun internet shart emas.
4. Brauzer avtomatik ochilmasa, `http://localhost:8501` ga kiring.

## Tanlovdagi boshqa kompyuter
Internet va Python 3.11 o‘rnatish huquqi bo‘lsa ZIP ni ochib START.bat ni bosing. Kutubxonalar avvaldan o‘rnatilmagan kompyuterda dastlabki ishga tushirish vaqt oladi. Eng qulay ko‘rsatish uchun oldindan o‘z noutbukingizda sinab ko‘ring; boshqa kompyuterda ham oldindan sinov qiling.

## Natijalar va cheklovlar
ResNet18, 38 ta PlantVillage sinfi, 1140 ta muvozanatli rasm bilan dastlabki o‘qitish. 10 849 ta alohida test rasmida 83,87% umumiy aniqlik. Dala sharoitida bunday aniqlik kafolatlanmaydi. 38 ta sinfning bir qismi sog‘lom barg holatidir. Ilova noma’lum barg yoki kasallikni ham mavjud sinflardan biriga moslashtirishi mumkin; bu tasdiqlangan tashxis emas. Model faylini o‘chirmang.

Modelni kompyuterdan tashqariga uzatish uchun ishlatiladigan fayl: `AgroAI_v7_model.pth`.
