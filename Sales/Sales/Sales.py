import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledFrame
import pygame
import sys
from math import sin, cos, radians

# Функція для запуску анімації перед tkinter
def run_animation():
    # Ініціалізація Pygame
    pygame.init()

    # Розміри екрану
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Подорожі мрії")

    # Завантаження зображення літака
    plane_image = pygame.image.load("images/plane.png")
    plane_image = pygame.transform.scale(plane_image, (150, 150))

    # Завантаження фонового зображення неба з хмарами
    background_image = pygame.image.load("images/cloud.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Встановлення початкової позиції літака
    plane_x = 0
    plane_y = screen_height // 2 - 75 - 100  # Піднімаємо літак на 100 пікселів
    plane_speed = 5

    # Кольори для тексту
    text_color = (255, 255, 255)  # Білий колір

    # Фонти для текстових повідомлень
    font = pygame.font.SysFont(None, 72)  # Збільшений розмір шрифту
    title_surface = font.render("Подорожі мрії", True, text_color)
    instruction_surface = pygame.font.SysFont(None, 48).render("Нажміть на любу кнопку щоб продовжити", True,
                                                               text_color)

    # Прапори станів анімації
    animation_stage = 0
    angle = 0

    # Основний цикл
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and animation_stage == 3:
                running = False  # Закінчуємо програму після натискання клавіші

        # Малюємо фонове зображення (хмари)
        screen.blit(background_image, (0, 0))

        if animation_stage == 0:
            # Рух літака вперед до потрібної позиції на екрані
            plane_x += plane_speed
            screen.blit(plane_image, (plane_x, plane_y))
            if plane_x >= screen_width // 2 - 75:
                animation_stage = 1

        elif animation_stage == 1:
            # Виконання "петлі смерті"
            angle += 2  # Кут повороту для плавного обертання

            if angle >= 360:
                angle = 0
                animation_stage = 2
            else:
                center_x = screen_width // 2 - 75
                center_y = screen_height // 2 + 75 - 100  # Піднятий центр на 100 пікселів
                plane_x = center_x + 150 * sin(radians(angle))
                plane_y = center_y - 150 * cos(radians(angle))
                rotated_plane = pygame.transform.rotate(plane_image, -angle)

                rotated_rect = rotated_plane.get_rect(center=(plane_x + 75, plane_y + 75))

                screen.blit(rotated_plane, rotated_rect.topleft)

        elif animation_stage == 2:
            # Продовження руху до правого краю екрану
            plane_x += plane_speed
            screen.blit(plane_image, (plane_x, plane_y))
            if plane_x >= screen_width:
                animation_stage = 3

        elif animation_stage == 3:
            # Відображення тексту після завершення анімації
            screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 4))
            screen.blit(instruction_surface, (
                screen_width // 2 - instruction_surface.get_width() // 2,
                screen_height // 2 + title_surface.get_height()))
            screen.blit(plane_image,
                        (screen_width // 2 - 75,
                         screen_height // 2 - 75 - 30))  # Піднятий літак після закінчення анімації

        # Оновлення екрану
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Початковий список турів
tour_packages = {
    "Париж": {
        "description": "Тур на 5 днів до Парижу. Відвідайте Ейфелеву вежу, Лувр, Нотр-Дам та інші відомі місця. Вартість: 500 євро.",
        "image": "images/paris.jpg",
        "price": "500 євро"
    },
    "Рим": {
        "description": "Тур на 7 днів до Риму. Відвідайте Колізей, Ватикан, Фонтан Треві та інші історичні місця. Вартість: 700 євро.",
        "image": "images/rome.jpg",
        "price": "700 євро"
    },
    "Барселона": {
        "description": "Тур на 6 днів до Барселони. Пориньте у світ Гауді, відвідайте Саграда Фамілія та Ла Рамбла. Вартість: 600 євро.",
        "image": "images/barcelona.jpg",
        "price": "600 євро"
    },
    "Амстердам": {
        "description": "Тур на 4 дні до Амстердаму. Прогуляйтеся каналами, відвідайте музеї Ван Гога та Анни Франк. Вартість: 450 євро.",
        "image": "images/amsterdam.jpg",
        "price": "450 євро"
    },
    "Берлін": {
        "description": "Тур на 5 днів до Берліну. Відвідайте Бранденбурзькі ворота, Рейхстаг і залишки Берлінської стіни. Вартість: 550 євро.",
        "image": "images/berlin.jpg",
        "price": "550 євро"
    },
    "Прага": {
        "description": "Тур на 6 днів до Праги. Прогуляйтеся Староміською площею, Карловим мостом і відвідайте Празький Град. Вартість: 600 євро.",
        "image": "images/prague.jpg",
        "price": "600 євро"
    },
    "Лондон": {
        "description": "Тур на 5 днів до Лондону. Відвідайте Біг-Бен, Лондонське око і Тауер місто. Вартість: 700 євро.",
        "image": "images/london.jpg",
        "price": "700 євро"
    },
    "Відень": {
        "description": "Тур на 3 дні до Відня. Відвідайте Шонбруннський палац, Оперний театр і Музей Мистецтво-історії. Вартість: 400 євро.",
        "image": "images/vienna.jpg",
        "price": "400 євро"
    },
    "Токіо": {
        "description": "Тур на 7 днів до Токіо. Пориньте у світ сучасної та традиційної Японії, відвідайте Сіндзюку та Асакуса. Вартість: 900 євро.",
        "image": "images/tokyo.jpg",
        "price": "900 євро"
    }
}


# З'єднання з базою даних
conn = sqlite3.connect('tours.db')
c = conn.cursor()

# Створення таблиці користувачів
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT PRIMARY KEY, password TEXT)''')

# Створення таблиці турів користувачів
c.execute('''CREATE TABLE IF NOT EXISTS user_tours 
             (username TEXT, tour_name TEXT, tour_date TEXT, 
              FOREIGN KEY(username) REFERENCES users(username))''')
conn.commit()
current_user = None
selected_tours = []


# Функція для завантаження зображень
def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


# Функція для зміни фреймів
def show_frame(frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    frame()


# Функція для відображення головного меню
def main_menu():
    clear_buttons()
    for widget in main_frame.winfo_children():
        widget.destroy()
    tk.Label(main_frame, text="Подорожі Мрії", font=("Arial", 24, "bold")).pack(pady=20)
    tour_image = load_image("images/company.png", (1100, 600))
    tk.Label(main_frame, image=tour_image).pack(pady=20)
    main_frame.image = tour_image  # Збереження посилання на зображення
    login_button_text = "Вихід" if current_user else "Вхід"
    ttk.Button(inner_buttons_frame, text=login_button_text, command=handle_login).pack(side=tk.LEFT, padx=20)


# Обробка натискання кнопки "Вхід/Вихід"
def handle_login():
    if current_user:
        logout()
    else:
        show_frame(login_screen)


# Вихід з аккаунту
def logout():
    global current_user
    current_user = None
    show_frame(main_menu)


# Екран авторизації
def login_screen():
    clear_buttons()
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Вітальне повідомлення
    tk.Label(main_frame, text="Ласкаво просимо! Будь ласка, увійдіть у свій акаунт.", font=("Arial", 18)).pack(pady=10)

    # Додавання зображення
    welcome_image = load_image("images/welcome_image.jpg", (400, 400))  # Змініть на шлях до вашого зображення
    tk.Label(main_frame, image=welcome_image).pack(pady=10)
    main_frame.image = welcome_image  # Збереження ф-ції на зображення

    tk.Label(main_frame, text="Вхід", font=("Arial", 24)).pack(pady=20)
    tk.Label(main_frame, text="Логін:", font=("Arial", 14)).pack()
    username_entry = ttk.Entry(main_frame, font=("Arial", 14))
    username_entry.pack()
    tk.Label(main_frame, text="Пароль:", font=("Arial", 14)).pack()
    password_entry = ttk.Entry(main_frame, show="*", font=("Arial", 14))
    password_entry.pack()
    ttk.Button(main_frame, text="Увійти", command=lambda: login(username_entry.get(), password_entry.get())).pack(
        pady=10)
    # Додатковий фрейм для кнопок
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Назад", command=lambda: show_frame(main_menu)).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Реєстрація", command=register_screen).grid(row=0, column=1, padx=5)
# Функція для входу
def login(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        global current_user
        current_user = username
        messagebox.showinfo("Успіх", "Вхід успішний!")
        load_user_tours()
        show_frame(main_menu)
    else:
        messagebox.showerror("Помилка", "Невірний логін або пароль!")


# Завантаження турів користувача
def load_user_tours():
    global selected_tours
    c.execute("SELECT tour_name, tour_date FROM user_tours WHERE username=?", (current_user,))
    user_tours = c.fetchall()
    selected_tours = [{"name": tour[0], "date": tour[1], "tour_info": tour_packages[tour[0]]} for tour in user_tours]


# Екран реєстрації
def register_screen():
    clear_buttons()
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Опис
    tk.Label(main_frame, text="Зареєструйтесь зараз та отримайте знижки на ваші улюблені тури!",
             font=("Arial", 18)).pack(pady=10)

    # Додавання зображення
    register_image = load_image("images/register_image.jpg", (600, 400))  # Змініть на шлях до вашого зображення
    tk.Label(main_frame, image=register_image).pack(pady=10)
    main_frame.image = register_image  # Збереження ф-ції на зображення

    tk.Label(main_frame, text="Реєстрація", font=("Arial", 24)).pack(pady=20)
    tk.Label(main_frame, text="Логін:", font=("Arial", 14)).pack()
    username_entry = ttk.Entry(main_frame, font=("Arial", 14))
    username_entry.pack()
    tk.Label(main_frame, text="Пароль:", font=("Arial", 14)).pack()
    password_entry = ttk.Entry(main_frame, show="*", font=("Arial", 14))
    password_entry.pack()
    ttk.Button(main_frame, text="Зареєструватись",
               command=lambda: register(username_entry.get(), password_entry.get())).pack(pady=10)
    ttk.Button(main_frame, text="Назад", command=login_screen).pack(pady=10)


# Функція для реєстрації
def register(username, password):
    if not username or not password:
        messagebox.showerror("Помилка", "Заповніть всі поля!")
        return
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        messagebox.showerror("Помилка", "Користувач з таким логіном вже існує!")
    else:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Успіх", "Реєстрація успішна! Тепер ви можете увійти.")
        login_screen()


# Функція для пошуку турів
def search_tours():
    if not current_user:
        show_not_logged_in_message()
        return
    cities = list(tour_packages.keys())
    for widget in main_frame.winfo_children():
        widget.destroy()
    bg_image = load_image("images/background.jpg", (1200, 900))  # Шлях до вашого фонового зображення
    bg_label = tk.Label(main_frame, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Розтягуємо зображення на весь екран
    main_frame.image = bg_image  # Зберігаємо посилання на зображення
    buttons_frame = tk.Frame(main_frame, bg='', highlightbackground="black", highlightthickness=0)
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    for idx, city in enumerate(cities):
        row = idx // 3
        col = idx % 3
        button = ttk.Button(buttons_frame, text=city, command=lambda city=city: show_city_details(city))
        button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
    for i in range((len(cities) + 2) // 3):
        buttons_frame.grid_rowconfigure(i, weight=1)
    for j in range(3):
        buttons_frame.grid_columnconfigure(j, weight=1)


# Функція для показу деталей туру після натискання на кнопку
def show_city_details(city):
    global current_tour
    current_tour = city
    show_frame(show_tour_details)


# Деталі туру
def show_tour_details():
    tour_info = tour_packages[current_tour]
    tk.Label(main_frame, text=f"Місто: {current_tour}", font=("Arial", 16)).pack(pady=10)
    tk.Label(main_frame, text=tour_info["description"], wraplength=800, font=("Arial", 14)).pack(pady=10)
    tour_image = load_image(tour_info["image"], (800, 600))
    tk.Label(main_frame, image=tour_image).pack(pady=10)
    main_frame.image = tour_image
    global buttons_frame
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(pady=10)
    ttk.Button(buttons_frame, text="Обрати", command=choose_tour).pack(side=tk.LEFT, padx=20)
    ttk.Button(buttons_frame, text="Назад", command=lambda: show_frame(search_tours)).pack(side=tk.LEFT, padx=20)


# Вибір туру
def choose_tour():
    for widget in main_frame.winfo_children():
        widget.destroy()
    tour_info = tour_packages[current_tour]
    tk.Label(main_frame, text=f"Тур: {current_tour}", font=("Arial", 16)).pack(pady=10)
    tk.Label(main_frame, text=f"Ціна: {tour_info['price']}", font=("Arial", 14)).pack(pady=10)
    tour_image = load_image(tour_info['image'], (700, 500))
    tk.Label(main_frame, image=tour_image).pack(pady=10)
    main_frame.image = tour_image

    tk.Label(main_frame, text="Оберіть дату туру:", font=("Arial", 12)).pack(pady=10)

    # Списки для дня, місяця та року
    days = [str(i).zfill(2) for i in range(1, 32)]
    months = [str(i).zfill(2) for i in range(1, 13)]
    years = [str(i) for i in range(2024, 2030)]

    day_var = tk.StringVar(value=days[0])
    month_var = tk.StringVar(value=months[0])
    year_var = tk.StringVar(value=years[0])

    # Створюємо фрейм для списків вибору дати
    date_frame = tk.Frame(main_frame)
    date_frame.pack(pady=10)

    day_menu = ttk.OptionMenu(date_frame, day_var, days[0], *days)
    day_menu.pack(side=tk.LEFT, padx=5)

    month_menu = ttk.OptionMenu(date_frame, month_var, months[0], *months)
    month_menu.pack(side=tk.LEFT, padx=5)

    year_menu = ttk.OptionMenu(date_frame, year_var, years[0], *years)
    year_menu.pack(side=tk.LEFT, padx=5)

    def confirm_tour():
        current_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
        selected_tours.append({"name": current_tour, "date": current_date, "tour_info": tour_info})
        c.execute("INSERT INTO user_tours (username, tour_name, tour_date) VALUES (?, ?, ?)",
                  (current_user, current_tour, current_date))
        conn.commit()
        messagebox.showinfo("Підтверджено", "Тур успішно обрано!")
        show_frame(main_menu)

    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(pady=10)
    ttk.Button(buttons_frame, text="Підтвердити", command=confirm_tour).pack(side=tk.LEFT, padx=20)
    ttk.Button(buttons_frame, text="Назад", command=lambda: show_frame(show_tour_details)).pack(side=tk.LEFT, padx=20)


# Мої путівки з умовним скролбаром
def my_tours():
    if not current_user:
        show_not_logged_in_message()
        return
    clear_buttons()
    for widget in main_frame.winfo_children():
        widget.destroy()
    tk.Label(main_frame, text=f"{current_user}, ваші путівки", font=("Arial", 20, 'bold')).pack(pady=20)
    if not selected_tours:
        tk.Label(main_frame, text="Ще не має путівок...", font=("Arial", 16)).pack(pady=20)
        sad_image = load_image("images/sad.jpg", (800, 600))
        tk.Label(main_frame, image=sad_image).pack(pady=20)
        main_frame.image = sad_image
    else:
        # Використання ScrolledFrame, якщо є путівки
        scrolled_frame = ScrolledFrame(main_frame, autohide=True)
        scrolled_frame.pack(expand=True, fill="both")
        for idx, tour in enumerate(selected_tours):
            frame = ttk.Frame(scrolled_frame, relief="solid", padding="10")
            frame.pack(pady=10, fill=tk.X)

            # Центрування назви та дати
            tk.Label(frame, text=f"{tour['name']} (Дата: {tour['date']})", font=("Arial", 16, 'bold')).pack(pady=5,
                                                                                                            anchor="center")

            tour_image = load_image(tour['tour_info']['image'], (600, 400))
            tk.Label(frame, image=tour_image).pack(pady=10)
            frame.image = tour_image  # Зберігаємо спільне посилання на зображення

            # Центрування кнопки
            ttk.Button(frame, text="Переглянути деталі",
                command=lambda idx=idx: show_frame(lambda: show_my_tour_details(idx))
            ).pack(pady=5, anchor="center")


# Деталі моєї обраної путівки
def show_my_tour_details(index):
    selected_tour = selected_tours[index]
    tour_info = selected_tour['tour_info']
    tour_date = selected_tour['date']
    tk.Label(main_frame, text=f"Тур: {selected_tour['name']}", font=("Arial", 16)).pack(pady=10)
    tk.Label(main_frame, text=tour_info['description'], font=("Arial", 14)).pack(pady=10)
    tour_image = load_image(tour_info["image"], (750, 550))
    tk.Label(main_frame, image=tour_image).pack(pady=10)
    main_frame.image = tour_image
    tk.Label(main_frame, text=f"Дата туру: {tour_date}", font=("Arial", 14)).pack(pady=10)
    today = datetime.today().date()
    tour_datetime = datetime.strptime(tour_date, "%Y-%m-%d").date()
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(pady=20)
    if tour_datetime > today:
        ttk.Button(buttons_frame, text="Скасувати", command=lambda: cancel_tour(index)).pack(side=tk.LEFT, padx=20)
    else:
        tk.Label(buttons_frame, text="Тур вже відбувся", font=("Arial", 14), fg="red").pack(side=tk.LEFT, padx=20)
    ttk.Button(buttons_frame, text="Назад", command=lambda: show_frame(my_tours)).pack(side=tk.LEFT, padx=20)


# Скасування туру
def cancel_tour(index):
    tour_name = selected_tours[index]["name"]
    tour_date = selected_tours[index]["date"]
    c.execute("DELETE FROM user_tours WHERE username=? AND tour_name=? AND tour_date=?",
              (current_user, tour_name, tour_date))
    conn.commit()
    del selected_tours[index]
    messagebox.showinfo("Скасовано", "Тур успішно скасовано!")
    show_frame(my_tours)


# Показує повідомлення та залишає користувача на головній сторінці
def show_not_logged_in_message():
    show_frame(main_menu)
    tk.messagebox.showinfo("Увага", "Ви повинні увійти в акаунт, щоб використати цю функцію.")


# Функція для очищення кнопок
def clear_buttons():
    for widget in inner_buttons_frame.winfo_children():
        widget.destroy()
    ttk.Button(inner_buttons_frame, text="Головна", command=lambda: show_frame(main_menu)).pack(side=tk.LEFT, padx=20)
    ttk.Button(inner_buttons_frame, text="Шукати путівки", command=lambda: show_frame(search_tours)).pack(side=tk.LEFT,
                                                                                                          padx=20)
    ttk.Button(inner_buttons_frame, text="Мої путівки", command=lambda: show_frame(my_tours)).pack(side=tk.LEFT,
                                                                                                   padx=20)


# Запуск анімації перед запуском tkinter
run_animation()

# Головне вікно
root = tk.Tk()
root.title("Туристична агенція")
root.geometry("1200x900")

# Стилі
style = Style()  # Initialize ttkbootstrap style
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TFrame", background="white")
style.configure("TLabel", background="white", font=("Arial", 12))

buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.TOP, pady=10)
inner_buttons_frame = tk.Frame(buttons_frame)
inner_buttons_frame.pack()
main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH)

show_frame(main_menu)
root.mainloop()
