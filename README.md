### Проєкт Облік Ліків

Проєкт "Облік Ліків" — це програма для управління аптечним обліком лікарських засобів. Користувачі можуть додавати нові ліки, оновлювати інформацію про наявні препарати, здійснювати пошук за різними критеріями, створювати замовлення на поповнення запасів і керувати постачаннями. Ця програма спрощує ведення обліку та забезпечує оптимальний контроль за станом аптечного складу.

#### Залежності
- Python 3.x
- Tkinter (входить у стандартну бібліотеку Python)
- ttkbootstrap (для створення сучасного інтерфейсу)

#### Встановлення
1. Завантажте та встановіть python з офіційного сайту
   https://www.python.org/
   

2. Запустіть вікно терміналу
   ```
   cmd
   ```
3. Пропишіть локацію клонування репозиторію (якщо потрібно)
   ```
   cd desktop
   ```
4. Клонуйте репозиторій за допомогою команди:
   ```
   git clone https://github.com/dmytro-hudorozkin/pharmacy-management.git
   ```
5. Перейдіть до папки з проєктом:
   ```
   cd pharmacy-management
   ```
6. Встановіть необхідні залежності:
   ```
   pip install -r requirements.txt
   ```
7. Запустіть програму:
   ```
   python main.py
   ```

Також можна запустити вже готовий .exe файл в папці "already compiled program" або завантажити його в релізах цього репозиторію.

Після цього ви можете користуватися програмою для обліку ліків на вашому комп'ютері.

#### Використання

##### Основний інтерфейс
Після запуску програми користувач побачить головне меню з такими функціями:
- **Склад**: відображає список усіх наявних медикаментів з можливістю редагування та видалення інформації про них.
- **Замовлення**: дозволяє створювати нові замовлення на поповнення медикаментів і керувати існуючими замовленнями.
- **Вийти**: завершує роботу програми.

##### Основні функції програми
- **Додавання нового медикаменту**: дозволяє додати новий препарат, вказуючи його назву, кількість, ціну та опис.
- **Редагування інформації про медикаменти**: дозволяє оновити дані про ліки, якщо є зміни в ціні, кількості чи інших параметрах.
- **Видалення медикаментів**: видаляє препарати зі списку, якщо вони більше не потрібні або закінчилися.
- **Створення та обробка замовлень**: дозволяє створювати нові замовлення на поповнення запасів ліків, а також відслідковувати статус виконання замовлень.
