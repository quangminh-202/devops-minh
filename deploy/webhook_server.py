#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сервер Webhook для GitHub (Лабораторная работа №1 DevOps)

Назначение:
 - Получает события из GitHub (push)
 - Клонирует или обновляет репозиторий catty-reminders-app
 - Устанавливает зависимости
 - Собирает и тестирует приложение
 - Перезапускает веб-приложение (FastAPI)
"""

from flask import Flask, request, jsonify
import hmac
import hashlib
import subprocess
import os
from datetime import datetime

# ============ Конфигурация ============
REPO_URL = "https://github.com/quangminh-202/catty-reminders-app.git"
APP_DIR = "/home/quangminh/devops-minh/catty-reminders-app"
APP_SERVICE = "app.service"
SECRET_TOKEN = "devops"  # токен должен совпадать с секретом GitHub webhook
LOG_FILE = "/home/quangminh/devops-minh/deploy/webhook.log"

app = Flask(__name__)

# ======================================


def log(message: str):
    """Запись сообщений в лог и консоль"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def verify_signature(payload: bytes, signature_header: str) -> bool:
    """Проверка подписи HMAC SHA256 от GitHub"""
    if not signature_header:
        return False
    try:
        sha_name, signature = signature_header.split("=")
        mac = hmac.new(SECRET_TOKEN.encode(), msg=payload, digestmod=hashlib.sha256)
        return hmac.compare_digest(mac.hexdigest(), signature)
    except Exception as e:
        log(f"⚠ Ошибка проверки подписи: {e}")
        return False


def clone_or_pull_repo():
    """Клонирование или обновление репозитория"""
    if not os.path.exists(APP_DIR):
        log("📁 Репозиторий не найден — выполняется клонирование...")
        subprocess.run(["git", "clone", REPO_URL, APP_DIR], check=True)
    else:
        log("📦 Обновление кода из GitHub (git pull)...")
        subprocess.run(["git", "-C", APP_DIR, "pull"], check=True)


def install_dependencies():
    """Установка зависимостей из requirements.txt"""
    req_file = os.path.join(APP_DIR, "requirements.txt")
    if os.path.exists(req_file):
        log("📦 Установка зависимостей из requirements.txt...")
        subprocess.run(["pip3", "install", "-r", req_file], check=True)
    else:
        log("ℹ Файл requirements.txt не найден — пропуск установки зависимостей.")


def build_app():
    """Сборка приложения (если требуется)"""
    build_script = os.path.join(APP_DIR, "build.sh")
    setup_py = os.path.join(APP_DIR, "setup.py")

    if os.path.exists(build_script):
        log("🔧 Найден build.sh — выполняется сборка...")
        subprocess.run(["bash", build_script], check=True)
    elif os.path.exists(setup_py):
        log("🔧 Найден setup.py — выполняется сборка setup.py build...")
        subprocess.run(["python3", setup_py, "build"], check=True)
    else:
        log("ℹ Скрипт сборки не найден — пропуск шага сборки.")


def deploy_app():
    """Развертывание и перезапуск веб-приложения"""
    log("♻ Перезапуск приложения через systemd...")
    subprocess.run(["sudo","systemctl", "restart", APP_SERVICE], check=True)


# ======================================


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Webhook-сервер работает"}), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    event = request.headers.get("X-GitHub-Event", "ping")
    payload = request.data

    # Проверка подписи
    if not verify_signature(payload, signature):
        log("❌ Неверная подпись webhook — запрос отклонён.")
        return jsonify({"error": "invalid signature"}), 403

    log(f"📦 Получено событие GitHub: {event}")

    if event == "ping":
        return jsonify({"msg": "pong"}), 200

    if event == "push":
        try:
            log("🚀 Запуск процесса автоматического развертывания...")

            clone_or_pull_repo()
            install_dependencies()
            build_app()
            deploy_app()

            log("✅ Развертывание успешно завершено!")
            return jsonify({"status": "success"}), 200

        except subprocess.CalledProcessError as e:
            log(f"❌ Ошибка при развертывании: {e}")
            return jsonify({"status": "failed", "error": str(e)}), 500

    log(f"⚠ Событие {event} не поддерживается.")
    return jsonify({"msg": "ignored event"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
