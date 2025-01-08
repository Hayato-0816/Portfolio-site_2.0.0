function showConfirmation(){
    if (!validateForm()) {
        return;
    }

    document.getElementById("conf_company").textContent = document.getElementById("company_name_field").querySelector("input").value;
    document.getElementById("conf_name").textContent = document.getElementById("name_field").querySelector("input").value;
    document.getElementById("conf_email").textContent = document.getElementById("email_field").querySelector("input").value;
    document.getElementById("conf_phone").textContent = document.getElementById("phone_number_field").querySelector("input").value;
    document.getElementById("conf_message").textContent = document.getElementById("message_field").querySelector("textarea").value;

    document.getElementById("contact_form").style.top = "40px";
    document.getElementById("input_confirmation").classList.add("input_active");

    window.history.pushState({page: 'contact form'}, '', window.location.pathname);
    window.addEventListener('popstate', function(event) {
        hideConfirmation();
    }, {once: true});
}

function validateForm() {
    // 必須項目の取得
    const name = document.getElementById("name_field").querySelector("input").value.trim();
    const email = document.getElementById("email_field").querySelector("input").value.trim();
    const message = document.getElementById("message_field").querySelector("textarea").value.trim();
    const phone = document.getElementById("phone_number_field").querySelector("input").value.trim();

    let isValid = true;

    // お名前のバリデーション
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

    // メールアドレスのバリデーション
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

    // お問い合わせ内容のバリデーション
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

    // 電話番号のバリデーション（任意項目）
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
    document.getElementById("contact_form").style.position = "";
    document.getElementById("contact_form").style.top = "";
    document.getElementById("input_confirmation").classList.remove("active");
}

// フォーム送信処理を追加
async function submitForm(event) {
    event.preventDefault();
    
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
                
                // ブラウザバック無効化
                window.history.pushState(null, '', window.location.pathname);
                window.addEventListener('popstate', function() {
                    window.history.pushState(null, '', window.location.pathname);
                });
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

// フォームにイベントリスナーを追加
document.getElementById('contactForm').addEventListener('submit', submitForm);