function initDarkMode(){
    var theme="light";

    if(localStorage.getItem("theme")){
        if(localStorage.getItem("theme") === "dark"){
            theme = "dark";
        }
    } else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        theme = "dark";
    }

    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);

    var toggleSwitch = document.querySelector('#theme-switch input[type="checkbox"]');
    if(theme === "dark") {
        toggleSwitch.checked = true;
    }

    toggleSwitch.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute("data-theme", "dark");
            localStorage.setItem("theme", "dark");
        } else {
            document.documentElement.setAttribute("data-theme", "light");
            localStorage.setItem("theme", "light");
        }
    }, false)
}
initDarkMode();
