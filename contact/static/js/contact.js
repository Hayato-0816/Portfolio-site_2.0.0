function showConfirmation(){
    if (!validateForm()) {
        return;
    }

    // 入力内容の表示
    document.getElementById("conf_company").textContent = document.getElementById("company_name_field").querySelector("input").value;
    document.getElementById("conf_name").textContent = document.getElementById("name_field").querySelector("input").value;
    document.getElementById("conf_email").textContent = document.getElementById("email_field").querySelector("input").value;
    document.getElementById("conf_phone").textContent = document.getElementById("phone_number_field").querySelector("input").value;
    document.getElementById("conf_message").textContent = document.getElementById("message_field").querySelector("textarea").value;

    // cssの変更
    document.getElementById("contact_form").style.top = "40px";
    document.getElementById("input_confirmation").classList.add("input_active");

    // ブラウザの戻るボタンを無効化
    window.history.pushState({page: 'contact form'}, '', window.location.pathname);

    // ブラウザの戻るボタンを押したとき一度だけ実行
    window.addEventListener('popstate', function(event) {
        hideConfirmation();
    }, {once: true});
}

function validateForm() {
    // validation対象の取得
    const name = document.getElementById("name_field").querySelector("input").value.trim();
    const email = document.getElementById("email_field").querySelector("input").value.trim();
    const message = document.getElementById("message_field").querySelector("textarea").value.trim();
    const phone = document.getElementById("phone_number_field").querySelector("input").value.trim();
    
    let isValid = true;
    // 名前のvalidation
    const nameRequired = document.getElementById("name_required");
    if (!name) {
        nameRequired.dataset.tooltip = "お名前は必須項目です。";
        nameRequired.classList.add("error");
        isValid = false;
    } else if (name.length > 50) {
        nameRequired.dataset.tooltip = "お名前は50文字以内で入力してください。";
        nameRequired.classList.add("error");
        isValid = false;
    } else {
        nameRequired.dataset.tooltip = "必須項目";
        nameRequired.classList.remove("error");
    }

    // メールアドレスのvalidation
    const emailRequired = document.getElementById("email_required");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
        emailRequired.dataset.tooltip = "メールアドレスは必須項目です。";
        emailRequired.classList.add("error");
        isValid = false;
    } else if (!emailRegex.test(email)) {
        emailRequired.dataset.tooltip = "正しいメールアドレスの形式で入力してください。";
        emailRequired.classList.add("error");
        isValid = false;
    } else {
        emailRequired.dataset.tooltip = "必須項目";
        emailRequired.classList.remove("error");
    }

    // お問い合わせ内容のvalidation
    const messageRequired = document.getElementById("message_required");
    if (!message) {
        messageRequired.dataset.tooltip = "お問い合わせ内容は必須項目です。";
        messageRequired.classList.add("error");
        isValid = false;
    } else if (message.length > 1000) {
        messageRequired.dataset.tooltip = "お問い合わせ内容は1000文字以内で入力してください。";
        messageRequired.classList.add("error");
        isValid = false;
    } else {
        messageRequired.dataset.tooltip = "必須項目";
        messageRequired.classList.remove("error");
    }

    // 電話番号のvalidation（任意項目）
    const phoneRequired = document.getElementById("phone_required");
    const phoneRegex = /^[0-9-]{10,13}$/;
    if (phone && !phoneRegex.test(phone)) {
        phoneRequired.dataset.tooltip = "電話番号は10桁から13桁の数字とハイフンで入力してください。";
        phoneRequired.classList.add("error");
        isValid = false;
    } else {
        phoneRequired.dataset.tooltip = "";
        phoneRequired.classList.remove("error");
    }

    if (!isValid) {
        // エラーがある場合はツールチップを表示
        document.querySelectorAll('.error').forEach(element => {
            element.style.visibility = 'visible';
            element.style.opacity = '1';
        });
    }

    return isValid;
}

function hideConfirmation(){
    // cssの変更
    document.getElementById("contact_form").style.position = "";
    document.getElementById("contact_form").style.top = "";
    document.getElementById("input_confirmation").classList.remove("input_active");
}

function hideCompletion(){
    // 入力内容のクリア
    document.getElementById("company_name_field").querySelector("input").value = "";
    document.getElementById("name_field").querySelector("input").value = "";
    document.getElementById("email_field").querySelector("input").value = "";
    document.getElementById("phone_number_field").querySelector("input").value = "";
    document.getElementById("message_field").querySelector("textarea").value = "";

    // cssの変更
    document.getElementById("contact_form").style.top = "80px";
    document.getElementById("input_confirmation").classList.remove("input_active");
    document.getElementById("completion").classList.remove("active");
}

async function submitForm(event) {
    event.preventDefault();
    
    // フォームデータの取得
    const formData = new FormData(event.target);
    
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
                document.getElementById("contact_form").style.top = "30px";
                document.getElementById("input_confirmation").style.top = "55px";
                setTimeout(() => {
                    document.getElementById("completion").classList.add("active");
                }, 500);
                
                window.history.pushState(null, '', window.location.pathname);
            } else {
                alert('送信に失敗しました。もう一度お試しください。');
            }
        } else {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('エラーが発生しました。もう一度お試しください。');
    }
}

document.getElementById('contactForm').addEventListener('submit', submitForm);