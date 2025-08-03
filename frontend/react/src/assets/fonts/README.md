# Локальные шрифты

Вместо загрузки шрифтов с Google Fonts, мы используем системные шрифты для ускорения загрузки страницы.

## Замененные шрифты

| Google Font | Системная замена |
|-------------|------------------|
| Varela Round | Segoe UI, Arial, Helvetica |
| JetBrains Mono | Consolas, Monaco, Courier New |
| Inter | Segoe UI, Arial, Helvetica |

## Преимущества

- ✅ **Быстрая загрузка** - нет внешних запросов к Google Fonts
- ✅ **Работает офлайн** - шрифты уже установлены в системе
- ✅ **Меньше зависимостей** - не нужен доступ к интернету
- ✅ **Лучшая производительность** - нет блокировки рендеринга

## Использование

Шрифты автоматически применяются через CSS-классы:

```css
.font-varela {
  font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
}

.font-jetbrains {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.font-inter {
  font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
}
```

## Совместимость

Системные шрифты доступны на всех современных операционных системах:

- **Windows**: Segoe UI, Arial
- **macOS**: Helvetica, Monaco
- **Linux**: Arial, Helvetica, Consolas

## Если нужны оригинальные шрифты

Если в будущем понадобятся оригинальные Google Fonts:

1. Скачайте шрифты с Google Fonts
2. Поместите .woff2 файлы в папку `fonts/`
3. Обновите `fonts.css` с правильными путями
4. Измените CSS-классы обратно на оригинальные названия 