/*
Init and show Bootstrap toasts
*/

window.onload = (event) => {
    let toastList = document.getElementsByClassName("toast");
    if (toastList.length > 0) {
        for (let toast of toastList) {
            let toastInit = new bootstrap.Toast(toast);
            toastInit.show();
        }
    }
};
