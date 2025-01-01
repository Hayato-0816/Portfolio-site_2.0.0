document.addEventListener('DOMContentLoaded', function() {
    const categoryList = document.querySelector('.category-list');
    
    categoryList.addEventListener('wheel', function(e) {
        // デフォルトの縦スクロールを防止
        e.preventDefault();
        
        // 横スクロールの実行
        categoryList.scrollLeft += e.deltaY;
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const categoryList = document.getElementById('category-sortable');
    const categoryItems = categoryList.getElementsByClassName('category_box');
    
    Array.from(categoryItems).forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
    });

    categoryList.addEventListener('dragover', handleDragOver);
    categoryList.addEventListener('drop', handleDrop);

    let draggedItem = null;
    let dropTarget = null;
    let insertMode = 'swap'; // 'swap' または 'insert'

    function handleDragStart(e) {
        draggedItem = this;
        this.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
    }

    function handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';

        const draggable = document.querySelector('.dragging');
        if (!draggable) return;

        const result = getDropTarget(e.clientX, e.clientY);
        if (result) {
            dropTarget = result.element;
            insertMode = result.mode;
        }
    }

    function handleDrop(e) {
        e.preventDefault();
        if (!draggedItem || !dropTarget || draggedItem === dropTarget) return;
    
        // ドロップ前の位置を記録
        const initialRect = draggedItem.getBoundingClientRect();
    
        // 既存のアニメーションクラスを削除
        draggedItem.classList.remove('animating');
        
        if (insertMode === 'swap') {
            // 要素の入れ替え処理
            const tempNode = document.createElement('div');
            draggedItem.parentNode.insertBefore(tempNode, draggedItem);
            dropTarget.parentNode.insertBefore(draggedItem, dropTarget);
            tempNode.replaceWith(dropTarget);
        } else {
            // 要素の間に挿入
            const mouseX = e.clientX;
            const targetRect = dropTarget.getBoundingClientRect();
            const targetCenter = targetRect.left + targetRect.width / 2;
            if (mouseX > targetCenter) {
                dropTarget.after(draggedItem);
            } else {
                dropTarget.before(draggedItem);
            }
        }
    
        // アニメーションの適用
        const finalRect = draggedItem.getBoundingClientRect();
        const deltaX = initialRect.left - finalRect.left;
    
        if (Math.abs(deltaX) > 0) {
            // トランジションを一時的に無効化
            draggedItem.style.transition = 'none';
            draggedItem.style.transform = `translateX(${deltaX}px)`;
            
            // リフローを強制
            draggedItem.offsetHeight;
            
            // トランジションを再有効化してアニメーションを開始
            draggedItem.style.transition = 'transform 0.3s ease-out';
            draggedItem.style.transform = '';
    
            // アニメーション完了時の処理
            const handleTransitionEnd = () => {
                draggedItem.style.transition = '';
                draggedItem.style.transform = '';
                draggedItem.removeEventListener('transitionend', handleTransitionEnd);
            };
    
            draggedItem.addEventListener('transitionend', handleTransitionEnd);
        }
    
        const newOrder = Array.from(categoryItems).map(item => item.dataset.categoryId);
        console.log('New order:', newOrder);
    }

    function handleDragEnd(e) {
        this.classList.remove('dragging');
        draggedItem = null;
        dropTarget = null;
    }

    function getDropTarget(mouseX, mouseY) {
        const draggableElements = [...categoryList.querySelectorAll('.category_box:not(.dragging)')];
        if (!draggableElements.length) return null;

        for (const element of draggableElements) {
            const rect = element.getBoundingClientRect();
            const isOverElement = mouseY >= rect.top && mouseY <= rect.bottom;
            
            if (isOverElement) {
                // 要素の上にある場合
                if (mouseX >= rect.left && mouseX <= rect.right) {
                    return {
                        element: element,
                        mode: 'swap'
                    };
                }
                
                // 要素の間の場合
                const prevElement = element.previousElementSibling;
                if (prevElement && !prevElement.classList.contains('dragging')) {
                    const prevRect = prevElement.getBoundingClientRect();
                    if (mouseX >= prevRect.right && mouseX <= rect.left) {
                        return {
                            element: element,
                            mode: 'insert'
                        };
                    }
                }
            }
        }

        // 最後の要素の後ろの場合
        const lastElement = draggableElements[draggableElements.length - 1];
        if (lastElement && mouseX > lastElement.getBoundingClientRect().right) {
            return {
                element: lastElement,
                mode: 'insert'
            };
        }

        return null;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const categoryBoxes = document.querySelectorAll('.category_box');
    const categoryBoxesP = document.querySelectorAll('.category_box p');
    const articles = document.querySelectorAll('.blog_article');

    // すべての記事を表示する関数
    function showAllArticles() {
        articles.forEach(article => {
            article.style.opacity = '1';
            article.style.height = 'auto';
            article.style.marginBottom = '20px';
            article.style.visibility = 'visible';
        });
    }

    // カテゴリーでフィルタリングする関数
    function filterByCategory(categoryName) {
        articles.forEach(article => {
            const articleCategory = article.querySelector('.meta').textContent;
            if (articleCategory.includes(categoryName)) {
                article.style.opacity = '1';
                article.style.height = 'auto';
                article.style.marginBottom = '20px';
                article.style.visibility = 'visible';
            } else {
                article.style.opacity = '0';
                article.style.height = '0';
                article.style.marginBottom = '0';
                article.style.visibility = 'hidden';
            }
        });
    }

    // カテゴリーボックスのクリックイベント
    categoryBoxes.forEach(box => {
        box.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 既に選択されているカテゴリーをクリックした場合
            if (this.classList.contains('active')) {
                // 選択を解除してすべての記事を表示
                this.classList.remove('active');
                this.querySelector('p').classList.remove('active');
                showAllArticles();
            } else {
                // 新しいカテゴリーを選択
                categoryBoxes.forEach(b => b.classList.remove('active'));
                categoryBoxesP.forEach(p => p.classList.remove('active'));
                this.classList.add('active');
                this.querySelector('p').classList.add('active');
                
                const categoryName = this.dataset.categoryName;
                filterByCategory(categoryName);
            }
        });
    });
});