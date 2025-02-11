document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('.main_category, .sub_category, .skill');
    const editContainer = document.querySelector('.edit_contaner');
    let lastShownButtons = null;

    // 各カテゴリーにクリックイベントを追加
    categories.forEach(category => {
        category.addEventListener('click', async function(e) {
            // イベントの伝播を停止
            e.stopPropagation();
            
            // 前回表示されていたボタンがあれば非表示にする
            if (lastShownButtons) {
                lastShownButtons.style.opacity = 0;
                lastShownButtons.parentElement.style.backgroundColor = 'transparent';
            }
            
            // クリックされた要素内のedit_delete_buttonを取得
            const buttons = this.querySelector('.edit_delete_button');
            
            // ボタンを表示
            buttons.style.opacity = 1;
            this.style.backgroundColor = '#cacaca';
            
            // 現在表示しているボタンを記録
            lastShownButtons = buttons;

            // データ属性からIDとタイプを取得
            const categoryId = this.dataset.id;
            const categoryType = this.dataset.type;
            
            try {
                // データを非同期で取得
                const response = await fetch(`/dashboard/about/${categoryType}/${categoryId}/get/`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    // 編集フォームを表示
                    showEditForm(data.item);
                } else {
                    throw new Error('Network response was not ok');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('データの取得に失敗しました。');
            }
        });
    });

    // 編集フォームを表示する関数
    function showEditForm(item) {
        // 編集フォームのHTML要素を更新
        const formContainer = document.querySelector('.edit_main_category_contaner');
        formContainer.querySelector('input[name="name"]').value = item.name;
        formContainer.querySelector('input[name="item_id"]').value = item.id;
        formContainer.querySelector('input[name="type"]').value = item.type;
        
        // フォームを表示
        editContainer.style.display = 'block';
        
        // フォームの送信イベントを設定
        const form = formContainer.querySelector('form');
        form.addEventListener('submit', handleFormSubmit);
    }

    // フォーム送信を処理する関数
    async function handleFormSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);

        try {
            const response = await fetch('', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === 'success') {
                    alert('更新しました');
                    // 更新後のデータで表示を更新
                    updateCategoryDisplay(data.item);
                    // フォームを非表示
                    editContainer.style.display = 'none';
                } else {
                    alert('更新に失敗しました：' + data.errors);
                }
            } else {
                throw new Error('Network response was not ok');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('エラーが発生しました。');
        }
    }

    // カテゴリー表示を更新する関数
    function updateCategoryDisplay(item) {
        const category = document.querySelector(`.category[data-id="${item.id}"]`);
        if (category) {
            const nameElement = category.querySelector('h3, h4, p');
            if (nameElement) {
                // タイプに応じて適切な形式で名前を更新
                switch (item.type) {
                    case 'main':
                        nameElement.textContent = `■ ${item.name}`;
                        break;
                    case 'sub':
                        nameElement.textContent = item.name;
                        break;
                    case 'skill':
                        nameElement.textContent = ` - ${item.name}`;
                        break;
                }
            }
        }
    }

    // ページ全体をクリックした時のイベント
    document.addEventListener('click', function() {
        if (lastShownButtons) {
            lastShownButtons.style.opacity = 0;
            lastShownButtons.parentElement.style.backgroundColor = 'transparent';
            lastShownButtons = null;
        }
    });
});