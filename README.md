# 🛍️ دیجی‌استور - فروشگاه آنلاین ایرانی

فروشگاه آنلاین مدرن ایرانی با طراحی زیبا و عملکرد بالا.

## ✨ امکانات

- 🎨 طراحی مدرن و ریسپانسیو
- 📱 پشتیبانی کامل از موبایل
- 🔍 جستجوی سریع محصولات
- 🛒 سبد خرید با ذخیره‌سازی محلی
- 💳 اتصال به درگاه پرداخت زرین‌پال
- 📊 پنل مدیریت جامع
- 🔒 احراز هویت امن با Supabase
- 🚀 عملکرد بالا با Next.js 14

## 🛠️ استک فناوری

| لایه | فناوری |
|------|--------|
| فرانت‌اند | Next.js 14 + TypeScript |
| استایل | Tailwind CSS |
| دیتابیس | Supabase (PostgreSQL) |
| احراز هویت | Supabase Auth |
| پرداخت | زرین‌پال |
| هاست | Vercel |

## 🚀 راهاندازی سریع

### ۱. پیش‌نیازها

- Node.js 18+ (دانلود از https://nodejs.org)
- npm یا yarn
- حساب رایگان Supabase
- حساب رایگان Vercel

### ۲. کلون کردن پروژه

```bash
git clone https://github.com/yourusername/digistore.git
cd digistore
```

### ۳. نصب وابستگی‌ها

```bash
npm install
```

### ۴. تنظیم متغیرهای محیطی

```bash
cp .env.local.example .env.local
```

فایل `.env.local` را ویرایش کنید و مقادیر زیر را وارد کنید:

```
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
ZARINPAL_MERCHANT_ID=your-merchant-id
ZARINPAL_CALLBACK_URL=https://your-domain.com/checkout/verify
```

### ۵. تنظیم دیتابیس Supabase

1. به [supabase.com](https://supabase.com) بروید و حساب بسازید
2. یک پروژه جدید ایجاد کنید
3. به بخش SQL Editor بروید
4. محتوای فایل `supabase/schema.sql` را اجرا کنید
5. URL پروژه و anon key را در `.env.local` وارد کنید

### ۶. اجرای پروژه

```bash
npm run dev
```

پروژه در آدرس `http://localhost:3000` اجرا می‌شود.

## 📦 ساختار پروژه

```
digistore/
├── public/                  # فایل‌های استاتیک
├── src/
│   ├── app/                 # صفحات (App Router)
│   ├── components/          # کامپوننت‌ها
│   ├── lib/                 # ابزارها و تنظیمات
│   └── store/               # مدیریت وضعیت
├── supabase/
│   └── schema.sql           # ساختار دیتابیس
├── package.json
├── tailwind.config.ts
└── next.config.js
```

## 🎨 صفحات

- `/` - صفحه اصلی با اسلایدر و محصولات ویژه
- `/products` - لیست محصولات با فیلتر و جستجو
- `/products/[id]` - جزئیات محصول
- `/cart` - سبد خرید
- `/checkout` - فرآیند پرداخت
- `/admin` - پنل مدیریت

## 🔧 سفارشی‌سازی

### تغییر رنگ‌ها

فایل `tailwind.config.ts` را ویرایش کنید:

```typescript
colors: {
  primary: {
    50: '#eff6ff',
    // ...
    600: '#2563eb',  // رنگ اصلی
  },
}
```

### اضافه کردن محصولات جدید

از پنل مدیریت `/admin` یا مستقیماً از Supabase استفاده کنید.

## 🚀 استقرار در Vercel

1. کد را در GitHub آپلود کنید
2. به [vercel.com](https://vercel.com) بروید
3. پروژه جدید بسازید و ریپازیتوری GitHub را انتخاب کنید
4. متغیرهای محیطی را در Vercel وارد کنید
5. دکمه Deploy را بزنید

## 💰 هزینه‌ها

| آیتم | هزینه |
|------|-------|
| هاست (Vercel) | رایگان ✅ |
| دیتابیس (Supabase) | رایگان ✅ |
| دامنه (.ir) | ~۵۰,۰۰۰ تومان/سال |
| درگاه پرداخت | رایگان (کارمزد تراکنش) |

## 📝 لایسنس

MIT License

## 🤝 مشارکت

مشارکت شما خوش آمدید! لطفاً Issue یا Pull Request بسازید.

## 📞 پشتیبانی

اگر سوالی دارید، Issue بسازید اا با ما تماس بگیرید.
