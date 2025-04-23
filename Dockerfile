FROM golang:1.23-alpine

WORKDIR /app

# Копируем файлы модулей
COPY go.mod go.sum ./

# Скачиваем зависимости
RUN go mod download

# Копируем весь код
COPY . .

# Собираем приложение
RUN go build -o main .

RUN ls
# Открываем порт
EXPOSE 8080

# Запускаем приложение
CMD ["/app/main"]