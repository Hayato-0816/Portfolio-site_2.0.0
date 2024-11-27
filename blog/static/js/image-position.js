document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.blog_image img');
    
    images.forEach(img => {
        let isDragging = false;
        let startX, startY;
        // ローカルストレージから保存された位置を取得、なければデフォルト値を使用
        let currentX = parseInt(localStorage.getItem('imagePositionX')) || 50;
        let currentY = parseInt(localStorage.getItem('imagePositionY')) || 50;

        // 初期位置を設定
        img.style.objectPosition = `${currentX}% ${currentY}%`;

        img.addEventListener('mousedown', startDragging);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDragging);

        function startDragging(e) {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            e.preventDefault();
        }

        function drag(e) {
            if (!isDragging) return;

            const deltaX = e.clientX - startX;
            const deltaY = e.clientY - startY;

            currentX = Math.max(0, Math.min(100, currentX - (deltaX * 0.1)));
            currentY = Math.max(0, Math.min(100, currentY - (deltaY * 0.1)));

            img.style.objectPosition = `${currentX}% ${currentY}%`;

            // 位置をローカルストレージに保存
            localStorage.setItem('imagePositionX', currentX);
            localStorage.setItem('imagePositionY', currentY);

            startX = e.clientX;
            startY = e.clientY;
        }

        function stopDragging() {
            isDragging = false;
        }
    });
});