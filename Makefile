# Makefile for HarchaMAq Flask Backend

.PHONY: help build run dev prod clean test docker-build docker-run docker-dev docker-prod

help:
	@echo "Comandos disponibles:"
	@echo "  build        - Construir imagen Docker"
	@echo "  run          - Ejecutar contenedor Docker"
	@echo "  dev          - Desarrollo con docker-compose"
	@echo "  prod         - Producción con docker-compose"
	@echo "  clean        - Limpiar sistema Docker"
	@echo "  local        - Ejecutar localmente (sin Docker)"
	@echo "  install      - Instalar dependencias Python"

install:
	pip install -r requirements.txt

local:
	python run.py

build:
	docker build -t harchamaq-backend .

run:
	docker run --rm -p 5000:5000 --env-file .env.example harchamaq-backend

dev:
	docker-compose up --build

prod:
	docker-compose -f docker-compose.prod.yml up --build

clean:
	docker system prune -f
	docker-compose down --volumes --remove-orphans

stop:
	docker-compose down