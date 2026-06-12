document.addEventListener("DOMContentLoaded", function () {
    const uploadBlocks = document.querySelectorAll(".company-create-form .file-upload");

    uploadBlocks.forEach(function (fileInput) {
        const container = fileInput.closest(".position-relative");
        const previewImage = container ? container.querySelector(".upload-pic") : null;
        const uploadButton = container ? container.querySelector(".upload-button") : null;

        if (previewImage) {
            fileInput.addEventListener("change", function () {
                const file = this.files && this.files[0];
                if (!file) return;

                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                };
                reader.readAsDataURL(file);
            });
        }

        if (uploadButton) {
            uploadButton.addEventListener("click", function () {
                fileInput.click();
            });
        }
    });
});