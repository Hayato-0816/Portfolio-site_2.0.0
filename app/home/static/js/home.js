class RevealEffect {
    constructor() {
        this.overlay = document.getElementById('overlayLayer');
        this.activeEffects = new Set();
        this.isRunning = true;
        this.autoInterval = 2000;
        this.maxEffects = 10;          
        this.minSize = 150;            
        this.maxSize = 800;            
        this.displayDuration = 2000;    
        this.fadeOutDuration = 1200;    
        this.init();
    }

    init() {
        // DOMContentLoadedを待たずに即座に開始
        this.startAutoGenerate();
        
        // クリックイベントの設定
        this.overlay.addEventListener('click', (e) => {
            this.createEffect(e.clientX, e.clientY);
        });

        // ページの表示状態の監視
        document.addEventListener('visibilitychange', () => {
            this.isRunning = !document.hidden;
            if (this.isRunning) {
                this.startAutoGenerate();
            }
        });
    }

    startAutoGenerate() {
        const generateRandom = () => {
            if (!this.isRunning) return;

            const rect = this.overlay.getBoundingClientRect();
            // ランダムな座標を生成（rectの範囲内で）
            const randomX = rect.left + (Math.random() * rect.width);
            const randomY = rect.top + (Math.random() * rect.height);
            
            // createEffectに直接座標を渡す
            this.createEffect(randomX, randomY);

            setTimeout(generateRandom, this.autoInterval);
        };

        generateRandom();
    }

    getRandomColor() {
        const hue = Math.floor(Math.random() * 360);
        const saturation = 70;  // 彩度（0-100）
        const lightness = 60;   // 明度（0-100）
        const alpha = 0.1;      // 透明度
        return `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`;
    }

    createEffect(clientX, clientY) {
        if (this.activeEffects.size >= this.maxEffects) {
            const oldestEffect = this.activeEffects.values().next().value;
            this.removeEffect(oldestEffect);
        }

        const effect = document.createElement('div');
        effect.className = 'blur-effect';

        const rect = this.overlay.getBoundingClientRect();
        // 要素の相対位置を正しく計算
        const x = clientX - rect.left;
        const y = clientY - rect.top;

        effect.style.left = `${x}px`;
        effect.style.top = `${y}px`;
        effect.style.borderRadius = this.getRandomShape();
        effect.style.background = this.getRandomColor();
        
        this.overlay.appendChild(effect);
        this.activeEffects.add(effect);

        requestAnimationFrame(() => {
            const size = Math.random() * 100 + 150; // 150-250pxのランダムなサイズ
            effect.style.width = `${size}px`;
            effect.style.height = `${size}px`;
            effect.classList.add('blur-effect-visible');
        });

        // フェードアウト
        setTimeout(() => {
            effect.style.backdropFilter = 'opacity(0)';
            effect.style.webkitBackdropFilter = 'opacity(0)';
            setTimeout(() => this.removeEffect(effect), 1200);
        }, 2000);
    }

    getRandomShape() {
        const randomNum = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
        return `${randomNum(30, 70)}% ${randomNum(30, 70)}% ${randomNum(30, 70)}% ${randomNum(30, 70)}% / ${randomNum(30, 70)}% ${randomNum(30, 70)}% ${randomNum(30, 70)}% ${randomNum(30, 70)}%`;
    }

    removeEffect(effect) {
        this.activeEffects.delete(effect);
        effect.remove();
    }
}

// 初期化
const revealEffect = new RevealEffect();