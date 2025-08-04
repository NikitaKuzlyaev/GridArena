// Предзагрузка шрифтов Bootstrap Icons для оптимизации производительности

// Функция для предзагрузки шрифтов
function preloadFonts() {
  const fontUrls = [
    '/assets/fonts/fonts/bootstrap-icons.woff2',
    '/assets/fonts/fonts/bootstrap-icons.woff'
  ];

  fontUrls.forEach(url => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'font';
    link.type = 'font/woff2';
    link.href = url;
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
  });
}

// Запускаем предзагрузку при загрузке страницы
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', preloadFonts);
} else {
  preloadFonts();
}

// Экспортируем функцию для использования в других модулях
export { preloadFonts }; 