import time
import subprocess
import os


def run_stage(name, command):
    print(f"\n--- Запуск: {name} ---")
    try:
        # Запускаем команду в терминале
        subprocess.run(command, shell=True, check=True)
        print(f"[{name}] Успешно завершено!")
    except subprocess.CalledProcessError as e:
        print(f"[{name}] ОШИБКА: {e}")
        raise e


def automate_pipeline():
    # 1. Data Engineering
    run_stage("Stage 1: Data Engineering", "python code\\datasets\\data_engineering.py")

    # 2. Model Engineering
    run_stage("Stage 2: Model Training", "python code\\models\\train_model.py")

    # 3. Deployment (Обновление модели)
    # Так как FastAPI загружает модель только при старте, нам нужно перезапустить контейнер,
    # чтобы он подхватил свежий файл model.pkl из прокинутой папки.
    run_stage("Stage 3: API Restart", "cd code\\deployment && docker compose restart fastapi")


if __name__ == "__main__":
    print("🚀 MLOps Pipeline Оркестратор запущен!")

    while True:
        print(f"\n[🕒 {time.strftime('%H:%M:%S')}] Начало нового цикла пайплайна...")

        try:
            automate_pipeline()
            print("\n✅ Цикл пайплайна успешно завершен!")
        except Exception as e:
            print("\n❌ Пайплайн остановлен из-за ошибки.")

        # Ждем 5 минут (300 секунд) перед следующим запуском
        print("⏳ Ожидание 5 минут до следующего запуска...\n")
        time.sleep(300)