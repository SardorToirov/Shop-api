# SHOP API
# E-Commerce REST API

Bu loyiha **Django** va **Django REST Framework (DRF)** yordamida qurilgan to'liq funksional E-Commerce (Elektron tijorat) API tizimidir. Loyiha zamonaviy web-dasturlash standartlariga javob beradi va ma'lumotlar bazasi bilan ishlash uchun turli xil yondashuvlarni (ViewSets, Generics, APIView) o'z ichiga oladi.

## 🚀 Loyiha Haqida

Ushbu API onlayn do'kon uchun zarur bo'lgan asosiy backend logikasini ta'minlaydi. Foydalanuvchilar mahsulotlarni ko'rishlari, kategoriyalarga ajratishlari, izlashlari, sharh qoldirishlari va chegirmalardan foydalanishlari mumkin.

### 🛠 Texnologiyalar
* **Python** 3.x
* **Django** 4.x or 5.x
* **Django REST Framework**
* **SQLite / PostgreSQL** (sozlamalarga qarab)

## ✨ Asosiy Imkoniyatlar (Features)

Loyihada DRF ning turli xil ko'rinishlari va qo'shimcha imkoniyatlaridan foydalanilgan:

* **Views:**
    * **ViewSets:** Asosiy CRUD operatsiyalari uchun (masalan, `ProductViewSet`, `CategoryViewSet`).
    * **Generic Views:** Aniq maqsadli so'rovlar uchun (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`).
    * **APIView:** Maxsus logika talab qiladigan murakkabroq jarayonlar uchun.
* **Pagination:** Katta hajmdagi ma'lumotlarni sahifalab chiqarish.
* **Filtering:** Mahsulotlarni narxi, kategoriyasi va boshqa parametrlari bo'yicha filtrlash.
* **Search:** Mahsulot nomi va tavsifi bo'yicha qidiruv tizimi.

## 🗂 Ma'lumotlar Bazasi Tuzilishi (Modellar)

Loyiha quyidagi asosiy modellardan tashkil topgan:

1.  **Category:** Mahsulotlar turkumi (Masalan: Elektronika, Kiyim-kechak).
2.  **Product:** Sotuvdagi mahsulot (Nomi, Narxi, Tavsifi).
3.  **Review:** Foydalanuvchilar tomonidan mahsulotga qoldirilgan baho va izoh.
4.  **FlashSale:** Vaqt bilan cheklangan chegirmalar (Start va End vaqtlari bilan).
5.  **ProductViewHistory:** Foydalanuvchilarning mahsulotlarni ko'rish tarixi (Analytics).

```mermaid
erDiagram
    CATEGORY ||--|{ PRODUCT : contains
    PRODUCT ||--|{ REVIEW : bas_on
    PRODUCT ||--|{ FLASHSALE : includes
    PRODUCT ||--|{ PRODUCTVIEWHISTORY : viewed_in
    USER ||--|{ REVIEW : writes
    USER ||--|{ PRODUCTVIEWHISTORY : views
