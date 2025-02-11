document.addEventListener('DOMContentLoaded', function() {
    // ===============================
    // 定数とグローバル変数
    // ===============================
    const categories = document.querySelectorAll('.main_category, .sub_category, .skill');
    const editContainer = document.querySelector('.edit_about_contaner');
    let lastShownButtons = null;

    // ===============================
    // 初期化
    // ===============================
    initializeCategories();
    document.addEventListener('click', hideLastShownButtons);

    function initializeCategories() {
        categories.forEach(category => {
            setDataType(category);
            category.addEventListener('click', handleCategoryClick);
            initializeDeleteButton(category);
        });
        initializeUpdateButton();
    }

    function hideLastShownButtons() {
        if (lastShownButtons) {
            lastShownButtons.style.opacity = 0;
            lastShownButtons.parentElement.style.backgroundColor = 'transparent';
            lastShownButtons = null;
        }
    }

    // ===============================
    // カテゴリー管理の基本機能
    // ===============================
    function setDataType(category) {
        if (category.classList.contains('main_category'))
            category.dataset.type = 'main';
        else if (category.classList.contains('sub_category'))
            category.dataset.type = 'sub';
        else if (category.classList.contains('skill'))
            category.dataset.type = 'skill';
    }

    // ===============================
    // カテゴリークリック時の処理
    // ===============================
    async function handleCategoryClick(e) {
        e.stopPropagation();
        updateClickedCategoryVisual(this);
        await fetchAndShowEditForm(this);
    }

    function updateClickedCategoryVisual(category) {
        if (lastShownButtons) hideLastShownButtons();
        
        const buttons = category.querySelector('.category_delete_button');
        buttons.style.opacity = 1;
        category.style.backgroundColor = '#cacaca';
        lastShownButtons = buttons;
    }

    async function fetchAndShowEditForm(category) {
        const categoryId = category.dataset.id;
        const categoryType = category.dataset.type;
        
        try {
            const response = await fetch(`/dashboard/about/${categoryType}/${categoryId}/get/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            });
            
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            showEditForm(data.item);
        } catch (error) {
            console.error('Error:', error);
            alert('データの取得に失敗しました。');
        }
    }

    // ===============================
    // 編集フォームの管理
    // ===============================
    function showEditForm(item) {
        setBasicFormValues(editContainer, item);
        handleCategorySelects(editContainer, item);
        editContainer.style.display = 'flex';
        
        const form = editContainer.querySelector('form');
        form.addEventListener('submit', e => {
            e.preventDefault();
        });
    }

    function setBasicFormValues(editContainer, item) {
        const inputs = {
            name: item.name,
            item_id: item.id,
            type: item.type,
            is_active: item.is_active,
            order: item.order
        };

        Object.entries(inputs).forEach(([key, value]) => {
            const input = editContainer.querySelector(`input[name="${key}"]`);
            if (input.type === 'checkbox') input.checked = value;
            else input.value = value;
        });
    }

    function handleCategorySelects(editContainer, item) {
        const mainSelect = editContainer.querySelector('select[name="main_category"]');
        const subSelect = editContainer.querySelector('select[name="sub_category"]');
        
        const setupFunctions = {
            main: () => hideAllCategorySelects(mainSelect, subSelect),
            sub: () => setupSubCategorySelect(mainSelect, subSelect, item),
            skill: () => setupSkillCategorySelect(mainSelect, subSelect, item)
        };

        (setupFunctions[item.type] || setupFunctions.main)();
    }

    function hideAllCategorySelects(mainSelect, subSelect) {
        mainSelect.style.display = 'none';
        subSelect.style.display = 'none';
    }

    function setupSubCategorySelect(mainSelect, subSelect, item) {
        mainSelect.style.display = 'block';
        subSelect.style.display = 'none';
        const mainOptionValue = `${item.main_category_id}:${item.main_category_name}`;
        selectOption(mainSelect, mainOptionValue);
    }

    function setupSkillCategorySelect(mainSelect, subSelect, item) {
        mainSelect.style.display = 'none';
        subSelect.style.display = 'block';
        const subOptionValue = `${item.sub_category_id}:${item.sub_category_name}`;
        selectOption(subSelect, subOptionValue);
    }

    function selectOption(select, value) {
        Array.from(select.options).forEach(option => {
            if (option.value === value) {
                option.selected = true;
            }
        });
    }

    // ===============================
    // 編集処理
    // ===============================
    function initializeUpdateButton() {
        const form = document.querySelector('.edit_about_form');
        const updateButton = form.querySelector('.update_button');
        
        if (updateButton) {
            updateButton.addEventListener('click', e => {
                e.preventDefault();
                e.stopPropagation();
                handleUpdateSubmit(form);
            });
        }
    }
    
    async function handleUpdateSubmit(form) {
        const formData = new FormData(form);
        const type = formData.get('type');
        const itemId = formData.get('item_id');
        try {
            const response = await fetch(`/dashboard/about/${type}/${itemId}/update/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();
            if (data.status === 'success') {
                handleUpdateSubmitResponse(data);
            } else {
                alert('更新に失敗しました：' + JSON.stringify(data.errors));
            }
        } catch (error) {
            console.error('Update try error:', error);
            alert('エラーが発生しました。');
        }
    }

    function handleUpdateSubmitResponse(data) {
        if (data.status === 'success') {
            alert('更新しました');
            updateCategoryDisplay(data.item);
            editContainer.style.display = 'none';
        } else {
            alert('更新に失敗しました：' + JSON.stringify(data.errors));
        }
    }

    // ===============================
    // 削除処理
    // ===============================
    function initializeDeleteButton(category) {
        const deleteButton = category.querySelector('.category_delete_button');
        if (deleteButton) {
            deleteButton.addEventListener('click', e => {
                e.stopPropagation();
                handleDelete(category);
            });
        }
    }

    async function handleDelete(category) {
        if (!confirm('本当に削除しますか？')) return;

        const type = category.dataset.type;
        const itemId = category.dataset.id;
        
        try {
            const response = await fetch(`/dashboard/about/${type}/${itemId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                handleDeleteResponse(data, category);
            } else {
                throw new Error('Network response was not ok');
            }
        } catch (error) {
            console.error('Delete try error:', error);
        }
    }

    function handleDeleteResponse(data, category) {
        if (data.status === 'success') {
            category.remove();
            alert('削除しました');
        } else {
            alert('削除に失敗しました：' + data.message);
        }
    }

    // ===============================
    // カテゴリー表示更新
    // ===============================
    function updateCategoryDisplay(item) {
        // typeも含めて要素を特定する
        const category = document.querySelector(`.${item.type}_category.category[data-id="${item.id}"]`);
        if (category) {
            const nameElement = category.querySelector('h3, h4, p');
            if (nameElement) {
                updateNameElementText(nameElement, item);
            }
        }
    }

    function updateNameElementText(element, item) {
        const nameFormats = {
            'main': name => `■ ${name}`,
            'sub': name => name,
            'skill': name => ` - ${name}`
        };
        element.textContent = nameFormats[item.type](item.name);
    }
});