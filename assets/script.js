document.addEventListener("DOMContentLoaded", () => {
    
    // =========================================
    // THEME TOGGLE LOGIC
    // =========================================
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.body;
    
    // 1. Check for saved user preference in localStorage
    const savedTheme = localStorage.getItem('site-theme');
    
    // 2. Apply the saved theme on load
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
    }

    // 3. Handle the toggle button click
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            // Toggle the dark-theme class on the body
            body.classList.toggle('dark-theme');
            
            // Save the user's choice to localStorage
            if (body.classList.contains('dark-theme')) {
                localStorage.setItem('site-theme', 'dark');
            } else {
                localStorage.setItem('site-theme', 'light');
            }
        });
    }

    // =========================================
    // FAQ ACCORDION FUNCTIONALITY
    // =========================================
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(question => {
        question.addEventListener("click", () => {
            const answer = question.nextElementSibling;
            const icon = question.querySelector('.icon');

            // Close all other answers
            document.querySelectorAll(".faq-answer").forEach(item => {
                if (item !== answer) {
                    item.style.maxHeight = null;
                    item.previousElementSibling.querySelector('.icon').innerText = '+';
                }
            });

            // Toggle current answer
            if (answer.style.maxHeight) {
                answer.style.maxHeight = null;
                icon.innerText = '+';
            } else {
                answer.style.maxHeight = answer.scrollHeight + "px";
                icon.innerText = '-';
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // 1. Select the element you want to change (e.g., the h1 tag)
    const titleElement = document.querySelector('h1'); 

    // 2. Make sure the element exists and actually contains a dot
    if (titleElement && titleElement.textContent.includes('.')) {
        
        // 3. Split the text at the first dot
        const text = titleElement.textContent;
        const dotIndex = text.indexOf('.');
        
        // 4. Separate the text into two pieces
        const firstPart = text.substring(0, dotIndex);
        const restOfText = text.substring(dotIndex); // Includes the dot and everything after
        
        // 5. Update the HTML with the first part wrapped in a red span
        titleElement.innerHTML = `<span style="color: red;">${firstPart}</span>${restOfText}`;
    }
});