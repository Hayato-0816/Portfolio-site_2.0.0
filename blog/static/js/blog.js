const blog = {
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.besideScroll();
            this.dragAndDrop();
            this.categoryFilter();
            this.searchForm();
        });
    },

    // カテゴリーリストの横スクロール処理
    besideScroll() {
        const categoryList = document.querySelector('.category-list');
        if (categoryList) {
            categoryList.addEventListener('wheel', function(e) {
                e.preventDefault();
                categoryList.scrollLeft += e.deltaY;
            });
        }
    },

    // カテゴリーのドラッグ&ドロップ処理
    dragAndDrop() {
        const categoryListSortable = document.getElementById('category_sortable');
        if (!categoryListSortable) return;
    
        const handleDragStart = function(e) {
            draggedItem = this;
            this.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        };
    
        const handleDragEnd = function() {
            this.classList.remove('dragging');
            draggedItem = dropTarget = null;
        };
    
        let draggedItem = null;
        let dropTarget = null;
        
        const categoryItems = categoryListSortable.querySelectorAll('.category_box');
    
        Array.from(categoryItems).forEach(item => {
            item.addEventListener('dragstart', handleDragStart);
            item.addEventListener('dragend', handleDragEnd);
        });
    
        const handleDragOver = function(e) {
            e.preventDefault();
            const result = getDropTarget(e.clientX, e.clientY);
            dropTarget = result?.element || null;
        };
    
        const handleDrop = function(e) {
            e.preventDefault();
            if (!draggedItem || !dropTarget || draggedItem === dropTarget) return;
    
            const initialRect = draggedItem.getBoundingClientRect();
            
            // 要素の移動
            const mouseX = e.clientX;
            const targetRect = dropTarget.getBoundingClientRect();
            const insertAfter = mouseX > targetRect.left + targetRect.width / 2;
            insertAfter ? dropTarget.after(draggedItem) : dropTarget.before(draggedItem);
    
            // アニメーション
            const finalRect = draggedItem.getBoundingClientRect();
            const deltaX = initialRect.left - finalRect.left;
            
            if (Math.abs(deltaX) > 0) {
                draggedItem.style.transform = `translateX(${deltaX}px)`;
                requestAnimationFrame(() => {
                    draggedItem.style.transition = 'transform 0.3s ease-out';
                    draggedItem.style.transform = '';
                });
            }
    
            // 新しい順序を記録
            const newOrder = [...categoryListSortable.getElementsByClassName('category_box')]
                .map(item => item.dataset.categoryId);
            console.log('New order:', newOrder);
        };
    
        const getDropTarget = function(mouseX, mouseY) {
            const elements = [...categoryListSortable.querySelectorAll('.category_box:not(.dragging)')];
            return elements.find(element => {
                const rect = element.getBoundingClientRect();
                return mouseY >= rect.top && mouseY <= rect.bottom;
            });
        };
    
        // イベントリスナーの設定
        categoryListSortable.querySelectorAll('.category_box').forEach(item => {
            item.addEventListener('dragstart', handleDragStart);
            item.addEventListener('dragend', handleDragEnd);
        });
    
        categoryListSortable.addEventListener('dragover', handleDragOver);
        categoryListSortable.addEventListener('drop', handleDrop);
    },

    // カテゴリーフィルタリング処理
    categoryFilter() {
        function showAllArticles() {
            articles.forEach(article => {
                article.style.opacity = '1';
                article.style.height = 'auto';
                article.style.marginBottom = '20px';
                article.style.visibility = 'visible';
            });
        }
        
        const articles = document.querySelectorAll('.blog_article');
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
    
        const categoryBoxes = document.querySelectorAll('.category_box');
        const categoryBoxesP = document.querySelectorAll('.category_box p');
        categoryBoxes.forEach(box => {
            box.addEventListener('click', function(e) {
                e.preventDefault();
                
                if (this.classList.contains('active')) {
                    this.classList.remove('active');
                    this.querySelector('p').classList.remove('active');
                    showAllArticles();
                } else {
                    categoryBoxes.forEach(b => b.classList.remove('active'));
                    categoryBoxesP.forEach(p => p.classList.remove('active'));
                    this.classList.add('active');
                    this.querySelector('p').classList.add('active');
                    
                    const categoryName = this.dataset.categoryName;
                    filterByCategory(categoryName);
                }
            });
        });
    },

    // 検索フォーム処理
    searchForm() {
        const searchForm = document.querySelector('.search_form');
        const searchInput = document.querySelector('.search_input');
        const errorMessage = document.querySelector('.search-error-message');
        const specialChars = /[<>{}]/;

        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.classList.add('show');
            searchInput.classList.add('error');
        }

        function clearError() {
            errorMessage.textContent = '';
            errorMessage.classList.remove('show');
            searchInput.classList.remove('error');
        }

        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                const searchValue = searchInput.value.trim();
                clearError();

                if (searchValue === '') {
                    e.preventDefault();
                    showError('※検索キーワードを入力してください。');
                    return;
                }

                if (searchValue.length < 2) {
                    e.preventDefault();
                    showError('※検索キーワードは2文字以上で入力してください。');
                    return;
                }

                if (searchValue.length > 50) {
                    e.preventDefault();
                    showError('※検索キーワードは50文字以内で入力してください。');
                    return;
                }

                if (specialChars.test(searchValue)) {
                    e.preventDefault();
                    showError('※特殊文字は使用できません。');
                    return;
                }

                if (/\s\s+/.test(searchValue)) {
                    e.preventDefault();
                    showError('※連続する空白は使用できません。');
                    return;
                }
            });

            let validationTimeout;
            searchInput.addEventListener('input', function() {
                const searchValue = this.value.trim();
                clearTimeout(validationTimeout);
                clearError();
                
                validationTimeout = setTimeout(() => {
                    if (searchValue.length > 50) {
                        showError('※検索キーワードは50文字以内で入力してください。');
                    } else if (searchValue.length === 1) {
                        showError('※検索キーワードは2文字以上で入力してください。');
                    } else if (specialChars.test(searchValue)) {
                        showError('※特殊文字は使用できません。');
                    }
                }, 500);
            });

            searchInput.addEventListener('focus', clearError);
        }
    }
    
}

blog.init();