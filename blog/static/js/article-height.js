document.addEventListener('DOMContentLoaded', function() {
    function adjustArticlesHeight() {
        const articlesContainer = document.querySelector('.articles');
        const articleElements = document.querySelectorAll('.articles a');
        let totalHeight = 0;

        // 各記事の高さとマージンを計算
        articleElements.forEach((article, index) => {
            totalHeight += article.offsetHeight;
            // 最後の記事以外にマージンを追加
            if (index < articleElements.length - 1) {
                totalHeight += 40; // 記事間の隙間
            }
        });

        // 下部にも40pxの隙間を追加
        totalHeight += 40;

        // 新しい高さを設定
        articlesContainer.style.height = `${totalHeight}px`;
    }

    // 初期実行
    adjustArticlesHeight();

    // ウィンドウサイズが変更された時にも実行
    window.addEventListener('resize', adjustArticlesHeight);
});