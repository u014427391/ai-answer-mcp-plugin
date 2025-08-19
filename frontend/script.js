document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const problemText = document.getElementById('problemText');
    const answerText = document.getElementById('answerText');
    const stepsList = document.getElementById('stepsList');
    const processingTime = document.getElementById('processingTime');
    const tokensUsed = document.getElementById('tokensUsed');

    let selectedImage = null;

    // 点击上传区域触发文件选择
    uploadArea.addEventListener('click', (e) => {
        if (!e.target.closest('button')) {
            imageUpload.click();
        }
    });

    // 拖拽功能
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2980b9';
        uploadArea.style.backgroundColor = '#f0f8ff';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#3498db';
        uploadArea.style.backgroundColor = 'white';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3498db';
        uploadArea.style.backgroundColor = 'white';

        if (e.dataTransfer.files.length) {
            handleImage(e.dataTransfer.files[0]);
        }
    });

    // 处理选择的图片
    imageUpload.addEventListener('change', () => {
        if (imageUpload.files.length) {
            handleImage(imageUpload.files[0]);
        }
    });

    // 显示预览图片
    function handleImage(file) {
        if (!file.type.startsWith('image/')) {
            alert('请上传图片文件（支持JPG、PNG等格式）');
            return;
        }

        // 检查文件大小（限制10MB）
        if (file.size > 10 * 1024 * 1024) {
            alert('图片文件过大，请上传小于10MB的图片');
            return;
        }

        selectedImage = file;
        const reader = new FileReader();

        reader.onload = (e) => {
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="预览图片">`;
        };

        reader.readAsDataURL(file);
    }

    // 提交图片进行处理
    submitBtn.addEventListener('click', async () => {
        if (!selectedImage) {
            alert('请先选择一张图片');
            return;
        }

        // 重置结果区域
        problemText.textContent = '-';
        answerText.textContent = '-';
        stepsList.innerHTML = '';
        processingTime.textContent = '-';
        tokensUsed.textContent = '-';

        // 显示加载状态
        loading.style.display = 'block';

        try {
            // 创建FormData
            const formData = new FormData();
            formData.append('image', selectedImage);

            // 发送请求
            const response = await fetch('/solve_math_problem', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            // 隐藏加载状态
            loading.style.display = 'none';

            if (!response.ok) {
                throw new Error(result.error || '处理失败，请重试');
            }

            // 显示结果
            problemText.textContent = result.problem || '未识别到有效题目';
            answerText.textContent = result.answer || '未获取到答案';

            // 显示统计信息
            processingTime.textContent = result.processing_time || '未知';
            tokensUsed.textContent = result.tokens_used || '未知';

            // 显示解题步骤
            if (result.steps && result.steps.length) {
                stepsList.innerHTML = result.steps.map(step => {
                    // 简单的数学公式处理（粗体显示数字和符号）
                    step = step.replace(/(\d+|\+|\-|\×|\÷|\=|\(|\)|\[|\]|\{|\}|\.|\/|\*)/g, '<strong>$1</strong>');
                    return `<li>${step}</li>`;
                }).join('');
            } else {
                stepsList.innerHTML = '<li>无解题步骤</li>';
            }

        } catch (error) {
            loading.style.display = 'none';
            alert(error.message);
            console.error('错误:', error);
        }
    });
});