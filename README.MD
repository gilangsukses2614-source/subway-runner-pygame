 🚇 Subway Runner 

Subway Runner adalah game 2D endless runner yang dibuat menggunakan Python dan Pygame.  
Pemain menghindari rintangan, mengumpulkan koin, membuka skin, dan memilih level dengan tingkat kesulitan berbeda.

 🎮 Fitur Utama

- 🎯 Gameplay endless runner
- 🪙 Sistem koin
- 🧥 Sistem skin (shop & inventory)
- 💾 Save & load progress (JSON)
- 🏆 High score
- 🎵 Background music & sound effect
- 📊 Pilih level (difficulty scaling)
- 🖱️ UI interaktif (hover, klik, animasi)

---

 🖥️ Preview Gameplay

- Menu utama
- Gameplay dengan background bergerak
- Inventory skin
- Shop skin
- Game Over screen
- Level selection

---

 🗂️ Struktur Folder
├── main.py
├── save.json
├── .gitignore
├── assets
│ ├── player.png
│ ├── road1.jpg
│ ├── obstacle1.png
│ ├── menu_bg.jpg
│ ├── skins
│ │ ├── default.png
│ │ ├── red.png
│ │ ├── blue.png
│ │ ├── gold.png
│ │ ├── purple.png
│ │ └── diamond.png
├── sounds
│ ├── bgm_game.mp3
│ ├── bgm_menu.mp3
│ ├── click.wav
│ ├── coin.wav
│ └── crash.wav

💾 Sistem Save Game

Progress game disimpan di file:

save.json


Data yang disimpan:

Total coins

Skin yang dimiliki

Skin aktif

High score

🎨 Sistem Skin

Skin dapat dibeli menggunakan koin

Skin yang dimiliki bisa dipilih di inventory

Skin aktif digunakan saat bermain

Efek visual saat membeli skin

🧠 Sistem Level

Game memiliki 8 level dengan perbedaan:

Kecepatan obstacle

Frekuensi spawn obstacle

Semakin tinggi level, semakin sulit gameplay.

📌 Kontrol Game
Aksi	Tombol
Gerak kiri	⬅️
Gerak kanan	➡️
Pilih	Klik mouse
Kembali	ESC
Menu (Game Over)	ENTER


