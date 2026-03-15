document.addEventListener("DOMContentLoaded", () => {
    // FAQ Accordion functionality
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